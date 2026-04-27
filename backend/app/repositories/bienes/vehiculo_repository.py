"""Repository for Vehiculo (Vehicle) data access operations."""
from typing import Optional
from app.models import db
from app.models.bienes.vehiculo import Vehiculo
from app.repositories.bienes.base_bien_repository import BaseBienRepository


class VehiculoRepository(BaseBienRepository[Vehiculo]):
    """
    Data Access Layer for Vehiculo (Vehicle) entities.
    
    Extends BaseBienRepository with Vehiculo-specific operations.
    """
    
    # Fields that can be updated
    UPDATABLE_FIELDS = [
        'tipo_vehiculo', 'placa', 'marca', 'serie_referencia',
        'ano_modelo', 'ano_nacimiento_conductor', 'codigo_fasecolda',
        'valor_vehiculo', 'valor_accesorios_avaluo'
    ]

    def __init__(self):
        super().__init__(Vehiculo)

    def get_by_placa(self, placa: str) -> Optional[Vehiculo]:
        """Retrieve a vehicle by its license plate."""
        return Vehiculo.query.filter_by(placa=placa).first()

    def get_by_marca(self, marca: str) -> list[Vehiculo]:
        """Retrieve all vehicles of a specific brand."""
        return Vehiculo.query.filter_by(marca=marca).all()

    def get_by_tipo(self, tipo_vehiculo: str) -> list[Vehiculo]:
        """Retrieve all vehicles of a specific type."""
        return Vehiculo.query.filter_by(tipo_vehiculo=tipo_vehiculo).all()

    def update(self, vehiculo: Vehiculo, data: dict) -> Vehiculo:
        """Update an existing vehicle asset."""
        return super().update(vehiculo, data, self.UPDATABLE_FIELDS)


# Singleton instance for static-like access
_repository = VehiculoRepository()

# Static-like methods for backwards compatibility with existing pattern
get_all = _repository.get_all
get_by_id = _repository.get_by_id
get_by_usuario_id = _repository.get_by_usuario_id
get_by_placa = _repository.get_by_placa
get_by_marca = _repository.get_by_marca
get_by_tipo = _repository.get_by_tipo
create = _repository.create
update = _repository.update
delete = _repository.delete
