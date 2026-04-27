from types import SimpleNamespace

from app import create_app
from app.security import create_access_token, hash_password


class FakeUser:
    def __init__(self, user_id: int, username: str, role: str, password: str):
        self.id = user_id
        self.usuario = username
        self.tipo_usuario = role
        self.clave = password

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "tipo_usuario": self.tipo_usuario,
        }


def _build_app():
    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET_KEY": "test-secret",
            "JWT_ACCESS_TOKEN_EXPIRES_MINUTES": 30,
            "JWT_REFRESH_TOKEN_EXPIRES_DAYS": 7,
        }
    )


def test_login_success(monkeypatch):
    app = _build_app()
    client = app.test_client()

    user = FakeUser(1, "admin", "ADMINISTRADOR", hash_password("admin123"))
    monkeypatch.setattr(
        "app.blueprints.auth.UsuarioRepository.get_by_usuario", lambda username: user if username == "admin" else None
    )

    response = client.post("/api/auth/login", json={"usuario": "admin", "clave": "admin123"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert "access_token" in payload["data"]["tokens"]
    assert "refresh_token" in payload["data"]["tokens"]
    assert "clave" not in payload["data"]["user"]


def test_login_invalid_credentials(monkeypatch):
    app = _build_app()
    client = app.test_client()

    monkeypatch.setattr("app.blueprints.auth.UsuarioRepository.get_by_usuario", lambda _: None)

    response = client.post("/api/auth/login", json={"usuario": "bad", "clave": "bad"})
    payload = response.get_json()

    assert response.status_code == 401
    assert payload["error"]["code"] == "AUTH_UNAUTHORIZED"


def test_protected_endpoint_without_token_returns_401():
    app = _build_app()
    client = app.test_client()

    response = client.get("/api/usuarios")
    payload = response.get_json()

    assert response.status_code == 401
    assert payload["error"]["code"] == "AUTH_UNAUTHORIZED"


def test_forbidden_role_returns_403(monkeypatch):
    app = _build_app()
    client = app.test_client()

    user = FakeUser(9, "cliente", "CLIENTE", hash_password("cliente123"))

    monkeypatch.setattr("app.security.decorators.UsuarioRepository.get_by_id", lambda _: user)

    with app.app_context():
        token = create_access_token(user.id, user.tipo_usuario)

    response = client.get("/api/usuarios", headers={"Authorization": f"Bearer {token}"})
    payload = response.get_json()

    assert response.status_code == 403
    assert payload["error"]["code"] == "AUTH_FORBIDDEN"


def test_me_returns_authenticated_user(monkeypatch):
    app = _build_app()
    client = app.test_client()

    user = FakeUser(3, "agente01", "AGENTE", hash_password("agente123"))

    monkeypatch.setattr("app.security.decorators.UsuarioRepository.get_by_id", lambda _: user)

    with app.app_context():
        token = create_access_token(user.id, user.tipo_usuario)

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["user"]["usuario"] == "agente01"
