# Polizas (Insurance Policies) repositories
from app.repositories.polizas.base_poliza_repository import BasePolizaRepository
from app.repositories.polizas.poliza_hogar_repository import poliza_hogar_repository
from app.repositories.polizas.poliza_vehiculo_repository import poliza_vehiculo_repository
from app.repositories.polizas.poliza_copropiedad_repository import poliza_copropiedad_repository
from app.repositories.polizas.poliza_otro_bien_repository import poliza_otro_bien_repository

__all__ = [
    'BasePolizaRepository',
    'poliza_hogar_repository',
    'poliza_vehiculo_repository',
    'poliza_copropiedad_repository',
    'poliza_otro_bien_repository'
]
