## ADDED Requirements

### Requirement: Generar documento Excel de entrega para cada rubro
El sistema SHALL permitir generar documentos Excel de entrega para los 4 rubros: Hogar, Copropiedad, Vehículos y Otros. La generación SHALL usar las plantillas XLSX de entrega registradas en el backend y las mismas variables `[N]` que la propuesta del rubro correspondiente.

#### Scenario: Generar entrega de Hogar desde página de generación
- **WHEN** el usuario está en la página `/propuestas/hogar/{id}/generar` y hace clic en "Generar Entrega"
- **THEN** el sistema envía las variables y las imágenes al endpoint `POST /api/propuestas/generate` con `template_name: 'entrega_hogar'` y descarga el archivo Excel generado

#### Scenario: Generar entrega de Copropiedad desde página de generación
- **WHEN** el usuario está en la página `/propuestas/copropiedad/{id}/generar` y hace clic en "Generar Entrega"
- **THEN** el sistema envía las variables al endpoint con `template_name: 'entrega_copropiedades'` y descarga el archivo Excel generado

#### Scenario: Generar entrega de Vehículos desde página de generación
- **WHEN** el usuario está en la página `/propuestas/vehiculo/{id}/generar` y hace clic en "Generar Entrega"
- **THEN** el sistema envía las variables al endpoint con `template_name: 'entrega_vehiculos'` y descarga el archivo Excel generado

#### Scenario: Generar entrega de Otros desde página de generación
- **WHEN** el usuario está en la página `/propuestas/otro/{id}/generar` y hace clic en "Generar Entrega"
- **THEN** el sistema envía las variables al endpoint con `template_name: 'entrega_otros'` y descarga el archivo Excel generado

### Requirement: Botón Generar Propuesta visible en detalle de todos los rubros
El sistema SHALL mostrar un botón "Generar Propuesta" en la página de detalle de los 4 rubros cuando el estado de la póliza sea PROSPECTO. El botón SHALL navegar a la ruta `/propuestas/{rubro}/{id}/generar`.

#### Scenario: Botón Generar Propuesta visible en Hogar
- **WHEN** el usuario visualiza una póliza de Hogar con estado PROSPECTO
- **THEN** aparece el botón verde "Generar Propuesta" que navega a `/propuestas/hogar/{id}/generar`

#### Scenario: Botón Generar Propuesta visible en Vehículo
- **WHEN** el usuario visualiza una póliza de Vehículo con estado PROSPECTO
- **THEN** aparece el botón verde "Generar Propuesta" que navega a `/propuestas/vehiculo/{id}/generar`

#### Scenario: Botón Generar Propuesta visible en Otros
- **WHEN** el usuario visualiza una póliza de Otro Bien con estado PROSPECTO
- **THEN** aparece el botón verde "Generar Propuesta" que navega a `/propuestas/otro/{id}/generar`

### Requirement: Botón Generar Entrega visible en detalle cuando VIGENTE
El sistema SHALL mostrar un botón "Generar Entrega" en la página de detalle de los 4 rubros cuando el estado de la póliza sea VIGENTE. El botón SHALL navegar a la ruta `/propuestas/{rubro}/{id}/generar`.

#### Scenario: Botón Generar Entrega en póliza VIGENTE de Hogar
- **WHEN** el usuario visualiza una póliza de Hogar con estado VIGENTE
- **THEN** aparece el botón verde "Generar Entrega" que navega a `/propuestas/hogar/{id}/generar`

#### Scenario: Botón Generar Entrega no visible en póliza PROSPECTO
- **WHEN** el usuario visualiza una póliza con estado PROSPECTO
- **THEN** el botón "Generar Entrega" NO es visible

### Requirement: Templates de entrega registrados en backend
El backend SHALL tener registradas las 4 plantillas de entrega en el dict TEMPLATES del PropuestaService: `entrega_hogar`, `entrega_copropiedades`, `entrega_vehiculos`, `entrega_otros`.

#### Scenario: Solicitar generación con template de entrega
- **WHEN** el frontend envía `template_name: 'entrega_hogar'` al endpoint de generación
- **THEN** el backend localiza la plantilla `entrega_hogar.xlsx`, aplica las variables y devuelve el archivo Excel

#### Scenario: Template de entrega no existente
- **WHEN** el frontend envía un `template_name` no registrado
- **THEN** el backend retorna error 400 indicando que el template no existe
