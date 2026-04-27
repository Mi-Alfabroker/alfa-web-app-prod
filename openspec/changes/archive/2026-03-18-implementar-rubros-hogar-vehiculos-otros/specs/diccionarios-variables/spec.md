## ADDED Requirements

### Requirement: Diccionario de códigos para Hogar

El sistema SHALL proporcionar un diccionario TypeScript que mapea códigos compactos `[N]` a nombres de campos descriptivos para el rubro de Hogar, siguiendo la convención del diccionario de Copropiedades.

#### Scenario: Estructura de diccionario de Hogar

- **WHEN** se define el diccionario de Hogar
- **THEN** incluye exportación `DICCIONARIO_CAMPOS_HOGAR` como Record<string, string>
- **THEN** incluye exportación `DICCIONARIO_INVERSO_HOGAR` para búsquedas inversas
- **THEN** incluye función helper `getAseguradoraOffset()` para calcular offset de cada aseguradora

#### Scenario: Rangos de variables para Hogar

- **WHEN** se asignan rangos de variables
- **THEN** `[1]`-`[2]` son para encabezado (fecha, vigencia)
- **THEN** `[3]`-`[14]` son para cliente y generales del hogar (12 campos)
- **THEN** `[15]`-`[19]` son para valores de avalúo (5 campos)
- **THEN** `[20]`-`[25]` son para valores asegurados (6 campos)
- **THEN** `[26]`-`[30]` son para infraseguro (5 campos)
- **THEN** cada aseguradora ocupa 70 campos consecutivos

### Requirement: Diccionario de códigos para Vehículos

El sistema SHALL proporcionar un diccionario TypeScript para el rubro de Vehículos con estructura similar pero adaptada a las necesidades del rubro.

#### Scenario: Estructura de diccionario de Vehículos

- **WHEN** se define el diccionario de Vehículos
- **THEN** incluye exportación `DICCIONARIO_CAMPOS_VEHICULOS`
- **THEN** incluye exportación `DICCIONARIO_INVERSO_VEHICULOS`
- **THEN** incluye función helper `getAseguradoraOffset()`

#### Scenario: Rangos de variables para Vehículos

- **WHEN** se asignan rangos de variables
- **THEN** `[1]`-`[2]` son para encabezado
- **THEN** `[3]`-`[14]` son para cliente y datos del vehículo (incluye placa, marca, código Fasecolda, año conductor)
- **THEN** cada aseguradora ocupa ~100 campos consecutivos (más que otros rubros por sublímites RC)

### Requirement: Diccionario de códigos para Otros

El sistema SHALL proporcionar un diccionario TypeScript para el rubro de Otros Seguros.

#### Scenario: Estructura de diccionario de Otros

- **WHEN** se define el diccionario de Otros
- **THEN** incluye exportación `DICCIONARIO_CAMPOS_OTROS`
- **THEN** incluye exportación `DICCIONARIO_INVERSO_OTROS`
- **THEN** estructura es similar a Hogar pero con 6 campos generales mínimos

### Requirement: Documentación Markdown de variables

El sistema SHALL proporcionar archivos Markdown documentando el mapeo completo de variables para cada rubro, siguiendo el formato del diccionario de Copropiedades.

#### Scenario: Contenido de documentación

- **WHEN** se crea documentación de variables
- **THEN** archivo include tabla con columnas: Variable, Campo, Descripción
- **THEN** variables se agrupan por secciones semánticas
- **THEN** se documenta el offset de cada aseguradora
- **THEN** se incluye ejemplo de uso del formato separado por comas

#### Scenario: Archivos requeridos

- **WHEN** se genera documentación
- **THEN** existe archivo `DICCIONARIO_VARIABLES_HOGAR.md` en raíz del proyecto
- **THEN** existe archivo `DICCIONARIO_VARIABLES_VEHICULOS.md` en raíz del proyecto
- **THEN** existe archivo `DICCIONARIO_VARIABLES_OTROS.md` en raíz del proyecto

### Requirement: Convención de nombres de campos

El sistema SHALL seguir convención consistente para nombres de campos en los diccionarios.

#### Scenario: Formato de nombres

- **WHEN** se definen nombres de campos
- **THEN** se usa snake_case para nombres descriptivos
- **THEN** se incluye sufijo `_aseg_N` para campos específicos de aseguradora
- **THEN** campos de deducibles se nombran con patrón: `<cobertura>_<tipo>_porcentaje/tipo/minimo`
