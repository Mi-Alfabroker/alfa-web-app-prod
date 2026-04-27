# Bienes (Assets) services
from app.services.bienes.hogar_service import HogarService
from app.services.bienes.vehiculo_service import VehiculoService
from app.services.bienes.copropiedad_service import CopropiedadService
from app.services.bienes.otro_bien_service import OtroBienService

__all__ = ['HogarService', 'VehiculoService', 'CopropiedadService', 'OtroBienService']
