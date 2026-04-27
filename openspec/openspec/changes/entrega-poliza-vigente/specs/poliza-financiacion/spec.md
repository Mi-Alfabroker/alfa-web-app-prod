## ADDED Requirements

### Requirement: Persistencia de valores de cuotas calculadas
El sistema SHALL guardar los valores de cuotas calculadas para planes de 3, 5, 8, y 11 cuotas en campos separados (valor_cuota_3, valor_cuota_5, valor_cuota_8, valor_cuota_11) al momento de generar o actualizar una propuesta.

#### Scenario: Guardar valores calculados al generar propuesta
- **WHEN** un usuario genera propuesta con prima = 1000000 y tasa_interes = 2.3%
- **THEN** el sistema calcula y guarda valor_cuota_3 = 333333, valor_cuota_5 = 215789, valor_cuota_8 = 139456, valor_cuota_11 = 102345

#### Scenario: Valores NULL si propuesta no generada
- **WHEN** una póliza es creada pero no se ha generado propuesta PDF
- **THEN** los campos valor_cuota_3, valor_cuota_5, valor_cuota_8, valor_cuota_11 permanecen como NULL

#### Scenario: Re-cálculo al cambiar valor de prima en propuesta
- **WHEN** un usuario modifica valor_prima_aseg_2 después de generar propuesta
- **THEN** el sistema recalcula y actualiza los 4 campos de valor_cuota cuando se vuelve a generar propuesta

### Requirement: Selección de plan de financiación en entrega
El sistema SHALL permitir al usuario seleccionar un plan de financiación (contado o número de cuotas) al entregar la póliza, copiando el valor de cuota correspondiente desde los valores pre-calculados.

#### Scenario: Entrega con pago de contado
- **WHEN** un usuario entrega póliza con medio_pago = "contado"
- **THEN** el sistema guarda financiacion_num_cuotas = NULL, financiacion_valor_cuota = NULL, estado_cartera puede ser NULL o "recaudado"

#### Scenario: Entrega con financiación de 5 cuotas
- **WHEN** un usuario entrega póliza con medio_pago = "financiera" y financiacion_num_cuotas = 5
- **THEN** el sistema copia valor_cuota_5 a financiacion_valor_cuota y requiere financiacion_fecha_primera_cuota

#### Scenario: Rechazo de entrega financiera sin número de cuotas
- **WHEN** un usuario envía medio_pago = "financiera" pero financiacion_num_cuotas es NULL
- **THEN** el sistema retorna error 400 con mensaje "Debe especificar número de cuotas para financiera"

#### Scenario: Rechazo de número de cuotas inválido
- **WHEN** un usuario envía financiacion_num_cuotas = 6
- **THEN** el sistema retorna error 400 con mensaje "Número de cuotas debe ser 3, 5, 8 o 11"

#### Scenario: Rechazo de financiera sin fecha de primera cuota
- **WHEN** un usuario envía medio_pago = "financiera" con financiacion_num_cuotas = 5 pero financiacion_fecha_primera_cuota es NULL
- **THEN** el sistema retorna error 400 con mensaje "Debe especificar fecha de primera cuota"

### Requirement: Cálculo de cuotas con amortización constante
El sistema SHALL calcular valores de cuotas usando fórmula de amortización con tasa efectiva mensual: `cuota = prima * ((tasa * (1 + tasa)^n) / ((1 + tasa)^n - 1))` donde n es el número de cuotas.

#### Scenario: Cálculo con tasa de interés positiva
- **WHEN** prima = 1000000, tasa = 2.3% mensual, num_cuotas = 5
- **THEN** el valor de cuota calculado es 215789 (redondeado a entero)

#### Scenario: Cálculo sin interés para 3 cuotas
- **WHEN** prima = 1000000, tasa = 0%, num_cuotas = 3
- **THEN** el valor de cuota calculado es 333333 (prima / num_cuotas)

#### Scenario: Almacenamiento como BigInteger
- **WHEN** un valor de cuota es calculado con decimales
- **THEN** el sistema redondea a entero más cercano y guarda como BigInteger (sin centavos)

### Requirement: Tracking manual de cuota actual
El sistema SHALL permitir actualizar manualmente el campo financiacion_cuota_actual para indicar en qué cuota va el cliente, sin automatización de incremento.

#### Scenario: Inicialización de cuota actual al entregar
- **WHEN** un usuario entrega póliza con financiacion_num_cuotas = 8
- **THEN** el sistema inicializa financiacion_cuota_actual = 1

#### Scenario: Actualización manual de cuota actual
- **WHEN** un usuario actualiza financiacion_cuota_actual de 2 a 3
- **THEN** el sistema guarda el nuevo valor sin validar pagos ni generar eventos

#### Scenario: Validación de cuota actual no excede total
- **WHEN** un usuario intenta actualizar financiacion_cuota_actual = 9 pero financiacion_num_cuotas = 8
- **THEN** el sistema retorna error 400 con mensaje "Cuota actual no puede exceder número total de cuotas"

### Requirement: Gestión de estado de cartera
El sistema SHALL permitir marcar estado de cartera con valores: recaudado, pendiente, cancelado, en_solicitud.

#### Scenario: Estado inicial de cartera al entregar con financiera
- **WHEN** un usuario entrega póliza con medio_pago = "financiera"
- **THEN** el sistema inicializa estado_cartera = "pendiente" por defecto

#### Scenario: Actualización de estado a recaudado
- **WHEN** un usuario cambia estado_cartera de "pendiente" a "recaudado"
- **THEN** el sistema guarda el cambio sin realizar acciones automáticas (gestión manual)

#### Scenario: Validación de valores permitidos
- **WHEN** un usuario intenta asignar estado_cartera = "vencido" (no permitido)
- **THEN** el sistema retorna error 400 con mensaje listando valores permitidos

### Requirement: Modelo simplificado de fechas de pago
El sistema SHALL guardar únicamente la fecha de primera cuota y periodicidad (default: mensual), calculando fechas subsecuentes cuando se requieran en frontend.

#### Scenario: Cálculo de fecha de próxima cuota
- **WHEN** financiacion_fecha_primera_cuota = "2026-04-01", financiacion_cuota_actual = 3, periodicidad = "mensual"
- **THEN** el frontend calcula fecha próxima cuota = "2026-06-01" (primera_cuota + 2 meses)

#### Scenario: Validación de periodicidad
- **WHEN** un usuario intenta asignar financiacion_periodicidad = "anual" (no implementado en v1)
- **THEN** el sistema retorna error 400 indicando valores permitidos: "mensual"

### Requirement: Valores de cuotas consistentes con propuesta
El sistema SHALL garantizar que el valor de cuota usado en la entrega sea exactamente el mismo valor calculado y mostrado en el PDF de propuesta, evitando recálculos que podrían introducir inconsistencias.

#### Scenario: Detección de desincronización
- **WHEN** valor_prima_aseg_2 cambió después de guardar valor_cuota_5, y usuario intenta entregar con aseguradora_seleccionada = 2 y financiacion_num_cuotas = 5
- **THEN** el sistema emite advertencia pero permite continuar con el valor de cuota ya guardado (no recalcula)

#### Scenario: Imposibilidad de entregar si valores de cuota no existen
- **WHEN** un usuario intenta entregar con medio_pago = "financiera" pero los campos valor_cuota_* son NULL (propuesta no generada)
- **THEN** el sistema retorna error 400 con mensaje "Debe generar propuesta antes de entregar con financiación"

### Requirement: Visualización de detalles de financiación
El sistema SHALL proveer en la respuesta de detalle de póliza todos los campos necesarios para que el frontend muestre plan de financiación completo: número de cuotas, cuota actual, valor de cuota, fecha próxima, y estado de cartera.

#### Scenario: Respuesta de detalle incluye campos de financiación
- **WHEN** un usuario consulta GET /api/polizas/vehiculo/456
- **THEN** el sistema retorna JSON incluyendo financiacion_num_cuotas, financiacion_cuota_actual, financiacion_valor_cuota, financiacion_fecha_primera_cuota, financiacion_periodicidad, estado_cartera

#### Scenario: Campos de financiación NULL para pago de contado
- **WHEN** una póliza tiene medio_pago = "contado"
- **THEN** los campos financiacion_* (excepto periodicidad default) son NULL en la respuesta
