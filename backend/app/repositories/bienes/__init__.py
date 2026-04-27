# Bienes (Assets) repositories
from app.repositories.bienes.hogar_repository import HogarRepository
from app.repositories.bienes.vehiculo_repository import VehiculoRepository
from app.repositories.bienes.copropiedad_repository import CopropiedadRepository
from app.repositories.bienes.otro_bien_repository import OtroBienRepository

__all__ = [
    'HogarRepository', 
    'VehiculoRepository', 
    'CopropiedadRepository', 
    'OtroBienRepository'
]
