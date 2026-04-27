## Why

Actualmente el sistema permite crear propuestas de pólizas (estado PROSPECTO) con múltiples opciones de aseguradoras y planes de financiación, pero no existe un proceso formal para registrar la entrega de la póliza cuando el cliente acepta y la aseguradora la expide. Los agentes necesitan capturar información adicional crítica (número de póliza, datos de financiación seleccionada, estado de cartera) y hacer seguimiento al ciclo de vida de pólizas vigentes.

## What Changes

- Agregar campos adicionales en `BasePolizaMixin` para capturar información de entrega: nombre aseguradora, numeral asistencia, valor total prima modificable, medio de pago, estado de cartera, y datos completos de financiación
- Crear endpoint `/api/polizas/{rubro}/{id}/entregar` para transición de PROSPECTO a VIGENTE con validaciones de negocio
- Implementar formulario de entrega en frontend que auto-llena datos de la aseguradora seleccionada y permite configurar financiación
- Mejorar vista de detalle de póliza para mostrar información de entrega como sección principal cuando estado=VIGENTE
- Agregar endpoint PATCH para actualizar campos de entrega (administración manual de estado de cartera y cuota actual)
- Guardar valores de cuotas calculadas para cada plan de financiación (3, 5, 8, 11 cuotas) al momento de generar propuesta, para mantener consistencia con lo ofrecido al cliente

## Capabilities

### New Capabilities
- `poliza-entrega`: Gestión completa de entrega de pólizas incluyendo captura de datos, validaciones de transición de estado, auto-llenado de información de aseguradora, y registro de plan de financiación seleccionado
- `poliza-financiacion`: Cálculo, almacenamiento y gestión de planes de financiación con cuotas, incluyendo valores pre-calculados por plan, tracking de cuota actual, fechas de pago, y estado de cartera

### Modified Capabilities
<!-- No hay modificaciones a capabilities existentes, solo nuevas funcionalidades -->

## Impact

**Backend:**
- Modelo `BasePolizaMixin`: +11 campos nuevos (nombre_aseguradora, numeral_asistencia, valor_total_prima, medio_pago, estado_cartera, financiacion_num_cuotas, financiacion_cuota_actual, financiacion_valor_cuota, financiacion_fecha_primera_cuota, valor_cuota_3, valor_cuota_5, valor_cuota_8, valor_cuota_11)
- Migración SQL para agregar columnas en todas las tablas de pólizas (polizas_copropiedad, polizas_hogar, polizas_vehiculo, polizas_otro_bien)
- Nuevos blueprints/endpoints en módulos de pólizas para entrega y actualización
- Servicios de validación para reglas de negocio de entrega
- Repositorio de aseguradoras para consultas de auto-llenado

**Frontend:**
- Nueva ruta `/propuestas/{rubro}/{id}/entregar` con formulario completo
- Modificación de páginas de generación de propuesta para guardar valores de cuotas calculadas
- Refactorización de vista de detalle `/polizas/{rubro}/{id}` para mostrar información de entrega
- Componente de administración de financiación editable
- Validaciones de formulario y manejo de estados condicionales (contado vs financiera)

**Database:**
- Schema change en 4 tablas de pólizas
- Sin impacto en datos existentes (campos nullable, valores default)
