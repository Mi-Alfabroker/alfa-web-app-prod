## ADDED Requirements

### Requirement: Generar propuesta de Vehículos desde póliza

El sistema SHALL permitir generar una propuesta de seguro de Vehículos en formato Excel desde una póliza existente, incluyendo datos del vehículo, conductor, aseguradoras configuradas y coberturas de responsabilidad civil.

#### Scenario: Generación exitosa con 2 aseguradoras

- **WHEN** usuario accede a generar propuesta para una póliza de vehículo con 2 aseguradoras configuradas
- **THEN** sistema muestra formulario prellenado con datos del vehículo, cliente y coberturas
- **THEN** usuario puede editar campos manuales (asesor, comentarios, tasa de interés)
- **THEN** al hacer clic en "Generar Propuesta", sistema construye JSON con variables `[1]` a `[N]` y descarga archivo Excel

#### Scenario: Inclusión de datos del conductor

- **WHEN** se genera propuesta de vehículo
- **THEN** JSON incluye año de nacimiento del conductor
- **THEN** JSON incluye código Fasecolda del vehículo

### Requirement: Construcción de diccionario de variables para Vehículos

El sistema SHALL construir un diccionario de reemplazo mapeando códigos `[N]` a valores reales del vehículo, conductor, póliza y aseguradoras, siguiendo el formato definido en `diccionario_campos_vehiculos.ts`.

#### Scenario: Mapeo de datos del vehículo

- **WHEN** se construye el diccionario de variables
- **THEN** `[3]` a `[14]` contienen datos del cliente, vehículo, placa, marca, modelo, año, código Fasecolda
- **THEN** valores de vehículo y accesorios se formatean como moneda

#### Scenario: Mapeo de coberturas por aseguradora con RC

- **WHEN** se procesan coberturas de aseguradoras
- **THEN** cada aseguradora ocupa ~100 campos consecutivos
- **THEN** se incluyen deducibles de pérdida parcial, pérdida total, terremoto, hurto
- **THEN** se incluyen 4 sublímites de RC: bienes terceros, amparo patrimonial, muerte/lesión una persona, dos o más personas
- **THEN** hasta 7 coberturas adicionales (checks) se mapean a variables booleanas

### Requirement: Cálculo de sublímites de RC

El sistema SHALL mapear correctamente los sublímites de Responsabilidad Civil para cada aseguradora, incluyendo daños a bienes de terceros, amparo patrimonial y lesiones/muerte.

#### Scenario: Mapeo de 4 sublímites RC

- **WHEN** aseguradora tiene configurados sublímites de RC
- **THEN** variable de RC Daños Bienes Terceros se incluye en JSON
- **THEN** variable de RC Amparo Patrimonial se incluye en JSON
- **THEN** variables de RC Muerte/Lesión (una persona y dos o más) se incluyen en JSON

### Requirement: Validación de código Fasecolda

El sistema SHALL incluir el código Fasecolda del vehículo en la propuesta si está disponible.

#### Scenario: Vehículo con código Fasecolda

- **WHEN** vehículo tiene código Fasecolda registrado
- **THEN** código se incluye en variable correspondiente del JSON

#### Scenario: Vehículo sin código Fasecolda

- **WHEN** vehículo no tiene código Fasecolda
- **THEN** variable queda vacía sin generar error

### Requirement: Descarga de archivo Excel generado

El sistema SHALL enviar el archivo Excel generado al navegador con nombre descriptivo y guardarlo en el servidor.

#### Scenario: Descarga exitosa

- **WHEN** propuesta se genera exitosamente
- **THEN** archivo se descarga con nombre "propuesta_vehiculos_YYYYMMDD_HHMMSS.xlsx"
- **THEN** sistema muestra modal de éxito con el nombre del archivo
- **THEN** archivo se guarda en servidor en ruta `/opt/gestion_documental_ab/propuestas/`
