# Domain models and entities
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.aseguradora import Aseguradora
from app.models.usuario import Usuario
from app.models.bienes import Hogar, Vehiculo, Copropiedad, OtroBien
from app.models.polizas import (
    BasePolizaMixin,
    EstadoPoliza,
    PolizaHogar,
    PolizaVehiculo,
    PolizaCopropiedad,
    PolizaOtroBien
)

__all__ = [
    'db', 
    'Aseguradora', 
    'Usuario', 
    'Hogar', 
    'Vehiculo', 
    'Copropiedad', 
    'OtroBien',
    'BasePolizaMixin',
    'EstadoPoliza',
    'PolizaHogar',
    'PolizaVehiculo',
    'PolizaCopropiedad',
    'PolizaOtroBien'
]