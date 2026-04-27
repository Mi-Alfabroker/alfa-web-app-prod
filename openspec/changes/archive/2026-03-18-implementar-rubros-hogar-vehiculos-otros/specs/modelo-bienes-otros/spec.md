## ADDED Requirements

### Requirement: Campo estado en modelo OtroBien

El modelo OtroBien SHALL incluir campo `estado` para almacenar el estado actual del bien.

#### Scenario: Agregado de campo estado

- **WHEN** se extiende modelo OtroBien
- **THEN** se agrega columna `estado` tipo VARCHAR(100)
- **THEN** campo es nullable
- **THEN** campo se incluye en método `to_dict()`

### Requirement: Campo comentarios en modelo OtroBien

El modelo OtroBien SHALL incluir campo `comentarios` para almacenar información adicional del bien (complemento al campo `detalles_bien_asegurado` existente).

#### Scenario: Agregado de campo comentarios

- **WHEN** se extiende modelo OtroBien
- **THEN** se agrega columna `comentarios` tipo TEXT
- **THEN** campo es nullable
- **THEN** campo se incluye en método `to_dict()`

### Requirement: Migración de base de datos para OtroBien

El sistema SHALL proporcionar script de migración SQL para agregar los nuevos campos a la tabla `otros_bienes`.

#### Scenario: Script ALTER TABLE para otros_bienes

- **WHEN** se ejecuta migración
- **THEN** se agregan 2 columnas a tabla `otros_bienes`: `estado` y `comentarios`
- **THEN** columnas existentes no se modifican
- **THEN** datos existentes no se afectan
