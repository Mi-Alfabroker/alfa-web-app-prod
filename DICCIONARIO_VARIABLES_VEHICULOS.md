# Diccionario de Variables para Propuestas de Vehículos

Este documento describe todas las variables utilizadas en las propuestas de seguros de **Vehículos**. Las variables se reemplazan en la plantilla Excel `propuesta_vehiculos.xlsx` para generar cotizaciones personalizadas.

## Estructura General

El diccionario mapea códigos compactos `[N]` a nombres descriptivos de campos. El sistema soporta hasta **5 aseguradoras** por propuesta, cada una con 26 campos configurables (el más complejo de los 3 rubros).

**Total de variables:** 155 campos  
- **Campos generales:** 25 (encabezado, cliente, vehículo, avalúos, asegurados)
- **Por aseguradora:** 26 campos × 5 = 130 campos

---

## 1. Encabezado del Documento

Variables calculadas automáticamente al momento de generar la propuesta.

| Código | Nombre Variable | Tipo | Descripción | Ejemplo |
|--------|----------------|------|-------------|---------|
| `[1]` | `fecha_expedicion` | Calculado | Fecha actual en formato "DD de mes YYYY" | `18 de marzo 2026` |
| `[2]` | `año_vigencia` | Calculado | Año de vigencia en formato "YYYY-YYYY" | `2026-2027` |

---

## 2. Datos del Cliente y Vehículo

Campos prellenados desde la base de datos (usuarios + vehiculos) y editables manualmente.

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[3]` | `nombre_cliente` | BD | usuarios.nombre / razon_social | Nombre del cliente o razón social |
| `[4]` | `nit` | BD | usuarios.nit / numero_documento | Identificación del cliente |
| `[5]` | `tipo_vehiculo` | BD | vehiculos.tipo_vehiculo | Automóvil, Camioneta, Motocicleta, etc. |
| `[6]` | `marca` | BD | vehiculos.marca | Marca del vehículo (Toyota, Chevrolet, etc.) |
| `[7]` | `ano_modelo` | BD | vehiculos.ano_modelo | Año modelo del vehículo |
| `[8]` | `placa` | BD | vehiculos.placa | Placa del vehículo (formato: ABC123) |
| `[9]` | `codigo_fasecolda` | BD | vehiculos.codigo_fasecolda | Código Fasecolda del vehículo |
| `[10]` | `ciudad_residencia` | BD | usuarios.ciudad_residencia | Ciudad de circulación del vehículo |
| `[11]` | `uso_vehiculo` | BD | polizas.uso_vehiculo | Particular, Servicio Público, Comercial |
| `[12]` | `asesor` | Manual | Usuario | Nombre del asesor que elabora la propuesta |
| `[13]` | `poliza_actual` | Manual | Usuario | Número de póliza actual (si aplica) |
| `[14]` | `aseguradora_actual` | Manual | Usuario | Aseguradora actual del cliente |
| `[15]` | `tasa_interes` | Manual | Usuario | Tasa de interés mensual (%) para cálculo de cuotas |
| `[16]` | `comentarios` | Manual | Usuario | Comentarios o condiciones especiales |

---

## 3. Valores del Bien (Avalúo Comercial)

Valores de avalúo comercial prellenados desde la base de datos.

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[17]` | `valor_vehiculo` | BD | vehiculos.valor_vehiculo | Valor Fasecolda del vehículo |
| `[18]` | `valor_accesorios_avaluo` | BD | vehiculos.valor_accesorios_avaluo | Valor de accesorios adicionales |
| `[19]` | `valor_rc_avaluo` | BD | polizas.valor_rc_avaluo | Valor de responsabilidad civil (avalúo) |
| `[20]` | `valor_total_avaluo` | Calculado | [17] + [18] | Valor total del avalúo (vehículo + accesorios) |
| `[21]` | `ano_modelo_vigencia` | BD | vehiculos.ano_modelo | Año modelo (repetido para vigencia) |

**Formato:** COP con separadores de miles (ej: `85.000.000`)

---

## 4. Valores Asegurados

Valores asegurados configurados en la póliza (pueden ser menores o iguales al avalúo).

| Código | Nombre Variable | Tipo | Origen | Descripción |
|--------|----------------|------|--------|-------------|
| `[22]` | `valor_asegurado_vehiculo` | BD | polizas.valor_asegurado_vehiculo | Valor asegurado del vehículo |
| `[23]` | `valor_asegurado_accesorios` | BD | polizas.valor_asegurado_accesorios | Valor asegurado de accesorios |
| `[24]` | `valor_asegurado_rc` | BD | polizas.valor_asegurado_rc | Valor asegurado de responsabilidad civil |
| `[25]` | `valor_total_asegurado` | Calculado | [22] + [23] | Valor total asegurado (vehículo + accesorios) |

**Formato:** COP con separadores de miles (ej: `80.000.000`)

---

## 5. Configuración por Aseguradora

Cada aseguradora tiene **26 campos configurables** (el más complejo de los 3 rubros). El sistema soporta hasta 5 aseguradoras simultáneas.

### 5.1 Estructura de Campos (igual para las 5 aseguradoras)

#### Campos Generales (5 campos)

| Offset | Nombre Variable | Descripción |
|--------|----------------|-------------|
| `+0` | `nombre_aseg_N` | Nombre de la aseguradora |
| `+1` | `pais_origen_aseg_N` | Ruta de la bandera del país de origen |
| `+2` | `respaldo_aseg_N` | Texto de respaldo o "Compañía Internacional" |
| `+3` | `valor_prima_aseg_N` | Prima anual (COP con separadores) |
| `+4` | `valor_total_anual_aseg_N` | Total anual (igual a prima) |

#### Deducibles de Pérdida (3 campos)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+5` | `veh_deducible_perdida_parcial_aseg_N` | Deducible por pérdida parcial | `10% Valor asegurable Mín $500.000` |
| `+6` | `veh_deducible_perdida_total_aseg_N` | Deducible por pérdida total | `10% Valor asegurable Mín $1.000.000` |
| `+7` | `veh_deducible_terremoto_aseg_N` | Deducible por terremoto | `10% Valor asegurable Mín $1.000.000` |

#### Deducibles de Hurto (2 campos)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+8` | `veh_hurto_perdida_parcial_aseg_N` | Deducible hurto pérdida parcial | `10% Valor asegurable Mín $500.000` |
| `+9` | `veh_hurto_perdida_total_aseg_N` | Deducible hurto pérdida total | `20% Valor asegurable Mín $3.000.000` |

#### Deducible RC (1 campo)

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+10` | `veh_deducible_rc_aseg_N` | Deducible responsabilidad civil | `10% Valor asegurado Mín $500.000` |

#### Sublímites de RC (4 campos) - EXCLUSIVO DE VEHÍCULOS

| Offset | Nombre Variable | Descripción | Formato |
|--------|----------------|-------------|---------|
| `+11` | `veh_rc_sublimite_bienes_terceros_aseg_N` | Sublímite daños a bienes de terceros | `50.000.000` (COP) |
| `+12` | `veh_rc_sublimite_amparo_patrimonial_aseg_N` | Sublímite amparo patrimonial | `100.000.000` (COP) |
| `+13` | `veh_rc_sublimite_muerte_lesion_una_aseg_N` | Sublímite muerte/lesión 1 persona | `200.000.000` (COP) |
| `+14` | `veh_rc_sublimite_muerte_lesion_dos_mas_aseg_N` | Sublímite muerte/lesión 2+ personas | `500.000.000` (COP) |

#### Coberturas Adicionales (7 campos) - CHECKBOXES

| Offset | Nombre Variable | Descripción | Tipo | Valores |
|--------|----------------|-------------|------|---------|
| `+15` | `veh_cobertura_adicional_1_aseg_N` | RC Voluntaria | Boolean | `SI` / `NO` |
| `+16` | `veh_cobertura_adicional_2_aseg_N` | Daños a Ocupantes | Boolean | `SI` / `NO` |
| `+17` | `veh_cobertura_adicional_3_aseg_N` | Asistencia en Viaje | Boolean | `SI` / `NO` |
| `+18` | `veh_cobertura_adicional_4_aseg_N` | Vehículo de Reemplazo | Boolean | `SI` / `NO` |
| `+19` | `veh_cobertura_adicional_5_aseg_N` | Exención Deducible | Boolean | `SI` / `NO` |
| `+20` | `veh_cobertura_adicional_6_aseg_N` | Accidentes Personales Conductor | Boolean | `SI` / `NO` |
| `+21` | `veh_cobertura_adicional_7_aseg_N` | Eventos de la Naturaleza | Boolean | `SI` / `NO` |

#### Campos Adicionales (4 campos)

| Offset | Nombre Variable | Descripción |
|--------|----------------|-------------|
| `+22` | `veh_observaciones_aseg_N` | Observaciones generales de la aseguradora |
| `+23` | `veh_asistencia_tipo_aseg_N` | Tipo de asistencia (ej: "Nacional 24/7") |
| `+24` | `veh_conductor_elegido_aseg_N` | Nombre del conductor elegido |
| `+25` | `veh_beneficiario_adicional_aseg_N` | Nombre del beneficiario adicional |

---

### 5.2 Tabla de Offsets por Aseguradora

| Aseguradora | Código Inicio | Código Fin | Campos |
|-------------|---------------|------------|--------|
| **Aseguradora 1** | `[26]` | `[51]` | 26 |
| **Aseguradora 2** | `[52]` | `[77]` | 26 |
| **Aseguradora 3** | `[78]` | `[103]` | 26 |
| **Aseguradora 4** | `[104]` | `[129]` | 26 |
| **Aseguradora 5** | `[130]` | `[155]` | 26 |

**Fórmula de offset:** `offset_base + campo_relativo`  
**Ejemplo:** Campo "veh_deducible_perdida_parcial" de Aseguradora 3 = `[78]` + 5 = `[83]`

---

### 5.3 Mapeo Completo Aseguradora 1: `[26]` - `[51]`

| Código | Variable | Descripción |
|--------|----------|-------------|
| `[26]` | `nombre_aseg_1` | Nombre de la aseguradora |
| `[27]` | `pais_origen_aseg_1` | Ruta bandera país |
| `[28]` | `respaldo_aseg_1` | Respaldo internacional |
| `[29]` | `valor_prima_aseg_1` | Prima anual (COP) |
| `[30]` | `valor_total_anual_aseg_1` | Total anual (COP) |
| `[31]` | `veh_deducible_perdida_parcial_aseg_1` | Deducible pérdida parcial |
| `[32]` | `veh_deducible_perdida_total_aseg_1` | Deducible pérdida total |
| `[33]` | `veh_deducible_terremoto_aseg_1` | Deducible terremoto |
| `[34]` | `veh_hurto_perdida_parcial_aseg_1` | Deducible hurto parcial |
| `[35]` | `veh_hurto_perdida_total_aseg_1` | Deducible hurto total |
| `[36]` | `veh_deducible_rc_aseg_1` | Deducible RC |
| `[37]` | `veh_rc_sublimite_bienes_terceros_aseg_1` | Sublímite bienes terceros (COP) |
| `[38]` | `veh_rc_sublimite_amparo_patrimonial_aseg_1` | Sublímite amparo patrimonial (COP) |
| `[39]` | `veh_rc_sublimite_muerte_lesion_una_aseg_1` | Sublímite muerte/lesión 1 persona (COP) |
| `[40]` | `veh_rc_sublimite_muerte_lesion_dos_mas_aseg_1` | Sublímite muerte/lesión 2+ personas (COP) |
| `[41]` | `veh_cobertura_adicional_1_aseg_1` | RC Voluntaria (SI/NO) |
| `[42]` | `veh_cobertura_adicional_2_aseg_1` | Daños Ocupantes (SI/NO) |
| `[43]` | `veh_cobertura_adicional_3_aseg_1` | Asistencia Viaje (SI/NO) |
| `[44]` | `veh_cobertura_adicional_4_aseg_1` | Vehículo Reemplazo (SI/NO) |
| `[45]` | `veh_cobertura_adicional_5_aseg_1` | Exención Deducible (SI/NO) |
| `[46]` | `veh_cobertura_adicional_6_aseg_1` | Accidentes Conductor (SI/NO) |
| `[47]` | `veh_cobertura_adicional_7_aseg_1` | Eventos Naturaleza (SI/NO) |
| `[48]` | `veh_observaciones_aseg_1` | Observaciones |
| `[49]` | `veh_asistencia_tipo_aseg_1` | Tipo de asistencia |
| `[50]` | `veh_conductor_elegido_aseg_1` | Conductor elegido |
| `[51]` | `veh_beneficiario_adicional_aseg_1` | Beneficiario adicional |

#### Aseguradoras 2-5: Mismo Patrón

Las aseguradoras 2, 3, 4 y 5 siguen **exactamente la misma estructura** con diferentes offsets base:

- **Aseguradora 2:** Reemplazar `[26-51]` por `[52-77]` y `_aseg_1` por `_aseg_2`
- **Aseguradora 3:** Reemplazar `[26-51]` por `[78-103]` y `_aseg_1` por `_aseg_3`
- **Aseguradora 4:** Reemplazar `[26-51]` por `[104-129]` y `_aseg_1` por `_aseg_4`
- **Aseguradora 5:** Reemplazar `[26-51]` por `[130-155]` y `_aseg_1` por `_aseg_5`

---

## 6. Formato de Deducibles

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

## 7. Formato de Sublímites RC

Los sublímites RC se almacenan como **valores monetarios simples** (string numérico).

**Ejemplo de almacenamiento:**  
```
"50000000"
```

**Formato de salida en propuesta:**  
```
50.000.000
```

**Características:**
- No usan formato de deducible (sin porcentaje ni tipo)
- Se formatean con separadores de miles en la salida
- Valores típicos: 50M, 100M, 200M, 500M COP

---

## 8. Diferencias Clave con Otros Rubros

### Campos Exclusivos de Vehículos

1. **Placa (`[8]`):** Campo único de vehículos
2. **Código Fasecolda (`[9]`):** Identificador único del modelo de vehículo
3. **Sublímites RC (4 campos por aseguradora):** Mayor detalle en cobertura de RC
4. **7 Coberturas Adicionales:** Más coberturas opcionales que Hogar (3) u Otros (3)
5. **Conductor Elegido/Beneficiario:** Campos adicionales no presentes en otros rubros

### Complejidad de Vehículos

- **Hogar:** 17 campos/aseguradora, 115 variables totales
- **Otros:** 15 campos/aseguradora, 71 variables totales
- **Vehículos:** 26 campos/aseguradora, 155 variables totales ⚠️ **MÁS COMPLEJO**

---

## 9. Ejemplos de Uso

### Ejemplo 1: Datos Básicos del Vehículo
```json
{
  "[3]": "María González López",
  "[4]": "52.123.456",
  "[5]": "Automóvil",
  "[6]": "Toyota",
  "[7]": "2023",
  "[8]": "ABC123",
  "[9]": "10456789"
}
```

### Ejemplo 2: Avalúos y Valores Asegurados
```json
{
  "[17]": "85.000.000",
  "[18]": "5.000.000",
  "[19]": "200.000.000",
  "[20]": "90.000.000",
  "[22]": "80.000.000",
  "[23]": "4.500.000",
  "[24]": "200.000.000",
  "[25]": "84.500.000"
}
```

### Ejemplo 3: Deducibles y Sublímites Aseguradora 1
```json
{
  "[31]": "10% Valor asegurable Mín $500.000",
  "[32]": "10% Valor asegurable Mín $1.000.000",
  "[36]": "10% Valor asegurado Mín $500.000",
  "[37]": "50.000.000",
  "[38]": "100.000.000",
  "[39]": "200.000.000",
  "[40]": "500.000.000"
}
```

### Ejemplo 4: Coberturas Adicionales Aseguradora 1
```json
{
  "[41]": "SI",
  "[42]": "SI",
  "[43]": "SI",
  "[44]": "NO",
  "[45]": "NO",
  "[46]": "SI",
  "[47]": "NO"
}
```

---

## 10. Origen de Datos

### Base de Datos
- **usuarios:** Información del cliente (nombre, NIT, ciudad)
- **vehiculos:** Detalles del vehículo (placa, marca, modelo, Fasecolda, avalúo)
- **polizas:** Valores asegurados, uso del vehículo, configuración de póliza
- **aseguradoras:** Valores por defecto de deducibles, sublímites y coberturas

### Calculados Automáticamente
- Fecha de expedición (fecha actual)
- Año de vigencia (año actual - año siguiente)
- Valor total avalúo (vehículo + accesorios)
- Valor total asegurado (vehículo + accesorios)

### Editables por Usuario
- Campos manuales de encabezado (asesor, póliza actual, tasa interés, comentarios)
- Deducibles editables por aseguradora (inicializados desde BD)
- Sublímites RC editables por aseguradora
- Coberturas adicionales (checkboxes SI/NO)
- Información adicional (tipo asistencia, conductor, beneficiario)

---

## 11. Validaciones

### Campos Obligatorios
- `[12]` asesor (requerido para generar propuesta)
- `[15]` tasa_interes (requerido para cálculo de cuotas)
- `[8]` placa (identificación del vehículo)
- `[9]` codigo_fasecolda (referencia Fasecolda)

### Campos Opcionales
- Todos los deducibles pueden estar vacíos
- Sublímites RC son opcionales
- Coberturas adicionales son opcionales (default: NO)
- Campos adicionales (asistencia, conductor, beneficiario) son opcionales

### Formato de Valores
- **Valores monetarios:** Sin decimales, con separadores de miles en salida
- **Deducibles:** Validar estructura "porcentaje,tipo,minimo"
- **Sublímites RC:** Valores numéricos sin formato especial
- **Coberturas adicionales:** Solo "SI" o "NO" (boolean)

---

## 12. Cálculo de Cuotas

El sistema incluye cálculo de cuotas con interés compuesto utilizando la fórmula de amortización:

```
cuota = prima × ((tasa × (1 + tasa)^n) / ((1 + tasa)^n - 1))
```

Donde:
- **prima:** Valor de la prima anual
- **tasa:** Tasa de interés mensual (ej: 0.025 para 2.5%)
- **n:** Número de cuotas (típicamente 5, 8, 11 cuotas)

---

## 13. SECCIÓN ENTREGA: Datos de Póliza Vigente `[517]-[528]`

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

## 14. Referencias

- **Archivo TypeScript:** `frontend/src/lib/data/diccionario_campos_vehiculos.ts`
- **Página de Generación:** `frontend/src/routes/propuestas/vehiculo/[id]/generar/+page.svelte`
- **Modelo Backend:** `backend/app/models/aseguradora.py` (campos `veh_*`)
- **Plantilla Excel:** `propuesta_vehiculos.xlsx` (debe existir en carpeta de templates)

---

**Última Actualización:** Marzo 2026  
**Versión:** 1.0  
**Autor:** Alfabroker Admin System
