"""Blueprint for authentication endpoints."""
from flask import Blueprint, jsonify, request
import jwt

from app.repositories.usuario_repository import UsuarioRepository
from app.security import (
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    decode_token,
    token_expiry_seconds,
    verify_password,
)
from app.security.decorators import require_auth, unauthorized


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _get_refresh_token_from_request() -> str:
    data = request.get_json(silent=True) or {}
    token_from_body = data.get("refresh_token")
    if token_from_body:
        return token_from_body

    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1].strip()

    return ""


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("usuario") or "").strip()
    password = data.get("clave") or ""

    if not username or not password:
        return jsonify(
            {
                "success": False,
                "error": {
                    "code": "AUTH_INVALID_REQUEST",
                    "message": "Fields 'usuario' and 'clave' are required",
                },
            }
        ), 400

    usuario = UsuarioRepository.get_by_usuario(username)
    if not usuario or not verify_password(password, usuario.clave):
        return unauthorized("Invalid username or password")

    role = (usuario.tipo_usuario or "").upper()
    access_token = create_access_token(usuario.id, role)
    refresh_token = create_refresh_token(usuario.id, role)

    return jsonify(
        {
            "success": True,
            "data": {
                "user": usuario.to_dict(),
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "Bearer",
                    "expires_in": token_expiry_seconds("access"),
                },
            },
        }
    ), 200


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    token = _get_refresh_token_from_request()
    if not token:
        return unauthorized("Missing refresh token")

    try:
        payload = decode_token(token, expected_type=REFRESH_TOKEN_TYPE)
    except jwt.ExpiredSignatureError:
        return unauthorized("Refresh token expired")
    except jwt.InvalidTokenError:
        return unauthorized("Invalid refresh token")

    user_id = int(payload.get("sub", 0))
    usuario = UsuarioRepository.get_by_id(user_id)
    if not usuario:
        return unauthorized("User no longer exists")

    role = (usuario.tipo_usuario or "").upper()
    access_token = create_access_token(usuario.id, role)

    return jsonify(
        {
            "success": True,
            "data": {
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": token_expiry_seconds("access"),
            },
        }
    ), 200


@auth_bp.route("/me", methods=["GET"])
@require_auth
def me():
    from flask import g

    return jsonify(
        {
            "success": True,
            "data": {
                "user": g.current_user.to_dict(),
            },
        }
    ), 200
