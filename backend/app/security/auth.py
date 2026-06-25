"""Authentication helpers for token management and password security."""
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash


ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def _get_secret_key() -> str:
    return current_app.config.get("JWT_SECRET_KEY", "change-this-in-production")


def _get_access_minutes() -> int:
    return int(current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30))


def _get_refresh_days() -> int:
    return int(current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7))


def is_password_hashed(value: str) -> bool:
    if not value:
        return False
    return (
        value.startswith("pbkdf2:")
        or value.startswith("scrypt:")
        or value.startswith("argon2:")
        or value.startswith("$2a$")
        or value.startswith("$2b$")
        or value.startswith("$2y$")
    )


def hash_password(raw_password: str) -> str:
    if is_password_hashed(raw_password):
        return raw_password
    # Default werkzeug hash method is secure and maintained by Flask ecosystem.
    return generate_password_hash(raw_password)


def verify_password(raw_password: str, stored_password: str) -> bool:
    if not raw_password or not stored_password:
        return False

    # Backward-compatible path for legacy plaintext rows before migration.
    if not is_password_hashed(stored_password):
        return raw_password == stored_password

    # Hashes bcrypt ($2a/$2b/$2y) vienen del seed de la DB (pgcrypto crypt()).
    # werkzeug.check_password_hash NO entiende este formato crudo -> verificar con bcrypt.
    if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            return bcrypt.checkpw(raw_password.encode("utf-8"), stored_password.encode("utf-8"))
        except ValueError:
            return False

    return check_password_hash(stored_password, raw_password)


def _build_payload(user_id: int, role: str, token_type: str, expires_delta: timedelta) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "sub": str(user_id),
        "role": role,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }


def create_access_token(user_id: int, role: str) -> str:
    payload = _build_payload(
        user_id=user_id,
        role=role,
        token_type=ACCESS_TOKEN_TYPE,
        expires_delta=timedelta(minutes=_get_access_minutes()),
    )
    return jwt.encode(payload, _get_secret_key(), algorithm="HS256")


def create_refresh_token(user_id: int, role: str) -> str:
    payload = _build_payload(
        user_id=user_id,
        role=role,
        token_type=REFRESH_TOKEN_TYPE,
        expires_delta=timedelta(days=_get_refresh_days()),
    )
    return jwt.encode(payload, _get_secret_key(), algorithm="HS256")


def decode_token(token: str, expected_type: Optional[str] = None) -> dict[str, Any]:
    payload = jwt.decode(token, _get_secret_key(), algorithms=["HS256"])
    token_type = payload.get("type")
    if expected_type and token_type != expected_type:
        raise jwt.InvalidTokenError(f"Invalid token type: expected {expected_type}")
    return payload


def token_expiry_seconds(token_type: str) -> int:
    if token_type == ACCESS_TOKEN_TYPE:
        return _get_access_minutes() * 60
    return _get_refresh_days() * 24 * 60 * 60
