"""Repository for PolizaCopropiedad (Co-ownership Insurance Policy) data access operations."""
from typing import List
from app.models.polizas.poliza_copropiedad import PolizaCopropiedad
from app.repositories.polizas.base_poliza_repository import BasePolizaRepository


class PolizaCopropiedadRepository(BasePolizaRepository[PolizaCopropiedad]):
    """
    Data Access Layer for PolizaCopropiedad entities.
    
    Inherits common operations from BasePolizaRepository and
    provides specific operations for co-ownership insurance policies.
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
        'valor_area_comun_asegurado',
        'valor_area_privada_asegurado',
        'valor_maquinaria_equipo_asegurado',
        'valor_equipo_electronico_asegurado',
        'valor_muebles_asegurado',
        'valor_directores_asegurado',
        'valor_rce_asegurado',
        'valor_manejo_asegurado',
        'valor_transporte_valores_vigencia_asegurado',
        'valor_transporte_valores_despacho_asegurado',
        'valor_cuota_3',
        'valor_cuota_5',
        'valor_cuota_8',
        'valor_cuota_11',
    ]
    
    def __init__(self):
        super().__init__(PolizaCopropiedad, 'id_copropiedad')

    def update(self, poliza: PolizaCopropiedad, data: dict) -> PolizaCopropiedad:
        """
        Update a co-ownership insurance policy.
        
        Args:
            poliza: The policy instance to update
            data: Dictionary with fields to update
            
        Returns:
            The updated policy instance
        """
        return super().update(poliza, data, self.UPDATABLE_FIELDS)

    def get_by_usuario_id(self, usuario_id: int) -> List[PolizaCopropiedad]:
        """
        Retrieve all co-ownership policies for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of co-ownership policies for this user (through their co-ownerships)
        """
        from app.models.bienes.copropiedad import Copropiedad
        return PolizaCopropiedad.query.join(Copropiedad).filter(
            Copropiedad.id_usuario == usuario_id
        ).all()


# Singleton instance for use in services
poliza_copropiedad_repository = PolizaCopropiedadRepository()
