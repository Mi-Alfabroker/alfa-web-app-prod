# Diccionario de Variables para Propuestas de Otros Bienes

Este documento describe todas las variables utilizadas en las propuestas de seguros de **Otros Bienes** (equipos electrónicos, maquinaria, otros activos). Las variables se reemplazan en la plantilla Excel `propuesta_otros.xlsx` para generar cotizaciones personalizadas.

## Estructura General

El diccionario mapea códigos compactos `[N]` a nombres descriptivos de campos. El sistema soporta hasta **3 aseguradoras** por propuesta (a diferencia de Hogar y Vehículos que soportan 5), cada una con 15 campos configurables.

**Total de variables:** 71 campos  
- Campos generales:** 26 (encabezado, cliente, bien, avalúos, asegurados, infraseguro)
- **Por aseguradora:** 15 campos × 3 = 45 campos

---

## 1. Encabezado del Documento

Variables calculadas automáticamente al momento de generar la propuesta.

| Código | Nombre Variable | Tipo | Descripción | Ejemplo |
|--------|----------------|------|-------------|---------|
| `[1]` | `fecha_expedicion` | Calculado | Fecha actual en formato "DD de mes YYYY" | `18 de marzo 2026` |
| `[2]` | `año_vigencia` | Calculado | Año de vigencia en formato "YYYY-YYYY" | `2026-2027` |

---

## 2. Datos del Cliente y Bien

Campos prellenados desde la base de datos (usuarios + otros_bienes) y editables manualmente.

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[3]` | `nombre_cliente` | BD | usuarios.nombre / razon_social | Nombre del cliente o razón social |
| `[4]` | `nit` | BD | usuarios.nit / numero_documento | Identificación del cliente |
| `[5]` | `tipo_seguro` | BD | otros_bienes.tipo_seguro | Tipo de seguro (Equipo Electrónico, Maquinaria, etc.) |
| `[6]` | `bien_asegurado` | BD | otros_bienes.bien_asegurado | Descripción del bien asegurado |
| `[7]` | `detalles` | BD | otros_bienes.detalles | Detalles adicionales del bien |
| `[8]` | `ciudad` | BD | usuarios.ciudad_residencia | Ciudad donde está ubicado el bien |
| `[9]` | `asesor` | Manual | Usuario | Nombre del asesor que elabora la propuesta |
| `[10]` | `poliza_actual` | Manual | Usuario | Número de póliza actual (si aplica) |
| `[11]` | `aseguradora_actual` | Manual | Usuario | Aseguradora actual del cliente |
| `[12]` | `tasa_interes` | Manual | Usuario | Tasa de interés mensual (%) para cálculo de cuotas |
| `[13]` | `comentarios` | Manual | Usuario | Comentarios o condiciones especiales |

---

## 3. Valores del Bien (Avalúo Comercial)

Valores de avalúo comercial prellenados desde la base de datos.

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[14]` | `valor_contenidos_normales_avaluo` | BD | otros_bienes.valor_contenidos_normales_avaluo | Valor de contenidos normales |
| `[15]` | `valor_contenidos_especiales_avaluo` | BD | otros_bienes.valor_contenidos_especiales_avaluo | Valor de contenidos especiales |
| `[16]` | `valor_equipo_electronico_avaluo` | BD | otros_bienes.valor_equipo_electronico_avaluo | Valor de equipos electrónicos |
| `[17]` | `valor_total_avaluo` | Calculado | [14] + [15] + [16] | Valor total del avalúo |

**Formato:** COP con separadores de miles (ej: `50.000.000`)

---

## 4. Valores Asegurados

Valores asegurados configurados en la póliza (pueden ser menores o iguales al avalúo).

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[18]` | `valor_asegurado_cn` | BD | polizas.valor_asegurado_cn | Valor asegurado de contenidos normales |
| `[19]` | `valor_asegurado_ce` | BD | polizas.valor_asegurado_ce | Valor asegurado de contenidos especiales |
| `[20]` | `valor_asegurado_ee` | BD | polizas.valor_asegurado_ee | Valor asegurado de equipo electrónico |
| `[21]` | `valor_rc_asegurado` | BD | polizas.valor_asegurado_rc | Valor asegurado de responsabilidad civil |
| `[22]` | `valor_total_asegurado` | Calculado | [18] + [19] + [20] | Valor total asegurado |

**Formato:** COP con separadores de miles (ej: `45.000.000`)

---

## 5. Infraseguro (%)

Porcentaje de infraseguro calculado automáticamente como: `(Valor Asegurado / Valor Avalúo) × 100`

| Código | Nombre Variable | Tipo | Descripción |
|--------|----------------|------|-------------|
| `[23]` | `infraseg_cn` | Calculado | % infraseguro de contenidos normales |
| `[24]` | `infraseg_ce` | Calculado | % infraseguro de contenidos especiales |
| `[25]` | `infraseg_ee` | Calculado | % infraseguro de equipo electrónico |
| `[26]` | `infraseg_total` | Calculado | % infraseguro total |

**Formato:** Porcentaje con 2 decimales (ej: `90.00%`, `100.00%`)

---

## 6. Configuración por Aseguradora

Cada aseguradora tiene **15 campos configurables**. El sistema soporta hasta **3 aseguradoras** simultáneas (a diferencia de Hogar y Vehículos que soportan 5).

### 6.1 Estructura de Campos (igual para las 3 aseguradoras)

#### Campos Generales (5 campos)

| Offset | Nombre Variable | Descripción |
|--------|----------------|-------------|
| `+0` | `nombre_aseg_N` | Nombre de la aseguradora |
| `+1` | `pais_origen_aseg_N` | Ruta de la bandera del país de origen |
| `+2` | `respaldo_aseg_N` | Texto de respaldo o "Compañía Internacional" |
| `+3` | `valor_prima_aseg_N` | Prima anual (COP con separadores) |
| `+4` | `valor_total_anual_aseg_N` | Total anual (igual a prima) |

#### Deducibles de Daños (3 campos)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+5` | `otr_deducible_terremoto_aseg_N` | Deducible por terremoto | `10% Valor asegurable Mín $500.000` |
| `+6` | `otr_deducible_amit_aseg_N` | Deducible por AMIT | `10% Valor asegurable Mín $500.000` |
| `+7` | `otr_deducible_demas_eventos_aseg_N` | Deducible otros eventos | `5% Valor asegurable Mín $300.000` |

#### Deducibles de Hurto (3 campos)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+8` | `otr_hurto_cn_deducible_aseg_N` | Deducible hurto contenidos normales | `10% Valor asegurable Mín $500.000` |
| `+9` | `otr_hurto_ce_deducible_aseg_N` | Deducible hurto contenidos especiales | `10% Valor asegurable Mín $500.000` |
| `+10` | `otr_hurto_ee_deducible_aseg_N` | Deducible hurto equipo electrónico | `10% Valor asegurable Mín $500.000` |

#### Coberturas Adicionales (3 campos)

| Offset | Nombre Variable | Descripción |
|--------|----------------|-------------|
| `+11` | `otr_cobertura_adicional_1_aseg_N` | Cobertura adicional 1 (texto libre) |
| `+12` | `otr_cobertura_adicional_2_aseg_N` | Cobertura adicional 2 (texto libre) |
| `+13` | `otr_cobertura_adicional_3_aseg_N` | Cobertura adicional 3 (texto libre) |

#### Observaciones (1 campo)

| Offset | Nombre Variable | Descripción |
|--------|----------------|-------------|
| `+14` | `otr_observaciones_aseg_N` | Observaciones generales de la aseguradora |

---

### 6.2 Tabla de Offsets por Aseguradora

| Aseguradora | Código Inicio | Código Fin | Campos |
|-------------|---------------|------------|--------|
| **Aseguradora 1** | `[27]` | `[41]` | 15 |
| **Aseguradora 2** | `[42]` | `[56]` | 15 |
| **Aseguradora 3** | `[57]` | `[71]` | 15 |

**Fórmula de offset:** `offset_base + campo_relativo`  
**Ejemplo:** Campo "otr_deducible_terremoto" de Aseguradora 2 = `[42]` + 5 = `[47]`

⚠️ **Nota:** Otros solo soporta 3 aseguradoras (vs 5 en Hogar y Vehículos)

---

### 6.3 Mapeo Completo por Aseguradora

#### Aseguradora 1: `[27]` - `[41]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[27]` | `nombre_aseg_1` | Nombre de la aseguradora |
| `[28]` | `pais_origen_aseg_1` | Ruta bandera país |
| `[29]` | `respaldo_aseg_1` | Respaldo internacional |
| `[30]` | `valor_prima_aseg_1` | Prima anual (COP) |
| `[31]` | `valor_total_anual_aseg_1` | Total anual (COP) |
| `[32]` | `otr_deducible_terremoto_aseg_1` | Deducible terremoto |
| `[33]` | `otr_deducible_amit_aseg_1` | Deducible AMIT |
| `[34]` | `otr_deducible_demas_eventos_aseg_1` | Deducible demás eventos |
| `[35]` | `otr_hurto_cn_deducible_aseg_1` | Deducible hurto CN |
| `[36]` | `otr_hurto_ce_deducible_aseg_1` | Deducible hurto CE |
| `[37]` | `otr_hurto_ee_deducible_aseg_1` | Deducible hurto EE |
| `[38]` | `otr_cobertura_adicional_1_aseg_1` | Cobertura adicional 1 |
| `[39]` | `otr_cobertura_adicional_2_aseg_1` | Cobertura adicional 2 |
| `[40]` | `otr_cobertura_adicional_3_aseg_1` | Cobertura adicional 3 |
| `[41]` | `otr_observaciones_aseg_1` | Observaciones |

#### Aseguradora 2: `[42]` - `[56]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[42]` | `nombre_aseg_2` | Nombre de la aseguradora |
| `[43]` | `pais_origen_aseg_2` | Ruta bandera país |
| `[44]` | `respaldo_aseg_2` | Respaldo internacional |
| `[45]` | `valor_prima_aseg_2` | Prima anual (COP) |
| `[46]` | `valor_total_anual_aseg_2` | Total anual (COP) |
| `[47]` | `otr_deducible_terremoto_aseg_2` | Deducible terremoto |
| `[48]` | `otr_deducible_amit_aseg_2` | Deducible AMIT |
| `[49]` | `otr_deducible_demas_eventos_aseg_2` | Deducible demás eventos |
| `[50]` | `otr_hurto_cn_deducible_aseg_2` | Deducible hurto CN |
| `[51]` | `otr_hurto_ce_deducible_aseg_2` | Deducible hurto CE |
| `[52]` | `otr_hurto_ee_deducible_aseg_2` | Deducible hurto EE |
| `[53]` | `otr_cobertura_adicional_1_aseg_2` | Cobertura adicional 1 |
| `[54]` | `otr_cobertura_adicional_2_aseg_2` | Cobertura adicional 2 |
| `[55]` | `otr_cobertura_adicional_3_aseg_2` | Cobertura adicional 3 |
| `[56]` | `otr_observaciones_aseg_2` | Observaciones |

#### Aseguradora 3: `[57]` - `[71]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[57]` | `nombre_aseg_3` | Nombre de la aseguradora |
| `[58]` | `pais_origen_aseg_3` | Ruta bandera país |
| `[59]` | `respaldo_aseg_3` | Respaldo internacional |
| `[60]` | `valor_prima_aseg_3` | Prima anual (COP) |
| `[61]` | `valor_total_anual_aseg_3` | Total anual (COP) |
| `[62]` | `otr_deducible_terremoto_aseg_3` | Deducible terremoto |
| `[63]` | `otr_deducible_amit_aseg_3` | Deducible AMIT |
| `[64]` | `otr_deducible_demas_eventos_aseg_3` | Deducible demás eventos |
| `[65]` | `otr_hurto_cn_deducible_aseg_3` | Deducible hurto CN |
| `[66]` | `otr_hurto_ce_deducible_aseg_3` | Deducible hurto CE |
| `[67]` | `otr_hurto_ee_deducible_aseg_3` | Deducible hurto EE |
| `[68]` | `otr_cobertura_adicional_1_aseg_3` | Cobertura adicional 1 |
| `[69]` | `otr_cobertura_adicional_2_aseg_3` | Cobertura adicional 2 |
| `[70]` | `otr_cobertura_adicional_3_aseg_3` | Cobertura adicional 3 |
| `[71]` | `otr_observaciones_aseg_3` | Observaciones |

---

## 7. Formato de Deducibles

Los deducibles se almacenan en BD como string separado por comas: `"porcentaje,tipo,minimo"`

**Ejemplo de almacenamiento:**  
```
"10,Valor asegurable,500000"
```

**Formato de salida en propuesta:**  
```
10% Valor asegurable Mín $500.000
```

**Componentes:**
1. **Porcentaje:** Número entero o decimal (ej: `10`, `15.5`)
2. **Tipo:** Texto libre (ej: `Valor asegurable`, `Valor declarado`, `Por evento`)
3. **Mínimo:** Valor monetario en COP sin separadores (ej: `500000`)

---

## 8. Diferencias con Otros Rubros

### Características Distintivas de Otros

1. **Solo 3 Aseguradoras:** A diferencia de Hogar y Vehículos (5 aseguradoras)
2. **15 Campos por Aseguradora:** Menos que Vehículos (26) pero similar a Hogar (17)
3. **Sin Sublímites RC:** A diferencia de Vehículos que incluye 4 sublímites
4. **3 Coberturas Adicionales:** Igual que Hogar, menos que Vehículos (7)
5. **Deducibles Simplificados:** Solo 6 deducibles vs 8 en Hogar o 11 en Vehículos

### Comparación de Complejidad

| Rubro | Aseguradoras | Campos/Aseg | Variables Totales | Complejidad |
|-------|--------------|-------------|-------------------|-------------|
| **Otros** | 3 | 15 | 71 | ⭐ Baja |
| **Hogar** | 5 | 17 | 115 | ⭐⭐ Media |
| **Vehículos** | 5 | 26 | 155 | ⭐⭐⭐ Alta |

---

## 9. Tipos de Seguro Soportados

El campo `tipo_seguro` (`[5]`) puede incluir:

- Equipo Electrónico
- Maquinaria y Equipo
- Herramientas
- Equipos Médicos
- Equipos de Cómputo
- Otros Activos

**Origen:** Base de datos (`otros_bienes.tipo_seguro`)

---

## 10. Ejemplos de Uso

### Ejemplo 1: Datos Básicos del Cliente y Bien
```json
{
  "[3]": "Empresa ABC S.A.S.",
  "[4]": "900.123.456-7",
  "[5]": "Equipo Electrónico",
  "[6]": "Servidores HP ProLiant DL380 Gen10",
  "[7]": "2 servidores en rack, con garantía extendida",
  "[8]": "Bogotá"
}
```

### Ejemplo 2: Avalúos y Valores Asegurados
```json
{
  "[14]": "30.000.000",
  "[15]": "10.000.000",
  "[16]": "20.000.000",
  "[17]": "60.000.000",
  "[18]": "28.000.000",
  "[19]": "9.000.000",
  "[20]": "18.000.000",
  "[22]": "55.000.000"
}
```

### Ejemplo 3: Deducibles Aseguradora 1
```json
{
  "[32]": "10% Valor asegurable Mín $500.000",
  "[33]": "10% Valor asegurable Mín $500.000",
  "[34]": "5% Valor asegurable Mín $300.000",
  "[35]": "10% Valor asegurable Mín $500.000",
  "[36]": "10% Valor asegurable Mín $500.000",
  "[37]": "10% Valor asegurable Mín $500.000"
}
```

---

## 11. Origen de Datos

### Base de Datos
- **usuarios:** Información del cliente (nombre, NIT, ciudad)
- **otros_bienes:** Detalles del bien (tipo, descripción, detalles, avalúos)
- **polizas:** Valores asegurados y configuración de póliza
- **aseguradoras:** Valores por defecto de deducibles y coberturas

### Calculados Automáticamente
- Fecha de expedición (fecha actual)
- Año de vigencia (año actual - año siguiente)
- Valor total avalúo (CN + CE + EE)
- Valor total asegurado (CN + CE + EE)
- Infraseguro (porcentaje según fórmula)

### Editables por Usuario
- Campos manuales de encabezado (asesor, póliza actual, tasa interés, comentarios)
- Coberturas y deducibles editables por aseguradora (inicializados desde BD pero modificables)

---

## 12. Validaciones

### Campos Obligatorios
- `[9]` asesor (requerido para generar propuesta)
- `[12]` tasa_interes (requerido para cálculo de cuotas)
- `[5]` tipo_seguro (identificación del tipo de bien)
- `[6]` bien_asegurado (descripción del bien)

### Campos Opcionales
- Todos los deducibles pueden estar vacíos
- Coberturas adicionales son opcionales
- Observaciones son opcionales
- Detalles del bien son opcionales

### Formato de Valores
- **Valores monetarios:** Sin decimales, con separadores de miles en salida
- **Porcentajes:** Con 2 decimales máximo
- **Deducibles:** Validar estructura "porcentaje,tipo,minimo"

---

## 13. Cálculo de Cuotas

El sistema incluye cálculo de cuotas con interés compuesto utilizando la fórmula de amortización:

```
cuota = prima × ((tasa × (1 + tasa)^n) / ((1 + tasa)^n - 1))
```

Donde:
- **prima:** Valor de la prima anual
- **tasa:** Tasa de interés mensual (ej: 0.025 para 2.5%)
- **n:** Número de cuotas (típicamente 5, 8, 11 cuotas)

---

## 14. SECCIÓN ENTREGA: Datos de Póliza Vigente `[517]-[528]`

Estas variables solo tienen valor cuando la póliza está en estado **VIGENTE** (luego de completar la entrega). Se usan exclusivamente en el template de entrega.

> Los campos de financiación solo aplican cuando `[522]` = `financiera`.

| Variable | Campo | Descripción |
|----------|-------|-------------|
| `[517]` | nombre_aseguradora | Nombre de la aseguradora elegida |
| `[518]` | numero_poliza | Número de póliza asignado por la aseguradora |
| `[519]` | fecha_inicio_vigencia | Fecha inicio de vigencia (ej: "1 de enero 2026") |
| `[520]` | fecha_fin_vigencia | Fecha fin de vigencia (ej: "1 de enero 2027") |
| `[521]` | valor_total_prima | Prima total pactada (con separadores de miles) |
| `[522]` | medio_pago | Forma de pago: `contado` o `financiera` |
| `[523]` | numeral_asistencia | Numeral de asistencia de la aseguradora elegida |
| `[524]` | financiacion_num_cuotas | Número de cuotas del plan (3, 5, 8 u 11) |
| `[525]` | financiacion_valor_cuota | Valor de cada cuota (con separadores de miles) |
| `[526]` | financiacion_fecha_primera | Fecha de la primera cuota (ej: "15 de marzo 2026") |
| `[527]` | financiacion_periodicidad | Periodicidad: `mensual`, `bimestral`, `trimestral` |
| `[528]` | financiacion_cuota_actual | Número de cuota actual (ej: 1) |

---

## 15. Referencias

- **Archivo TypeScript:** `frontend/src/lib/data/diccionario_campos_otros.ts`
- **Página de Generación:** `frontend/src/routes/propuestas/otro/[id]/generar/+page.svelte`
- **Modelo Backend:** `backend/app/models/aseguradora.py` (campos `otr_*`)
- **Plantilla Excel:** `propuesta_otros.xlsx` (debe existir en carpeta de templates)

---

**Última Actualización:** Marzo 2026  
**Versión:** 1.0  
**Autor:** Alfabroker Admin System
