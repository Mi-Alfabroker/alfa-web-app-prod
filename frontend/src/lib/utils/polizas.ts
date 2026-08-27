/**
 * Póliza presentation helpers.
 *
 * A póliza row shown to the user is a join across four collections
 * (póliza -> bien -> cliente, plus aseguradora). Deriving that in each page
 * duplicated the join four ways, so it lives here and every consumer — the
 * list, the topbar search, the dashboard and the detail pages — reads the same
 * shape.
 */

import type { Catalog } from '$lib/stores/catalog';
import type { Cliente } from '$lib/types/cliente';
import type { EstadoPoliza, Poliza, TipoPoliza } from '$lib/types/poliza';
import { formatDateShort, money, parseApiDate } from './formatters';

/** The four rubros, in the order the design lists them. */
export const RUBROS: { tipo: TipoPoliza; label: string; slug: string; sigla: string }[] = [
	{ tipo: 'HOGAR', label: 'Hogar', slug: 'hogar', sigla: 'HOG' },
	{ tipo: 'VEHICULO', label: 'Vehículos', slug: 'vehiculo', sigla: 'AUT' },
	{ tipo: 'COPROPIEDAD', label: 'Copropiedades', slug: 'copropiedad', sigla: 'COP' },
	{ tipo: 'OTRO', label: 'Otros ramos', slug: 'otro', sigla: 'OTR' }
];

export function rubroBySlug(slug: string | null | undefined) {
	return RUBROS.find((r) => r.slug === slug) ?? null;
}

export function rubroByTipo(tipo: TipoPoliza) {
	return RUBROS.find((r) => r.tipo === tipo) ?? RUBROS[0];
}

/** Estado labels: PROSPECTO is shown as "Propuesta" throughout the app. */
export const ESTADO_LABELS: Record<EstadoPoliza, string> = {
	PROSPECTO: 'Propuesta',
	VIGENTE: 'Vigente',
	VENCIDA: 'Vencida',
	CANCELADA: 'Cancelada'
};

export interface PolizaRow {
	id: number;
	tipo: TipoPoliza;
	rubroLabel: string;
	sigla: string;
	consecutivo: string;
	estado: EstadoPoliza;
	estadoLabel: string;
	clienteId: number;
	clienteNombre: string;
	documento: string;
	bienId: number;
	bienDesc: string;
	inicio: string;
	fin: string;
	vigencia: string;
	prima: number | null;
	primaLabel: string;
	aseguradoraNombre: string;
	href: string;
	raw: Poliza;
}

/** Display name for a cliente, whichever kind of person it is. */
export function clienteNombre(cliente: Cliente | undefined, fallbackId?: number): string {
	if (!cliente) return fallbackId ? `#${fallbackId}` : '—';
	const name =
		cliente.tipo_persona === 'PERSONA' ? cliente.nombre : cliente.razon_social;
	return name || cliente.usuario || `#${cliente.id}`;
}

/** Document label for a cliente: "C.C. 43.118.902" / "NIT 900.412.778". */
export function clienteDocumento(cliente: Cliente | undefined): string {
	if (!cliente) return '—';
	if (cliente.tipo_persona === 'EMPRESA') {
		return cliente.nit ? `NIT ${cliente.nit}` : '—';
	}
	if (!cliente.numero_documento) return '—';
	return `${cliente.tipo_documento || 'CC'} ${cliente.numero_documento}`;
}

/**
 * Prima actually in force: the selected aseguradora's quote when the póliza is
 * bound, otherwise the net prima, otherwise the first quote on record.
 */
export function primaVigente(poliza: Poliza): number | null {
	const quotes = [
		poliza.valor_prima_aseg_1,
		poliza.valor_prima_aseg_2,
		poliza.valor_prima_aseg_3,
		poliza.valor_prima_aseg_4,
		poliza.valor_prima_aseg_5
	];
	const selected = poliza.aseguradora_seleccionada;
	if (selected && selected >= 1 && selected <= 5) {
		const chosen = quotes[selected - 1];
		if (chosen !== null && chosen !== undefined) return chosen;
	}
	if (poliza.valor_prima_neta !== null && poliza.valor_prima_neta !== undefined) {
		return poliza.valor_prima_neta;
	}
	return quotes.find((q) => q !== null && q !== undefined) ?? null;
}

/** Aseguradora ids quoted on a póliza, in slot order. */
export function aseguradoraIds(poliza: Poliza): (number | null)[] {
	return [
		poliza.id_aseguradora_1,
		poliza.id_aseguradora_2,
		poliza.id_aseguradora_3,
		poliza.id_aseguradora_4,
		poliza.id_aseguradora_5
	];
}

/** Name of the bound aseguradora, or "—" while the póliza is still a proposal. */
export function aseguradoraVigente(poliza: Poliza, c: Catalog): string {
	const selected = poliza.aseguradora_seleccionada;
	const ids = aseguradoraIds(poliza);
	const id = selected && selected >= 1 && selected <= 5 ? ids[selected - 1] : null;
	if (!id) return '—';
	return c.aseguradoras.find((a) => a.id === id)?.nombre ?? `#${id}`;
}

function bienInfo(
	poliza: Poliza,
	c: Catalog
): { tipo: TipoPoliza; bienId: number; desc: string; clienteId: number } {
	if ('id_hogar' in poliza) {
		const bien = c.hogares.find((h) => h.id === poliza.id_hogar);
		return {
			tipo: 'HOGAR',
			bienId: poliza.id_hogar,
			desc: bien
				? [bien.tipo_inmueble || 'Hogar', bien.ciudad_inmueble].filter(Boolean).join(' · ')
				: `Hogar #${poliza.id_hogar}`,
			clienteId: bien?.id_usuario ?? 0
		};
	}
	if ('id_vehiculo' in poliza) {
		const bien = c.vehiculos.find((v) => v.id === poliza.id_vehiculo);
		return {
			tipo: 'VEHICULO',
			bienId: poliza.id_vehiculo,
			desc: bien
				? [bien.marca, bien.placa].filter(Boolean).join(' · ') || `Vehículo #${bien.id}`
				: `Vehículo #${poliza.id_vehiculo}`,
			clienteId: bien?.id_usuario ?? 0
		};
	}
	if ('id_copropiedad' in poliza) {
		const bien = c.copropiedades.find((x) => x.id === poliza.id_copropiedad);
		return {
			tipo: 'COPROPIEDAD',
			bienId: poliza.id_copropiedad,
			desc: bien
				? [bien.tipo_copropiedad || 'Copropiedad', bien.ciudad].filter(Boolean).join(' · ')
				: `Copropiedad #${poliza.id_copropiedad}`,
			clienteId: bien?.id_usuario ?? 0
		};
	}
	const bien = c.otrosBienes.find((o) => o.id === poliza.id_otro_bien);
	return {
		tipo: 'OTRO',
		bienId: poliza.id_otro_bien,
		desc: bien?.bien_asegurado || `Otro bien #${poliza.id_otro_bien}`,
		clienteId: bien?.id_usuario ?? 0
	};
}

/** Build one display row from a póliza. */
export function toPolizaRow(poliza: Poliza, c: Catalog): PolizaRow {
	const { tipo, bienId, desc, clienteId } = bienInfo(poliza, c);
	const rubro = rubroByTipo(tipo);
	const cliente = c.clientes.find((x) => x.id === clienteId);
	const prima = primaVigente(poliza);
	const inicio = formatDateShort(poliza.inicio_vigencia);
	const fin = formatDateShort(poliza.fin_vigencia);

	return {
		id: poliza.id,
		tipo,
		rubroLabel: rubro.label,
		sigla: rubro.sigla,
		consecutivo: poliza.consecutivo,
		estado: poliza.estado,
		estadoLabel: ESTADO_LABELS[poliza.estado] ?? poliza.estado,
		clienteId,
		clienteNombre: clienteNombre(cliente, clienteId),
		documento: clienteDocumento(cliente),
		bienId,
		bienDesc: desc,
		inicio,
		fin,
		vigencia: inicio === '—' && fin === '—' ? '—' : `${inicio} → ${fin}`,
		prima,
		primaLabel: money(prima),
		aseguradoraNombre: aseguradoraVigente(poliza, c),
		href: `/propuestas/${rubro.slug}/${poliza.id}`,
		raw: poliza
	};
}

/** All pólizas across the four rubros as display rows. */
export function buildPolizaRows(c: Catalog): PolizaRow[] {
	return [
		...c.polizasHogar,
		...c.polizasVehiculo,
		...c.polizasCopropiedad,
		...c.polizasOtroBien
	].map((p) => toPolizaRow(p, c));
}

/**
 * Days until a póliza's vigencia ends. Negative once expired, null when the
 * póliza has no end date on record.
 */
// ============================================================================
// RECORRIDO DE LA PÓLIZA
// ============================================================================

export type PasoId = 'datos' | 'cotizaciones' | 'propuesta' | 'entrega';

export interface PasoFlujo {
	id: PasoId;
	label: string;
	done: boolean;
	/** Es el paso donde está la póliza ahora mismo. */
	current: boolean;
	/** Se puede entrar; false cuando falta un requisito previo. */
	enabled: boolean;
	/** Acción del paso, si tiene una. */
	href?: string;
	/** Motivo del bloqueo, mostrado en el botón deshabilitado. */
	blockedReason?: string;
}

export interface FlujoPolizaInfo {
	pasos: PasoFlujo[];
	/** Próxima acción, o null si terminó o el estado es terminal. */
	siguiente: PasoFlujo | null;
	/** VENCIDA o CANCELADA: la barra se muestra inactiva. */
	terminal: boolean;
}

/**
 * Deriva el recorrido de una póliza desde sus propios datos.
 *
 * Vive aquí y no dentro del componente porque cuatro pantallas necesitan la
 * misma respuesta —detalle, generar, entregar y el menú de la lista— y escrita
 * por pantalla se desincronizaría: la lista se volvería una puerta trasera al
 * orden que el detalle sí respeta.
 *
 * El progreso NO usa el enum de estado: vive en las marcas de documento, para
 * no inventar estados nuevos en una máquina que ya funciona.
 */
export function flujoPoliza(poliza: Poliza, rubroSlug: string): FlujoPolizaInfo {
	const base = `/propuestas/${rubroSlug}/${poliza.id}`;
	const terminal = poliza.estado === 'VENCIDA' || poliza.estado === 'CANCELADA';

	const registro = poliza as unknown as Record<string, unknown>;
	const tieneCotizacion = [1, 2, 3, 4, 5].some(
		(slot) => registro[`valor_prima_aseg_${slot}`] != null
	);
	const tienePropuesta = poliza.propuesta_generada_at != null;
	const entregada = poliza.aseguradora_seleccionada != null && !!poliza.numero_poliza_aseguradora;

	const pasos: PasoFlujo[] = [
		{
			id: 'datos',
			label: 'Datos',
			done: true,
			current: false,
			enabled: true,
			href: base
		},
		{
			id: 'cotizaciones',
			label: 'Cotizaciones',
			done: tieneCotizacion,
			current: false,
			enabled: true,
			href: base,
			blockedReason: tieneCotizacion ? undefined : 'Registra al menos una prima cotizada'
		},
		{
			id: 'propuesta',
			label: 'Propuesta',
			done: tienePropuesta,
			current: false,
			// Un paso ya cumplido siempre es accesible: exigirle su requisito
			// bloquearía algo que de hecho ya ocurrió (una póliza histórica está
			// entregada aunque nunca se registrara su propuesta).
			enabled: tieneCotizacion || tienePropuesta,
			href: `${base}/generar`,
			blockedReason:
				tieneCotizacion || tienePropuesta ? undefined : 'Primero registra las cotizaciones'
		},
		{
			id: 'entrega',
			label: 'Entrega',
			done: entregada,
			current: false,
			enabled: tienePropuesta || entregada,
			href: `${base}/entregar`,
			blockedReason: tienePropuesta || entregada ? undefined : 'Primero genera la propuesta'
		}
	];

	/*
	 * El siguiente paso es el primero sin cumplir, PERO sólo si el recorrido no
	 * lo dejó atrás. Una póliza histórica puede estar entregada sin marca de
	 * propuesta (esa columna no existía cuando se emitió); tomar sin más el
	 * primer pendiente pediría "Continuar: Propuesta" sobre una póliza que ya
	 * está vigente.
	 */
	const ultimoCumplido = pasos.reduce((ultimo, p, i) => (p.done ? i : ultimo), -1);
	const primerPendiente = pasos.findIndex((p) => !p.done);

	const siguiente =
		terminal || primerPendiente === -1 || primerPendiente < ultimoCumplido
			? null
			: pasos[primerPendiente];

	if (siguiente) siguiente.current = true;

	return { pasos, siguiente, terminal };
}

export function diasParaVencer(poliza: Poliza): number | null {
	const fin = parseApiDate(poliza.fin_vigencia);
	if (!fin) return null;
	// Compare calendar days, not instants, so the count does not flip with the
	// time of day the page happens to be opened.
	const today = new Date();
	const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());
	const oneDay = 24 * 60 * 60 * 1000;
	return Math.round((fin.getTime() - startOfToday.getTime()) / oneDay);
}
