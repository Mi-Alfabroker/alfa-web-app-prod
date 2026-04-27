# Blueprints package - API Layer
from app.blueprints.health import health_bp
from app.blueprints.auth import auth_bp
from app.blueprints.aseguradoras import aseguradoras_bp
from app.blueprints.usuarios import usuarios_bp
from app.blueprints.bienes import bienes_bp
from app.blueprints.polizas import polizas_bp

__all__ = ['health_bp', 'auth_bp', 'aseguradoras_bp', 'usuarios_bp', 'bienes_bp', 'polizas_bp']
