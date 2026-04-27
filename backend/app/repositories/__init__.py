# Data access layer - Repository pattern
from app.repositories.aseguradora_repository import AseguradoraRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.polizas import (
    BasePolizaRepository,
    poliza_hogar_repository,
    poliza_vehiculo_repository,
    poliza_copropiedad_repository,
    poliza_otro_bien_repository
)

__all__ = [
    'AseguradoraRepository', 
    'UsuarioRepository',
    'BasePolizaRepository',
    'poliza_hogar_repository',
    'poliza_vehiculo_repository',
    'poliza_copropiedad_repository',
    'poliza_otro_bien_repository'
]