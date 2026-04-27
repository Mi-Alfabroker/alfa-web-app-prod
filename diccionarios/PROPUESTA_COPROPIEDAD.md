# Diccionario de Variables - Propuesta Copropiedad

Este documento describe las variables utilizadas para el reemplazo en la plantilla Excel `propuesta_cop.xlsx` de propuestas de copropiedades.

## Formato de Variables

Las variables se definen con el formato `[N]` donde `N` es un número único. Estas variables se reemplazan automáticamente al generar el documento de propuesta.

**Total de variables:** 516 campos  
- **Campos generales:** 39 (encabezado, cliente, detalles, avalúos, asegurados, infraseguro)
- **Por aseguradora:** 91 campos × 5 = 455 campos
- **Campos calculados y financiación:** 22 campos

---

## SECCIÓN 1: ENCABEZADO `[1]-[2]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[1]` | fecha_expedicion | Fecha de expedición del documento (formato: "8 de enero 2026") |
| `[2]` | año_vigencia | Año de vigencia de la póliza (formato: "2026-2027") |

---

## SECCIÓN 2: DATOS DEL CLIENTE / COPROPIEDAD `[3]-[9]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[3]` | nombre_cliente | Nombre completo del cliente o razón social |
| `[4]` | nit | NIT o número de documento del cliente |
| `[5]` | administrador | Nombre del administrador de la copropiedad |
| `[6]` | tipo_copropiedad | Tipo de copropiedad (Residencial, Comercial, etc.) |
| `[7]` | ciudad | Ciudad donde se ubica la copropiedad |
| `[8]` | direccion | Dirección de la copropiedad |
| `[9]` | asesor | Nombre del asesor comercial |

---

## SECCIÓN 3: DETALLES DE LA COPROPIEDAD `[10]-[19]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[10]` | ano_construccion | Año de construcción del edificio |
| `[11]` | estrato | Estrato socioeconómico |
| `[12]` | numero_torres | Número de torres |
| `[13]` | numero_maximo_pisos | Número máximo de pisos |
| `[14]` | numero_maximo_sotanos | Número máximo de sótanos |
| `[15]` | cantidad_unidades_casa | Cantidad de unidades tipo casa |
| `[16]` | cantidad_unidades_apartamentos | Cantidad de apartamentos |
| `[17]` | cantidad_unidades_locales | Cantidad de locales comerciales |
| `[18]` | cantidad_unidades_oficinas | Cantidad de oficinas |
| `[19]` | cantidad_unidades_otros | Cantidad de otras unidades |

---

## SECCIÓN 4: VALORES DEL BIEN (AVALÚO) `[20]-[24]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[20]` | valor_edificio_area_comun_avaluo | Valor avalúo área común |
| `[21]` | valor_edificio_area_privada_avaluo | Valor avalúo área privada |
| `[22]` | valor_maquinaria_equipo_avaluo | Valor avalúo maquinaria y equipo |
| `[23]` | valor_equipo_electrico_electronico_avaluo | Valor avalúo equipo eléctrico/electrónico |
| `[24]` | valor_muebles_avaluo | Valor avalúo muebles |

---

## SECCIÓN 5: VALORES ASEGURADOS `[25]-[34]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[25]` | valor_area_comun_asegurado | Valor asegurado área común |
| `[26]` | valor_area_privada_asegurado | Valor asegurado área privada |
| `[27]` | valor_maquinaria_equipo_asegurado | Valor asegurado maquinaria y equipo |
| `[28]` | valor_equipo_electronico_asegurado | Valor asegurado equipo electrónico |
| `[29]` | valor_muebles_asegurado | Valor asegurado muebles |
| `[30]` | valor_directores_asegurado | Valor asegurado directores y administradores |
| `[31]` | valor_rce_asegurado | Valor asegurado RCE |
| `[32]` | valor_manejo_asegurado | Valor asegurado manejo |
| `[33]` | valor_transporte_valores_vigencia_asegurado | Valor asegurado transporte valores (vigencia) |
| `[34]` | valor_transporte_valores_despacho_asegurado | Valor asegurado transporte valores (despacho) |

---

## SECCIÓN 6: INFRASEGURO `[35]-[39]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[35]` | infraseg_area_comun | Porcentaje infraseguro área común |
| `[36]` | infraseg_area_privada | Porcentaje infraseguro área privada |
| `[37]` | infraseg_maquinaria | Porcentaje infraseguro maquinaria |
| `[38]` | infraseg_equipo_electrico | Porcentaje infraseguro equipo eléctrico |
| `[39]` | infraseg_muebles | Porcentaje infraseguro muebles |

---

## SECCIÓN 7: ASEGURADORAS `[40]-[494]`

Cada aseguradora tiene **91 campos** con un offset específico:

| Aseguradora | Rango | Offset Base |
|-------------|-------|-------------|
| Aseguradora 1 | `[40]` - `[130]` | 40 |
| Aseguradora 2 | `[131]` - `[221]` | 131 |
| Aseguradora 3 | `[222]` - `[312]` | 222 |
| Aseguradora 4 | `[313]` - `[403]` | 313 |
| Aseguradora 5 | `[404]` - `[494]` | 404 |

### Estructura de campos por aseguradora (offset +N)

#### Datos Base `[+0]` a `[+8]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +0 | nombre_aseg | Nombre de la aseguradora |
| +1 | pais_origen_aseg | País de origen / Logo |
| +2 | respaldo_aseg | Respaldo de la aseguradora |
| +3 | numeral_asistencia_aseg | Numeral de asistencia |
| +4 | valor_prima_aseg | Valor de la prima |
| +5 | valor_total_anual_aseg | Valor total anual |
| +6 | no_demerito_uso_aseg | No demérito por uso (texto editable) |
| +7 | cobertura_accidentes_consejo_aseg | Cobertura accidentes consejo (texto editable) |
| +8 | rotura_vidrios_eventos_aseg | Rotura de vidrios por eventos |

#### DM - Daños Materiales `[+9]` a `[+23]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +9 | dm_terremoto_porcentaje | Terremoto - Porcentaje |
| +10 | dm_terremoto_tipo | Terremoto - Tipo |
| +11 | dm_terremoto_minimo | Terremoto - Mínimo |
| +12 | dm_inundacion_porcentaje | Inundación - Porcentaje |
| +13 | dm_inundacion_tipo | Inundación - Tipo |
| +14 | dm_inundacion_minimo | Inundación - Mínimo |
| +15 | dm_incendio_porcentaje | Incendio - Porcentaje |
| +16 | dm_incendio_tipo | Incendio - Tipo |
| +17 | dm_incendio_minimo | Incendio - Mínimo |
| +18 | dm_amit_porcentaje | AMIT - Porcentaje |
| +19 | dm_amit_tipo | AMIT - Tipo |
| +20 | dm_amit_minimo | AMIT - Mínimo |
| +21 | dm_tuberia_vidrio_porcentaje | Tubería/Vidrio - Porcentaje |
| +22 | dm_tuberia_vidrio_tipo | Tubería/Vidrio - Tipo |
| +23 | dm_tuberia_vidrio_minimo | Tubería/Vidrio - Mínimo |

#### DI - Daños Internos `[+24]` a `[+29]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +24 | di_maq_equipo_porcentaje | Maquinaria/Equipo - Porcentaje |
| +25 | di_maq_equipo_tipo | Maquinaria/Equipo - Tipo |
| +26 | di_maq_equipo_minimo | Maquinaria/Equipo - Mínimo |
| +27 | di_equipo_electronico_porcentaje | Equipo Electrónico - Porcentaje |
| +28 | di_equipo_electronico_tipo | Equipo Electrónico - Tipo |
| +29 | di_equipo_electronico_minimo | Equipo Electrónico - Mínimo |

#### SCV - Sustracción con Violencia `[+30]` a `[+41]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +30 | scv_maq_equipo_porcentaje | Maquinaria/Equipo - Porcentaje |
| +31 | scv_maq_equipo_tipo | Maquinaria/Equipo - Tipo |
| +32 | scv_maq_equipo_minimo | Maquinaria/Equipo - Mínimo |
| +33 | scv_equipo_electronico_porcentaje | Equipo Electrónico - Porcentaje |
| +34 | scv_equipo_electronico_tipo | Equipo Electrónico - Tipo |
| +35 | scv_equipo_electronico_minimo | Equipo Electrónico - Mínimo |
| +36 | scv_dineros_porcentaje | Dineros - Porcentaje |
| +37 | scv_dineros_tipo | Dineros - Tipo |
| +38 | scv_dineros_minimo | Dineros - Mínimo |
| +39 | scv_muebles_porcentaje | Muebles - Porcentaje |
| +40 | scv_muebles_tipo | Muebles - Tipo |
| +41 | scv_muebles_minimo | Muebles - Mínimo |

#### DA - Directores y Administradores `[+42]` a `[+44]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +42 | da_amparo_basico_porcentaje | Amparo Básico - Porcentaje |
| +43 | da_amparo_basico_tipo | Amparo Básico - Tipo |
| +44 | da_amparo_basico_minimo | Amparo Básico - Mínimo |

#### RCE - Deducibles `[+45]` a `[+59]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +45 | rce_ded_contratistas_porcentaje | Contratistas - Porcentaje |
| +46 | rce_ded_contratistas_tipo | Contratistas - Tipo |
| +47 | rce_ded_contratistas_minimo | Contratistas - Mínimo |
| +48 | rce_ded_cruzada_porcentaje | Cruzada - Porcentaje |
| +49 | rce_ded_cruzada_tipo | Cruzada - Tipo |
| +50 | rce_ded_cruzada_minimo | Cruzada - Mínimo |
| +51 | rce_ded_patronal_porcentaje | Patronal - Porcentaje |
| +52 | rce_ded_patronal_tipo | Patronal - Tipo |
| +53 | rce_ded_patronal_minimo | Patronal - Mínimo |
| +54 | rce_ded_parqueaderos_porcentaje | Parqueaderos - Porcentaje |
| +55 | rce_ded_parqueaderos_tipo | Parqueaderos - Tipo |
| +56 | rce_ded_parqueaderos_minimo | Parqueaderos - Mínimo |
| +57 | rce_ded_gastos_medicos_porcentaje | Gastos Médicos - Porcentaje |
| +58 | rce_ded_gastos_medicos_tipo | Gastos Médicos - Tipo |
| +59 | rce_ded_gastos_medicos_minimo | Gastos Médicos - Mínimo |

#### RCE - Sublímites `[+60]` a `[+74]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +60 | rce_sub_contratistas_porcentaje | Contratistas - Porcentaje |
| +61 | rce_sub_contratistas_tipo | Contratistas - Tipo |
| +62 | rce_sub_contratistas_minimo | Contratistas - Mínimo |
| +63 | rce_sub_cruzada_porcentaje | Cruzada - Porcentaje |
| +64 | rce_sub_cruzada_tipo | Cruzada - Tipo |
| +65 | rce_sub_cruzada_minimo | Cruzada - Mínimo |
| +66 | rce_sub_patronal_porcentaje | Patronal - Porcentaje |
| +67 | rce_sub_patronal_tipo | Patronal - Tipo |
| +68 | rce_sub_patronal_minimo | Patronal - Mínimo |
| +69 | rce_sub_parqueaderos_porcentaje | Parqueaderos - Porcentaje |
| +70 | rce_sub_parqueaderos_tipo | Parqueaderos - Tipo |
| +71 | rce_sub_parqueaderos_minimo | Parqueaderos - Mínimo |
| +72 | rce_sub_gastos_medicos_porcentaje | Gastos Médicos - Porcentaje |
| +73 | rce_sub_gastos_medicos_tipo | Gastos Médicos - Tipo |
| +74 | rce_sub_gastos_medicos_minimo | Gastos Médicos - Mínimo |

#### Manejo `[+75]` a `[+77]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +75 | manejo_amparo_basico_porcentaje | Amparo Básico - Porcentaje |
| +76 | manejo_amparo_basico_tipo | Amparo Básico - Tipo |
| +77 | manejo_amparo_basico_minimo | Amparo Básico - Mínimo |

#### Transporte de Valores `[+78]` a `[+80]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +78 | tv_amparo_basico_porcentaje | Amparo Básico - Porcentaje |
| +79 | tv_amparo_basico_tipo | Amparo Básico - Tipo |
| +80 | tv_amparo_basico_minimo | Amparo Básico - Mínimo |

#### Asistencias Área Común `[+81]` a `[+85]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +81 | asist_comun_vidrieria | Vidriería |
| +82 | asist_comun_plomeria | Plomería |
| +83 | asist_comun_cerrajeria | Cerrajería |
| +84 | asist_comun_electricista | Electricista |
| +85 | asist_comun_total | Total asistencias área común |

#### Asistencias Área Privada `[+86]` a `[+90]`

| Offset | Campo | Descripción |
|--------|-------|-------------|
| +86 | asist_privada_vidrieria | Vidriería |
| +87 | asist_privada_plomeria | Plomería |
| +88 | asist_privada_cerrajeria | Cerrajería |
| +89 | asist_privada_electricista | Electricista |
| +90 | asist_privada_total | Total asistencias área privada |

---

## Ejemplo de Cálculo de Variables por Aseguradora

```
Variable = Offset_Base_Aseguradora + Offset_Campo
```

**Ejemplo**: Nombre de la Aseguradora 3 → `222 + 0` = `[222]`  
**Ejemplo**: DM Terremoto Porcentaje de la Aseguradora 2 → `131 + 9` = `[140]`

---

## SECCIÓN 8: CAMPOS CALCULADOS `[495]-[496]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[495]` | valor_bienes_asegurados | Suma de: Área Común + Maquinaria/Equipo + Eq. Electrónico + Muebles |
| `[496]` | bienes_total_asegurado | Suma de: Área Común + Área Privada + Maquinaria/Equipo + Eq. Electrónico + Muebles |

---

## SECCIÓN 9: FINANCIACIÓN `[497]-[516]`

### 3 Cuotas sin interés `[497]-[501]`
Fórmula: Prima ÷ 3

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[497]` | financiacion_3c_aseg_1 | 3 cuotas sin interés - Aseguradora 1 |
| `[498]` | financiacion_3c_aseg_2 | 3 cuotas sin interés - Aseguradora 2 |
| `[499]` | financiacion_3c_aseg_3 | 3 cuotas sin interés - Aseguradora 3 |
| `[500]` | financiacion_3c_aseg_4 | 3 cuotas sin interés - Aseguradora 4 |
| `[501]` | financiacion_3c_aseg_5 | 3 cuotas sin interés - Aseguradora 5 |

### 5 Cuotas con interés `[502]-[506]`
Fórmula de amortización: `Prima * ((tasa * (1+tasa)^5) / ((1+tasa)^5 - 1))`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[502]` | financiacion_5c_aseg_1 | 5 cuotas con interés - Aseguradora 1 |
| `[503]` | financiacion_5c_aseg_2 | 5 cuotas con interés - Aseguradora 2 |
| `[504]` | financiacion_5c_aseg_3 | 5 cuotas con interés - Aseguradora 3 |
| `[505]` | financiacion_5c_aseg_4 | 5 cuotas con interés - Aseguradora 4 |
| `[506]` | financiacion_5c_aseg_5 | 5 cuotas con interés - Aseguradora 5 |

### 8 Cuotas con interés `[507]-[511]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[507]` | financiacion_8c_aseg_1 | 8 cuotas con interés - Aseguradora 1 |
| `[508]` | financiacion_8c_aseg_2 | 8 cuotas con interés - Aseguradora 2 |
| `[509]` | financiacion_8c_aseg_3 | 8 cuotas con interés - Aseguradora 3 |
| `[510]` | financiacion_8c_aseg_4 | 8 cuotas con interés - Aseguradora 4 |
| `[511]` | financiacion_8c_aseg_5 | 8 cuotas con interés - Aseguradora 5 |

### 11 Cuotas con interés `[512]-[516]`

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[512]` | financiacion_11c_aseg_1 | 11 cuotas con interés - Aseguradora 1 |
| `[513]` | financiacion_11c_aseg_2 | 11 cuotas con interés - Aseguradora 2 |
| `[514]` | financiacion_11c_aseg_3 | 11 cuotas con interés - Aseguradora 3 |
| `[515]` | financiacion_11c_aseg_4 | 11 cuotas con interés - Aseguradora 4 |
| `[516]` | financiacion_11c_aseg_5 | 11 cuotas con interés - Aseguradora 5 |

---

## Notas Importantes

1. **Formato de valores monetarios**: Se formatean con separadores de miles sin símbolo de moneda
2. **Formato de fecha**: "día de mes año" (ej: "8 de enero 2026")
3. **Valores SI/NO**: Los campos booleanos se muestran como "SI" o "NO"
4. **Infraseguro**: Se calcula como porcentaje: `(asegurado / avalúo) * 100`
5. **Plantilla**: `propuesta_cop.xlsx`

---

*Última actualización: Abril 2026*
