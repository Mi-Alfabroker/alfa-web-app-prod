## Why

El sistema de propuestas solo generaba documentos Excel de propuesta para Copropiedad. Los rubros Hogar, Vehículo y Otros tenían las páginas de generación implementadas pero no eran accesibles desde la interfaz (faltaba el botón "Generar Propuesta" en las páginas de detalle). Además, no existía funcionalidad para generar documentos Excel de entrega para ningún rubro, a pesar de que las plantillas XLSX ya existían en el backend.

## What Changes

- Agregar botón "Generar Propuesta" en las páginas de detalle de Hogar, Vehículo y Otros (Copropiedad ya lo tenía)
- Agregar botón "Generar Entrega" en las páginas de detalle de los 4 rubros (visible cuando estado=VIGENTE)
- Agregar función `generarEntrega()` en las 4 páginas `/generar` que reutiliza el mismo `buildVariablesJson()` pero apunta a templates de entrega
- Registrar 4 templates de entrega en el backend (`entrega_hogar`, `entrega_copropiedades`, `entrega_vehiculos`, `entrega_otros`)
- Fix: copiar `propuesta_vehiculos copy.xlsx` → `propuesta_vehiculos.xlsx` para que el backend encuentre la plantilla
- Los diccionarios de variables `[N]` son los mismos para propuesta y entrega inicialmente; la arquitectura permite divergirlos en el futuro creando un `buildVariablesEntregaJson()` separado

## Capabilities

### New Capabilities
- `generar-entrega`: Generación de documentos Excel de entrega para los 4 rubros (Hogar, Copropiedad, Vehículos, Otros) usando plantillas XLSX de entrega con las mismas variables `[N]` que las propuestas

### Modified Capabilities
<!-- Sin cambios a capabilities existentes, solo se habilitan funcionalidades que estaban desconectadas en la UI -->

## Impact

- **Frontend**: 8 archivos modificados (4 páginas de detalle + 4 páginas de generar)
- **Backend**: 1 archivo modificado (`propuesta_service.py` — TEMPLATES dict ampliado con 4 entradas de entrega)
- **Templates**: 1 archivo corregido (`propuesta_vehiculos.xlsx`), 4 plantillas de entrega ya existentes ahora mapeadas
- **API**: Sin cambios — el endpoint `POST /api/propuestas/generate` ya soporta cualquier template_name registrado
