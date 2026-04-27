# 🧪 Guía de Testing - Entrega de Pólizas

## ✅ Estado del Sistema

**Migración:** ✓ Ejecutada exitosamente  
**Backend:** ✓ Corriendo en http://localhost:5000  
**Frontend:** ✓ Corriendo en http://localhost:3000  
**Base de Datos:** ✓ Campos agregados a las 4 tablas de pólizas

---

## 📋 Flujo de Prueba Manual

### 1. **Acceder a la aplicación**
```
http://localhost:3000
```
- Iniciar sesión con tus credenciales

### 2. **Crear una póliza de prueba** (si no tienes una)
1. Ir a **Propuestas** → **Nueva Propuesta**
2. Seleccionar tipo de bien (Hogar, Vehículo, Copropiedad, u Otros)
3. Completar información básica
4. Agregar al menos 1 aseguradora con valor de prima
5. Guardar la propuesta

### 3. **Generar PDF de la propuesta** ⭐
1. Abrir la propuesta recién creada
2. Click en **Generar Propuesta**
3. Completar campos requeridos (tasas, coberturas)
4. Click en **Generar PDF**
5. ✓ **Se guardan automáticamente valor_cuota_3, 5, 8, 11**
6. Descargar el PDF generado

### 4. **Entregar la póliza** ⭐ (Nuevo)
1. En la página de detalle de la propuesta, buscar el botón **Entregar Póliza**
2. Click en **Entregar Póliza**
3. Completar el formulario:

   **Sección Aseguradora:**
   - Número de Aseguradora (1-5) → Auto-rellena nombre y numeral
   - Verificar que los datos se completen automáticamente
   - Valor Total Prima (debería pre-llenarse)

   **Sección Datos de la Póliza:**
   - Número de Póliza (ej: POL-2026-001)
   - Fecha Inicio Vigencia (ej: 2026-03-18)
   - Fecha Fin Vigencia (ej: 2027-03-18)

   **Sección Forma de Pago:**
   - Medio de Pago: Seleccionar **Contado** o **Financiera**
   - Estado Cartera: Seleccionar (Recaudado, Pendiente, etc.)
   - Valor Comisión (opcional)

   **Sección Financiación** (solo si seleccionaste "Financiera"):
   - Entidad Financiera (ej: Bancolombia)
   - Periodicidad: Mensual/Semestral/Anual
   - Número de Cuotas: 3/5/8/11
   - Fecha Primera Cuota
   - Cuota Actual (generalmente 1)

4. Click en **Entregar Póliza**

### 5. **Verificar transición de estado** ⭐
1. Deberías ver una notificación de éxito
2. La página debería redirigir al detalle de la póliza
3. **El estado debe cambiar a VIGENTE** (badge verde)
4. **Debe aparecer una nueva sección "Información de Entrega"** al principio

### 6. **Verificar Sección de Entrega** ⭐
La nueva sección debe mostrar:
- ✓ Información de Aseguradora
- ✓ Datos de la Póliza (número, vigencias)
- ✓ Forma de Pago (medio de pago, estado cartera, comisión)
- ✓ **Si es financiera:** Sección de Financiación con:
  - Entidad, periodicidad, número de cuotas
  - Fecha primera cuota, cuota actual
  - **Tarjeta de "Próximo Pago"** con monto y fecha calculada

### 7. **Verificar cálculo de próximo pago** (solo financiera)
Si seleccionaste financiación:
- Verifica que el **Próximo Pago** muestre:
  - Cuota actual correcta
  - Fecha calculada (fecha_primera + meses transcurridos)
  - Monto correcto según el plan (3, 5, 8 u 11 cuotas)

---

## 🔍 Puntos Críticos a Probar

### ✅ Auto-relleno de aseguradora
```
1. Seleccionar "Número de Aseguradora: 1"
2. Verificar que se auto-completen:
   - Nombre Aseguradora
   - Numeral de Asistencia
   - Valor Total Prima
```

### ✅ Validación de campos requeridos
```
1. Intentar enviar formulario vacío
2. Debe mostrar errores de validación
3. Llenar campos requeridos y verificar que se habilite el botón
```

### ✅ Condicional de financiación
```
1. Seleccionar "Medio de Pago: Contado"
   → No debe aparecer sección de financiación
2. Seleccionar "Medio de Pago: Financiera"
   → Debe expandirse sección de financiación automáticamente
```

### ✅ Valores de cuota pre-guardados
```
1. En el backend, verificar que al generar PDF se guardaron los valores:
   docker exec alfabroker-db psql -U admin -d alfabroker -c "SELECT id, consecutivo, valor_cuota_3, valor_cuota_5, valor_cuota_8, valor_cuota_11 FROM polizas_hogar ORDER BY id DESC LIMIT 3;"
   
2. Los valores NO deben ser NULL después de generar el PDF
```

### ✅ Cálculo de cuota con interés
```
Fórmula: cuota = prima * ((r * (1+r)^n) / ((1+r)^n - 1))
Donde: r = tasa mensual (0.023 = 2.3%), n = número de cuotas

Ejemplo con prima $1,000,000 y 5 cuotas:
- valor_cuota_3 = $333,333 (sin interés)
- valor_cuota_5 = $215,472 (con interés 2.3%)
- valor_cuota_8 = $138,826
- valor_cuota_11 = $103,235
```

### ✅ Estado de cartera
```
Verificar colores de badges:
- Recaudado → Verde
- Pendiente → Amarillo
- Cancelado → Rojo
- En Solicitud → Azul
```

---

## 🐛 Escenarios de Error a Probar

### Error 1: Entregar sin generar PDF
```
✓ No debe ser posible (botón solo aparece si hay valores de prima)
```

### Error 2: Seleccionar aseguradora no asignada
```
1. Intentar seleccionar "Aseguradora 5" si la póliza solo tiene 3
2. Debe mostrar notificación de advertencia
```

### Error 3: Entregar póliza ya entregada
```
1. Intentar acceder a /entregar en una póliza VIGENTE
2. Debe redirigir al detalle con error
```

### Error 4: Fechas de vigencia inválidas
```
1. Fecha fin anterior a fecha inicio
2. Backend debe rechazar con error de validación
```

---

## 📊 Verificación de Base de Datos

### Ver pólizas entregadas
```sql
docker exec alfabroker-db psql -U admin -d alfabroker -c "
SELECT 
  id, 
  consecutivo, 
  estado, 
  nombre_aseguradora, 
  numero_poliza,
  medio_pago,
  estado_cartera
FROM polizas_hogar 
WHERE estado = 'VIGENTE' 
ORDER BY id DESC 
LIMIT 5;
"
```

### Ver financiación activa
```sql
docker exec alfabroker-db psql -U admin -d alfabroker -c "
SELECT 
  id,
  consecutivo,
  financiacion_entidad,
  financiacion_num_cuotas,
  financiacion_cuota_actual,
  financiacion_fecha_primera_cuota
FROM polizas_hogar
WHERE medio_pago = 'financiera'
AND estado = 'VIGENTE';
"
```

### Ver valores de cuotas guardados
```sql
docker exec alfabroker-db psql -U admin -d alfabroker -c "
SELECT 
  id,
  consecutivo,
  valor_total_prima,
  valor_cuota_3,
  valor_cuota_5,
  valor_cuota_8,
  valor_cuota_11
FROM polizas_hogar
ORDER BY id DESC
LIMIT 5;
"
```

---

## 🔧 Troubleshooting

### El botón "Entregar Póliza" no aparece
**Causa:** No hay valores de prima asignados  
**Solución:** Edita la póliza y asigna valor a al menos una aseguradora

### Auto-relleno no funciona
**Causa:** Backend no responde o ID de aseguradora inválido  
**Solución:** Verificar logs del backend:
```bash
docker logs alfabroker-api --tail 50
```

### Sección de Entrega no aparece
**Causa:** Estado no es VIGENTE o no tiene numero_poliza  
**Solución:** Verificar estado en base de datos

### Valores de cuota son NULL
**Causa:** No se generó el PDF o hubo error al guardar  
**Solución:** Re-generar el PDF y verificar console.log del frontend

### Frontend no carga
**Solución:**
```bash
cd c:\Striker-dev\Alfabroker-admin-app\frontend
npm install
npm run dev
```

### Backend no responde
**Solución:**
```bash
cd c:\Striker-dev\Alfabroker-admin-app\backend
docker compose up -d
docker logs alfabroker-api
```

---

## ✅ Checklist de Prueba Completa

- [ ] Login exitoso
- [ ] Crear propuesta nueva
- [ ] Asignar aseguradoras con valores
- [ ] Generar PDF exitosamente
- [ ] Verificar valor_cuota_* guardados en DB
- [ ] Ver botón "Entregar Póliza" en detalle
- [ ] Abrir formulario de entrega
- [ ] Auto-relleno funciona al seleccionar aseguradora
- [ ] Validación de campos requeridos funciona
- [ ] Entregar póliza con forma de pago "Contado"
- [ ] Estado cambia a VIGENTE
- [ ] Aparece Sección de Entrega
- [ ] Crear otra propuesta para probar financiación
- [ ] Entregar con forma de pago "Financiera"
- [ ] Sección de financiación se muestra correctamente
- [ ] Tarjeta "Próximo Pago" calcula correctamente
- [ ] Probar los 4 rubros (Hogar, Vehículo, Copropiedad, Otros)
- [ ] Badges de estado_cartera tienen colores correctos
- [ ] Verificar queries SQL funcionan

---

## 📞 Soporte

Si encuentras algún problema:
1. Verificar logs del backend: `docker logs alfabroker-api`
2. Verificar consola del navegador (F12)
3. Verificar estructura de la base de datos
4. Revisar los archivos modificados en el commit

---

**Fecha de testing:** 2026-03-18  
**Versión:** 1.0.0  
**Feature:** Entrega de Pólizas con Financiación
