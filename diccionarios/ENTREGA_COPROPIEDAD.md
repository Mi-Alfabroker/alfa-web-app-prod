# Diccionario de Variables - Entrega Copropiedad

Este documento describe las variables utilizadas para el reemplazo en la plantilla Excel `entrega_copropiedades.xlsx` de entrega de pólizas de copropiedades.

## Formato de Variables

Las variables se definen con el formato `[N]` donde `N` es un número único. Estas variables se reemplazan automáticamente al generar el documento de entrega.

> **Nota:** La entrega reutiliza todas las variables de la propuesta (`[1]`-`[516]`) más las variables específicas de entrega documentadas aquí.

---

## Variables Reutilizadas de Propuesta

La plantilla de entrega incluye los mismos datos de la propuesta original:

- `[1]-[2]`: Encabezado (fecha, año vigencia)
- `[3]-[9]`: Datos del cliente/copropiedad
- `[10]-[19]`: Detalles de la copropiedad
- `[20]-[24]`: Valores del bien (avalúo)
- `[25]-[34]`: Valores asegurados
- `[35]-[39]`: Infraseguro
- `[40]-[494]`: Datos de las 5 aseguradoras
- `[495]-[496]`: Campos calculados
- `[497]-[516]`: Financiación

> Consultar `PROPUESTA_COPROPIEDAD.md` para el detalle completo de estas variables.

---

## SECCIÓN ENTREGA: Datos de Póliza Vigente `[517]-[528]`

Estas variables **solo tienen valor cuando la póliza está en estado VIGENTE** (luego de completar la entrega). Se usan exclusivamente en este template de entrega.

### Datos de la Aseguradora Seleccionada

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[517]` | nombre_aseguradora | BD | Nombre de la aseguradora elegida |
| `[518]` | numero_poliza | Manual | Número de póliza asignado por la aseguradora |
| `[523]` | numeral_asistencia | BD | Numeral de asistencia de la aseguradora elegida |

### Vigencia de la Póliza

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[519]` | fecha_inicio_vigencia | Manual | Fecha inicio de vigencia (ej: "1 de enero 2026") |
| `[520]` | fecha_fin_vigencia | Manual | Fecha fin de vigencia (ej: "1 de enero 2027") |

### Datos Financieros

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[521]` | valor_total_prima | BD | Prima total pactada (con separadores de miles) |
| `[522]` | medio_pago | Manual | Forma de pago: `contado` o `financiera` |

### Financiación (solo si `[522]` = `financiera`)

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[524]` | financiacion_num_cuotas | Manual | Número de cuotas del plan (3, 5, 8 u 11) |
| `[525]` | financiacion_valor_cuota | Calculado | Valor de cada cuota (con separadores de miles) |
| `[526]` | financiacion_fecha_primera | Manual | Fecha de la primera cuota (ej: "15 de marzo 2026") |
| `[527]` | financiacion_periodicidad | Manual | Periodicidad: `mensual`, `bimestral`, `trimestral` |
| `[528]` | financiacion_cuota_actual | Manual | Número de cuota actual (ej: 1) |

---

## Flujo de Datos para la Entrega

```
1. Usuario selecciona número de aseguradora (1-5)
2. Sistema auto-rellena:
   - [517] nombre_aseguradora (desde datos de la aseguradora seleccionada)
   - [521] valor_total_prima (desde valor_prima_aseg_N)
   - [523] numeral_asistencia (desde aseguradora)
3. Usuario completa manualmente:
   - [518] número de póliza
   - [519]-[520] fechas de vigencia
   - [522] medio de pago
4. Si medio_pago = "financiera":
   - [524]-[528] datos de financiación
5. Estado cambia de PROSPECTO → VIGENTE
```

---

## Notas Importantes

1. **Formato de valores monetarios**: Con separadores de miles sin símbolo de moneda
2. **Formato de fecha**: "día de mes año" (ej: "1 de enero 2026")
3. **Medio de pago**: Solo acepta `contado` o `financiera`
4. **Cuotas disponibles**: 3 (sin interés), 5, 8 u 11 (con interés)
5. **Plantilla**: `entrega_copropiedades.xlsx`

---

*Última actualización: Abril 2026*
