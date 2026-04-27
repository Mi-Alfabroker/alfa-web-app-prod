# 🔍 Correcciones: Diccionarios vs Código Real

Revisión cruzada entre los archivos `.md` de diccionarios, los archivos TypeScript (`.ts`) en `frontend/src/lib/data/`, y las páginas `generar/+page.svelte` donde se construyen las variables.

---

## 🔴 CRÍTICO — Discrepancias de Offsets

### 1. Copropiedad: Nombres de campos +6 y +7 incorrectos en el .md

El diccionario `PROPUESTA_COPROPIEDAD.md` documenta los offsets de aseguradora como:

| Offset | Variable documentada (.md) |
|--------|---------------------------|
| +6 | `cobertura_diferenciadora_1` |
| +7 | `cobertura_diferenciadora_2` |

Pero el **código TS real** (`diccionario_campos_copropiedad.ts`) usa:

| Código TS | Variable real | Offset |
|-----------|--------------|--------|
| `[46]` | `no_demerito_uso_aseg_1` | +6 |
| `[47]` | `cobertura_accidentes_consejo_aseg_1` | +7 |

> **Acción:** Actualizar `PROPUESTA_COPROPIEDAD.md` con los nombres reales: `no_demerito_uso` (+6) y `cobertura_accidentes_consejo` (+7).

---

### 2. Otros Bienes: Avalúos `[14]-[17]` desalineados

El `.md` documenta:

| Código | Variable .md |
|--------|-------------|
| `[14]` | valor_contenidos_normales_avaluo |
| `[15]` | valor_contenidos_especiales_avaluo |
| `[16]` | valor_equipo_electronico_avaluo |
| `[17]` | valor_total_avaluo (calculado) |

El **código TS** y **Svelte** realmente mapean:

| Código | Variable real |
|--------|-------------|
| `[14]` | **valor_inmueble_avaluo** |
| `[15]` | valor_contenidos_normales_avaluo |
| `[16]` | valor_contenidos_especiales_avaluo |
| `[17]` | valor_equipo_electronico_avaluo |

> **Acción:** Corregir `PROPUESTA_OTROS.md`: `[14]` debe ser `valor_inmueble_avaluo`. El `.md` omite este campo y desplaza todo.

---

### 3. Otros Bienes: Valores Asegurados `[18]-[22]` desalineados

El `.md` dice:

| Código | Variable .md |
|--------|-------------|
| `[18]` | valor_asegurado_cn |
| `[19]` | valor_asegurado_ce |
| `[20]` | valor_asegurado_ee |
| `[21]` | valor_rc_asegurado |
| `[22]` | valor_total_asegurado (calculado) |

El **TS y Svelte** realmente mapean:

| Código | Variable real |
|--------|-------------|
| `[18]` | **valor_inmueble_asegurado** |
| `[19]` | valor_contenidos_normales_asegurado |
| `[20]` | valor_contenidos_especiales_asegurado |
| `[21]` | valor_equipo_electronico_asegurado |
| `[22]` | valor_rc_asegurado |

> **Acción:** Corregir `PROPUESTA_OTROS.md`: 5 valores asegurados reales (inmueble incluido), no 4 + 1 calculado.

---

### 4. Otros Bienes: Infraseguro `[23]-[26]` incorrecto

El `.md` tiene: `infraseg_cn`, `infraseg_ce`, `infraseg_ee`, `infraseg_total`

El **TS** tiene: `infraseg_inmueble`, `infraseg_contenidos_normales`, `infraseg_contenidos_especiales`, `infraseg_equipo_electronico`

> **Acción:** Corregir: `[23]`=`infraseg_inmueble`, `[24]`=`infraseg_contenidos_normales`, `[25]`=`infraseg_contenidos_especiales`, `[26]`=`infraseg_equipo_electronico` (sin `infraseg_total`).

---

### 5. Otros Bienes: `[7]` y `[8]` intercambiados — campo "detalles" perdido

El `.md` original asignaba `[7]` = `detalles` (del bien), pero el **TS y Svelte** mapean:

```
[7] → cliente.ciudad_residencia (ciudad)
[8] → cliente.direccion_residencia (dirección)
```

El campo `detalles` del bien no está mapeado a ninguna variable `[N]` en el código.

> **Acción:** Verificar si la plantilla XLSX usa el campo `detalles`. Si sí, agregar una variable; si no, corregir el `.md`.

---

## 🟡 IMPORTANTE — Otras Inconsistencias

### 6. Plantillas XLSX de entrega con tamaño idéntico

```
entrega_copropiedades.xlsx  → 10,554,928 bytes
entrega_hogar.xlsx          → 10,554,928 bytes
entrega_otro.xlsx           → 10,554,928 bytes
entrega_vehiculos.xlsx      → 10,554,928 bytes
```

Todas tienen **exactamente el mismo tamaño**, lo que sugiere que son **copias genéricas** sin personalizar por rubro.

Comparar con propuesta:
```
propuesta_cop.xlsx          → 10,526,588 bytes (DIFERENTE)
propuesta_hogar.xlsx        → 10,554,928 bytes
propuesta_otros.xlsx        → 10,554,928 bytes
propuesta_vehiculos.xlsx    → 10,554,928 bytes
```

> **Acción:** Verificar que cada plantilla XLSX de entrega contenga los placeholders `[N]` correctos y diferenciados para su rubro.

---

### 7. Copropiedad TS: Faltan campos `[495]-[516]` (calculados + financiación)

El diccionario TS (`diccionario_campos_copropiedad.ts`) termina en `[494]`. No incluye:
- `[495]-[496]`: Campos calculados (bienes asegurados, total)
- `[497]-[516]`: Financiación (3, 5, 8, 11 cuotas × 5 aseguradoras)

El **Svelte los genera correctamente**, pero no se pueden buscar en el diccionario inverso.

> **Acción:** Agregar campos `[495]-[516]` a `diccionario_campos_copropiedad.ts`.

---

### 8. Todos los TS: Faltan campos de entrega `[517]-[528]`

Ningún archivo `.ts` de diccionario incluye los campos de entrega `[517]-[528]`. Estos se hardcodean directamente en cada Svelte.

> **Acción:** Considerar agregar `[517]-[528]` a todos los diccionarios TS para mantener consistencia documental.

---

## ✅ Verificados como CORRECTOS

| Rubro | Generales | Aseguradoras | Offsets TS | Entrega Svelte |
|-------|-----------|-------------|-----------|---------------|
| Copropiedad | ✅ `[1]-[39]` | ✅ 5 × 91 campos | ✅ Correctos | ✅ `[517]-[528]` OK |
| Hogar | ✅ `[1]-[30]` | ✅ 5 × 17 campos | ✅ Correctos | ✅ `[517]-[528]` OK |
| Vehículos | ✅ `[1]-[25]` | ✅ 5 × 26 campos | ✅ Correctos | ✅ `[517]-[528]` OK |
| Otros | ⚠️ Items 2-5 | ✅ 3 × 15 campos | ✅ Correctos | ✅ `[517]-[528]` OK |

---

## 📋 Resumen de Acciones por Prioridad

| # | Prio | Rubro | Archivo a corregir | Acción |
|---|------|-------|-------------------|--------|
| 1 | 🔴 | Cop | `PROPUESTA_COPROPIEDAD.md` | Renombrar +6 → `no_demerito_uso`, +7 → `cobertura_accidentes_consejo` |
| 2 | 🔴 | Otros | `PROPUESTA_OTROS.md` | Agregar `valor_inmueble_avaluo` en `[14]`, desplazar resto |
| 3 | 🔴 | Otros | `PROPUESTA_OTROS.md` | Agregar `valor_inmueble_asegurado` en `[18]`, desplazar resto |
| 4 | 🔴 | Otros | `PROPUESTA_OTROS.md` | Corregir infraseguro: agregar `infraseg_inmueble`, quitar `infraseg_total` |
| 5 | 🔴 | Otros | `PROPUESTA_OTROS.md` | Corregir `[7]=ciudad`, `[8]=dirección`; verificar si `detalles` se necesita |
| 6 | 🟡 | Todos | Plantillas XLSX | Verificar que las 4 de entrega no sean copias idénticas |
| 7 | 🟡 | Cop | `diccionario_campos_copropiedad.ts` | Agregar `[495]-[516]` al TS |
| 8 | 🟢 | Todos | `diccionario_campos_*.ts` | Agregar `[517]-[528]` a todos los diccionarios TS |

---

*Revisión realizada: Abril 2026*
