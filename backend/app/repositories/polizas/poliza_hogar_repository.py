"""Repository for PolizaHogar (Home Insurance Policy) data access operations."""
from typing import List
from app.models.polizas.poliza_hogar import PolizaHogar
from app.repositories.polizas.base_poliza_repository import BasePolizaRepository


class PolizaHogarRepository(BasePolizaRepository[PolizaHogar]):
    """
    Data Access Layer for PolizaHogar entities.
    
    Inherits common operations from BasePolizaRepository and
    provides specific operations for home insurance policies.
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
        'valor_inmueble_asegurado',
        'valor_contenidos_normales_asegurado',
        'valor_contenidos_especiales_asegurado',
        'valor_equipo_electronico_asegurado',
        'valor_maquinaria_equipo_asegurado',
        'valor_rc_asegurado',
        'valor_cuota_3',
        'valor_cuota_5',
        'valor_cuota_8',
        'valor_cuota_11',
    ]
    
    def __init__(self):
        super().__init__(PolizaHogar, 'id_hogar')

    def update(self, poliza: PolizaHogar, data: dict) -> PolizaHogar:
        """
        Update a home insurance policy.
        
        Args:
            poliza: The policy instance to update
            data: Dictionary with fields to update
            
        Returns:
            The updated policy instance
        """
        return super().update(poliza, data, self.UPDATABLE_FIELDS)

    def get_by_usuario_id(self, usuario_id: int) -> List[PolizaHogar]:
        """
        Retrieve all home policies for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of home policies for this user (through their homes)
        """
        from app.models.bienes.hogar import Hogar
        return PolizaHogar.query.join(Hogar).filter(
            Hogar.id_usuario == usuario_id
        ).all()


# Singleton instance for use in services
poliza_hogar_repository = PolizaHogarRepository()
