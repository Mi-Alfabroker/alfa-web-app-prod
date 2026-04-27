"""Decorators and helpers for authentication and RBAC enforcement."""
from functools import wraps
from typing import Callable, Iterable, Optional

import jwt
from flask import g, jsonify, request

from app.repositories.usuario_repository import UsuarioRepository
from app.security.auth import ACCESS_TOKEN_TYPE, decode_token


def _error_response(status_code: int, code: str, message: str):
    return jsonify(
        {
            "success": False,
            "error": {
                "code": code,
                "message": message,
            },
        }
    ), status_code


def unauthorized(message: str = "Authentication required"):
    return _error_response(401, "AUTH_UNAUTHORIZED", message)


def forbidden(message: str = "Insufficient role permissions"):
    return _error_response(403, "AUTH_FORBIDDEN", message)


def _extract_bearer_token() -> Optional[str]:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        return None

    parts = auth_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip()


def _resolve_current_user_from_token():
    token = _extract_bearer_token()
    if not token:
        return None, unauthorized("Missing Bearer token")

    try:
        payload = decode_token(token, expected_type=ACCESS_TOKEN_TYPE)
    except jwt.ExpiredSignatureError:
        return None, unauthorized("Access token expired")
    except jwt.InvalidTokenError:
        return None, unauthorized("Invalid access token")

    user_id = payload.get("sub")
    if not user_id:
        return None, unauthorized("Token payload missing subject")

    usuario = UsuarioRepository.get_by_id(int(user_id))
    if not usuario:
        return None, unauthorized("User no longer exists")

    g.current_user = usuario
    g.current_role = (usuario.tipo_usuario or "").upper()
    return usuario, None


def authorize_request(required_roles: Optional[Iterable[str]] = None):
    usuario, error_response = _resolve_current_user_from_token()
    if error_response:
        return error_response

    if required_roles:
        normalized = {role.upper() for role in required_roles}
        if (usuario.tipo_usuario or "").upper() not in normalized:
            return forbidden()

    return None


def require_auth(fn: Callable):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        error_response = authorize_request()
        if error_response:
            return error_response
        return fn(*args, **kwargs)

    return wrapper


def require_roles(*roles: str):
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            error_response = authorize_request(roles)
            if error_response:
                return error_response
            return fn(*args, **kwargs)

        return wrapper

    return decorator
