## ADDED Requirements

### Requirement: Entregar póliza con validación de transición de estado
El sistema SHALL permitir la transición de una póliza de estado PROSPECTO a VIGENTE mediante un proceso de entrega que valide campos obligatorios y datos de aseguradora seleccionada.

#### Scenario: Entrega exitosa con todos los campos requeridos
- **WHEN** un usuario envía solicitud de entrega con aseguradora_seleccionada, numero_poliza_aseguradora, inicio_vigencia, fin_vigencia, y medio_pago
- **THEN** el sistema actualiza el estado a VIGENTE, auto-llena nombre_aseguradora y numeral_asistencia desde la tabla aseguradoras, y retorna código 200 con datos completos

#### Scenario: Rechazo de entrega sin aseguradora seleccionada
- **WHEN** un usuario intenta entregar póliza sin especificar aseguradora_seleccionada
- **THEN** el sistema retorna error 400 con mensaje "Debe seleccionar una aseguradora"

#### Scenario: Rechazo de entrega sin número de póliza
- **WHEN** un usuario envía entrega con aseguradora_seleccionada pero sin numero_poliza_aseguradora
- **THEN** el sistema retorna error 400 con mensaje "Debe ingresar el número de póliza"

#### Scenario: Rechazo de entrega sin fechas de vigencia
- **WHEN** un usuario envía entrega sin inicio_vigencia o fin_vigencia
- **THEN** el sistema retorna error 400 indicando el campo faltante

#### Scenario: Validación de aseguradora seleccionada existe en propuesta
- **WHEN** un usuario selecciona aseguradora_seleccionada = 3 pero id_aseguradora_3 es NULL en la póliza
- **THEN** el sistema retorna error 400 con mensaje "La opción 3 no tiene aseguradora asignada"

#### Scenario: Rechazo de entrega desde estado no permitido
- **WHEN** un usuario intenta entregar una póliza con estado CANCELADA
- **THEN** el sistema retorna error 400 con mensaje "Una póliza cancelada no puede cambiar de estado"

### Requirement: Auto-llenado de datos de aseguradora
El sistema SHALL obtener automáticamente el nombre y numeral de asistencia de la aseguradora seleccionada desde la tabla aseguradoras y guardarlos en la póliza.

#### Scenario: Obtención de datos de aseguradora al seleccionar opción
- **WHEN** un usuario consulta GET /api/aseguradoras/{id}/datos-entrega
- **THEN** el sistema retorna JSON con campos nombre, numeral_asistencia, y otros datos relevantes con código 200

#### Scenario: Datos desnormalizados no cambian si aseguradora actualiza información
- **WHEN** una póliza tiene nombre_aseguradora = "SURA Seguros" y posteriormente la aseguradora cambia su nombre en la tabla aseguradoras
- **THEN** el nombre_aseguradora en la póliza permanece como "SURA Seguros" (snapshot del momento de entrega)

### Requirement: Valor total prima modificable
El sistema SHALL pre-llenar el campo valor_total_prima con el valor correspondiente a la aseguradora seleccionada (valor_prima_aseg_X) pero permitir que el usuario lo modifique antes de guardar.

#### Scenario: Pre-llenado de valor total prima
- **WHEN** un usuario solicita datos de entrega para una póliza donde aseguradora_seleccionada = 2 y valor_prima_aseg_2 = 1500000
- **THEN** el sistema retorna valor_total_prima = 1500000 como valor sugerido

#### Scenario: Modificación de valor total prima
- **WHEN** un usuario envía entrega con valor_total_prima = 1450000 aunque valor_prima_aseg_2 = 1500000
- **THEN** el sistema acepta el valor modificado y guarda valor_total_prima = 1450000

### Requirement: Actualización de datos de entrega post-vigencia
El sistema SHALL permitir la actualización de todos los campos de entrega (excepto consecutivo y cliente) en pólizas con estado VIGENTE sin re-validar transición de estado.

#### Scenario: Edición de datos de financiación en póliza vigente
- **WHEN** un usuario envía PATCH /api/polizas/{rubro}/{id}/actualizar-entrega con financiacion_cuota_actual = 3
- **THEN** el sistema actualiza el campo sin validar campos obligatorios de entrega y retorna código 200

#### Scenario: Actualización de estado de cartera manualmente
- **WHEN** un usuario cambia estado_cartera de "pendiente" a "recaudado" en póliza vigente
- **THEN** el sistema guarda el cambio sin realizar acciones automáticas (no envía notificaciones ni genera eventos)

### Requirement: Validación de rango de aseguradora seleccionada
El sistema SHALL validar que aseguradora_seleccionada esté en el rango 1-5.

#### Scenario: Rechazo de valor fuera de rango
- **WHEN** un usuario envía entrega con aseguradora_seleccionada = 6
- **THEN** el sistema retorna error 400 con mensaje "La aseguradora seleccionada debe estar entre 1 y 5"

#### Scenario: Rechazo de valor cero o negativo
- **WHEN** un usuario envía entrega con aseguradora_seleccionada = 0
- **THEN** el sistema retorna error 400 con mensaje "La aseguradora seleccionada debe estar entre 1 y 5"

### Requirement: Vista de detalle prioriza información de entrega para pólizas vigentes
El sistema SHALL mostrar los datos de entrega (aseguradora, vigencia, financiación, estado de cartera) como sección principal en la vista de detalle cuando el estado de la póliza es VIGENTE.

#### Scenario: Sección de entrega destacada en póliza vigente
- **WHEN** un usuario accede a GET /api/polizas/{rubro}/{id} donde estado = "VIGENTE"
- **THEN** el sistema retorna JSON incluyendo campos de entrega completos en objeto raíz (no anidado)

#### Scenario: Sección de entrega oculta en póliza prospecto
- **WHEN** un usuario accede a detalle de póliza con estado = "PROSPECTO"
- **THEN** el frontend no muestra sección de información de entrega (campos son NULL)

### Requirement: Endpoint dedicado para entrega
El sistema SHALL proveer endpoint POST /api/polizas/{rubro}/{id}/entregar separado de endpoints de actualización general.

#### Scenario: Entrega mediante endpoint dedicado
- **WHEN** un usuario envía POST /api/polizas/hogar/123/entregar con datos válidos
- **THEN** el sistema ejecuta validaciones de entrega, transiciona estado, y retorna póliza actualizada con código 200

#### Scenario: Logging de evento de entrega
- **WHEN** una póliza es entregada exitosamente
- **THEN** el sistema registra evento de auditoría con timestamp, usuario, y detalles de entrega
