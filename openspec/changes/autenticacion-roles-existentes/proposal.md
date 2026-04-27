## Why

Actualmente la aplicacion ya maneja tipos de usuario (AGENTE, ADMINISTRADOR, SUPERADMIN, CLIENTE), pero no tiene una autenticacion robusta ni controles de acceso por rol en backend y frontend. Esto expone operaciones sensibles y dificulta operar el sistema de forma segura y consistente.

## What Changes

- Agregar autenticacion de usuarios para el panel (inicio de sesion, validacion de credenciales y sesion vigente).
- Implementar autorizacion basada en roles usando los roles existentes: AGENTE, ADMINISTRADOR, SUPERADMIN, CLIENTE.
- Proteger endpoints del backend con reglas de acceso por rol para evitar acceso no autorizado.
- Incorporar guardas de navegacion y visibilidad de modulos en frontend segun rol autenticado.
- Estandarizar respuestas de errores de autenticacion/autorizacion (401/403) para manejo consistente en UI.
- Mejorar el manejo de credenciales para no exponer ni persistir contrasenas en texto plano. **BREAKING**: el flujo de consumo de APIs pasa de acceso abierto a acceso autenticado.

## Capabilities

### New Capabilities
- `auth-rbac-roles-existentes`: autenticacion y control de acceso por rol para AGENTE, ADMINISTRADOR, SUPERADMIN y CLIENTE en backend y frontend.

### Modified Capabilities
- Ninguna.

## Impact

- Backend Flask: nuevos endpoints de autenticacion y middleware/decoradores de autorizacion por rol.
- Modelo de usuario y persistencia: migracion de credenciales a esquema seguro y ajustes en validaciones.
- Frontend SvelteKit: flujo de login, estado de sesion, proteccion de rutas y navegacion condicionada por rol.
- API contract: endpoints funcionales requeriran token/sesion valida y podran responder 401/403.
- QA y pruebas: nuevos escenarios de autenticacion, expiracion de sesion y matriz de permisos por rol.
