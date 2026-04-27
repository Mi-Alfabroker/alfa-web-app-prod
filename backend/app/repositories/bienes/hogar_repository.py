"""Repository for Hogar (Home) data access operations."""
from typing import Optional
from app.models import db
from app.models.bienes.hogar import Hogar
from app.repositories.bienes.base_bien_repository import BaseBienRepository


class HogarRepository(BaseBienRepository[Hogar]):
    """
    Data Access Layer for Hogar (Home) entities.
    
    Extends BaseBienRepository with Hogar-specific operations.
    """
    
    # Fields that can be updated
    UPDATABLE_FIELDS = [
        'tipo_inmueble', 'ciudad_inmueble', 'direccion_inmueble',
        'numero_pisos', 'ano_construccion', 'valor_inmueble_avaluo',
        'valor_contenidos_normales_avaluo', 'valor_contenidos_especiales_avaluo',
        'valor_equipo_electronico_avaluo', 'valor_maquinaria_equipo_avaluo'
    ]

    def __init__(self):
        super().__init__(Hogar)

    def get_by_ciudad(self, ciudad: str) -> list[Hogar]:
        """Retrieve all homes in a specific city."""
        return Hogar.query.filter_by(ciudad_inmueble=ciudad).all()

    def get_by_tipo(self, tipo_inmueble: str) -> list[Hogar]:
        """Retrieve all homes of a specific type."""
        return Hogar.query.filter_by(tipo_inmueble=tipo_inmueble).all()

    def update(self, hogar: Hogar, data: dict) -> Hogar:
        """Update an existing home asset."""
        return super().update(hogar, data, self.UPDATABLE_FIELDS)


# Singleton instance for static-like access
_repository = HogarRepository()

# Static-like methods for backwards compatibility with existing pattern
get_all = _repository.get_all
get_by_id = _repository.get_by_id
get_by_usuario_id = _repository.get_by_usuario_id
get_by_ciudad = _repository.get_by_ciudad
get_by_tipo = _repository.get_by_tipo
create = _repository.create
update = _repository.update
delete = _repository.delete
