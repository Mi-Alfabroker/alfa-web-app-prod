## Why

El sistema actualmente solo soporta generación de propuestas para el rubro de Copropiedades. Los clientes necesitan generar propuestas para los rubros de Hogar, Vehículos y Otros Seguros, que representan una parte significativa de su negocio. Sin esta funcionalidad, deben generar propuestas manualmente, lo que aumenta tiempos de entrega y errores.

## What Changes

- Extender modelo `Aseguradora` con campos de configuración para rubros Hogar (`hog_*`), Vehículos (`veh_*`) y Otros (`otr_*`)
- Agregar campos faltantes a modelos de bienes `Hogar` y `OtroBien` (estado, comentarios)
- Crear diccionarios de variables TypeScript para mapear placeholders `[N]` a campos descriptivos
- Implementar páginas de generación de propuestas en frontend para cada rubro
- Crear documentación de variables (formato Markdown) para referencia del cliente
- Actualizar `PropuestaService` para soportar plantillas de los nuevos rubros
- Implementar lógica de construcción de JSON de variables en frontend (función `buildVariablesJson()`)

## Capabilities

### New Capabilities

- `propuestas-hogar`: Generación de propuestas de seguro de Hogar con plantilla Excel, incluyendo formulario de captura, construcción de diccionario de variables, y descarga del documento generado
- `propuestas-vehiculos`: Generación de propuestas de seguro de Vehículos con plantilla Excel, incluyendo formulario de captura, construcción de diccionario de variables, y descarga del documento generado
- `propuestas-otros`: Generación de propuestas de Otros Seguros con plantilla Excel, incluyendo formulario de captura, construcción de diccionario de variables, y descarga del documento generado
- `diccionarios-variables`: Sistema de mapeo de códigos compactos `[N]` a nombres de campos descriptivos para cada rubro, con documentación completa

### Modified Capabilities

- `configuracion-aseguradoras`: Extensión del modelo de aseguradoras para incluir campos de configuración (deducibles, coberturas, sublímites) para los rubros Hogar, Vehículos y Otros
- `modelo-bienes-hogar`: Agregar campos `estado` y `comentarios_detalles` al modelo Hogar
- `modelo-bienes-otros`: Agregar campos `estado` y `comentarios` al modelo OtroBien

## Impact

**Backend:**
- `backend/app/models/aseguradora.py`: Agregar ~240 campos nuevos (70 para Hogar, 100 para Vehículos, 70 para Otros)
- `backend/app/models/bienes/hogar.py`: Agregar 2 campos
- `backend/app/models/bienes/otro_bien.py`: Agregar 2 campos
- `backend/app/services/propuestas/propuesta_service.py`: Actualizar diccionario TEMPLATES
- Migración SQL: ALTER TABLE para agregar columnas a `aseguradoras`, `hogares`, `otros_bienes`

**Frontend:**
- Crear 3 archivos de diccionarios: `diccionario_campos_hogar.ts`, `diccionario_campos_vehiculos.ts`, `diccionario_campos_otros.ts`
- Crear 3 páginas de generación: `routes/propuestas/hogar/[id]/generar/+page.svelte`, `vehiculos/[id]/generar/+page.svelte`, `otros/[id]/generar/+page.svelte`
- Cada página incluye ~500-800 líneas de código con formularios, validaciones y lógica de construcción del JSON

**Documentación:**
- Crear 3 archivos Markdown: `DICCIONARIO_VARIABLES_HOGAR.md`, `DICCIONARIO_VARIABLES_VEHICULOS.md`, `DICCIONARIO_VARIABLES_OTROS.md`
- Cada documento con mapeo completo de variables `[N]` → campo → descripción para referencia del cliente

**Plantillas Excel:**
- Las plantillas ya existen en `backend/app/resources/plantillas_xlsx/` (propuesta_hogar.xlsx, propuesta_vehiculos.xlsx, propuesta_otros.xlsx)
