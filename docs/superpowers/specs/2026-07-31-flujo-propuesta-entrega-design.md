# Flujo propuesta → entrega, y densidad de formularios

Fecha: 2026-07-31
Estado: aprobado, pendiente de plan de implementación

## Problema

Generar la propuesta y entregar la póliza hoy son dos botones hermanos en la
pantalla de detalle, sin orden visible ni requisitos declarados. Concretamente:

1. `/propuestas/{tipo}/{id}/generar` hace **dos cosas distintas** según el estado
   de la póliza: produce el documento de propuesta si está en `PROSPECTO`, o el
   documento de entrega si está en `VIGENTE`. Misma ruta, dos propósitos, y el
   segundo caso vive en un botón que sólo aparece a veces.
2. `/generar` **no** cambia el estado; `/entregar` sí (pasa a `VIGENTE`). Nada en
   la interfaz dice cuál mueve qué.
3. El estado se modifica desde **tres** sitios: el modal "Cambiar estado" del
   detalle, el endpoint `entregar`, y nada en generar.
4. No existe registro de que una propuesta haya sido generada, así que no hay
   forma de exigir que la propuesta preceda a la entrega.

En paralelo, los formularios crecen sin control porque `.form-field` es
`grid-cols-[280px_1fr]`: etiqueta a la izquierda, **un campo por fila**, siempre.

| Formulario | Campos | Secciones |
|---|---|---|
| `bienes/nuevo` | 43 | 4 |
| `propuestas/nueva/[tipo]` | 27 | 5 |
| `clientes/nuevo` | 19 | 5 |
| `bienes/copropiedad/[id]/editar` | 18 | 4 |
| `clientes/[id]/editar` | 17 | 4 |

(`aseguradoras/nueva` y `aseguradoras/[id]/editar` ya usan pestañas por rubro y
rejilla; quedan fuera de este cambio.)

## Objetivo

- Un recorrido visible y ordenado: datos → cotizaciones → propuesta → entrega.
- La entrega sólo es posible después de generar la propuesta.
- Formularios a dos columnas, sin cambiar cómo se guardan.

## Decisiones tomadas

| Decisión | Elegido | Descartado |
|---|---|---|
| Forma del flujo | Rutas separadas + barra de progreso compartida | Wizard en una sola ruta; botón único "siguiente paso" |
| Hito "propuesta generada" | Columna nueva en backend | Deducirlo en frontend; endpoint que liste archivos en disco |
| Layout de formularios | 2 columnas + acordeones actuales | Secciones como pasos; secciones como pestañas |
| Rigidez del orden | Bloqueo, con escape para ADMINISTRADOR/SUPERADMIN | Bloqueo total; sólo advertencia |

## Modelo de pasos

Cuatro pasos. Ninguno introduce estados nuevos: el enum sigue siendo
`PROSPECTO | VIGENTE | VENCIDA | CANCELADA`. El progreso vive en las marcas de
documento, no en el estado.

| Paso | Cumplido cuando | Origen del dato |
|---|---|---|
| ① Datos | la póliza existe | ya existe |
| ② Cotizaciones | hay al menos un `valor_prima_aseg_N` no nulo | ya existe |
| ③ Propuesta | `propuesta_generada_at` no es nulo | **nuevo** |
| ④ Entrega | `aseguradora_seleccionada` y `numero_poliza_aseguradora` presentes | ya existe |

Completar ④ implica `estado = VIGENTE` (lo hace el endpoint `entregar`, sin
cambios).

`entrega_generada_at` **no es un paso ni bloquea nada**. Registra que el
documento de entrega fue producido, y se muestra como marca dentro del paso ④ ya
cumplido ("Documento de entrega generado el …"). Existe por trazabilidad y para
que el detalle pueda distinguir "entregada" de "entregada y con documento".

`VENCIDA` y `CANCELADA` no son pasos. Con la póliza en uno de esos estados la
barra se muestra inactiva, con el estado terminal como etiqueta y sin acción
siguiente (salvo el escape de admin).

### Una sola función de derivación

En `frontend/src/lib/utils/polizas.ts`:

```ts
export type PasoId = 'datos' | 'cotizaciones' | 'propuesta' | 'entrega';

export interface PasoFlujo {
  id: PasoId;
  label: string;
  done: boolean;
  /** Es el paso en el que está la póliza ahora. */
  current: boolean;
  /** Se puede entrar al paso; false cuando falta un requisito. */
  enabled: boolean;
  /** Ruta de la acción del paso, si tiene una. */
  href?: string;
  /** Por qué está bloqueado; se muestra en el botón deshabilitado. */
  blockedReason?: string;
}

export interface FlujoPoliza {
  pasos: PasoFlujo[];
  /** Próxima acción, o null si terminó o el estado es terminal. */
  siguiente: PasoFlujo | null;
  terminal: boolean;
}

export function flujoPoliza(poliza: Poliza, rubroSlug: string): FlujoPoliza;
```

La consumen cuatro sitios: el detalle, `/generar`, `/entregar`, y el menú de
acciones de la lista de pólizas (para que "Entregar" también salga deshabilitado
ahí). Escrita por pantalla se desincronizaría; por eso vive en utils y no en un
componente.

## Cambios de backend

### Migración

`backend/migrations/add_documentos_generados.sql`, siguiendo la convención del
repo (SQL plano aplicado a mano, no Alembic — ver `add_entrega_poliza_fields.sql`):

```sql
ALTER TABLE polizas_hogar       ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_hogar       ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
ALTER TABLE polizas_vehiculo    ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_vehiculo    ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
ALTER TABLE polizas_copropiedad ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_copropiedad ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
ALTER TABLE polizas_otro_bien   ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_otro_bien   ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
```

Ambas columnas son nulas para todo lo existente. Las pólizas ya vigentes quedan
con el paso ③ sin marcar; es correcto — nadie registró ese documento. El escape
de admin cubre la corrección si hace falta.

### Modelo

`backend/app/models/polizas/base_poliza.py`: las dos columnas, e incluirlas en
`to_dict()` en formato ISO (o `None`), igual que `created_at` / `updated_at`.

### Endpoint

`PATCH /api/polizas/{tipo}/{id}/marcar-documento`

```json
{ "documento": "propuesta" }   // o "entrega"
```

Escribe `now()` en la columna correspondiente y devuelve la póliza actualizada.
Rechaza cualquier otro valor de `documento` con 400. Mismo control de acceso que
el resto de `/api/polizas`.

**Por qué un endpoint aparte y no marcarlo dentro de `/api/propuestas/generate`:**
ese endpoint recibe `template_name` y un diccionario de variables; no sabe de qué
póliza proviene. Pasarle el id acoplaría el servicio de propuestas al de pólizas,
en contra de la separación por dominio que sigue el backend.

**Riesgo asumido:** si la descarga funciona pero el PATCH falla, el hito no queda
marcado. El frontend muestra el aviso de error y el usuario puede volver a
generar; la operación es idempotente. No se introduce reintento automático.

## Cambios de frontend

### Componente nuevo

`frontend/src/lib/components/FlujoPoliza.svelte`

```
export let poliza: Poliza;
export let rubroSlug: string;
/** Marca el paso en curso cuando la pantalla ES ese paso. */
export let pasoActual: PasoId | null = null;
```

Barra horizontal de 4 pasos: cumplido (relleno dorado + check), en curso (borde
dorado), pendiente (gris). Cada paso cumplido o habilitado es un enlace; los
bloqueados no lo son y llevan `title` con el motivo. En móvil se reduce a
"Paso 3 de 4 · Propuesta" con la barra de progreso, para no comprimir cuatro
etiquetas en 390px.

### Pantallas

**Detalle** (`PolizaDetalle.svelte`) — `<FlujoPoliza>` bajo el `PageHeader`, y en
el slot de acciones **un solo botón primario** "Continuar: …" que refleja
`flujo.siguiente`. Las demás acciones pasan a secundarias o al riel. Si
`flujo.terminal`, no hay botón primario.

**`/generar`** — misma barra con `pasoActual="propuesta"`. Al terminar la
descarga con éxito llama `marcarDocumento('propuesta')` y navega al detalle.
Deja de decidir por estado qué documento produce: esta ruta genera **sólo** la
propuesta.

**`/entregar`** — misma barra con `pasoActual="entrega"`. Si el paso está
bloqueado, el formulario no se monta: se muestra el motivo y un enlace a
`/generar`. La validación de `estado === 'PROSPECTO'` que ya existe se conserva.

**Documento de entrega** — el botón "Generar entrega" que hoy vive escondido en
`/generar` se mueve al paso ④: aparece en el detalle una vez la póliza está
vigente, y marca `entrega_generada_at`.

**Lista de pólizas** (`/propuestas`) — el menú de acciones de cada fila también
lee `flujoPoliza`: "Generar propuesta" y "Entregar póliza" se deshabilitan con el
mismo motivo que en el detalle, en vez de ofrecer siempre las dos. Sin esto la
lista seguiría siendo una puerta trasera al orden que el detalle sí respeta.

### Escape de admin

El modal "Cambiar estado" de `PolizaDetalle` se envuelve en
`hasAnyRole(['ADMINISTRADOR', 'SUPERADMIN'])` (helper ya existente en
`$stores/auth`). Para los demás roles el estado sólo se mueve por el flujo.

## Densidad de formularios

Dos cambios compartidos, sin tocar cómo se arma ni se envía el payload:

1. `FormField.svelte` — la variante vertical (etiqueta arriba) pasa a ser el
   comportamiento por defecto. El componente ya tiene la prop `vertical`; se
   invierte el default y se añade `wide` para los campos que deben ocupar la fila
   completa.
2. `.form-section-content` en `app.css` — de `space-y-6` a
   `grid gap-x-5 gap-y-4; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`.
   `.form-field-wide` hace `grid-column: 1 / -1`.

Alcance: los 6 formularios listados arriba mejoran a la vez. Los acordeones
(`FormSection`) se conservan tal cual.

Regla para marcar `wide`, aplicada campo por campo al hacer el cambio:

- el control es un `textarea`, o
- el valor esperado supera ~40 caracteres (direcciones, razón social,
  observaciones, detalles del bien), o
- el campo es el único de su sección.

Todo lo demás (documentos, teléfonos, ciudades, fechas, montos, selects) queda a
media fila. Ante la duda, media fila: `wide` de más devuelve el formulario a una
columna, que es justo lo que se quiere evitar.

## Verificación

1. `npm run build` pasa; `svelte-check` no suma errores nuevos sobre la línea
   base (261 errores preexistentes en 14 archivos).
2. Aplicar la migración contra la base local y comprobar que `to_dict()` devuelve
   las dos columnas nuevas.
3. Recorrido completo con el backend real sobre una póliza `PROSPECTO`:
   cotizaciones → generar (descarga + hito marcado) → entregar (habilitado sólo
   ahora) → estado `VIGENTE` → generar documento de entrega.
4. Con una póliza sin cotizaciones: "Generar propuesta" bloqueado con motivo.
   Con cotizaciones pero sin propuesta: "Entregar" bloqueado con motivo.
5. Con un usuario `AGENTE`: el modal "Cambiar estado" no se ofrece.
6. Formularios a 1440px y 390px: dos columnas y una columna respectivamente, sin
   desbordes; guardar un cliente y un bien y verificar que el payload no cambió.
7. Revertir cualquier dato de prueba creado durante la verificación.
