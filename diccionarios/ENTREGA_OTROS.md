# Diccionario de Variables - Entrega Otros Bienes

Este documento describe las variables para la plantilla `entrega_otro.xlsx`.

> **Nota:** La entrega reutiliza todas las variables de propuesta (`[1]`-`[71]`) más las de entrega. Consultar `PROPUESTA_OTROS.md` (corregido).

---

## SECCIÓN ENTREGA: Datos de Póliza Vigente `[517]-[528]`

Variables exclusivas de la entrega. Solo tienen valor cuando la póliza está en estado **VIGENTE**.

### Datos de la Aseguradora Seleccionada

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[517]` | nombre_aseguradora | BD | Nombre de la aseguradora elegida |
| `[518]` | numero_poliza | Manual | Número de póliza asignado por la aseguradora |
| `[523]` | numeral_asistencia | BD | Numeral de asistencia de la aseguradora elegida |

### Vigencia de la Póliza

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[519]` | fecha_inicio_vigencia | Manual | Fecha inicio (ej: "1 de enero 2026") |
| `[520]` | fecha_fin_vigencia | Manual | Fecha fin (ej: "1 de enero 2027") |

### Datos Financieros

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[521]` | valor_total_prima | BD | Prima total pactada (con separadores de miles) |
| `[522]` | medio_pago | Manual | Forma de pago: `contado` o `financiera` |

### Financiación (solo si `[522]` = `financiera`)

| Variable | Campo | Tipo | Descripción |
|----------|-------|------|-------------|
| `[524]` | financiacion_num_cuotas | Manual | Número de cuotas (3, 5, 8 u 11) |
| `[525]` | financiacion_valor_cuota | Calculado | Valor de cada cuota |
| `[526]` | financiacion_fecha_primera | Manual | Fecha primera cuota |
| `[527]` | financiacion_periodicidad | Manual | `mensual`, `bimestral`, `trimestral` |
| `[528]` | financiacion_cuota_actual | Manual | Número de cuota actual (ej: 1) |

---

## Flujo de Entrega

> ⚠️ En Otros Bienes solo hay 3 aseguradoras (1-3)

1. Seleccionar aseguradora (1-3) → auto-rellena `[517]`, `[521]`, `[523]`
2. Completar `[518]`-`[520]`, `[522]`
3. Si financiera: completar `[524]`-`[528]`
4. Estado cambia PROSPECTO → VIGENTE

**Plantilla:** `entrega_otro.xlsx`

---

*Última actualización: Abril 2026*
