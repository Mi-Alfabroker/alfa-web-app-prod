## 1. Backend - Modelo y Migración

- [x] 1.1 Crear migración SQL para agregar 15 columnas nuevas en BasePolizaMixin (nombre_aseguradora, numeral_asistencia, valor_total_prima, medio_pago, estado_cartera, financiacion_num_cuotas, financiacion_cuota_actual, financiacion_valor_cuota, financiacion_fecha_primera_cuota, financiacion_periodicidad, valor_cuota_3, valor_cuota_5, valor_cuota_8, valor_cuota_11, con defaults y nullable)
- [x] 1.2 Agregar CHECK constraint para medio_pago IN ('contado', 'financiera') en migración
- [x] 1.3 Agregar CHECK constraint para estado_cartera IN ('recaudado', 'pendiente', 'cancelado', 'en_solicitud') en migración
- [x] 1.4 Agregar CHECK constraint para financiacion_periodicidad IN ('mensual', 'bimestral', 'trimestral') en migración
- [x] 1.5 Agregar CHECK constraint para financiacion_num_cuotas IN (NULL, 3, 5, 8, 11) en migración
- [x] 1.6 Agregar campos al modelo BasePolizaMixin en backend/app/models/polizas/base_poliza.py
- [x] 1.7 Agregar campos de financiación al método to_base_dict() en BasePolizaMixin
- [ ] 1.8 Ejecutar migración en base de datos de desarrollo y verificar que aplica correctamente en las 4 tablas de pólizas

## 2. Backend - Validaciones y Lógica de Negocio

- [x] 2.1 Crear método validar_entrega_poliza() en BasePolizaMixin con todas las validaciones de specs/poliza-entrega
- [x] 2.2 Agregar validación de rango aseguradora_seleccionada (1-5) en validar_entrega_poliza()
- [x] 2.3 Agregar validación de campos obligatorios (numero_poliza, inicio_vigencia, medio_pago) en validar_entrega_poliza()
- [x] 2.4 Agregar validación condicional: si medio_pago='financiera' requiere financiacion_num_cuotas y financiacion_fecha_primera_cuota
- [x] 2.5 Agregar validación de que id_aseguradora_X no sea NULL para la opción seleccionada
- [x] 2.6 Agregar validación de que valores de cuota existen si se intenta entregar con financiación
- [x] 2.7 Crear método calcular_valor_cuota() estático en BasePolizaMixin usando fórmula de amortización
- [x] 2.8 Agregar validación de financiacion_cuota_actual no excede financiacion_num_cuotas

## 3. Backend - Endpoints de Entrega

- [x] 3.1 Crear endpoint POST /api/polizas/copropiedad/<id>/entregar en blueprint de copropiedades
- [x] 3.2 Crear endpoint POST /api/polizas/hogar/<id>/entregar en blueprint de hogares
- [x] 3.3 Crear endpoint POST /api/polizas/vehiculo/<id>/entregar en blueprint de vehículos
- [x] 3.4 Crear endpoint POST /api/polizas/otro/<id>/entregar en blueprint de otros bienes
- [x] 3.5 Implementar lógica de auto-llenado: consultar aseguradoras.nombre y numeral_asistencia según aseguradora_seleccionada
- [x] 3.6 Implementar lógica de pre-llenado valor_total_prima desde valor_prima_aseg_X
- [x] 3.7 Implementar lógica de copia de valor_cuota_N a financiacion_valor_cuota según financiacion_num_cuotas
- [x] 3.8 Implementar inicialización de financiacion_cuota_actual = 1 y estado_cartera = 'pendiente' para financiera
- [x] 3.9 Implementar transición de estado a VIGENTE después de validaciones exitosas
- [x] 3.10 Agregar logging de evento de entrega con usuario y timestamp

## 4. Backend - Endpoints de Actualización

- [x] 4.1 Crear endpoint PATCH /api/polizas/copropiedad/<id>/actualizar-entrega
- [x] 4.2 Crear endpoint PATCH /api/polizas/hogar/<id>/actualizar-entrega
- [x] 4.3 Crear endpoint PATCH /api/polizas/vehiculo/<id>/actualizar-entrega
- [x] 4.4 Crear endpoint PATCH /api/polizas/otro/<id>/actualizar-entrega
- [x] 4.5 Implementar actualización sin re-validación de transición de estado (solo validar tipos de datos y constraints)
- [x] 4.6 Permitir actualización de financiacion_cuota_actual, estado_cartera, y otros campos editables

## 5. Backend - Endpoint Auxiliar de Aseguradoras

- [x] 5.1 Crear endpoint GET /api/aseguradoras/<id>/datos-entrega en blueprint de aseguradoras
- [x] 5.2 Retornar JSON con nombre, numeral_asistencia, y otros datos relevantes para el formulario de entrega
- [x] 5.3 Manejar caso de aseguradora no encontrada con error 404

## 6. Frontend - Guardar Valores de Cuotas en Propuesta

- [ ] 6.1 Modificar frontend/src/routes/propuestas/copropiedad/[id]/generar/+page.svelte para guardar valores calculados
- [ ] 6.2 Agregar llamada PATCH después de calcular cuotas para actualizar valor_cuota_3, valor_cuota_5, valor_cuota_8, valor_cuota_11 en póliza de copropiedad
- [ ] 6.3 Modificar frontend/src/routes/propuestas/hogar/[id]/generar/+page.svelte para guardar valores calculados
- [ ] 6.4 Agregar llamada PATCH para actualizar valores de cuotas en póliza de hogar
- [ ] 6.5 Modificar frontend/src/routes/propuestas/vehiculo/[id]/generar/+page.svelte para guardar valores calculados
- [ ] 6.6 Agregar llamada PATCH para actualizar valores de cuotas en póliza de vehículo
- [ ] 6.7 Modificar frontend/src/routes/propuestas/otro/[id]/generar/+page.svelte para guardar valores calculados
- [ ] 6.8 Agregar llamada PATCH para actualizar valores de cuotas en póliza de otro bien

## 7. Frontend - Formulario de Entrega

- [ ] 7.1 Crear ruta frontend/src/routes/propuestas/copropiedad/[id]/entregar/+page.svelte
- [ ] 7.2 Crear ruta frontend/src/routes/propuestas/hogar/[id]/entregar/+page.svelte
- [ ] 7.3 Crear ruta frontend/src/routes/propuestas/vehiculo/[id]/entregar/+page.svelte
- [ ] 7.4 Crear ruta frontend/src/routes/propuestas/otro/[id]/entregar/+page.svelte
- [ ] 7.5 Crear componente FormularioEntrega.svelte reutilizable con secciones: Aseguradora, Datos de Póliza, Forma de Pago, Comisión
- [ ] 7.6 Implementar selector de aseguradora (1-5) que dispare auto-llenado de nombre y numeral asistencia
- [ ] 7.7 Implementar campo editable valor_total_prima pre-llenado con valor_prima_aseg_X
- [ ] 7.8 Implementar radio buttons para medio_pago (contado / financiera)
- [ ] 7.9 Implementar sección condicional de financiación (visible solo si medio_pago='financiera')
- [ ] 7.10 Implementar selector de número de cuotas (3, 5, 8, 11) que auto-llene valor_cuota desde valores guardados
- [ ] 7.11 Implementar campo de fecha para financiacion_fecha_primera_cuota
- [ ] 7.12 Implementar validaciones de formulario en frontend según specs/poliza-entrega
- [ ] 7.13 Implementar manejo de errores y mensajes de validación del backend
- [ ] 7.14 Implementar botón "Entregar Póliza" que llame a POST /api/polizas/{rubro}/{id}/entregar
- [ ] 7.15 Implementar redirección a vista de detalle de póliza después de entrega exitosa

## 8. Frontend - Vista de Detalle Mejorada

- [ ] 8.1 Modificar frontend/src/routes/polizas/copropiedad/[id]/+page.svelte para mostrar información de entrega
- [ ] 8.2 Modificar frontend/src/routes/polizas/hogar/[id]/+page.svelte para mostrar información de entrega
- [ ] 8.3 Modificar frontend/src/routes/polizas/vehiculo/[id]/+page.svelte para mostrar información de entrega
- [ ] 8.4 Modificar frontend/src/routes/polizas/otro/[id]/+page.svelte para mostrar información de entrega
- [ ] 8.5 Crear componente SeccionEntrega.svelte que muestre: aseguradora, vigencia, valores, financiación, estado de cartera
- [ ] 8.6 Implementar lógica condicional: mostrar SeccionEntrega como sección principal solo si estado='VIGENTE'
- [ ] 8.7 Implementar cálculo de "próximo pago" en frontend: financiacion_fecha_primera_cuota + (financiacion_cuota_actual - 1) meses
- [ ] 8.8 Implementar indicador visual de estado_cartera con colores (recaudado=verde, pendiente=amarillo, cancelado=rojo, en_solicitud=azul)
- [ ] 8.9 Agregar botón "Editar Entrega" que permita actualizar campos vía PATCH /api/polizas/{rubro}/{id}/actualizar-entrega

## 9. Frontend - Componente de Administración de Financiación

- [ ] 9.1 Crear componente GestionFinanciacion.svelte editable para pólizas vigentes
- [ ] 9.2 Implementar campo editable para financiacion_cuota_actual con incremento/decremento
- [ ] 9.3 Implementar selector editable para estado_cartera
- [ ] 9.4 Implementar botón "Guardar Cambios" que llame a PATCH /api/polizas/{rubro}/{id}/actualizar-entrega
- [ ] 9.5 Mostrar resumen: "Cuota 3 de 8 - Próximo pago: 01/06/2026"

## 10. Testing Backend

- [ ] 10.1 Crear tests unitarios para validar_entrega_poliza() con casos exitosos y de error
- [ ] 10.2 Crear tests unitarios para calcular_valor_cuota() con diferentes valores de prima, tasa, y num_cuotas
- [ ] 10.3 Crear tests de integración para POST /api/polizas/{rubro}/{id}/entregar con datos válidos
- [ ] 10.4 Crear tests de integración para validaciones de entrega (aseguradora no seleccionada, campos faltantes, etc.)
- [ ] 10.5 Crear tests de integración para PATCH /api/polizas/{rubro}/{id}/actualizar-entrega
- [ ] 10.6 Crear tests para GET /api/aseguradoras/{id}/datos-entrega
- [ ] 10.7 Verificar que migración SQL es reversible y no rompe datos existentes

## 11. Testing Frontend

- [ ] 11.1 Probar flujo completo: crear propuesta → generar PDF → verificar valores guardados → entregar → verificar estado VIGENTE
- [ ] 11.2 Probar auto-llenado de datos de aseguradora al cambiar selección
- [ ] 11.3 Probar validaciones de formulario en frontend (campos obligatorios, condicionales)
- [ ] 11.4 Probar que sección de financiación se oculta/muestra según medio_pago
- [ ] 11.5 Probar cálculo de próxima fecha de pago en vista de detalle
- [ ] 11.6 Probar edición de datos de entrega en póliza vigente
- [ ] 11.7 Probar actualización de estado_cartera y financiacion_cuota_actual

## 12. Documentación y Despliegue

- [ ] 12.1 Documentar endpoints nuevos en README o archivo de API docs
- [ ] 12.2 Actualizar ARCHITECTURE.md si aplica con descripción del flujo de entrega
- [ ] 12.3 Crear script de migración para base de datos de producción
- [ ] 12.4 Verificar que todos los campos nuevos tienen valores NULL en pólizas existentes
- [ ] 12.5 Desplegar backend a entorno de staging y verificar
- [ ] 12.6 Desplegar frontend a entorno de staging y verificar
- [ ] 12.7 Realizar prueba end-to-end en staging con usuario de prueba
- [ ] 12.8 Desplegar a producción con plan de rollback preparado
