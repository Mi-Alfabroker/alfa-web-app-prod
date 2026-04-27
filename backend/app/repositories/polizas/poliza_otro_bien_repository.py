"""Repository for PolizaOtroBien (Other Asset Insurance Policy) data access operations."""
from typing import List
from app.models.polizas.poliza_otro_bien import PolizaOtroBien
from app.repositories.polizas.base_poliza_repository import BasePolizaRepository


class PolizaOtroBienRepository(BasePolizaRepository[PolizaOtroBien]):
    """
    Data Access Layer for PolizaOtroBien entities.
    
    Inherits common operations from BasePolizaRepository and
    provides specific operations for other asset insurance policies.
    """
    
    # Fields that can be updated via the update method
    UPDATABLE_FIELDS = [
        'estado',
        'inicio_vigencia',
        'fin_vigencia',
        'valor_prima_aseg_1',
        'valor_prima_aseg_2',
        'valor_prima_aseg_3',
        'valor_prima_aseg_4',
        'valor_prima_aseg_5',
        'id_aseguradora_1',
        'id_aseguradora_2',
        'id_aseguradora_3',
        'id_aseguradora_4',
        'id_aseguradora_5',
        'aseguradora_seleccionada',
        'numero_poliza_aseguradora',
        'valor_prima_neta',
        'valor_otros_costos',
        'valor_iva',
        'ingreso_comision_percibido',
        'valor_asegurado',
        'valor_cuota_3',
        'valor_cuota_5',
        'valor_cuota_8',
        'valor_cuota_11',
    ]
    
    def __init__(self):
        super().__init__(PolizaOtroBien, 'id_otro_bien')

    def update(self, poliza: PolizaOtroBien, data: dict) -> PolizaOtroBien:
        """
        Update an other asset insurance policy.
        
        Args:
            poliza: The policy instance to update
            data: Dictionary with fields to update
            
        Returns:
            The updated policy instance
        """
        return super().update(poliza, data, self.UPDATABLE_FIELDS)

    def get_by_usuario_id(self, usuario_id: int) -> List[PolizaOtroBien]:
        """
        Retrieve all other asset policies for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of other asset policies for this user (through their other assets)
        """
        from app.models.bienes.otro_bien import OtroBien
        return PolizaOtroBien.query.join(OtroBien).filter(
            OtroBien.id_usuario == usuario_id
        ).all()


# Singleton instance for use in services
poliza_otro_bien_repository = PolizaOtroBienRepository()
