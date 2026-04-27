"""Repository for OtroBien (Other Asset) data access operations."""
from typing import Optional
from app.models import db
from app.models.bienes.otro_bien import OtroBien
from app.repositories.bienes.base_bien_repository import BaseBienRepository


class OtroBienRepository(BaseBienRepository[OtroBien]):
    """
    Data Access Layer for OtroBien (Other Asset) entities.
    
    Extends BaseBienRepository with OtroBien-specific operations.
    """
    
    # Fields that can be updated
    UPDATABLE_FIELDS = [
        'tipo_seguro', 'bien_asegurado', 'valor_bien_asegurar',
        'detalles_bien_asegurado'
    ]

    def __init__(self):
        super().__init__(OtroBien)

    def get_by_tipo_seguro(self, tipo_seguro: str) -> list[OtroBien]:
        """Retrieve all assets of a specific insurance type."""
        return OtroBien.query.filter_by(tipo_seguro=tipo_seguro).all()

    def update(self, otro_bien: OtroBien, data: dict) -> OtroBien:
        """Update an existing other asset."""
        return super().update(otro_bien, data, self.UPDATABLE_FIELDS)


# Singleton instance for static-like access
_repository = OtroBienRepository()

# Static-like methods for backwards compatibility with existing pattern
get_all = _repository.get_all
get_by_id = _repository.get_by_id
get_by_usuario_id = _repository.get_by_usuario_id
get_by_tipo_seguro = _repository.get_by_tipo_seguro
create = _repository.create
update = _repository.update
delete = _repository.delete
