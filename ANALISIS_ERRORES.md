# Análisis de Errores - Alfabroker Admin App

**Fecha:** 2026-04-24
**Scope:** backend/ (Flask + SQLAlchemy), frontend/ (Svelte + Vite + TS), docker-compose, migrations

---

## Resumen

| Severidad | Cantidad |
|-----------|----------|
| Crítico   | 3        |
| Alto      | 2        |
| Medio     | 8        |
| Bajo      | 4        |

---

## CRÍTICO

### 1. JWT_SECRET_KEY con default hardcoded
- **Archivos:** `backend/app/__init__.py:57`, `backend/app/security/auth.py:15`
- **Problema:** Default `"change-this-in-production"` si falta env var. Permite forjar tokens válidos → bypass total de autenticación.
- **Fix:** Fallar al arranque si `JWT_SECRET_KEY` no está definida.

```python
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # sin default
```

### 2. Credenciales commiteadas en `.env`
- **Archivos:** `backend/.env:2-6,14`, `docker-compose-db.yml:6-8`
- **Problema:** Credenciales BD (`admin/admin`) y connection strings en repo.
- **Fix:** Añadir `.env` a `.gitignore`, crear `.env.example` con placeholders, rotar credenciales expuestas.

### 3. Credenciales débiles por defecto en PostgreSQL
- **Archivo:** `docker-compose-db.yml:6-8`
- **Problema:** `POSTGRES_USER=admin`, `POSTGRES_PASSWORD=admin`.
- **Fix:** Requerir variables externas sin default.

---

## ALTO

### 4. `FLASK_DEBUG=1` en `.env` committed
- **Archivo:** `backend/.env:11`
- **Problema:** Debug mode expone stack traces + REPL interactivo (Werkzeug debugger = RCE).
- **Fix:** `FLASK_DEBUG=0` en producción. Controlar por entorno.

### 5. Comparación de contraseñas en plano (backward-compat)
- **Archivo:** `backend/app/security/auth.py:49-51`
- **Problema:** Fallback acepta passwords en plano. Si BD comprometida → passwords expuestas. Vulnerable a timing attacks.
- **Fix:** Migración forzada a bcrypt/argon2, eliminar fallback plaintext.

---

## MEDIO

### 6. `to_dict_full()` expone campo `clave`
- **Archivo:** `backend/app/models/usuario.py:100`
- **Problema:** Si se llama desde endpoint → leak de password hash.
- **Fix:** Eliminar `clave` también en `to_dict_full()`, o renombrar para uso interno explícito.

### 7. `except:` desnudo
- **Archivo:** `backend/app/__init__.py:103,120`
- **Problema:** Captura `SystemExit`/`KeyboardInterrupt`. Oculta errores críticos.
- **Fix:** `except Exception:` con logging estructurado.

### 8. Falta validación en query params
- **Archivos:** `backend/app/blueprints/usuarios.py:31`, `backend/app/blueprints/bienes.py:39,197,379,545`
- **Problema:** `tipo_usuario`, `usuario_id` sin validar contra whitelist.
- **Fix:** Validar contra `VALID_TIPOS_USUARIO`, castear `usuario_id` a int con try/except.

### 9. Logging con `print()`
- **Archivos:** `backend/app/__init__.py:100,115-117`, `backend/app/services/propuestas/propuesta_service.py` (múltiples)
- **Problema:** `print()` en lugar de módulo `logging`. Sin niveles ni formato estructurado.
- **Fix:** `import logging; logger = logging.getLogger(__name__)`.

### 10. Docker network externa no auto-creada
- **Archivo:** `backend/docker-compose.yml:21`
- **Problema:** Network `alfabroker_network` debe existir previamente → deploy falla.
- **Fix:** Marcar como `external: false` o documentar en README.

### 11. Contrato API frontend/backend inconsistente
- **Frontend:** `frontend/src/lib/services/api.ts:77-88` espera `response.data`
- **Backend:** `backend/app/blueprints/propuestas.py:26-30` envuelve `{success, data, count}`
- **Fix:** Unificar envoltura. Tipos compartidos vía OpenAPI o tipos TS generados.

### 12. Servicio frontend duplicado `_NEW`
- **Archivo:** `frontend/src/lib/services/propuesta.service_NEW.ts`
- **Problema:** Coexiste con versión original. Ambigüedad de cuál está en uso.
- **Fix:** Eliminar obsoleto, commit con rename claro.

### 13. PUT sin pre-validación
- **Archivo:** `backend/app/blueprints/usuarios.py:143-149`
- **Problema:** `request.get_json()` pasa raw al service.
- **Fix:** Validar con Marshmallow/Pydantic schema antes de llamar service.

---

## BAJO

### 14. Módulo `clientes/` vacío
- **Archivo:** `backend/app/services/clientes/__init__.py`
- **Problema:** Solo contiene comentario. Dead code.
- **Fix:** Eliminar.

### 15. TODO pendiente de audit logging
- **Archivo:** `backend/app/services/polizas/poliza_hogar_service.py:347`
- **Comment:** `# TODO: Add audit logging here`
- **Fix:** Implementar o crear issue.

### 16. Mismatch timeout frontend
- **`frontend/.env:6`:** 10000ms
- **`frontend/src/lib/config/index.ts:11`:** default 30000ms
- **Fix:** Alinear ambos valores.

### 17. Parse JSON frágil en frontend
- **Archivo:** `frontend/src/lib/services/api.ts:89-97`
- **Problema:** Si respuesta no es JSON (ej. HTML 500) → parse falla en silencio.
- **Fix:** Verificar `content-type` antes de `response.json()`.

---

## Notas positivas
- Uso de SQLAlchemy ORM con parameterized queries → sin SQL injection detectada.
- Estructura blueprints/services separada correctamente.

---

## Acciones prioritarias
1. Rotar `JWT_SECRET_KEY` + quitar default
2. `.env` fuera de git + rotar credenciales BD
3. `FLASK_DEBUG=0`
4. Eliminar fallback plaintext passwords
5. Reemplazar `print()` con `logging`
6. Limpiar `_NEW.ts` y módulo `clientes/` vacío
