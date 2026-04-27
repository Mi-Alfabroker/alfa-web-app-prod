# Diccionario de Variables - Propuesta Otros Bienes

Este documento describe las variables para la plantilla `propuesta_otros.xlsx`.

**Total de variables:** 71 campos  
- **Campos generales:** 26 (encabezado, cliente, bien, avalúos, asegurados, infraseguro)
- **Por aseguradora:** 15 campos × 3 = 45 campos

> ⚠️ **Nota:** Otros solo soporta **3 aseguradoras** (vs 5 en Hogar y Vehículos)

---

## SECCIÓN 1: ENCABEZADO `[1]-[2]`

| Variable | Campo | Tipo | Descripción | Ejemplo |
|----------|-------|------|-------------|---------|
| `[1]` | fecha_expedicion | Calculado | Fecha actual "DD de mes YYYY" | `18 de marzo 2026` |
| `[2]` | año_vigencia | Calculado | "YYYY-YYYY" | `2026-2027` |

---

## SECCIÓN 2: DATOS DEL CLIENTE Y BIEN `[3]-[13]`

| Variable | Campo | Tipo | Origen | Descripción |
|----------|-------|------|--------|-------------|
| `[3]` | nombre_cliente | BD | usuarios | Nombre del cliente o razón social |
| `[4]` | nit | BD | usuarios | Identificación del cliente |
| `[5]` | tipo_seguro | BD | otros_bienes | Equipo Electrónico, Maquinaria, etc. |
| `[6]` | bien_asegurado | BD | otros_bienes | Descripción del bien asegurado |
| `[7]` | ciudad | BD | usuarios | Ciudad donde está el bien |
| `[8]` | direccion | BD | usuarios | Dirección donde está el bien |
| `[9]` | asesor | Manual | — | Nombre del asesor |
| `[10]` | poliza_actual | Manual | — | Número de póliza actual |
| `[11]` | aseguradora_actual | Manual | — | Aseguradora actual |
| `[12]` | tasa_interes | Manual | — | Tasa de interés mensual (%) |
| `[13]` | comentarios | Manual | — | Comentarios especiales |

---

## SECCIÓN 3: VALORES DEL BIEN (AVALÚO) `[14]-[17]`

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[14]` | valor_inmueble_avaluo | BD | Valor avalúo del inmueble |
| `[15]` | valor_contenidos_normales_avaluo | BD | Valor contenidos normales |
| `[16]` | valor_contenidos_especiales_avaluo | BD | Valor contenidos especiales |
| `[17]` | valor_equipo_electronico_avaluo | BD | Valor equipos electrónicos |

---

## SECCIÓN 4: VALORES ASEGURADOS `[18]-[22]`

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[18]` | valor_inmueble_asegurado | BD | Valor asegurado del inmueble |
| `[19]` | valor_contenidos_normales_asegurado | BD | Valor asegurado contenidos normales |
| `[20]` | valor_contenidos_especiales_asegurado | BD | Valor asegurado contenidos especiales |
| `[21]` | valor_equipo_electronico_asegurado | BD | Valor asegurado equipo electrónico |
| `[22]` | valor_rc_asegurado | BD | Valor asegurado RC |

---

## SECCIÓN 5: INFRASEGURO `[23]-[26]`

Fórmula: `1 - (Valor Asegurado / Valor Avalúo)` → expresado como porcentaje

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[23]` | infraseg_inmueble | % infraseguro del inmueble |
| `[24]` | infraseg_contenidos_normales | % infraseguro contenidos normales |
| `[25]` | infraseg_contenidos_especiales | % infraseguro contenidos especiales |
| `[26]` | infraseg_equipo_electronico | % infraseguro equipo electrónico |

---

## SECCIÓN 6: ASEGURADORAS `[27]-[71]`

Cada aseguradora tiene **15 campos**. Solo **3 aseguradoras**:

| Aseguradora | Código Inicio | Código Fin | Campos |
|-------------|---------------|------------|--------|
| **Aseguradora 1** | `[27]` | `[41]` | 15 |
| **Aseguradora 2** | `[42]` | `[56]` | 15 |
| **Aseguradora 3** | `[57]` | `[71]` | 15 |

### Estructura por aseguradora (offset +N)

#### Generales `[+0]` a `[+4]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +0 | nombre_aseg_N | Nombre de la aseguradora |
| +1 | pais_origen_aseg_N | Bandera país de origen |
| +2 | respaldo_aseg_N | Respaldo internacional |
| +3 | valor_prima_aseg_N | Prima anual (COP) |
| +4 | valor_total_anual_aseg_N | Total anual |

#### Deducibles de Daños `[+5]` a `[+7]`

| Offset | Campo | Formato |
|--------|-------|---------|
| +5 | otr_deducible_terremoto | `10% Valor asegurable Mín $500.000` |
| +6 | otr_deducible_amit | `10% Valor asegurable Mín $500.000` |
| +7 | otr_deducible_demas_eventos | `5% Valor asegurable Mín $300.000` |

#### Deducibles de Hurto `[+8]` a `[+10]`

| Offset | Campo | Formato |
|--------|-------|---------|
| +8 | otr_hurto_cn_deducible | `10% Valor asegurable Mín $500.000` |
| +9 | otr_hurto_ce_deducible | `10% Valor asegurable Mín $500.000` |
| +10 | otr_hurto_ee_deducible | `10% Valor asegurable Mín $500.000` |

#### Coberturas Adicionales `[+11]` a `[+13]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +11 | otr_cobertura_adicional_1 | Cobertura adicional 1 (texto libre) |
| +12 | otr_cobertura_adicional_2 | Cobertura adicional 2 (texto libre) |
| +13 | otr_cobertura_adicional_3 | Cobertura adicional 3 (texto libre) |

#### Observaciones `[+14]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +14 | otr_observaciones | Observaciones generales |

---

### Mapeo Completo Aseguradora 1: `[27]` - `[41]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[27]` | nombre_aseg_1 | Nombre aseguradora |
| `[28]` | pais_origen_aseg_1 | Bandera país |
| `[29]` | respaldo_aseg_1 | Respaldo |
| `[30]` | valor_prima_aseg_1 | Prima anual |
| `[31]` | valor_total_anual_aseg_1 | Total anual |
| `[32]` | otr_deducible_terremoto_aseg_1 | Ded. terremoto |
| `[33]` | otr_deducible_amit_aseg_1 | Ded. AMIT |
| `[34]` | otr_deducible_demas_eventos_aseg_1 | Ded. demás eventos |
| `[35]` | otr_hurto_cn_deducible_aseg_1 | Hurto CN |
| `[36]` | otr_hurto_ce_deducible_aseg_1 | Hurto CE |
| `[37]` | otr_hurto_ee_deducible_aseg_1 | Hurto EE |
| `[38]` | otr_cobertura_adicional_1_aseg_1 | Cobertura adic. 1 |
| `[39]` | otr_cobertura_adicional_2_aseg_1 | Cobertura adic. 2 |
| `[40]` | otr_cobertura_adicional_3_aseg_1 | Cobertura adic. 3 |
| `[41]` | otr_observaciones_aseg_1 | Observaciones |

> **Aseguradoras 2-3:** Mismo patrón con offsets `[42-56]`, `[57-71]`.

---

## Tipos de Seguro Soportados

- Equipo Electrónico
- Maquinaria y Equipo
- Herramientas
- Equipos Médicos
- Equipos de Cómputo
- Otros Activos

---

## Notas Importantes

1. **Solo 3 aseguradoras** (a diferencia de Hogar y Vehículos con 5)
2. **Sin sublímites RC** (a diferencia de Vehículos)
3. **Plantilla**: `propuesta_otros.xlsx`

---

*Última actualización: Abril 2026*
