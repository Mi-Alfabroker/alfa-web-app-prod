## Context

El sistema de gestión de pólizas Alfabroker genera documentos Excel (propuestas y entregas) reemplazando variables `[N]` en plantillas XLSX. El backend tiene un `PropuestaService` genérico que acepta cualquier `template_name` registrado en su dict `TEMPLATES` y aplica el reemplazo de variables en el XML interno del XLSX.

Estado actual antes de este cambio:
- Solo Copropiedad tenía el botón "Generar Propuesta" en su página de detalle
- Las páginas `/generar` ya existían para los 4 rubros con `buildVariablesJson()` completo
- Las plantillas XLSX de entrega ya existían en disco pero no estaban registradas en el backend
- `propuesta_vehiculos.xlsx` tenía un nombre incorrecto ("copy" en el nombre)

## Goals / Non-Goals

**Goals:**
- Habilitar generación de propuestas Excel para los 4 rubros desde la UI
- Habilitar generación de entregas Excel para los 4 rubros desde la UI
- Reutilizar las mismas variables `[N]` entre propuesta y entrega (mismo `buildVariablesJson()`)
- Arquitectura preparada para divergir los diccionarios de entrega en el futuro

**Non-Goals:**
- No se crean diccionarios de variables separados para entrega (se reutilizan los de propuesta)
- No se modifica el endpoint del backend (`POST /api/propuestas/generate` ya es genérico)
- No se modifica el componente `FormularioEntrega` ni el flujo de cambio de estado

## Decisions

### 1. Reutilizar `buildVariablesJson()` para entrega
**Decisión:** La función `generarEntrega()` llama al mismo `buildVariablesJson()` y `buildImagenesJson()` que `generarPropuesta()`, solo cambia el `template_name`.

**Alternativa descartada:** Crear `buildVariablesEntregaJson()` separado desde el inicio.

**Razón:** Las plantillas de entrega usan los mismos códigos `[N]`, duplicar ahora sería código muerto. Cuando los diccionarios divergan, se creará la función separada.

### 2. Botón "Generar Entrega" en página de detalle cuando VIGENTE
**Decisión:** El botón aparece cuando `poliza.estado === 'VIGENTE'` y navega a la misma ruta `/generar` donde el usuario puede usar el botón verde "Generar Entrega".

**Razón:** Evita crear rutas nuevas. La página `/generar` ya tiene toda la lógica de carga de datos, coberturas editables, etc.

### 3. Registrar templates de entrega en el mismo dict TEMPLATES
**Decisión:** Las 4 plantillas de entrega se agregan al dict existente con prefijo `entrega_`.

**Razón:** El `PropuestaService` ya es genérico, solo necesita el mapping nombre→archivo.

## Risks / Trade-offs

- **[Divergencia futura]** → Cuando los diccionarios de entrega necesiten variables distintas, habrá que crear `buildVariablesEntregaJson()` en cada página. El costo es moderado pero manejable.
- **[Plantilla vehículos]** → El archivo original tenía un nombre incorrecto. Se copió con el nombre correcto pero queda el archivo viejo "copy". Riesgo bajo.
- **[Mismos códigos [N]]** → Si una plantilla de entrega tiene códigos `[N]` que no existen en `buildVariablesJson()`, quedarán sin reemplazar. Mitigación: validar plantillas contra diccionarios.
