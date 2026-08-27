# Flujo propuesta → entrega + densidad de formularios — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hacer visible y obligatorio el orden datos → cotizaciones → propuesta → entrega, y pasar los formularios a dos columnas.

**Architecture:** Una función pura `flujoPoliza()` deriva los 4 pasos desde la póliza; un componente `FlujoPoliza` la pinta; tres pantallas y el menú de la lista la consumen. El único dato nuevo son dos columnas de timestamp por tabla de pólizas, escritas por un endpoint PATCH dedicado. Los formularios se densifican cambiando un componente compartido y una clase CSS.

**Tech Stack:** SvelteKit 2 / Svelte 4 (sin runes), TypeScript, Tailwind 3, Flask + SQLAlchemy, PostgreSQL.

## Global Constraints

- **No hay framework de tests en este repo.** El ciclo de verificación de cada tarea es: `npm run build` (debe terminar en `✔ done`), `npm run check` (no sumar errores sobre la línea base de **261 errores en 14 archivos**), `curl` contra `http://localhost:5000` para backend, y comprobación en navegador contra el backend real.
- Backend en Docker: `alfabroker-api` (:5000) y `alfabroker-db` (:5432). **El API no monta las fuentes: son parte de la imagen.** Todo cambio de backend exige `cd backend && docker compose build api && docker compose up -d api`; un `docker restart` NO recoge los cambios. Usuario de BD: `admin`, base `alfabroker`. Frontend en `:3000` — **obligatorio ese puerto**, el CORS del backend sólo permite `:3000` y `:5173`.
- Credenciales de prueba: `superadmin` / `admin123`.
- Migraciones: archivos `.sql` planos en `backend/migrations/`, aplicados a mano. **No hay Alembic.**
- El enum de estado NO cambia: `PROSPECTO | VIGENTE | VENCIDA | CANCELADA`.
- Idioma de la interfaz: español. Los identificadores en código, en inglés o español según el archivo que se toque (seguir el vecino).
- Todo dato de prueba creado durante la verificación debe revertirse al terminar la tarea.
- No commitear salvo que el usuario lo pida.

---

### Task 1: Columnas de documentos generados (backend)

**Files:**
- Create: `backend/migrations/add_documentos_generados.sql`
- Modify: `backend/app/models/polizas/base_poliza.py`

**Interfaces:**
- Consumes: nada.
- Produces: columnas `propuesta_generada_at` y `entrega_generada_at` (nullable `TIMESTAMPTZ`) en las 4 tablas de pólizas, expuestas por `to_dict()` como cadena ISO o `null`.

- [ ] **Step 1: Escribir la migración**

`backend/migrations/add_documentos_generados.sql`:

```sql
-- Marca de que los documentos de una póliza ya fueron generados.
-- Nulo = nunca se generó. Se dejan nulas las pólizas existentes a propósito:
-- nadie registró esos documentos, e inventar la fecha ensuciaría el histórico.
ALTER TABLE polizas_hogar       ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_hogar       ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
ALTER TABLE polizas_vehiculo    ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_vehiculo    ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
ALTER TABLE polizas_copropiedad ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_copropiedad ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
ALTER TABLE polizas_otro_bien   ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_otro_bien   ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
```

- [ ] **Step 2: Aplicar la migración**

```bash
docker exec -i alfabroker-db psql -U admin -d alfabroker < backend/migrations/add_documentos_generados.sql
```

(Si el usuario/base difieren, leerlos de `docker-compose-db.yml` antes de correr.)

- [ ] **Step 3: Verificar que las columnas existen**

```bash
docker exec alfabroker-db psql -U admin -d alfabroker -c \
  "SELECT table_name, column_name FROM information_schema.columns
   WHERE column_name IN ('propuesta_generada_at','entrega_generada_at') ORDER BY 1,2;"
```

Esperado: 8 filas (2 columnas × 4 tablas).

- [ ] **Step 4: Añadir las columnas al modelo**

En `backend/app/models/polizas/base_poliza.py`, junto a `created_at` / `updated_at`:

```python
    # Marcas de documentos generados. Nulo = nunca se generó.
    propuesta_generada_at = db.Column(db.DateTime(timezone=True))
    entrega_generada_at = db.Column(db.DateTime(timezone=True))
```

Y en `to_dict()`, junto a las demás fechas:

```python
            'propuesta_generada_at': self.propuesta_generada_at.isoformat() if self.propuesta_generada_at else None,
            'entrega_generada_at': self.entrega_generada_at.isoformat() if self.entrega_generada_at else None,
```

- [ ] **Step 5: Reiniciar el API y verificar que las devuelve**

```bash
cd backend && docker compose build api && docker compose up -d api && sleep 8 && cd ..
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" \
  -d '{"usuario":"superadmin","clave":"admin123"}' | python -c "import sys,json;print(json.load(sys.stdin)['data']['tokens']['access_token'])")
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/polizas/copropiedad/5 \
  | python -c "import sys,json;d=json.load(sys.stdin)['data'];print({k:d[k] for k in ('propuesta_generada_at','entrega_generada_at')})"
```

Esperado: `{'propuesta_generada_at': None, 'entrega_generada_at': None}`.

---

### Task 2: Endpoint para marcar documento (backend)

**Files:**
- Modify: `backend/app/services/polizas/poliza_hogar_service.py`
- Modify: `backend/app/services/polizas/poliza_vehiculo_service.py`
- Modify: `backend/app/services/polizas/poliza_copropiedad_service.py`
- Modify: `backend/app/services/polizas/poliza_otro_bien_service.py`
- Modify: `backend/app/blueprints/polizas.py`

**Interfaces:**
- Consumes: columnas de Task 1.
- Produces: `PATCH /api/polizas/{hogar|vehiculo|copropiedad|otro-bien}/<id>/marcar-documento`
  con cuerpo `{"documento": "propuesta"|"entrega"}` y respuesta
  `{"success": true, "data": <póliza>}`. 400 si `documento` no es uno de los dos
  valores; 404 si la póliza no existe.
  Método de servicio: `Poliza<Rubro>Service.marcar_documento(poliza_id: int, documento: str) -> tuple[dict, Optional[str]]`.

**Convención del repo (verificada, no asumida):** el blueprint **no** tiene rutas
genéricas por `<tipo>`. Hay una ruta explícita por rubro que delega en su
servicio, y cada servicio devuelve `(dict, error|None)`; el blueprint traduce ese
error a 404 si contiene `not found`, si no a 400. La persistencia se hace con
`poliza_<rubro>_repository.update(poliza, data_dict)`.

- [ ] **Step 1: Añadir el método al servicio de hogar**

En `backend/app/services/polizas/poliza_hogar_service.py`, junto a `cambiar_estado`:

```python
    @staticmethod
    def marcar_documento(poliza_id: int, documento: str) -> tuple[dict, Optional[str]]:
        """
        Record that a generated document exists for this policy.

        Kept out of /api/propuestas/generate on purpose: that endpoint receives a
        template name and a variables dict and has no idea which policy the
        document came from, so passing it the id would couple the proposal
        service to the policy service.

        Args:
            poliza_id: The policy ID
            documento: 'propuesta' or 'entrega'

        Returns:
            Tuple of (updated policy dict, error message or None)
        """
        campos = {
            'propuesta': 'propuesta_generada_at',
            'entrega': 'entrega_generada_at',
        }
        campo = campos.get(documento)
        if campo is None:
            return {}, "documento debe ser 'propuesta' o 'entrega'"

        poliza = poliza_hogar_repository.get_by_id(poliza_id)
        if not poliza:
            return {}, f"PolizaHogar with ID {poliza_id} not found"

        updated = poliza_hogar_repository.update(poliza, {campo: datetime.now(timezone.utc)})
        return updated.to_dict(), None
```

Añadir al import de fecha del archivo: `from datetime import date, datetime, timezone`
(el archivo ya importa `date`).

- [ ] **Step 2: Repetir en los otros tres servicios**

Mismo método en `poliza_vehiculo_service.py`, `poliza_copropiedad_service.py` y
`poliza_otro_bien_service.py`, cambiando únicamente el repositorio
(`poliza_vehiculo_repository`, `poliza_copropiedad_repository`,
`poliza_otro_bien_repository`) y el nombre en el mensaje de error
(`PolizaVehiculo`, `PolizaCopropiedad`, `PolizaOtroBien`).

- [ ] **Step 3: Añadir las cuatro rutas**

En `backend/app/blueprints/polizas.py`, cada una junto a la ruta `estado` de su
rubro. Para hogar:

```python
@polizas_bp.route('/hogar/<int:poliza_id>/marcar-documento', methods=['PATCH', 'OPTIONS'])
def marcar_documento_poliza_hogar(poliza_id: int):
    """
    Record that a document (proposal or delivery) was generated for this policy.

    Expected JSON body:
        - documento (required): 'propuesta' or 'entrega'
    """
    data = request.get_json()

    if not data or 'documento' not in data:
        return jsonify({
            'success': False,
            'error': 'Field documento is required'
        }), 400

    poliza, error = PolizaHogarService.marcar_documento(poliza_id, data['documento'])

    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code

    return jsonify({
        'success': True,
        'data': poliza,
        'message': f'Documento {data["documento"]} marcado como generado'
    }), 200
```

Repetir para `/vehiculo/...`, `/copropiedad/...` y `/otro-bien/...` cambiando la
ruta, el nombre de la función y el servicio.

- [ ] **Step 4: Reiniciar el API**

```bash
cd backend && docker compose build api && docker compose up -d api && sleep 8 && cd ..
```

- [ ] **Step 5: Probar el camino feliz**

```bash
cd backend && docker compose build api && docker compose up -d api && sleep 8 && cd ..
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" \
  -d '{"usuario":"superadmin","clave":"admin123"}' | python -c "import sys,json;print(json.load(sys.stdin)['data']['tokens']['access_token'])")
curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"documento":"propuesta"}' http://localhost:5000/api/polizas/copropiedad/5 \
  -o /dev/null -w "%{http_code}\n"
```

Esperado: `200`, y `propuesta_generada_at` ya no nulo al consultar la póliza.

- [ ] **Step 6: Probar el rechazo**

```bash
curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"documento":"otra-cosa"}' http://localhost:5000/api/polizas/copropiedad/5 \
  -o /dev/null -w "%{http_code}\n"
```

Esperado: `400`.

- [ ] **Step 7: Revertir el dato de prueba**

```bash
docker exec alfabroker-db psql -U admin -d alfabroker -c \
  "UPDATE polizas_copropiedad SET propuesta_generada_at = NULL WHERE id = 5;"
```

---

### Task 3: Derivación del flujo (frontend, sin UI)

**Files:**
- Modify: `frontend/src/lib/types/poliza.ts`
- Modify: `frontend/src/lib/utils/polizas.ts`
- Modify: `frontend/src/lib/utils/index.ts`
- Modify: `frontend/src/lib/services/poliza.service.ts`

**Interfaces:**
- Consumes: endpoint de Task 2.
- Produces:
  - `BasePoliza.propuesta_generada_at: string | null` y `entrega_generada_at: string | null`
  - `flujoPoliza(poliza: Poliza, rubroSlug: string): FlujoPolizaInfo`
  - tipos `PasoId`, `PasoFlujo`, `FlujoPolizaInfo`
  - `polizaService.<rubro>.marcarDocumento(id: number, documento: 'propuesta' | 'entrega'): Promise<Poliza>`

- [ ] **Step 1: Añadir los campos al tipo**

En `frontend/src/lib/types/poliza.ts`, dentro de `interface BasePoliza`, junto a `created_at`:

```ts
	/** Marcas de documentos generados. Nulo = nunca se generó. */
	propuesta_generada_at: string | null;
	entrega_generada_at: string | null;
```

- [ ] **Step 2: Añadir `marcarDocumento` al servicio**

En `frontend/src/lib/services/poliza.service.ts`, dentro de **cada uno** de los cuatro objetos (`polizaHogarService`, `polizaVehiculoService`, `polizaCopropiedadService`, `polizaOtroBienService`), replicando el patrón de `cambiarEstado` y cambiando sólo el segmento de ruta (`hogar` / `vehiculo` / `copropiedad` / `otro-bien`):

```ts
	async marcarDocumento(id: number, documento: 'propuesta' | 'entrega'): Promise<PolizaHogar> {
		const response = await api.patch<ApiResponse<PolizaHogar>>(
			`${BASE_ENDPOINT}/hogar/${id}/marcar-documento`,
			{ documento }
		);
		return response.data;
	},
```

- [ ] **Step 3: Escribir la derivación del flujo**

Al final de `frontend/src/lib/utils/polizas.ts`:

```ts
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
 * Vive aquí y no en el componente porque cuatro pantallas necesitan la misma
 * respuesta —detalle, generar, entregar y el menú de la lista—, y escrita por
 * pantalla se desincronizaría: la lista se volvería una puerta trasera al orden
 * que el detalle sí respeta.
 */
export function flujoPoliza(poliza: Poliza, rubroSlug: string): FlujoPolizaInfo {
	const base = `/propuestas/${rubroSlug}/${poliza.id}`;
	const terminal = poliza.estado === 'VENCIDA' || poliza.estado === 'CANCELADA';

	const tieneCotizacion = aseguradoraIds(poliza).some(
		(_, i) => (poliza as Record<string, any>)[`valor_prima_aseg_${i + 1}`] != null
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
			current: !tieneCotizacion,
			enabled: true,
			href: base,
			blockedReason: tieneCotizacion ? undefined : 'Registra al menos una prima cotizada'
		},
		{
			id: 'propuesta',
			label: 'Propuesta',
			done: tienePropuesta,
			current: tieneCotizacion && !tienePropuesta,
			enabled: tieneCotizacion,
			href: `${base}/generar`,
			blockedReason: tieneCotizacion ? undefined : 'Primero registra las cotizaciones'
		},
		{
			id: 'entrega',
			label: 'Entrega',
			done: entregada,
			current: tienePropuesta && !entregada,
			enabled: tienePropuesta,
			href: `${base}/entregar`,
			blockedReason: tienePropuesta ? undefined : 'Primero genera la propuesta'
		}
	];

	const siguiente = terminal ? null : (pasos.find((p) => !p.done) ?? null);
	return { pasos, siguiente, terminal };
}
```

- [ ] **Step 4: Exportar desde el barril**

En `frontend/src/lib/utils/index.ts`, añadir `flujoPoliza` a la lista de valores exportados desde `./polizas`, y `PasoId`, `PasoFlujo`, `FlujoPolizaInfo` a la línea de `export type`.

- [ ] **Step 5: Verificar**

```bash
cd frontend && npm run build
```

Esperado: `✔ done`. Y `npm run check` sin errores nuevos sobre la línea base.

---

### Task 4: Componente de la barra de pasos

**Files:**
- Create: `frontend/src/lib/components/FlujoPoliza.svelte`
- Modify: `frontend/src/lib/components/index.ts`
- Modify: `frontend/src/app.css`

**Interfaces:**
- Consumes: `flujoPoliza`, `PasoId` de Task 3.
- Produces: `<FlujoPoliza poliza rubroSlug pasoActual />` — barra de 4 pasos.

- [ ] **Step 1: Estilos de la barra**

En `frontend/src/app.css`, dentro de `@layer components`, junto a `.action-strip`:

```css
	/* --------------------------------------------
	   BARRA DE PASOS
	   -------------------------------------------- */
	.flujo {
		@apply flex items-center gap-1 flex-wrap rounded-2xl shadow-sm mb-3.5;
		padding: 10px 14px;
		background: var(--color-bg);
		border: 1px solid var(--color-divider);
	}

	.flujo-paso {
		@apply inline-flex items-center gap-2 rounded-full text-sm transition-colors;
		padding: 6px 12px;
		color: var(--color-text-60);
	}

	a.flujo-paso:hover {
		background: var(--color-accent-100);
	}

	.flujo-paso-done {
		color: var(--color-accent-900);
		font-weight: 500;
	}

	.flujo-paso-current {
		background: var(--color-accent-100);
		color: var(--color-accent-900);
		font-weight: 600;
		box-shadow: inset 0 0 0 1px var(--color-accent-400);
	}

	.flujo-paso-blocked {
		color: var(--color-text-45);
		cursor: not-allowed;
	}

	/* Marcador: número pendiente, check cumplido. */
	.flujo-marca {
		@apply grid place-items-center flex-none rounded-full text-xs font-semibold;
		width: 20px;
		height: 20px;
		background: var(--color-surface);
		color: var(--color-text-60);
	}

	.flujo-paso-done .flujo-marca {
		background: var(--color-accent-600);
		color: var(--color-accent-ink);
	}

	.flujo-sep {
		@apply flex-none;
		width: 16px;
		height: 1px;
		background: var(--color-divider);
	}

	.flujo-terminal {
		@apply text-sm;
		color: var(--color-text-60);
	}
```

- [ ] **Step 2: Escribir el componente**

`frontend/src/lib/components/FlujoPoliza.svelte`:

```svelte
<script lang="ts">
	/**
	 * FlujoPoliza - barra de pasos datos → cotizaciones → propuesta → entrega.
	 *
	 * No decide nada: sólo pinta lo que `flujoPoliza()` deriva, para que el
	 * detalle, generar, entregar y la lista muestren exactamente el mismo estado.
	 */
	import { flujoPoliza } from '$utils';
	import type { PasoId } from '$utils';
	import type { Poliza } from '$lib/types/poliza';
	import { ESTADO_LABELS } from '$utils';

	export let poliza: Poliza;
	export let rubroSlug: string;
	/** Marca el paso en curso cuando la pantalla ES ese paso. */
	export let pasoActual: PasoId | null = null;

	$: flujo = flujoPoliza(poliza, rubroSlug);
</script>

<nav class="flujo" aria-label="Progreso de la póliza">
	{#each flujo.pasos as paso, i}
		{#if i > 0}
			<span class="flujo-sep" aria-hidden="true"></span>
		{/if}

		{@const marcado = pasoActual ? paso.id === pasoActual : paso.current}
		{@const clases = `flujo-paso ${paso.done ? 'flujo-paso-done' : ''} ${
			marcado && !flujo.terminal ? 'flujo-paso-current' : ''
		} ${!paso.enabled ? 'flujo-paso-blocked' : ''}`}

		{#if paso.enabled && paso.href && !flujo.terminal}
			<a href={paso.href} class={clases} aria-current={marcado ? 'step' : undefined}>
				<span class="flujo-marca">{paso.done ? '✓' : i + 1}</span>
				{paso.label}
			</a>
		{:else}
			<span class={clases} title={paso.blockedReason ?? ''}>
				<span class="flujo-marca">{paso.done ? '✓' : i + 1}</span>
				{paso.label}
			</span>
		{/if}
	{/each}

	{#if flujo.terminal}
		<span class="flujo-terminal ml-auto">
			Póliza {ESTADO_LABELS[poliza.estado].toLowerCase()}
		</span>
	{/if}
</nav>
```

- [ ] **Step 3: Exportar**

En `frontend/src/lib/components/index.ts`, junto a `PolizaDetalle`:

```ts
export { default as FlujoPoliza } from './FlujoPoliza.svelte';
```

- [ ] **Step 4: Verificar**

```bash
cd frontend && npm run build
```

Esperado: `✔ done`. A 390px la barra debe envolver a dos filas sin desbordar.

**Desviación consciente respecto al spec:** el spec pedía reducir la barra en
móvil a "Paso 3 de 4 · Propuesta". Se implementa con `flex-wrap` (las cuatro
etiquetas envuelven a dos filas) porque son cortas y caben; una representación
distinta en móvil sería una segunda cosa que mantener sincronizada sin ganancia
real.

---

### Task 5: Detalle — barra, acción única y escape de admin

**Files:**
- Modify: `frontend/src/lib/components/PolizaDetalle.svelte`

**Interfaces:**
- Consumes: `FlujoPoliza` (Task 4), `flujoPoliza` (Task 3), `hasAnyRole` de `$stores/auth`.
- Produces: nada nuevo.

- [ ] **Step 1: Importar lo necesario**

Añadir a los imports de `PolizaDetalle.svelte`:

```ts
	import { FlujoPoliza } from '$components';
	import { flujoPoliza } from '$utils';
	import { auth } from '$lib/stores/auth';
```

- [ ] **Step 2: Derivar flujo y permiso**

Junto a los demás `$:` reactivos:

```ts
	$: flujo = poliza ? flujoPoliza(poliza, rubroSlug) : null;
	// Escape para corregir pólizas mal cargadas; el resto sigue el flujo.
	$: puedeForzarEstado =
		$auth.user?.tipo_usuario === 'ADMINISTRADOR' || $auth.user?.tipo_usuario === 'SUPERADMIN';
```

- [ ] **Step 3: Reemplazar el bloque de acciones del PageHeader**

Sustituir el contenido actual de `<svelte:fragment slot="actions">` por:

```svelte
		<svelte:fragment slot="actions">
			{#if poliza && flujo}
				{#if flujo.siguiente}
					{#if flujo.siguiente.enabled && flujo.siguiente.href}
						<a class="btn-primary !min-h-[38px]" href={flujo.siguiente.href}>
							Continuar: {flujo.siguiente.label}
						</a>
					{:else}
						<button class="btn-primary !min-h-[38px]" disabled title={flujo.siguiente.blockedReason}>
							{flujo.siguiente.blockedReason}
						</button>
					{/if}
				{/if}
				{#if !editMode}
					<button type="button" class="btn-secondary !min-h-[38px]" on:click={() => (editMode = true)}>
						Editar
					</button>
				{/if}
				{#if puedeForzarEstado && poliza.estado !== 'CANCELADA'}
					<button type="button" class="btn-secondary !min-h-[38px]" on:click={openCambiarEstadoModal}>
						Cambiar estado
					</button>
				{/if}
			{/if}
		</svelte:fragment>
```

- [ ] **Step 4: Insertar la barra bajo el PageHeader**

Inmediatamente después de `</PageHeader>`:

```svelte
	{#if poliza}
		<FlujoPoliza {poliza} {rubroSlug} />
	{/if}
```

- [ ] **Step 5: Ajustar la tarjeta "Acciones" del riel**

En la tarjeta `Acciones` del riel derecho: quitar los enlaces sueltos a `/generar` y `/entregar` (ahora los gobierna la barra y el botón primario) y dejar sólo:
- "Generar documento de entrega" → `{base}/generar?doc=entrega`, **visible sólo si** `poliza.estado === 'VIGENTE'`. Muestra la fecha de `entrega_generada_at` debajo si no es nula.
- "Cambiar estado" sólo si `puedeForzarEstado`.
- "Volver al listado".

- [ ] **Step 6: Verificar en navegador**

Con el frontend en `:3000` y sesión iniciada, abrir `/propuestas/copropiedad/5`:
- la barra muestra 4 pasos, con ③ bloqueado y motivo "Primero genera la propuesta" al pasar el cursor si aún no hay propuesta,
- hay **un solo** botón primario,
- con `superadmin` aparece "Cambiar estado".

```bash
cd frontend && npm run build
```

---

### Task 6: `/generar` — barra, un solo propósito y marcado del hito

**Files:**
- Modify: `frontend/src/routes/propuestas/hogar/[id]/generar/+page.svelte`
- Modify: `frontend/src/routes/propuestas/vehiculo/[id]/generar/+page.svelte`
- Modify: `frontend/src/routes/propuestas/copropiedad/[id]/generar/+page.svelte`
- Modify: `frontend/src/routes/propuestas/otro/[id]/generar/+page.svelte`

**Interfaces:**
- Consumes: `FlujoPoliza`, `polizaService.<rubro>.marcarDocumento`.
- Produces: nada nuevo.

Aplicar los mismos 4 cambios en los cuatro archivos, cambiando sólo el rubro (`hogar` / `vehiculo` / `copropiedad` / `otro`) y el servicio correspondiente (`polizaService.hogar`, `.vehiculo`, `.copropiedad`, `.otroBien`).

- [ ] **Step 1: Insertar la barra**

Después de `</PageHeader>`:

```svelte
	{#if poliza}
		<FlujoPoliza {poliza} rubroSlug="hogar" pasoActual="propuesta" />
	{/if}
```

Importar `FlujoPoliza` desde `$components`.

- [ ] **Step 2: Marcar el hito tras generar**

Dentro de `generarPropuesta()`, inmediatamente después de que `propuestaService.generateAndDownload(...)` resuelva con éxito y antes del `addNotification` de éxito:

```ts
			// El backend de generación no sabe de qué póliza viene el documento,
			// así que la marca se hace aquí. Si esto falla la descarga ya ocurrió:
			// se avisa y el usuario puede volver a generar (es idempotente).
			try {
				poliza = await polizaService.hogar.marcarDocumento(polizaId, 'propuesta');
			} catch (err) {
				addNotification({
					type: 'warning',
					title: 'Documento generado, marca pendiente',
					message: 'Se descargó la propuesta pero no se pudo registrar. Vuelve a generarla.'
				});
			}
```

- [ ] **Step 3: Quitar el doble propósito**

Eliminar el botón "Generar entrega" y la función `generarEntrega()` **sólo si** el parámetro de consulta `doc` no es `entrega`. Concretamente: leer `$page.url.searchParams.get('doc')` y renderizar el botón de entrega únicamente cuando valga `'entrega'`; en ese caso el botón de propuesta no se muestra. Así la ruta sigue sirviendo ambos documentos, pero **el modo lo decide la URL y no el estado**, que era la fuente de confusión.

En el modo entrega, tras `generateAndDownload` exitoso marcar `'entrega'` en lugar de `'propuesta'`.

- [ ] **Step 4: Volver al detalle tras generar**

Al final de `generarPropuesta()` exitoso, navegar a `/propuestas/<rubro>/${polizaId}` para que el usuario vea el paso ③ ya en verde.

- [ ] **Step 5: Verificar**

```bash
cd frontend && npm run build
```

Y en navegador: entrar a `/propuestas/copropiedad/5/generar`, generar, comprobar que vuelve al detalle con ③ marcado. Revertir después:

```bash
docker exec alfabroker-db psql -U admin -d alfabroker -c \
  "UPDATE polizas_copropiedad SET propuesta_generada_at = NULL WHERE id = 5;"
```

---

### Task 7: `/entregar` — barra y bloqueo

**Files:**
- Modify: `frontend/src/routes/propuestas/hogar/[id]/entregar/+page.svelte`
- Modify: `frontend/src/routes/propuestas/vehiculo/[id]/entregar/+page.svelte`
- Modify: `frontend/src/routes/propuestas/copropiedad/[id]/entregar/+page.svelte`
- Modify: `frontend/src/routes/propuestas/otro/[id]/entregar/+page.svelte`

**Interfaces:**
- Consumes: `FlujoPoliza`, `flujoPoliza`.
- Produces: nada nuevo.

Mismos cambios en los cuatro, cambiando el rubro.

- [ ] **Step 1: Insertar la barra y derivar el bloqueo**

Importar `FlujoPoliza` y `flujoPoliza`. Añadir:

```ts
	$: pasoEntrega = poliza ? flujoPoliza(poliza, 'hogar').pasos.find((p) => p.id === 'entrega') : null;
```

Y tras `</PageHeader>`:

```svelte
	{#if poliza}
		<FlujoPoliza {poliza} rubroSlug="hogar" pasoActual="entrega" />
	{/if}
```

- [ ] **Step 2: No montar el formulario si está bloqueado**

Envolver el formulario existente:

```svelte
	{#if poliza && pasoEntrega && !pasoEntrega.enabled}
		<EmptyState title="Falta generar la propuesta" text={pasoEntrega.blockedReason}>
			<a slot="action" class="btn-primary" href="/propuestas/hogar/{polizaId}/generar">
				Generar propuesta
			</a>
		</EmptyState>
	{:else}
		<!-- formulario actual, sin cambios -->
	{/if}
```

Importar `EmptyState` desde `$components`. La validación existente de `estado === 'PROSPECTO'` se conserva tal cual.

- [ ] **Step 3: Verificar**

```bash
cd frontend && npm run build
```

Y en navegador: con una póliza sin `propuesta_generada_at`, `/propuestas/{tipo}/{id}/entregar` debe mostrar el bloqueo con enlace a generar, no el formulario.

---

### Task 8: Lista de pólizas — cerrar la puerta trasera

**Files:**
- Modify: `frontend/src/routes/propuestas/+page.svelte`

**Interfaces:**
- Consumes: `flujoPoliza`.
- Produces: nada nuevo.

- [ ] **Step 1: Derivar el flujo por fila**

`PolizaRow` ya lleva `raw` (la póliza completa) y `tipo`. En el `{#each}` del listado:

```svelte
			{#each filtered as row (row.tipo + row.id)}
				{@const flujo = flujoPoliza(row.raw, rubroByTipo(row.tipo).slug)}
```

Importar `flujoPoliza` y `rubroByTipo` desde `$utils`.

- [ ] **Step 2: Deshabilitar las acciones bloqueadas del menú**

Sustituir los enlaces fijos del `DropdownMenu` por:

```svelte
						<DropdownMenu width={230} height={180}>
							<a class="menu-item" href={row.href}>Ver detalle</a>
							{#each flujo.pasos.filter((p) => p.id === 'propuesta' || p.id === 'entrega') as paso}
								{#if paso.enabled && paso.href}
									<a class="menu-item" href={paso.href}>
										{paso.id === 'propuesta' ? 'Generar propuesta' : 'Entregar póliza'}
									</a>
								{:else}
									<span class="menu-item opacity-50 cursor-not-allowed" title={paso.blockedReason}>
										{paso.id === 'propuesta' ? 'Generar propuesta' : 'Entregar póliza'}
									</span>
								{/if}
							{/each}
						</DropdownMenu>
```

- [ ] **Step 3: Verificar**

```bash
cd frontend && npm run build
```

En navegador: en `/propuestas`, el menú de una fila sin cotizaciones muestra "Generar propuesta" atenuado; el de una sin propuesta muestra "Entregar póliza" atenuado.

---

### Task 9: Formularios a dos columnas (cambio compartido)

**Files:**
- Modify: `frontend/src/lib/components/FormField.svelte`
- Modify: `frontend/src/app.css`

**Interfaces:**
- Consumes: nada.
- Produces: `FormField` con etiqueta arriba por defecto y prop `wide: boolean`.

- [ ] **Step 1: Invertir el default de FormField**

En `FormField.svelte`: cambiar `export let vertical: boolean = false;` por `= true`, y añadir:

```ts
	/** Ocupa la fila completa de la rejilla de la sección. */
	export let wide: boolean = false;
```

Añadir `form-field-wide` a las clases del contenedor cuando `wide` sea true.

- [ ] **Step 2: Convertir la sección en rejilla**

En `app.css`, sustituir:

```css
	.form-section-content {
		@apply pb-6 space-y-6;
	}
```

por:

```css
	/* Rejilla de dos columnas: la causa de que los formularios se vieran
	   infinitos era una sola línea — un campo por fila, siempre. */
	.form-section-content {
		@apply grid pb-6 gap-x-5 gap-y-4;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
	}

	.form-section-content > * {
		min-width: 0;
	}

	.form-field-wide {
		grid-column: 1 / -1;
	}
```

- [ ] **Step 3: Verificar que nada se rompió**

```bash
cd frontend && npm run build && npm run check 2>&1 | tail -2
```

Esperado: build `✔ done`; `check` sin errores nuevos.

- [ ] **Step 4: Revisar visualmente los 6 formularios**

Abrir a 1440px y confirmar dos columnas, y a 390px confirmar una sola:
`/clientes/nuevo`, `/clientes/1/editar`, `/bienes/nuevo?tipo=HOGAR`,
`/bienes/hogar/1/editar`, `/bienes/copropiedad/1/editar`, `/propuestas/nueva/hogar`.

---

### Task 10: Marcar los campos anchos

**Files:**
- Modify: `frontend/src/routes/clientes/nuevo/+page.svelte`
- Modify: `frontend/src/routes/clientes/[id]/editar/+page.svelte`
- Modify: `frontend/src/routes/bienes/nuevo/+page.svelte`
- Modify: `frontend/src/routes/bienes/hogar/[id]/editar/+page.svelte`
- Modify: `frontend/src/routes/bienes/vehiculo/[id]/editar/+page.svelte`
- Modify: `frontend/src/routes/bienes/copropiedad/[id]/editar/+page.svelte`
- Modify: `frontend/src/routes/bienes/otro/[id]/editar/+page.svelte`
- Modify: `frontend/src/routes/propuestas/nueva/[tipo]/+page.svelte`

**Interfaces:**
- Consumes: prop `wide` de Task 9.
- Produces: nada.

- [ ] **Step 1: Aplicar la regla campo por campo**

Añadir `wide` al `<FormField>` cuando se cumpla alguno de estos criterios:

- el control es un `textarea`, o
- el valor esperado supera ~40 caracteres (direcciones, razón social, observaciones, detalles del bien), o
- el campo es el único de su sección.

Todo lo demás (documentos, teléfonos, ciudades, fechas, montos, selects) queda a media fila. **Ante la duda, media fila:** un `wide` de más devuelve el formulario a una columna, que es justo lo que se quiere evitar.

- [ ] **Step 2: Verificar**

```bash
cd frontend && npm run build
```

Y revisar a 1440px que no quedan filas de una sola columna salvo las marcadas a propósito.

- [ ] **Step 3: Probar que el guardado no cambió**

Crear un cliente de prueba desde `/clientes/nuevo`, confirmar que se guarda, y borrarlo después:

```bash
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" \
  -d '{"usuario":"superadmin","clave":"admin123"}' | python -c "import sys,json;print(json.load(sys.stdin)['data']['tokens']['access_token'])")
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/usuarios/<id> -o /dev/null -w "%{http_code}\n"
```

---

## Verificación final

- [ ] `npm run build` termina en `✔ done`.
- [ ] `npm run check` no supera la línea base de 261 errores en 14 archivos.
- [ ] Recorrido completo sobre una póliza `PROSPECTO` con backend real: cotizaciones → generar (descarga + ③ marcado) → entregar (habilitado sólo ahora) → `VIGENTE` → documento de entrega.
- [ ] Póliza sin cotizaciones: "Generar propuesta" bloqueado, con motivo, en detalle **y** en el menú de la lista.
- [ ] Usuario `AGENTE`: no se ofrece "Cambiar estado".
- [ ] Formularios a 1440px en dos columnas y a 390px en una.
- [ ] Todo dato de prueba revertido.
