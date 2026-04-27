# Diccionario de Variables - Propuesta Vehículos

Este documento describe las variables para la plantilla `propuesta_vehiculos.xlsx`.

**Total de variables:** 155 campos  
- **Campos generales:** 25 (encabezado, cliente, vehículo, avalúos, asegurados)
- **Por aseguradora:** 26 campos × 5 = 130 campos

---

## SECCIÓN 1: ENCABEZADO `[1]-[2]`

| Variable | Campo | Tipo | Descripción | Ejemplo |
|----------|-------|------|-------------|---------|
| `[1]` | fecha_expedicion | Calculado | Fecha actual "DD de mes YYYY" | `18 de marzo 2026` |
| `[2]` | año_vigencia | Calculado | "YYYY-YYYY" | `2026-2027` |

---

## SECCIÓN 2: DATOS DEL CLIENTE Y VEHÍCULO `[3]-[16]`

| Variable | Campo | Tipo | Origen | Descripción |
|----------|-------|------|--------|-------------|
| `[3]` | nombre_cliente | BD | usuarios | Nombre del cliente o razón social |
| `[4]` | nit | BD | usuarios | Identificación del cliente |
| `[5]` | tipo_vehiculo | BD | vehiculos | Automóvil, Camioneta, Motocicleta |
| `[6]` | marca | BD | vehiculos | Marca del vehículo |
| `[7]` | ano_modelo | BD | vehiculos | Año modelo |
| `[8]` | placa | BD | vehiculos | Placa (formato: ABC123) |
| `[9]` | codigo_fasecolda | BD | vehiculos | Código Fasecolda |
| `[10]` | ciudad_residencia | BD | usuarios | Ciudad de circulación |
| `[11]` | uso_vehiculo | BD | polizas | Particular, Servicio Público, Comercial |
| `[12]` | asesor | Manual | — | Nombre del asesor |
| `[13]` | poliza_actual | Manual | — | Número de póliza actual |
| `[14]` | aseguradora_actual | Manual | — | Aseguradora actual |
| `[15]` | tasa_interes | Manual | — | Tasa de interés mensual (%) |
| `[16]` | comentarios | Manual | — | Comentarios especiales |

---

## SECCIÓN 3: VALORES DEL BIEN (AVALÚO) `[17]-[21]`

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[17]` | valor_vehiculo | BD | Valor Fasecolda del vehículo |
| `[18]` | valor_accesorios_avaluo | BD | Valor de accesorios adicionales |
| `[19]` | valor_rc_avaluo | BD | Valor de RC (avalúo) |
| `[20]` | valor_total_avaluo | Calculado | `[17]` + `[18]` |
| `[21]` | ano_modelo_vigencia | BD | Año modelo (repetido) |

---

## SECCIÓN 4: VALORES ASEGURADOS `[22]-[25]`

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[22]` | valor_asegurado_vehiculo | BD | Valor asegurado del vehículo |
| `[23]` | valor_asegurado_accesorios | BD | Valor asegurado de accesorios |
| `[24]` | valor_asegurado_rc | BD | Valor asegurado de RC |
| `[25]` | valor_total_asegurado | Calculado | `[22]` + `[23]` |

---

## SECCIÓN 5: ASEGURADORAS `[26]-[155]`

Cada aseguradora tiene **26 campos** (el más complejo de los rubros):

| Aseguradora | Código Inicio | Código Fin | Campos |
|-------------|---------------|------------|--------|
| **Aseguradora 1** | `[26]` | `[51]` | 26 |
| **Aseguradora 2** | `[52]` | `[77]` | 26 |
| **Aseguradora 3** | `[78]` | `[103]` | 26 |
| **Aseguradora 4** | `[104]` | `[129]` | 26 |
| **Aseguradora 5** | `[130]` | `[155]` | 26 |

### Estructura por aseguradora (offset +N)

#### Generales `[+0]` a `[+4]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +0 | nombre_aseg_N | Nombre de la aseguradora |
| +1 | pais_origen_aseg_N | Bandera país de origen |
| +2 | respaldo_aseg_N | Respaldo internacional |
| +3 | valor_prima_aseg_N | Prima anual (COP) |
| +4 | valor_total_anual_aseg_N | Total anual |

#### Deducibles de Pérdida `[+5]` a `[+7]`

| Offset | Campo | Formato |
|--------|-------|---------|
| +5 | veh_deducible_perdida_parcial | `10% Valor asegurable Mín $500.000` |
| +6 | veh_deducible_perdida_total | `10% Valor asegurable Mín $1.000.000` |
| +7 | veh_deducible_terremoto | `10% Valor asegurable Mín $1.000.000` |

#### Deducibles de Hurto `[+8]` a `[+9]`

| Offset | Campo | Formato |
|--------|-------|---------|
| +8 | veh_hurto_perdida_parcial | `10% Valor asegurable Mín $500.000` |
| +9 | veh_hurto_perdida_total | `20% Valor asegurable Mín $3.000.000` |

#### Deducible RC `[+10]`

| Offset | Campo | Formato |
|--------|-------|---------|
| +10 | veh_deducible_rc | `10% Valor asegurado Mín $500.000` |

#### Sublímites RC `[+11]` a `[+14]` — EXCLUSIVO VEHÍCULOS

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +11 | veh_rc_sublimite_bienes_terceros | Sublímite daños bienes terceros (COP) |
| +12 | veh_rc_sublimite_amparo_patrimonial | Sublímite amparo patrimonial (COP) |
| +13 | veh_rc_sublimite_muerte_lesion_una | Sublímite muerte/lesión 1 persona (COP) |
| +14 | veh_rc_sublimite_muerte_lesion_dos_mas | Sublímite muerte/lesión 2+ personas (COP) |

#### Coberturas Adicionales `[+15]` a `[+21]` — CHECKBOXES SI/NO

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +15 | veh_cobertura_adicional_1 | RC Voluntaria |
| +16 | veh_cobertura_adicional_2 | Daños a Ocupantes |
| +17 | veh_cobertura_adicional_3 | Asistencia en Viaje |
| +18 | veh_cobertura_adicional_4 | Vehículo de Reemplazo |
| +19 | veh_cobertura_adicional_5 | Exención Deducible |
| +20 | veh_cobertura_adicional_6 | Accidentes Personales Conductor |
| +21 | veh_cobertura_adicional_7 | Eventos de la Naturaleza |

#### Campos Adicionales `[+22]` a `[+25]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +22 | veh_observaciones | Observaciones generales |
| +23 | veh_asistencia_tipo | Tipo de asistencia (ej: "Nacional 24/7") |
| +24 | veh_conductor_elegido | Nombre del conductor elegido |
| +25 | veh_beneficiario_adicional | Nombre del beneficiario adicional |

---

### Mapeo Completo Aseguradora 1: `[26]` - `[51]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[26]` | nombre_aseg_1 | Nombre aseguradora |
| `[27]` | pais_origen_aseg_1 | Bandera país |
| `[28]` | respaldo_aseg_1 | Respaldo |
| `[29]` | valor_prima_aseg_1 | Prima anual |
| `[30]` | valor_total_anual_aseg_1 | Total anual |
| `[31]` | veh_deducible_perdida_parcial_aseg_1 | Ded. pérdida parcial |
| `[32]` | veh_deducible_perdida_total_aseg_1 | Ded. pérdida total |
| `[33]` | veh_deducible_terremoto_aseg_1 | Ded. terremoto |
| `[34]` | veh_hurto_perdida_parcial_aseg_1 | Hurto parcial |
| `[35]` | veh_hurto_perdida_total_aseg_1 | Hurto total |
| `[36]` | veh_deducible_rc_aseg_1 | Ded. RC |
| `[37]` | veh_rc_sublimite_bienes_terceros_aseg_1 | Sublím. bienes terceros |
| `[38]` | veh_rc_sublimite_amparo_patrimonial_aseg_1 | Sublím. amparo patrimonial |
| `[39]` | veh_rc_sublimite_muerte_lesion_una_aseg_1 | Sublím. muerte 1 persona |
| `[40]` | veh_rc_sublimite_muerte_lesion_dos_mas_aseg_1 | Sublím. muerte 2+ personas |
| `[41]`-`[47]` | veh_cobertura_adicional_1-7_aseg_1 | Coberturas (SI/NO) |
| `[48]` | veh_observaciones_aseg_1 | Observaciones |
| `[49]` | veh_asistencia_tipo_aseg_1 | Tipo asistencia |
| `[50]` | veh_conductor_elegido_aseg_1 | Conductor elegido |
| `[51]` | veh_beneficiario_adicional_aseg_1 | Beneficiario adicional |

> **Aseguradoras 2-5:** Mismo patrón con offsets `[52-77]`, `[78-103]`, `[104-129]`, `[130-155]`.

---

## Notas Importantes

1. **Plantilla**: `propuesta_vehiculos.xlsx`
2. **Sublímites RC**: Valores monetarios simples (sin formato deducible)
3. **Coberturas adicionales**: Solo "SI" o "NO"
4. **Vehículos es el rubro más complejo** (26 campos/aseguradora vs 17 Hogar, 15 Otros)

---

*Última actualización: Abril 2026*
