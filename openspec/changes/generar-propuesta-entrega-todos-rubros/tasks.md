## 1. Backend — Templates de Entrega

- [x] 1.1 Copiar `propuesta_vehiculos copy.xlsx` → `propuesta_vehiculos.xlsx` para corregir nombre
- [x] 1.2 Registrar 4 templates de entrega en `PropuestaService.TEMPLATES`: `entrega_hogar`, `entrega_copropiedades`, `entrega_vehiculos`, `entrega_otros`

## 2. Frontend — Botón Generar Propuesta en páginas de detalle

- [x] 2.1 Agregar botón "Generar Propuesta" en `propuestas/hogar/[id]/+page.svelte` (visible cuando PROSPECTO)
- [x] 2.2 Agregar botón "Generar Propuesta" en `propuestas/vehiculo/[id]/+page.svelte` (visible cuando PROSPECTO)
- [x] 2.3 Agregar botón "Generar Propuesta" en `propuestas/otro/[id]/+page.svelte` (visible cuando PROSPECTO)

## 3. Frontend — Función y botón Generar Entrega en páginas /generar

- [x] 3.1 Agregar variable `generatingEntrega` y función `generarEntrega()` en `propuestas/hogar/[id]/generar/+page.svelte`
- [x] 3.2 Agregar variable `generatingEntrega` y función `generarEntrega()` en `propuestas/copropiedad/[id]/generar/+page.svelte`
- [x] 3.3 Agregar variable `generatingEntrega` y función `generarEntrega()` en `propuestas/vehiculo/[id]/generar/+page.svelte`
- [x] 3.4 Agregar variable `generatingEntrega` y función `generarEntrega()` en `propuestas/otro/[id]/generar/+page.svelte`
- [x] 3.5 Agregar botón verde "Generar Entrega" en el header de las 4 páginas /generar junto al botón de propuesta

## 4. Frontend — Botón Generar Entrega en páginas de detalle

- [x] 4.1 Agregar botón "Generar Entrega" en `propuestas/hogar/[id]/+page.svelte` (visible cuando VIGENTE)
- [x] 4.2 Agregar botón "Generar Entrega" en `propuestas/copropiedad/[id]/+page.svelte` (visible cuando VIGENTE)
- [x] 4.3 Agregar botón "Generar Entrega" en `propuestas/vehiculo/[id]/+page.svelte` (visible cuando VIGENTE)
- [x] 4.4 Agregar botón "Generar Entrega" en `propuestas/otro/[id]/+page.svelte` (visible cuando VIGENTE)

## 5. Verificación

- [x] 5.1 Verificar que las 4 plantillas de entrega existen en `backend/app/resources/plantillas_xlsx/`
- [x] 5.2 Verificar que no hay errores de TypeScript en los 8 archivos modificados
- [x] 5.3 Probar flujo completo: detalle PROSPECTO → Generar Propuesta → descarga Excel
- [x] 5.4 Probar flujo completo: detalle VIGENTE → Generar Entrega → descarga Excel
