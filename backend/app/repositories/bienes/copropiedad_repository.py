"""Repository for Copropiedad (Co-ownership) data access operations."""
from typing import Optional
from app.models import db
from app.models.bienes.copropiedad import Copropiedad
from app.repositories.bienes.base_bien_repository import BaseBienRepository


class CopropiedadRepository(BaseBienRepository[Copropiedad]):
    """
    Data Access Layer for Copropiedad (Co-ownership) entities.
    
    Extends BaseBienRepository with Copropiedad-specific operations.
    """
    
    # Fields that can be updated
    UPDATABLE_FIELDS = [
        'tipo_copropiedad', 'ciudad', 'direccion', 'estrato', 'ano_construccion',
        'numero_torres', 'numero_maximo_pisos', 'numero_maximo_sotanos',
        'cantidad_unidades_casa', 'cantidad_unidades_apartamentos',
        'cantidad_unidades_locales', 'cantidad_unidades_oficinas',
        'cantidad_unidades_otros', 'valor_edificio_area_comun_avaluo',
        'valor_edificio_area_privada_avaluo', 'valor_maquinaria_equipo_avaluo',
        'valor_equipo_electrico_electronico_avaluo', 'valor_muebles_avaluo'
    ]

    def __init__(self):
        super().__init__(Copropiedad)

    def get_by_ciudad(self, ciudad: str) -> list[Copropiedad]:
        """Retrieve all co-ownerships in a specific city."""
        return Copropiedad.query.filter_by(ciudad=ciudad).all()

    def get_by_tipo(self, tipo_copropiedad: str) -> list[Copropiedad]:
        """Retrieve all co-ownerships of a specific type."""
        return Copropiedad.query.filter_by(tipo_copropiedad=tipo_copropiedad).all()

    def get_by_estrato(self, estrato: int) -> list[Copropiedad]:
        """Retrieve all co-ownerships of a specific socioeconomic stratum."""
        return Copropiedad.query.filter_by(estrato=estrato).all()

    def update(self, copropiedad: Copropiedad, data: dict) -> Copropiedad:
        """Update an existing co-ownership asset."""
        return super().update(copropiedad, data, self.UPDATABLE_FIELDS)


# Singleton instance for static-like access
_repository = CopropiedadRepository()

# Static-like methods for backwards compatibility with existing pattern
get_all = _repository.get_all
get_by_id = _repository.get_by_id
get_by_usuario_id = _repository.get_by_usuario_id
get_by_ciudad = _repository.get_by_ciudad
get_by_tipo = _repository.get_by_tipo
get_by_estrato = _repository.get_by_estrato
create = _repository.create
update = _repository.update
delete = _repository.delete
