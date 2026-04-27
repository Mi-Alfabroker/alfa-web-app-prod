## ADDED Requirements

### Requirement: Campo estado en modelo Hogar

El modelo Hogar SHALL incluir campo `estado` para almacenar el estado actual del inmueble.

#### Scenario: Agregado de campo estado

- **WHEN** se extiende modelo Hogar
- **THEN** se agrega columna `estado` tipo VARCHAR(100)
- **THEN** campo es nullable
- **THEN** campo se incluye en método `to_dict()`

### Requirement: Campo comentarios_detalles en modelo Hogar

El modelo Hogar SHALL incluir campo `comentarios_detalles` para almacenar información adicional del inmueble.

#### Scenario: Agregado de campo comentarios_detalles

- **WHEN** se extiende modelo Hogar
- **THEN** se agrega columna `comentarios_detalles` tipo TEXT
- **THEN** campo es nullable
- **THEN** campo se incluye en método `to_dict()`

### Requirement: Migración de base de datos para Hogar

El sistema SHALL proporcionar script de migración SQL para agregar los nuevos campos a la tabla `hogares`.

#### Scenario: Script ALTER TABLE para hogares

- **WHEN** se ejecuta migración
- **THEN** se agregan 2 columnas a tabla `hogares`: `estado` y `comentarios_detalles`
- **THEN** columnas existentes no se modifican
- **THEN** datos existentes no se afectan
