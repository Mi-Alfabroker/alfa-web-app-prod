## ADDED Requirements

### Requirement: Campos de configuración para Hogar en Aseguradora

El modelo Aseguradora SHALL incluir campos con prefijo `hog_*` para almacenar configuraciones de deducibles, coberturas y sublímites específicos del rubro de Hogar.

#### Scenario: Campos de deducibles de Hogar

- **WHEN** se configura aseguradora para Hogar
- **THEN** modelo incluye campos para deducibles de terremoto, AMIT, y demás eventos (daños)
- **THEN** modelo incluye campos para deducibles de hurto: contenidos normales, especiales, equipo electrónico
- **THEN** cada deducible se almacena como string con formato "porcentaje,tipo,mínimo"

#### Scenario: Total de campos agregados para Hogar

- **WHEN** se extiende modelo Aseguradora
- **THEN** se agregan aproximadamente 70 campos con prefijo `hog_*`
- **THEN** campos incluyen deducibles, valores asegurados y coberturas adicionales

### Requirement: Campos de configuración para Vehículos en Aseguradora

El modelo Aseguradora SHALL incluir campos con prefijo `veh_*` para almacenar configuraciones específicas del rubro de Vehículos, incluyendo sublímites de Responsabilidad Civil.

#### Scenario: Campos de deducibles de Vehículos

- **WHEN** se configura aseguradora para Vehículos
- **THEN** modelo incluye campos para deducibles de pérdida parcial, pérdida total, terremoto
- **THEN** modelo incluye campos para deducibles de hurto: pérdida parcial y total
- **THEN** modelo incluye campo para deducible de RC

#### Scenario: Sublímites de RC para Vehículos

- **WHEN** se configuran sublímites de RC
- **THEN** modelo incluye campo para RC Daños a Bienes Terceros
- **THEN** modelo incluye campo para RC Amparo Patrimonial
- **THEN** modelo incluye campo para RC Muerte/Lesión a una persona
- **THEN** modelo incluye campo para RC Muerte/Lesión a dos o más personas

#### Scenario: Total de campos agregados para Vehículos

- **WHEN** se extiende modelo Aseguradora
- **THEN** se agregan aproximadamente 100 campos con prefijo `veh_*`
- **THEN** mayor cantidad de campos es debido a sublímites de RC y coberturas adicionales (hasta 7)

### Requirement: Campos de configuración para Otros en Aseguradora

El modelo Aseguradora SHALL incluir campos con prefijo `otr_*` para almacenar configuraciones del rubro de Otros Seguros.

#### Scenario: Estructura similar a Hogar

- **WHEN** se configura aseguradora para Otros
- **THEN** estructura de campos es similar a Hogar
- **THEN** se agregan aproximadamente 70 campos con prefijo `otr_*`

### Requirement: Actualización de método to_dict()

El modelo Aseguradora SHALL actualizar su método `to_dict()` para incluir los nuevos campos en la serialización JSON.

#### Scenario: Inclusión de nuevos campos en JSON

- **WHEN** se serializa instancia de Aseguradora a diccionario
- **THEN** JSON incluye todos los campos `hog_*`
- **THEN** JSON incluye todos los campos `veh_*`
- **THEN** JSON incluye todos los campos `otr_*`

### Requirement: Migración de base de datos

El sistema SHALL proporcionar script de migración SQL para agregar las nuevas columnas a la tabla `aseguradoras`.

#### Scenario: Script ALTER TABLE

- **WHEN** se ejecuta migración
- **THEN** se agregan ~240 columnas nuevas a tabla `aseguradoras` (70 + 100 + 70)
- **THEN** todas las columnas son VARCHAR(255) y nullable
- **THEN** columnas existentes no se modifican
