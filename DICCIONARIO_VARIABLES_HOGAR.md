# Diccionario de Variables para Propuestas de Hogar

Este documento describe todas las variables utilizadas en las propuestas de seguros de **Hogar**. Las variables se reemplazan en la plantilla Excel `propuesta_hogar.xlsx` para generar cotizaciones personalizadas.

## Estructura General

El diccionario mapea códigos compactos `[N]` a nombres descriptivos de campos. El sistema soporta hasta **5 aseguradoras** por propuesta, cada una con 17 campos configurables.

**Total de variables:** 115 campos  
- **Campos generales:** 30 (encabezado, cliente, avalúos, asegurados, infraseguro)
- **Por aseguradora:** 17 campos × 5 = 85 campos

---

## 1. Encabezado del Documento

Variables calculadas automáticamente al momento de generar la propuesta.

| Código | Nombre Variable | Tipo | Descripción | Ejemplo |
|--------|----------------|------|-------------|---------|
| `[1]` | `fecha_expedicion` | Calculado | Fecha actual en formato "DD de mes YYYY" | `18 de marzo 2026` |
| `[2]` | `año_vigencia` | Calculado | Año de vigencia en formato "YYYY-YYYY" | `2026-2027` |

---

## 2. Datos del Cliente e Inmueble

Campos prellenados desde la base de datos (usuarios + hogares) y editables manualmente.

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[3]` | `nombre_cliente` | BD | usuarios.nombre / razon_social | Nombre del cliente o razón social |
| `[4]` | `nit` | BD | usuarios.nit / numero_documento | Identificación del cliente |
| `[5]` | `tipo_inmueble` | BD | hogares.tipo_inmueble | Casa, Apartamento, Finca |
| `[6]` | `ciudad_inmueble` | BD | hogares.ciudad | Ciudad donde está ubicado el inmueble |
| `[7]` | `direccion_inmueble` | BD | hogares.direccion | Dirección completa del inmueble |
| `[8]` | `numero_pisos` | BD | hogares.numero_pisos | Cantidad de pisos del inmueble |
| `[9]` | `ano_construccion` | BD | hogares.ano_construccion | Año de construcción del inmueble |
| `[10]` | `asesor` | Manual | Usuario | Nombre del asesor que elabora la propuesta |
| `[11]` | `poliza_actual` | Manual | Usuario | Número de póliza actual (si aplica) |
| `[12]` | `aseguradora_actual` | Manual | Usuario | Aseguradora actual del cliente |
| `[13]` | `tasa_interes` | Manual | Usuario | Tasa de interés mensual (%) para cálculo de cuotas |
| `[14]` | `comentarios` | Manual | Usuario | Comentarios o condiciones especiales |

---

## 3. Valores del Bien (Avalúo Comercial)

Valores de avalúo comercial prellenados desde la base de datos.

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[15]` | `valor_inmueble_avaluo` | BD | hogares.valor_inmueble_avaluo | Valor comercial del inmueble |
| `[16]` | `valor_contenidos_normales_avaluo` | BD | hogares.valor_contenidos_normales_avaluo | Valor de contenidos normales |
| `[17]` | `valor_contenidos_especiales_avaluo` | BD | hogares.valor_contenidos_especiales_avaluo | Valor de contenidos especiales (joyas, arte) |
| `[18]` | `valor_equipo_electronico_avaluo` | BD | hogares.valor_equipo_electronico_avaluo | Valor de equipos electrónicos |
| `[19]` | `valor_maquinaria_equipo_avaluo` | BD | hogares.valor_maquinaria_equipo_avaluo | Valor de maquinaria y equipos |

**Formato:** COP con separadores de miles (ej: `150.000.000`)

---

## 4. Valores Asegurados

Valores asegurados configurados en la póliza (pueden ser menores o iguales al avalúo).

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[20]` | `valor_inmueble_asegurado` | BD | polizas.valor_asegurado_inmueble | Valor asegurado del inmueble |
| `[21]` | `valor_contenidos_normales_asegurado` | BD | polizas.valor_asegurado_contenidos_normales | Valor asegurado de contenidos normales |
| `[22]` | `valor_contenidos_especiales_asegurado` | BD | polizas.valor_asegurado_contenidos_especiales | Valor asegurado de contenidos especiales |
| `[23]` | `valor_equipo_electronico_asegurado` | BD | polizas.valor_asegurado_equipo_electronico | Valor asegurado de equipos electrónicos |
| `[24]` | `valor_maquinaria_equipo_asegurado` | BD | polizas.valor_asegurado_maquinaria | Valor asegurado de maquinaria y equipos |
| `[25]` | `valor_rc_asegurado` | BD | polizas.valor_asegurado_rc | Valor asegurado de responsabilidad civil |

**Formato:** COP con separadores de miles (ej: `120.000.000`)

---

## 5. Infraseguro (%)

Porcentaje de infraseguro calculado automáticamente como: `(Valor Asegurado / Valor Avalúo) × 100`

| Código | Nombre Variable | Tipo | Descripción |
|--------|----------------|------|-------------|
| `[26]` | `infraseg_inmueble` | Calculado | % infraseguro del inmueble |
| `[27]` | `infraseg_contenidos_normales` | Calculado | % infraseguro de contenidos normales |
| `[28]` | `infraseg_contenidos_especiales` | Calculado | % infraseguro de contenidos especiales |
| `[29]` | `infraseg_equipo_electronico` | Calculado | % infraseguro de equipos electrónicos |
| `[30]` | `infraseg_maquinaria` | Calculado | % infraseguro de maquinaria y equipos |

**Formato:** Porcentaje con 2 decimales (ej: `85.50%`, `100.00%`)

---

## 6. Configuración por Aseguradora

Cada aseguradora tiene **17 campos configurables**. El sistema soporta hasta 5 aseguradoras simultáneas.

### 6.1 Estructura de Campos (igual para las 5 aseguradoras)

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
| `+5` | `hog_deducible_terremoto_aseg_N` | Deducible por terremoto | `10% Valor asegurable Mín $500.000` |
| `+6` | `hog_deducible_amit_aseg_N` | Deducible por AMIT | `10% Valor asegurable Mín $500.000` |
| `+7` | `hog_deducible_demas_eventos_aseg_N` | Deducible otros eventos | `10% Valor asegurable Mín $500.000` |

#### Deducibles Hurto Contenidos Normales (3 campos)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+8` | `hog_hurto_cn_terremoto_aseg_N` | Deducible hurto CN por terremoto | `10% Valor asegurable Mín $500.000` |
| `+9` | `hog_hurto_cn_demas_eventos_aseg_N` | Deducible hurto CN otros eventos | `10% Valor asegurable Mín $500.000` |
| `+10` | `hog_hurto_cn_hurto_aseg_N` | Deducible hurto CN por hurto | `10% Valor asegurable Mín $500.000` |

#### Deducibles Hurto Contenidos Especiales (1 campo)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+11` | `hog_hurto_ce_hurto_aseg_N` | Deducible hurto CE por hurto | `10% Valor asegurable Mín $500.000` |

#### Deducibles Hurto Equipo Electrónico (1 campo)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+12` | `hog_hurto_ee_hurto_aseg_N` | Deducible hurto EE por hurto | `10% Valor asegurable Mín $500.000` |

#### Coberturas Adicionales (3 campos)

| Offset | Nombre Variable | Descripción |
|--------|----------------|-------------|
| `+13` | `hog_cobertura_adicional_1_aseg_N` | Cobertura adicional 1 (texto libre) |
| `+14` | `hog_cobertura_adicional_2_aseg_N` | Cobertura adicional 2 (texto libre) |
| `+15` | `hog_cobertura_adicional_3_aseg_N` | Cobertura adicional 3 (texto libre) |

#### Observaciones (1 campo)

| Offset | Nombre Variable | Descripción |
|--------|----------------|-------------|
| `+16` | `hog_observaciones_aseg_N` | Observaciones generales de la aseguradora |

---

### 6.2 Tabla de Offsets por Aseguradora

| Aseguradora | Código Inicio | Código Fin | Campos |
|-------------|---------------|------------|--------|
| **Aseguradora 1** | `[31]` | `[47]` | 17 |
| **Aseguradora 2** | `[48]` | `[64]` | 17 |
| **Aseguradora 3** | `[65]` | `[81]` | 17 |
| **Aseguradora 4** | `[82]` | `[98]` | 17 |
| **Aseguradora 5** | `[99]` | `[115]` | 17 |

**Fórmula de offset:** `offset_base + campo_relativo`  
**Ejemplo:** Campo "hog_deducible_terremoto" de Aseguradora 3 = `[65]` + 5 = `[70]`

---

### 6.3 Mapeo Completo por Aseguradora

#### Aseguradora 1: `[31]` - `[47]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[31]` | `nombre_aseg_1` | Nombre de la aseguradora |
| `[32]` | `pais_origen_aseg_1` | Ruta bandera país |
| `[33]` | `respaldo_aseg_1` | Respaldo internacional |
| `[34]` | `valor_prima_aseg_1` | Prima anual (COP) |
| `[35]` | `valor_total_anual_aseg_1` | Total anual (COP) |
| `[36]` | `hog_deducible_terremoto_aseg_1` | Deducible terremoto |
| `[37]` | `hog_deducible_amit_aseg_1` | Deducible AMIT |
| `[38]` | `hog_deducible_demas_eventos_aseg_1` | Deducible demás eventos |
| `[39]` | `hog_hurto_cn_terremoto_aseg_1` | Hurto CN - terremoto |
| `[40]` | `hog_hurto_cn_demas_eventos_aseg_1` | Hurto CN - demás eventos |
| `[41]` | `hog_hurto_cn_hurto_aseg_1` | Hurto CN - hurto |
| `[42]` | `hog_hurto_ce_hurto_aseg_1` | Hurto CE - hurto |
| `[43]` | `hog_hurto_ee_hurto_aseg_1` | Hurto EE - hurto |
| `[44]` | `hog_cobertura_adicional_1_aseg_1` | Cobertura adicional 1 |
| `[45]` | `hog_cobertura_adicional_2_aseg_1` | Cobertura adicional 2 |
| `[46]` | `hog_cobertura_adicional_3_aseg_1` | Cobertura adicional 3 |
| `[47]` | `hog_observaciones_aseg_1` | Observaciones |

#### Aseguradoras 2-5: Mismo Patrón

Las aseguradoras 2, 3, 4 y 5 siguen **exactamente la misma estructura** con diferentes offsets base:

- **Aseguradora 2:** Reemplazar `[31-47]` por `[48-64]` y `_aseg_1` por `_aseg_2`
- **Aseguradora 3:** Reemplazar `[31-47]` por `[65-81]` y `_aseg_1` por `_aseg_3`
- **Aseguradora 4:** Reemplazar `[31-47]` por `[82-98]` y `_aseg_1` por `_aseg_4`
- **Aseguradora 5:** Reemplazar `[31-47]` por `[99-115]` y `_aseg_1` por `_aseg_5`

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

## 8. Ejemplos de Uso

### Ejemplo 1: Datos Básicos del Cliente
```json
{
  "[3]": "Juan Pérez García",
  "[4]": "900.123.456",
  "[5]": "Apartamento",
  "[6]": "Bogotá",
  "[7]": "Calle 100 # 15-20 Apto 501"
}
```

### Ejemplo 2: Avalúos y Valores Asegurados
```json
{
  "[15]": "250.000.000",
  "[16]": "50.000.000",
  "[20]": "250.000.000",
  "[21]": "45.000.000"
}
```

### Ejemplo 3: Deducibles de Aseguradora 1
```json
{
  "[36]": "10% Valor asegurable Mín $500.000",
  "[37]": "10% Valor asegurable Mín $500.000",
  "[38]": "5% Valor asegurable Mín $300.000"
}
```

---

## 9. Origen de Datos

### Base de Datos
- **usuarios:** Información del cliente (nombre, NIT, ciudad)
- **hogares:** Detalles del inmueble (tipo, dirección, avalúos)
- **polizas:** Valores asegurados y configuración de póliza
- **aseguradoras:** Valores por defecto de deducibles y coberturas

### Calculados Automáticamente
- Fecha de expedición (fecha actual)
- Año de vigencia (año actual - año siguiente)
- Infraseguro (porcentaje según fórmula)

### Editables por Usuario
- Campos manuales de encabezado (asesor, póliza actual, tasa interés, comentarios)
- Coberturas y deducibles editables por aseguradora (inicializados desde BD pero modificables)

---

## 10. Validaciones

### Campos Obligatorios
- `[10]` asesor (requerido para generar propuesta)
- `[13]` tasa_interes (requerido para cálculo de cuotas)

### Campos Opcionales
- Todos los deducibles pueden estar vacíos
- Coberturas adicionales son opcionales
- Observaciones son opcionales

### Formato de Valores
- **Valores monetarios:** Sin decimales, con separadores de miles en salida
- **Porcentajes:** Con 2 decimales máximo
- **Deducibles:** Validar estructura "porcentaje,tipo,minimo"

---

## 11. SECCIÓN ENTREGA: Datos de Póliza Vigente `[517]-[528]`

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

## 12. Referencias

- **Archivo TypeScript:** `frontend/src/lib/data/diccionario_campos_hogar.ts`
- **Página de Generación:** `frontend/src/routes/propuestas/hogar/[id]/generar/+page.svelte`
- **Modelo Backend:** `backend/app/models/aseguradora.py` (campos `hog_*`)
- **Plantilla Excel:** `propuesta_hogar.xlsx` (debe existir en carpeta de templates)

---

**Última Actualización:** Marzo 2026  
**Versión:** 1.0  
**Autor:** Alfabroker Admin System
