## ADDED Requirements

### Requirement: Generar propuesta de Otros Seguros desde póliza

El sistema SHALL permitir generar una propuesta de Otros Seguros (seguros no categorizados en Hogar, Vehículos o Copropiedades) en formato Excel desde una póliza existente.

#### Scenario: Generación exitosa con 3 aseguradoras

- **WHEN** usuario accede a generar propuesta para una póliza de otro bien con 3 aseguradoras configuradas
- **THEN** sistema muestra formulario prellenado con datos del bien, tipo de seguro y coberturas
- **THEN** usuario puede editar campos manuales (asesor, comentarios, tasa de interés)
- **THEN** al hacer clic en "Generar Propuesta", sistema construye JSON con variables `[1]` a `[N]` y descarga archivo Excel

#### Scenario: Validación de tipo de seguro

- **WHEN** se genera propuesta de otro bien
- **THEN** JSON incluye el tipo de seguro aplicable
- **THEN** JSON incluye descripción del bien asegurado
- **THEN** JSON incluye detalles y comentarios del bien

### Requirement: Construcción de diccionario de variables para Otros

El sistema SHALL construir un diccionario de reemplazo mapeando códigos `[N]` a valores reales del otro bien, cliente, póliza y aseguradoras, siguiendo el formato definido en `diccionario_campos_otros.ts`.

#### Scenario: Mapeo de datos de otro bien

- **WHEN** se construye el diccionario de variables
- **THEN** `[3]` a `[8]` contienen datos del cliente, estado, tipo de seguro, bien asegurado, valor y detalles
- **THEN** estructura de coberturas es similar a Hogar (70 campos por aseguradora)

#### Scenario: Flexibilidad en tipo de seguro

- **WHEN** tipo de seguro es cualquier categoría personalizada
- **THEN** valor se incluye sin validación específica
- **THEN** bien asegurado puede ser texto descriptivo libre

### Requirement: Soporte para múltiples aseguradoras

El sistema SHALL soportar hasta 3 aseguradoras para propuestas de Otros Seguros.

#### Scenario: Mapeo de 3 aseguradoras

- **WHEN** póliza tiene 3 aseguradoras configuradas
- **THEN** JSON incluye bloques de variables para aseguradora 1, 2 y 3
- **THEN** cada aseguradora ocupa 70 campos consecutivos

### Requirement: Descarga de archivo Excel generado

El sistema SHALL enviar el archivo Excel generado al navegador con nombre descriptivo y guardarlo en el servidor.

#### Scenario: Descarga exitosa

- **WHEN** propuesta se genera exitosamente
- **THEN** archivo se descarga con nombre "propuesta_otros_YYYYMMDD_HHMMSS.xlsx"
- **THEN** sistema muestra modal de éxito con el nombre del archivo
- **THEN** archivo se guarda en servidor en ruta `/opt/gestion_documental_ab/propuestas/`
