## Context

El sistema actualmente genera propuestas de pólizas con múltiples opciones de aseguradoras (1-5) y calcula valores de cuotas para diferentes planes de financiación (3, 5, 8, 11 cuotas) en el frontend al momento de generar el PDF. Sin embargo, estos cálculos no se persisten en la base de datos. Cuando el cliente acepta una propuesta, el agente debe registrar la "entrega" de la póliza, capturando información adicional como el número de póliza expedido por la aseguradora, el plan de financiación seleccionado, y establecer el estado de la póliza como VIGENTE.

**Arquitectura actual:**
- Backend: Flask con SQLAlchemy, modelo `BasePolizaMixin` compartido por 4 tipos de póliza (copropiedad, hogar, vehículo, otro bien)
- Frontend: SvelteKit, rutas separadas por rubro `/propuestas/{rubro}/{id}/generar`
- Base de datos: PostgreSQL

**Constraint critico:** Los valores de cuotas mostrados al cliente en la propuesta PDF deben ser exactamente los mismos valores usados en la entrega para evitar inconsistencias contractuales.

## Goals / Non-Goals

**Goals:**
- Agregar campos de entrega a `BasePolizaMixin` para capturar información post-aceptación
- Implementar endpoint de entrega con validaciones de transición de estado (PROSPECTO → VIGENTE)
- Auto-llenar datos de aseguradora seleccionada (nombre, numeral asistencia) desde tabla `aseguradoras`
- Persistir valores de cuotas calculadas en propuesta para mantener consistencia con lo ofrecido al cliente
- Permitir administración manual de estado de cartera y cuota actual sin automatizaciones
- Crear vista de detalle mejorada que muestre información de entrega como sección principal para pólizas vigentes

**Non-Goals:**
- Automatización de notificaciones de pago o vencimiento de cuotas
- Sistema de gestión de cobros o integración con pasarelas de pago
- Cálculo dinámico de intereses o recálculo de cuotas después de generar propuesta
- Tabla relacional separada para cuotas (innecesario para gestión manual simple)
- Modificación del flujo de generación de PDF (solo agregar persistencia de valores calculados)

## Decisions

### 1. Guardar valores de cuotas pre-calculadas en BasePolizaMixin

**Decisión:** Agregar 4 campos `valor_cuota_3`, `valor_cuota_5`, `valor_cuota_8`, `valor_cuota_11` en `BasePolizaMixin` para guardar los valores calculados al generar la propuesta.

**Rationale:** 
- ✅ Garantiza que el valor de cuota en la entrega coincide exactamente con el PDF mostrado al cliente
- ✅ Evita errores por cambios en tasas de interés entre generación de propuesta y entrega
- ✅ No requiere lógica de recálculo en backend
- ✅ Auditabilidad: se preserva el histórico de lo ofrecido

**Alternativas consideradas:**
- ❌ **Guardar solo la tasa y recalcular:** Riesgo de inconsistencia si la tasa cambia entre propuesta y entrega
- ❌ **Usuario ingresa valor manual:** Propenso a errores de digitación, sin validación contra lo ofrecido
- ❌ **No guardar valores (solo calcular en frontend):** Imposible recuperar valores exactos mostrados en propuesta anterior

**Implementación:** Calcular y guardar al hacer POST/PATCH en endpoint de generación de propuesta, no al crear la póliza inicial.

### 2. Modelo de datos para financiación: Campos en BasePolizaMixin vs tabla relacionada

**Decisión:** Agregar campos de financiación directamente en `BasePolizaMixin` (num_cuotas, cuota_actual, valor_cuota, fecha_primera_cuota, periodicidad, estado_cartera) en lugar de crear tabla `plan_pago` o `cuotas_poliza`.

**Rationale:**
- ✅ Suficiente para gestión manual declarada como no-goal (ver propuesta: "gestion es manual")
- ✅ Evita complejidad de JOINs en consultas frecuentes de detalles de póliza
- ✅ Todas las pólizas tienen máximo 1 plan de pago, no hay necesidad de relación 1:N
- ✅ Las "fechas de pago" se calculan trivialmente (fecha_primera + N meses), no necesitan fila por cuota

**Alternativas consideradas:**
- ❌ **Tabla `cuotas_poliza` con 1 fila por cuota:** Over-engineering para gestión manual, requeriría CRUD adicional
- ❌ **Tabla `plan_pago` separada:** Agrega complejidad sin beneficio claro para caso de uso actual

**Consecuencia:** Si en el futuro se requiere automatización de cobros con estado por cuota individual, será necesario refactorizar a modelo relacional.

### 3. Endpoint de entrega: PUT vs POST vs PATCH

**Decisión:** Crear endpoint `POST /api/polizas/{rubro}/{id}/entregar` dedicado para transición de estado, separado de actualización general.

**Rationale:**
- ✅ Semánticamente claro: "entregar" es una acción de negocio específica, no solo actualización de campos
- ✅ Permite validaciones específicas de transición (ver `validar_estado()` en BasePolizaMixin)
- ✅ Facilita logging/auditoría de evento crítico de negocio
- ✅ Endpoint adicional `PATCH /api/polizas/{rubro}/{id}/actualizar-entrega` para ediciones posteriores sin re-validar transición

**Alternativas consideradas:**
- ❌ **PATCH genérico:** Mezcla lógica de creación con actualización, dificulta validaciones específicas
- ❌ **PUT completo:** Requiere enviar todos los campos, verboso e innecesario

### 4. Auto-llenado de datos de aseguradora: Frontend vs Backend

**Decisión:** Backend retorna datos de aseguradora (nombre, numeral_asistencia) al recibir `aseguradora_seleccionada`, frontend los muestra read-only pero los envía de vuelta en el POST.

**Rationale:**
- ✅ Evita discrepancias si datos de aseguradora cambian después de generar propuesta (desnormalización intencional)
- ✅ Frontend obtiene datos vía endpoint dedicado `GET /api/aseguradoras/{id}/datos-entrega` al cambiar selección
- ✅ Campos `nombre_aseguradora` y `numeral_asistencia` en póliza son snapshot del momento de entrega
- ✅ Performance: evita JOIN con tabla aseguradoras en cada consulta de póliza

**Alternativas consideradas:**
- ❌ **Relación FK directa sin desnormalización:** JOIN innecesario en consultas frecuentes, riesgo de inconsistencia si aseguradora cambia nombre
- ❌ **Calcular en backend sin envío desde frontend:** Requiere lógica de "última escritura gana" si datos de aseguradora cambiaron

### 5. medio_pago enum vs boolean

**Decisión:** Usar `medio_pago VARCHAR(20)` con valores "contado" | "financiera" en lugar de boolean `is_financiado`.

**Rationale:**
- ✅ Extensible si en el futuro se agregan otros medios (ej: "tarjeta_credito", "cheque")
- ✅ Más legible en queries y logs: `WHERE medio_pago = 'financiera'` vs `WHERE is_financiado = true`
- ✅ Validación clara con CHECK constraint en SQL

**Alternativa considerada:**
- ❌ **Boolean:** Menos flexible, requiere migración si se agregan opciones

### 6. Fechas de pago: Modelo simplificado

**Decisión:** Guardar solo `financiacion_fecha_primera_cuota DATE` y `financiacion_periodicidad VARCHAR(20)` (default: "mensual"), calcular fechas subsecuentes en frontend cuando se necesiten mostrar.

**Rationale:**
- ✅ Suficiente para validación manual por agente: ver fecha próxima en UI = primera_cuota + (cuota_actual - 1) * 1 mes
- ✅ Evita campos redundantes (fecha_cuota_1, fecha_cuota_2, ...) o JSON complejo
- ✅ Flexible si en el futuro se requieren periodicidades no mensuales (bimestral, trimestral)

**Alternativa considerada:**
- ❌ **Array JSON de fechas:** Más rígido, dificulta queries, requiere re-guardar si cambia fecha base

## Risks / Trade-offs

### [Risk] Valores de cuotas guardados pueden quedar desincronizados si se edita valor de prima después de generar propuesta
**Mitigation:** Validación en backend: si `valor_prima_aseg_X` cambia después de guardar valores de cuotas, endpoint de entrega requiere re-generar propuesta primero (status check). Alternativamente, recalcular valores de cuota en endpoint de entrega si detección de desincronización.

### [Risk] Desnormalización de nombre_aseguradora puede causar inconsistencias si aseguradora cambia nombre
**Trade-off aceptado:** Snapshot intencional. El nombre en la póliza refleja el nombre de la aseguradora *al momento de la entrega*, no el nombre actual. Beneficio de performance y simplicidad supera el riesgo de confusión.

### [Risk] Campo periodicidad actualmente sin validación puede llevar a valores inconsistentes
**Mitigation:** CHECK constraint en SQL: `periodicidad IN ('mensual', 'bimestral', 'trimestral')`. Frontend solo permite "mensual" en v1.

### [Risk] Sin tabla de cuotas separada, difícil implementar pagos parciales o automatización en el futuro
**Trade-off aceptado:** Refactorización necesaria si se requiere automatización. Para caso de uso actual (gestión manual), complejidad adicional no justificada. Documentar como deuda técnica conocida.

### [Risk] Migración agrega 11 columnas a 4 tablas, impacto en queries existentes
**Mitigation:** Todas las columnas son nullable y no se usan en queries existentes. No hay breaking changes. Performance: agregar índice en `medio_pago` si se filtran pólizas por este campo frecuentemente (evaluar después de despliegue).

## Migration Plan

**Fase 1: Backend**
1. Crear migración SQL para agregar columnas en `BasePolizaMixin` (aplica a 4 tablas)
2. Agregar campos y métodos de validación en modelo Python
3. Crear endpoints de entrega y actualización
4. Endpoint auxiliar `GET /api/aseguradoras/{id}/datos-entrega`
5. Tests unitarios de validaciones de transición

**Fase 2: Frontend - Guardar cuotas en propuesta**
1. Modificar componentes de generación de propuesta (4 rubros) para guardar valores calculados
2. PATCH al endpoint de póliza para actualizar `valor_cuota_*` después de calcular

**Fase 3: Frontend - Formulario entrega**
1. Crear rutas `/propuestas/{rubro}/{id}/entregar`
2. Componente de formulario con auto-llenado y validaciones
3. Integración con endpoints de entrega

**Fase 4: Frontend - Vista detalle**
1. Refactorizar `/polizas/{rubro}/{id}` para mostrar info de entrega si estado=VIGENTE
2. Componente editable de gestión de cartera

**Rollback:** Migración es aditiva (solo columnas nuevas nullable), rollback de código suficiente. Si necesario, ejecutar `ALTER TABLE DROP COLUMN` en reverse.

## Open Questions

1. ¿Se requiere cambio en el modelo de permisos? ¿Solo admin puede hacer entrega o también agentes regulares?
   - **Asumir:** Agentes pueden entregar pólizas que ellos crearon. Admin puede entregar cualquiera.

2. ¿Calcular `ingreso_comision_percibido` automáticamente o requerir input manual?
   - **Asumir:** Campo editable, pre-llenado con lógica existente si ya existe.

3. ¿Validar que `inicio_vigencia` es posterior a fecha de creación de propuesta?
   - **Asumir:** Sí, agregar validación simple en backend.

4. ¿Permitir múltiples entregas? (ej: renovación de póliza vencida)
   - **Asumir:** No para v1. Póliza solo puede entregarseuna vez. Renovación creará nueva póliza separada.
