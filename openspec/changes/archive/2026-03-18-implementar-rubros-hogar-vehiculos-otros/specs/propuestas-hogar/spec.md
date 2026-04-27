## ADDED Requirements

### Requirement: Generar propuesta de Hogar desde póliza

El sistema SHALL permitir generar una propuesta de seguro de Hogar en formato Excel desde una póliza existente, utilizando los datos del bien, cliente, aseguradoras configuradas y valores de cobertura.

#### Scenario: Generación exitosa con 2 aseguradoras

- **WHEN** usuario accede a generar propuesta para una póliza de hogar con 2 aseguradoras configuradas
- **THEN** sistema muestra formulario prellenado con datos del hogar, cliente y coberturas de las aseguradoras
- **THEN** usuario puede editar campos manuales (asesor, comentarios, tasa de interés)
- **THEN** al hacer clic en "Generar Propuesta", sistema construye JSON con variables `[1]` a `[N]` y descarga archivo Excel

#### Scenario: Validación de datos faltantes

- **WHEN** usuario intenta generar propuesta pero faltan datos obligatorios del hogar
- **THEN** sistema muestra mensaje de error indicando campos faltantes

### Requirement: Construcción de diccionario de variables para Hogar

El sistema SHALL construir un diccionario de reemplazo mapeando códigos `[N]` a valores reales del hogar, cliente, póliza y aseguradoras, siguiendo el formato definido en `diccionario_campos_hogar.ts`.

#### Scenario: Mapeo de datos del hogar

- **WHEN** se construye el diccionario de variables
- **THEN** `[1]` contiene la fecha de expedición en formato "18 de marzo 2026"
- **THEN** `[2]` contiene el año de vigencia en formato "2026-2027"
- **THEN** `[3]` a `[14]` contienen datos del cliente y generales del hogar

#### Scenario: Mapeo de valores asegurados

- **WHEN** se construyen variables de valores asegurados
- **THEN** valores monetarios se formatean con separadores de miles sin decimales
- **THEN** `[15]` a `[19]` contienen valores de avalúo del hogar
- **THEN** `[20]` a `[25]` contienen valores asegurados de la póliza

#### Scenario: Mapeo de coberturas por aseguradora

- **WHEN** se procesan coberturas de aseguradoras
- **THEN** cada aseguradora ocupa 70 campos consecutivos
- **THEN** deducibles separados por comas (porcentaje,tipo,mínimo) se mapean a 3 variables individuales
- **THEN** valores de prima se usan para calcular cuotas con interés

### Requirement: Edición de coberturas antes de generar

El sistema SHALL permitir al usuario revisar y editar las coberturas, deducibles y sublímites de cada aseguradora antes de generar la propuesta.

#### Scenario: Edición de deducible

- **WHEN** usuario modifica el porcentaje de deducible de terremoto para aseguradora 1
- **THEN** el nuevo valor se incluye en el JSON de variables al generar
- **THEN** el valor original de la base de datos no se modifica

### Requirement: Cálculo de cuotas con interés

El sistema SHALL calcular valores de cuotas con interés mensual usando la fórmula de amortización para 5, 8 y 11 cuotas.

#### Scenario: Cálculo con tasa 2.5%

- **WHEN** prima es $1,000,000 y tasa es 2.5% mensual
- **THEN** cuota a 5 meses se calcula correctamente con fórmula: Prima * ((tasa * (1+tasa)^n) / ((1+tasa)^n - 1))
- **THEN** resultado se redondea al entero más cercano
- **THEN** si tasa es 0, se divide la prima equitativamente

### Requirement: Descarga de archivo Excel generado

El sistema SHALL enviar el archivo Excel generado al navegador con nombre descriptivo y guardarlo en el servidor en la ruta configurada.

#### Scenario: Descarga exitosa

- **WHEN** propuesta se genera exitosamente
- **THEN** archivo se descarga con nombre "propuesta_hogar_YYYYMMDD_HHMMSS.xlsx"
- **THEN** sistema muestra modal de éxito con el nombre del archivo
- **THEN** archivo se guarda en servidor en ruta `/opt/gestion_documental_ab/propuestas/`
