# Diccionario de Variables - Propuesta Hogar

Este documento describe las variables utilizadas para el reemplazo en la plantilla Excel `propuesta_hogar.xlsx` de propuestas de seguros de hogar.

## Formato de Variables

Las variables se definen con el formato `[N]` donde `N` es un número único. El sistema soporta hasta **5 aseguradoras** por propuesta, cada una con 17 campos configurables.

**Total de variables:** 115 campos  
- **Campos generales:** 30 (encabezado, cliente, avalúos, asegurados, infraseguro)
- **Por aseguradora:** 17 campos × 5 = 85 campos

---

## SECCIÓN 1: ENCABEZADO `[1]-[2]`

| Variable | Campo | Tipo | Descripción | Ejemplo |
|----------|-------|------|-------------|---------|
| `[1]` | fecha_expedicion | Calculado | Fecha actual en formato "DD de mes YYYY" | `18 de marzo 2026` |
| `[2]` | año_vigencia | Calculado | Año de vigencia en formato "YYYY-YYYY" | `2026-2027` |

---

## SECCIÓN 2: DATOS DEL CLIENTE E INMUEBLE `[3]-[14]`

| Variable | Campo | Tipo | Origen | Descripción |
|----------|-------|------|--------|-------------|
| `[3]` | nombre_cliente | BD | usuarios.nombre / razon_social | Nombre del cliente o razón social |
| `[4]` | nit | BD | usuarios.nit / numero_documento | Identificación del cliente |
| `[5]` | tipo_inmueble | BD | hogares.tipo_inmueble | Casa, Apartamento, Finca |
| `[6]` | ciudad_inmueble | BD | hogares.ciudad | Ciudad donde está ubicado el inmueble |
| `[7]` | direccion_inmueble | BD | hogares.direccion | Dirección completa del inmueble |
| `[8]` | numero_pisos | BD | hogares.numero_pisos | Cantidad de pisos del inmueble |
| `[9]` | ano_construccion | BD | hogares.ano_construccion | Año de construcción del inmueble |
| `[10]` | asesor | Manual | Usuario | Nombre del asesor que elabora la propuesta |
| `[11]` | poliza_actual | Manual | Usuario | Número de póliza actual (si aplica) |
| `[12]` | aseguradora_actual | Manual | Usuario | Aseguradora actual del cliente |
| `[13]` | tasa_interes | Manual | Usuario | Tasa de interés mensual (%) para cálculo de cuotas |
| `[14]` | comentarios | Manual | Usuario | Comentarios o condiciones especiales |

---

## SECCIÓN 3: VALORES DEL BIEN (AVALÚO) `[15]-[19]`

| Variable | Campo | Tipo | Origen | Descripción |
|----------|-------|------|--------|-------------|
| `[15]` | valor_inmueble_avaluo | BD | hogares.valor_inmueble_avaluo | Valor comercial del inmueble |
| `[16]` | valor_contenidos_normales_avaluo | BD | hogares.valor_contenidos_normales_avaluo | Valor de contenidos normales |
| `[17]` | valor_contenidos_especiales_avaluo | BD | hogares.valor_contenidos_especiales_avaluo | Valor de contenidos especiales (joyas, arte) |
| `[18]` | valor_equipo_electronico_avaluo | BD | hogares.valor_equipo_electronico_avaluo | Valor de equipos electrónicos |
| `[19]` | valor_maquinaria_equipo_avaluo | BD | hogares.valor_maquinaria_equipo_avaluo | Valor de maquinaria y equipos |

**Formato:** COP con separadores de miles (ej: `150.000.000`)

---

## SECCIÓN 4: VALORES ASEGURADOS `[20]-[25]`

| Variable | Campo | Tipo | Origen | Descripción |
|----------|-------|------|--------|-------------|
| `[20]` | valor_inmueble_asegurado | BD | polizas.valor_asegurado_inmueble | Valor asegurado del inmueble |
| `[21]` | valor_contenidos_normales_asegurado | BD | polizas.valor_asegurado_contenidos_normales | Valor asegurado de contenidos normales |
| `[22]` | valor_contenidos_especiales_asegurado | BD | polizas.valor_asegurado_contenidos_especiales | Valor asegurado de contenidos especiales |
| `[23]` | valor_equipo_electronico_asegurado | BD | polizas.valor_asegurado_equipo_electronico | Valor asegurado de equipos electrónicos |
| `[24]` | valor_maquinaria_equipo_asegurado | BD | polizas.valor_asegurado_maquinaria | Valor asegurado de maquinaria y equipos |
| `[25]` | valor_rc_asegurado | BD | polizas.valor_asegurado_rc | Valor asegurado de responsabilidad civil |

---

## SECCIÓN 5: INFRASEGURO `[26]-[30]`

Porcentaje calculado automáticamente: `(Valor Asegurado / Valor Avalúo) × 100`

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[26]` | infraseg_inmueble | Calculado | % infraseguro del inmueble |
| `[27]` | infraseg_contenidos_normales | Calculado | % infraseguro de contenidos normales |
| `[28]` | infraseg_contenidos_especiales | Calculado | % infraseguro de contenidos especiales |
| `[29]` | infraseg_equipo_electronico | Calculado | % infraseguro de equipos electrónicos |
| `[30]` | infraseg_maquinaria | Calculado | % infraseguro de maquinaria y equipos |

---

## SECCIÓN 6: ASEGURADORAS `[31]-[115]`

Cada aseguradora tiene **17 campos configurables**:

| Aseguradora | Código Inicio | Código Fin | Campos |
|-------------|---------------|------------|--------|
| **Aseguradora 1** | `[31]` | `[47]` | 17 |
| **Aseguradora 2** | `[48]` | `[64]` | 17 |
| **Aseguradora 3** | `[65]` | `[81]` | 17 |
| **Aseguradora 4** | `[82]` | `[98]` | 17 |
| **Aseguradora 5** | `[99]` | `[115]` | 17 |

### Estructura de campos por aseguradora (offset +N)

#### Campos Generales `[+0]` a `[+4]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +0 | nombre_aseg_N | Nombre de la aseguradora |
| +1 | pais_origen_aseg_N | Ruta de la bandera del país de origen |
| +2 | respaldo_aseg_N | Texto de respaldo o "Compañía Internacional" |
| +3 | valor_prima_aseg_N | Prima anual (COP con separadores) |
| +4 | valor_total_anual_aseg_N | Total anual (igual a prima) |

#### Deducibles de Daños `[+5]` a `[+7]`

| Offset | Campo | Descripción | Formato |
|--------|-------|-------------|---------|
| +5 | hog_deducible_terremoto_aseg_N | Deducible por terremoto | `10% Valor asegurable Mín $500.000` |
| +6 | hog_deducible_amit_aseg_N | Deducible por AMIT | `10% Valor asegurable Mín $500.000` |
| +7 | hog_deducible_demas_eventos_aseg_N | Deducible otros eventos | `10% Valor asegurable Mín $500.000` |

#### Deducibles Hurto Contenidos Normales `[+8]` a `[+10]`

| Offset | Campo | Descripción | Formato |
|--------|-------|-------------|---------|
| +8 | hog_hurto_cn_terremoto_aseg_N | Deducible hurto CN por terremoto | `10% Valor asegurable Mín $500.000` |
| +9 | hog_hurto_cn_demas_eventos_aseg_N | Deducible hurto CN otros eventos | `10% Valor asegurable Mín $500.000` |
| +10 | hog_hurto_cn_hurto_aseg_N | Deducible hurto CN por hurto | `10% Valor asegurable Mín $500.000` |

#### Deducibles Hurto Contenidos Especiales `[+11]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +11 | hog_hurto_ce_hurto_aseg_N | Deducible hurto CE por hurto |

#### Deducibles Hurto Equipo Electrónico `[+12]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +12 | hog_hurto_ee_hurto_aseg_N | Deducible hurto EE por hurto |

#### Coberturas Adicionales `[+13]` a `[+15]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +13 | hog_cobertura_adicional_1_aseg_N | Cobertura adicional 1 (texto libre) |
| +14 | hog_cobertura_adicional_2_aseg_N | Cobertura adicional 2 (texto libre) |
| +15 | hog_cobertura_adicional_3_aseg_N | Cobertura adicional 3 (texto libre) |

#### Observaciones `[+16]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +16 | hog_observaciones_aseg_N | Observaciones generales de la aseguradora |

---

### Mapeo Completo Aseguradora 1: `[31]` - `[47]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[31]` | nombre_aseg_1 | Nombre de la aseguradora |
| `[32]` | pais_origen_aseg_1 | Ruta bandera país |
| `[33]` | respaldo_aseg_1 | Respaldo internacional |
| `[34]` | valor_prima_aseg_1 | Prima anual (COP) |
| `[35]` | valor_total_anual_aseg_1 | Total anual (COP) |
| `[36]` | hog_deducible_terremoto_aseg_1 | Deducible terremoto |
| `[37]` | hog_deducible_amit_aseg_1 | Deducible AMIT |
| `[38]` | hog_deducible_demas_eventos_aseg_1 | Deducible demás eventos |
| `[39]` | hog_hurto_cn_terremoto_aseg_1 | Hurto CN - terremoto |
| `[40]` | hog_hurto_cn_demas_eventos_aseg_1 | Hurto CN - demás eventos |
| `[41]` | hog_hurto_cn_hurto_aseg_1 | Hurto CN - hurto |
| `[42]` | hog_hurto_ce_hurto_aseg_1 | Hurto CE - hurto |
| `[43]` | hog_hurto_ee_hurto_aseg_1 | Hurto EE - hurto |
| `[44]` | hog_cobertura_adicional_1_aseg_1 | Cobertura adicional 1 |
| `[45]` | hog_cobertura_adicional_2_aseg_1 | Cobertura adicional 2 |
| `[46]` | hog_cobertura_adicional_3_aseg_1 | Cobertura adicional 3 |
| `[47]` | hog_observaciones_aseg_1 | Observaciones |

> **Aseguradoras 2-5:** Mismo patrón con offsets `[48-64]`, `[65-81]`, `[82-98]`, `[99-115]`.

---

## Formato de Deducibles

Almacenamiento BD: `"porcentaje,tipo,minimo"` → Salida: `10% Valor asegurable Mín $500.000`

---

## Notas Importantes

1. **Formato de valores monetarios**: Sin decimales, con separadores de miles
2. **Formato de fecha**: "día de mes año" (ej: "18 de marzo 2026")
3. **Infraseguro**: `(Valor Asegurado / Valor Avalúo) × 100`
4. **Plantilla**: `propuesta_hogar.xlsx`

---

*Última actualización: Abril 2026*
