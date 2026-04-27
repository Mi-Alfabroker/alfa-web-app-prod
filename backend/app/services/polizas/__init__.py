# Polizas (Insurance Policies) services
from app.services.polizas.poliza_hogar_service import PolizaHogarService
from app.services.polizas.poliza_vehiculo_service import PolizaVehiculoService
from app.services.polizas.poliza_copropiedad_service import PolizaCopropiedadService
from app.services.polizas.poliza_otro_bien_service import PolizaOtroBienService

__all__ = [
    'PolizaHogarService',
    'PolizaVehiculoService',
    'PolizaCopropiedadService',
    'PolizaOtroBienService'
]
