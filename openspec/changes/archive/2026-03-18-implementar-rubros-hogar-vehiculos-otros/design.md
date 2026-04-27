## Context

El sistema actual tiene implementado completamente el flujo de generación de propuestas para Copropiedades:
- Modelo `Aseguradora` con campos `cop_*` para configuración de coberturas/deducibles
- Modelo `Copropiedad` con todos los campos necesarios
- Diccionario TypeScript `diccionario_campos_copropiedad.ts` mapeando [N] → campo
- Página de generación `/propuestas/copropiedad/[id]/generar/` con función `buildVariablesJson()`
- Backend `PropuestaService` con soporte para plantilla `propuesta_cop.xlsx`
- Documentación `DICCIONARIO_VARIABLES_COPROPIEDAD.md`

Los rubros de Hogar, Vehículos y Otros ya tienen:
- Modelos de bienes básicos (pero incompletos)
- Modelos de pólizas completos
- Plantillas Excel `.xlsx` existentes

**Falta:**
- Campos de configuración en modelo Aseguradora para los 3 rubros
- Diccionarios TypeScript para mapeo de variables
- Páginas de generación en frontend
- Documentación de variables

**Restricciones:**
- Timeline corto - cliente acepta riesgos de tabla ancha
- Seguir patrón existente de Copropiedades al pie de la letra
- No hay consumo de APIs externas (ej: código Fasecolda es texto libre)
- Valores separados por comas en Aseguradora (formato: "porcentaje,tipo,mínimo")

## Goals / Non-Goals

**Goals:**
- Replicar funcionalidad de propuestas de Copropiedades para Hogar, Vehículos y Otros
- Mantener consistencia arquitectónica con implementación existente
- Proporcionar documentación completa para el cliente sobre mapeo de variables
- Permitir configuración flexible de coberturas por aseguradora y rubro

**Non-Goals:**
- Refactorizar modelo Aseguradora a estructura normalizada (JSON/relacional) - timeline
- Implementar validaciones de negocio complejas - se acepta libertad en datos
- Integración con APIs externas (Fasecolda, etc.)
- Implementar gestión documental de pólizas generadas (fase futura)

## Decisions

### Decision 1: Extender modelo Aseguradora con columnas individuales

**Opción elegida:** Agregar ~240 columnas con prefijos `hog_*`, `veh_*`, `otr_*` a la tabla `aseguradoras`

**Alternativas consideradas:**
- **JSONB por rubro:** Hubiera sido más flexible pero complejiza queries y validaciones
- **Tabla relacional aseguradora_configuracion_rubro:** Más normalizada pero mayor complejidad de joins

**Rationale:** 
- Mantiene consistencia con patrón `cop_*` existente
- Frontend ya maneja este patrón (split de strings con comas)
- Cliente acepta trade-off de tabla ancha vs entrega rápida
- SQLAlchemy ORM maneja bien columnas numerosas

### Decision 2: Diccionarios TypeScript siguiendo patrón de Copropiedades

**Opción elegida:** Crear 3 archivos separados: `diccionario_campos_<rubro>.ts`, cada uno con:
```typescript
export const DICCIONARIO_CAMPOS_<RUBRO>: Record<string, string> = { ... }
export const DICCIONARIO_INVERSO_<RUBRO>: Record<string, string> = ...
export function getAseguradoraOffset(asegNum: number): number { ... }
```

**Rationale:**
- Separación por rubro facilita mantenimiento
- Consistencia con patrón existente reduce curva de aprendizaje
- Export de helpers reduce duplicación de código

### Decision 3: Rangos de variables por rubro

**Hogar:**
- [1]-[2]: Encabezado
- [3]-[14]: Cliente + Generales (12 campos)
- [15]-[19]: Avalúos (5 campos)
- [20]-[25]: Asegurados (6 campos)
- [26]-[30]: Infraseguro (5 campos)
- [31]-[100]: Aseguradora 1 (70 campos)
- [101]-[170]: Aseguradora 2
- [171]+: Aseguradoras 3-5, financiación

**Vehículos:**
- Similar estructura pero cada aseguradora ocupa ~100 campos (incluye 4 sublímites RC)

**Otros:**
- Similar a Hogar, soporta hasta 3 aseguradoras

**Rationale:** Mantiene lógica de offsets predecibles para simplificar construcción del JSON

### Decision 4: Construcción de JSON en frontend mediante función buildVariablesJson()

**Opción elegida:** Replicar patrón de Copropiedades - función en cada página que:
1. Lee datos de póliza, bien, cliente, aseguradoras
2. Aplica helpers de formato (formatMoney, calcularInfraseguro, etc.)
3. Construye objeto `{"[N]": "valor"}` indexado por número
4. Envía al endpoint `/api/propuestas/generate`

**Alternativas consideradas:**
- **Backend construye JSON:** Requeriría duplicar mucha lógica de formato y cálculo
- **Service compartido TypeScript:** Buen refactor futuro pero aumenta complejidad ahora

**Rationale:**
- Mantiene lógica de presentación en frontend donde se muestran los datos
- Usuario puede ver/editar valores antes de generar
- Backend solo se encarga de reemplazo en XML del Excel

### Decision 5: Campos string con separadores de comas en Aseguradora

**Formato:** Todos los deducibles/sublímites se almacenan como `VARCHAR(255)` con formato:
```
"porcentaje,tipo,mínimo"
Ejemplo: "10,porcentaje,50000"
```

**Separación en frontend:**
```typescript
const sep = (valor: string) => {
  const p = valor.split(',');
  return { porcentaje: p[0], tipo: p[1], minimo: p[2] };
};
```

**Rationale:**
- Patrón ya establecido en Copropiedades
- Frontend ya tiene lógica de split/join
- Permite edición sin re-guardar en BD (user input se usa para propuesta)

### Decision 6: Migración SQL incremental

**Opción elegida:** Script SQL con ALTER TABLE conservador:
```sql
-- Hogar (70 campos)
ALTER TABLE aseguradoras 
ADD COLUMN hog_deducible_terremoto VARCHAR(255),
ADD COLUMN hog_deducible_amit VARCHAR(255),
...;

-- Vehículos (100 campos)
ALTER TABLE aseguradoras 
ADD COLUMN veh_deducible_perdida_parcial VARCHAR(255),
...;

-- Otros (70 campos)
ALTER TABLE aseguradoras 
ADD COLUMN otr_deducible_terremoto VARCHAR(255),
...;

-- Bienes
ALTER TABLE hogares ADD COLUMN estado VARCHAR(100), ADD COLUMN comentarios_detalles TEXT;
ALTER TABLE otros_bienes ADD COLUMN estado VARCHAR(100), ADD COLUMN comentarios TEXT;
```

**Rationale:**
- No requiere ORM migration framework (Alembic)
- Ejecutable manualmente o vía script
- Rollback sencillo si necesario (DROP COLUMN)

### Decision 7: Documentación Markdown para cliente

**Opción elegida:** 3 archivos `.md` en raíz del proyecto con tablas detalladas:

```markdown
| Variable | Campo | Descripción |
|----------|-------|-------------|
| [1] | fecha_expedicion | Fecha de expedición (formato: "18 de marzo 2026") |
| [2] | año_vigencia | Año de vigencia (formato: "2026-2027") |
...
```

**Rationale:**
- Markdown renderiza bien en GitHub/editores
- Cliente puede buscar (`Ctrl+F`) variables o campos fácilmente
- Sirve como referencia para futuras traducciones/adaptaciones

## Risks / Trade-offs

### Risk: Tabla aseguradoras muy ancha (~280 columnas totales)

**Mitigación:**
- PostgreSQL maneja bien columnas numerosas
- Queries solo traen columnas necesarias (SELECT específico, no *)
- Cliente acepta este trade-off por velocidad de entrega

### Risk: Duplicación de código entre páginas de generación

**Mitigación:**
- Considerado aceptable por timeline
- Refactor futuro a componentes compartidos posible
- Cada rubro tiene suficientes particularidades que justifican código separado

### Risk: Validaciones en frontend solamente

**Mitigación:**
- Backend `PropuestaService` valida presencia de template y formato básico JSON
- Validaciones de negocio (avalúo vs asegurado) existen en modelos de póliza
- Errores de generación se capturan y muestran al usuario

### Risk: Formato string con comas propenso a errores

**Mitigación:**
- Input en frontend usa 3 campos separados (porcentaje, tipo, mínimo)
- Join se hace solo al enviar a backend
- Split se hace al cargar desde backend
- Usuario nunca manipula string raw

### Trade-off: Copiar/pegar de lógica de Copropiedades vs abstracción

**Decisión:** Aceptar duplicación inicial

**Rationale:**
- Abstracción prematura aumentaría complejidad
- Cada rubro tiene matices suficientes (ej: sublímites RC en vehículos)
- Refactor futuro más informado después de ver patrones emergentes

## Migration Plan

**Fase 1: Backend (sin downtime)**
1. Ejecutar script SQL de migración en horario de bajo tráfico
2. Actualizar modelos Python (`aseguradora.py`, `hogar.py`, `otro_bien.py`)
3. Actualizar `to_dict()` para incluir nuevos campos
4. Actualizar `PropuestaService.TEMPLATES` con 3 nuevos rubros
5. Deploy backend
6. Validar endpoint `/api/propuestas/templates` retorna 4 rubros

**Fase 2: Frontend**
1. Crear diccionarios TypeScript
2. Crear páginas de generación para cada rubro
3. Deploy frontend
4. Validar generación de propuestas con datos de prueba

**Fase 3: Documentación**
1. Generar archivos Markdown con tablas de variables
2. Commit a repositorio
3. Compartir con cliente para revisión

**Rollback:** 
- Backend: revertir commit, ejecutar `DROP COLUMN` si necesario
- Frontend: revertir deploy (páginas nuevas no afectan funcionalidad existente)

## Open Questions

1. **¿Necesitan configuración inicial de aseguradoras con datos de los nuevos rubros?**
   - Respuesta del usuario: No especificado aún - puede hacerse post-deploy vía interfaz admin

2. **¿Tasa de financiación es configurable o fija por rubro?**
   - Respuesta del usuario: Es igual para todos (ingreso manual como en Copropiedades)

3. **¿Validación de código Fasecolda contra base de datos externa?**
   - Respuesta del usuario: No - es texto libre sin validación
