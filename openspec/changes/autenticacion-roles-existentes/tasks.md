## 1. Preparacion y seguridad base

- [ ] 1.1 Definir variables de entorno de seguridad (secretos de firma, expiracion de access token y refresh token) para backend y entornos locales.
- [ ] 1.2 Agregar dependencias necesarias para hashing de password y tokens firmados en backend.
- [ ] 1.3 Documentar contrato de errores de autenticacion/autorizacion (401/403) para uso consistente entre backend y frontend.

## 2. Backend de autenticacion

- [ ] 2.1 Implementar endpoint de login que valide usuario/clave y retorne sesion con contexto de usuario y tipo_usuario.
- [ ] 2.2 Implementar endpoint de renovacion de sesion (refresh) y politicas de expiracion.
- [ ] 2.3 Implementar endpoint de sesion actual (me) para obtener usuario autenticado y rol vigente.
- [ ] 2.4 Asegurar que respuestas de auth no expongan clave ni datos sensibles.

## 3. Backend de autorizacion por roles

- [ ] 3.1 Crear utilidades compartidas (middleware/decoradores) de require_auth y require_roles.
- [ ] 3.2 Definir matriz de permisos inicial por endpoint para AGENTE, ADMINISTRADOR, SUPERADMIN y CLIENTE.
- [ ] 3.3 Aplicar proteccion por rol a blueprints y endpoints priorizados del panel.
- [ ] 3.4 Validar que autenticado sin permiso reciba 403 y no autenticado reciba 401.

## 4. Credenciales y migracion de datos

- [ ] 4.1 Implementar hashing obligatorio al crear/actualizar clave de usuario.
- [ ] 4.2 Diseñar y ejecutar script idempotente para migrar claves existentes en texto plano a hash seguro.
- [ ] 4.3 Ajustar seed y scripts SQL para no insertar nuevas credenciales en texto plano.
- [ ] 4.4 Definir procedimiento de backup y rollback de base de datos para la migracion.

## 5. Frontend de sesion y control de acceso

- [ ] 5.1 Crear pantalla y flujo de inicio de sesion en SvelteKit.
- [ ] 5.2 Implementar store de sesion/autenticacion con persistencia controlada y cierre de sesion.
- [ ] 5.3 Actualizar cliente API para adjuntar token y manejar 401 con flujo de refresh/logout.
- [ ] 5.4 Implementar guardas de rutas y visibilidad condicional de menu/modulos por rol.

## 6. Pruebas y salida a produccion

- [ ] 6.1 Crear pruebas de backend para login, refresh, me, 401 y 403 por rol.
- [ ] 6.2 Ejecutar pruebas de regresion funcional en frontend para rutas protegidas y navegacion por rol.
- [ ] 6.3 Validar escenario de migracion en entorno de staging con datos representativos.
- [ ] 6.4 Preparar checklist de despliegue gradual, monitoreo y criterios de rollback.
