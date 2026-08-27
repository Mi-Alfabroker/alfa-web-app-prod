/**
 * Catalog store — one lazily-loaded, session-cached copy of the reference data
 * that most screens need together.
 *
 * A póliza points at a bien, and only the bien knows which cliente owns it, so
 * anything that shows "which client does this policy belong to" needs clientes
 * + the four bien collections + the four póliza collections at once. That is
 * nine requests; the pólizas list already made all nine on its own, and the
 * global search in the topbar needs the same join. Caching them here means the
 * app pays for them once instead of per screen.
 *
 * Call `invalidateCatalog()` after any mutation so the next reader refetches.
 */

import { writable, get } from 'svelte/store';
import { clienteService } from '$services/cliente.service';
import { aseguradoraService } from '$services/aseguradora.service';
import { bienService } from '$services/bien.service';
import { polizaService } from '$services/poliza.service';
import type { Cliente } from '$lib/types/cliente';
import type { Aseguradora } from '$lib/types/aseguradora';
import type { Hogar, Vehiculo, Copropiedad, OtroBien } from '$lib/types/bien';
import type {
	PolizaHogar,
	PolizaVehiculo,
	PolizaCopropiedad,
	PolizaOtroBien
} from '$lib/types/poliza';

export interface Catalog {
	loaded: boolean;
	loading: boolean;
	error: string | null;
	clientes: Cliente[];
	aseguradoras: Aseguradora[];
	hogares: Hogar[];
	vehiculos: Vehiculo[];
	copropiedades: Copropiedad[];
	otrosBienes: OtroBien[];
	polizasHogar: PolizaHogar[];
	polizasVehiculo: PolizaVehiculo[];
	polizasCopropiedad: PolizaCopropiedad[];
	polizasOtroBien: PolizaOtroBien[];
}

const empty: Catalog = {
	loaded: false,
	loading: false,
	error: null,
	clientes: [],
	aseguradoras: [],
	hogares: [],
	vehiculos: [],
	copropiedades: [],
	otrosBienes: [],
	polizasHogar: [],
	polizasVehiculo: [],
	polizasCopropiedad: [],
	polizasOtroBien: []
};

export const catalog = writable<Catalog>({ ...empty });

/** In-flight load, so concurrent callers share one round of requests. */
let inFlight: Promise<void> | null = null;

export async function loadCatalog(force: boolean = false): Promise<void> {
	const current = get(catalog);
	if (!force && current.loaded) return;
	if (inFlight) return inFlight;

	catalog.update((c) => ({ ...c, loading: true, error: null }));

	inFlight = (async () => {
		try {
			const [clientes, aseguradoras, hogares, vehiculos, copropiedades, otrosBienes] =
				await Promise.all([
					clienteService.getAll(),
					aseguradoraService.getAll(),
					bienService.hogares.getAll(),
					bienService.vehiculos.getAll(),
					bienService.copropiedades.getAll(),
					bienService.otros.getAll()
				]);

			const [polizasHogar, polizasVehiculo, polizasCopropiedad, polizasOtroBien] =
				await Promise.all([
					polizaService.hogar.getAll(),
					polizaService.vehiculo.getAll(),
					polizaService.copropiedad.getAll(),
					polizaService.otroBien.getAll()
				]);

			const byIdDesc = <T extends { id: number }>(rows: T[]) => [...rows].sort((a, b) => b.id - a.id);

			catalog.set({
				loaded: true,
				loading: false,
				error: null,
				clientes,
				aseguradoras,
				hogares,
				vehiculos,
				copropiedades,
				otrosBienes,
				polizasHogar: byIdDesc(polizasHogar),
				polizasVehiculo: byIdDesc(polizasVehiculo),
				polizasCopropiedad: byIdDesc(polizasCopropiedad),
				polizasOtroBien: byIdDesc(polizasOtroBien)
			});
		} catch (err) {
			catalog.update((c) => ({
				...c,
				loading: false,
				error: err instanceof Error ? err.message : 'Error al cargar los datos'
			}));
		} finally {
			inFlight = null;
		}
	})();

	return inFlight;
}

/** Drop the cache so the next `loadCatalog()` refetches. */
export function invalidateCatalog(): void {
	catalog.set({ ...empty });
}
