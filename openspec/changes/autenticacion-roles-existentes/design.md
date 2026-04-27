## Context

El sistema ya tiene una entidad de usuarios con tipos de usuario (AGENTE, ADMINISTRADOR, SUPERADMIN, CLIENTE), pero actualmente no existe una capa de autenticacion/autorizacion aplicada de forma transversal. El backend expone endpoints sin control de acceso y el frontend no maneja sesion ni guardas por rol.

La implementacion debe cubrir backend Flask, frontend SvelteKit y base de datos PostgreSQL, manteniendo compatibilidad con los roles existentes para evitar una migracion funcional innecesaria.

## Goals / Non-Goals

**Goals:**
- Establecer autenticacion de usuarios para el panel administrativo con una sesion verificable.
- Aplicar autorizacion por rol en backend usando AGENTE, ADMINISTRADOR, SUPERADMIN y CLIENTE.
- Homogeneizar manejo de errores 401/403 para facilitar comportamiento consistente en frontend.
- Endurecer manejo de credenciales (hash seguro de contrasena y comparacion segura).
- Restringir navegacion/modulos en frontend segun rol autenticado.

**Non-Goals:**
- Redefinir o eliminar roles existentes del dominio.
- Implementar proveedor externo de identidad (OAuth, SSO corporativo) en esta fase.
- Redisenar todos los modulos funcionales; solo se ajusta acceso/autorizacion.
- Introducir permisos granulares por recurso (ACL por registro) en esta fase inicial.

## Decisions

1. Mecanismo de sesion basado en token firmado
- Decision: usar tokens firmados para autenticacion de API (access token de vida corta y refresh token de vida mayor).
- Rationale: se adapta al frontend SPA y permite validar acceso por request sin estado de sesion en servidor.
- Alternative considered: sesiones server-side con cookie. Se descarta por mayor friccion de despliegue y dependencia de estado compartido.

2. Autorizacion centralizada por decoradores/middleware en backend
- Decision: crear utilidades reutilizables (require_auth, require_roles) para proteger blueprints.
- Rationale: evita duplicacion y reduce riesgo de endpoints sin control.
- Alternative considered: validar rol manualmente en cada endpoint. Se descarta por propension a errores.

3. Canon de roles sin renombrar dominio
- Decision: conservar AGENTE, ADMINISTRADOR, SUPERADMIN y CLIENTE; mapear ADMINISTRADOR y SUPERADMIN a nivel administrativo completo en reglas iniciales.
- Rationale: minimiza cambios de datos y compatibilidad retroactiva.
- Alternative considered: crear solo admin/agente y migrar CLIENTE/SUPERADMIN. Se difiere para una fase posterior.

4. Password hashing obligatorio
- Decision: almacenar y validar claves mediante hash seguro (no texto plano), con migracion de usuarios existentes.
- Rationale: requisito basico de seguridad y cumplimiento de buenas practicas.
- Alternative considered: mantener esquema actual temporal. Se descarta por riesgo alto.

5. Guardas y UX de acceso en frontend
- Decision: agregar estado de autenticacion, pantalla de login, redireccion por sesion y render condicional de menu/modulos por rol.
- Rationale: reduce errores de UX y evita exponer navegacion no autorizada.
- Alternative considered: solo control backend sin cambios de frontend. Se descarta por mala experiencia y mayor tasa de errores de uso.

## Risks / Trade-offs

- [Riesgo: Endpoints sin proteger por omision] -> Mitigacion: inventario de rutas y checklist de proteccion por blueprint.
- [Riesgo: Regresiones por cambio de acceso abierto a autenticado] -> Mitigacion: matriz de pruebas por endpoint y rol con casos 200/401/403.
- [Riesgo: Migracion de claves invalida usuarios existentes] -> Mitigacion: script idempotente, backup previo y estrategia de rollback.
- [Riesgo: Bucles de refresh token en frontend] -> Mitigacion: reintento unico por request y logout controlado ante refresh fallido.
- [Trade-off: Mayor complejidad operacional] -> Mitigacion: documentar flujos de token y tiempos de expiracion estandar.

## Migration Plan

1. Preparar configuracion de seguridad (secretos, expiraciones, variables de entorno).
2. Incorporar endpoints de autenticacion y utilidades de autorizacion en backend.
3. Proteger rutas segun matriz de roles acordada.
4. Implementar hashing y ejecutar migracion de claves existentes.
5. Implementar login/sesion/guards en frontend y control de menu por rol.
6. Ejecutar pruebas de regresion funcional y de autorizacion.
7. Despliegue gradual con monitoreo de errores 401/403 y tasa de login.

Rollback:
- Revertir despliegue de backend/frontend a version previa.
- Restaurar backup de base de datos si falla migracion de credenciales.
- Mantener feature flag o ruta de escape operativa durante estabilizacion.

## Open Questions

- Definicion final de permisos de CLIENTE en este panel administrativo (sin acceso, lectura parcial o flujo especifico).
- Politica exacta de expiracion para access/refresh token en ambiente productivo.
- Si SUPERADMIN tendra diferencias funcionales respecto a ADMINISTRADOR en esta fase o quedaran equivalentes.
- Reglas de bloqueo temporal por intentos fallidos y politica de recuperacion de contrasena para fase inicial.
