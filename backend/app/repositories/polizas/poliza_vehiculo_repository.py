"""Repository for PolizaVehiculo (Vehicle Insurance Policy) data access operations."""
from typing import List
from app.models.polizas.poliza_vehiculo import PolizaVehiculo
from app.repositories.polizas.base_poliza_repository import BasePolizaRepository


class PolizaVehiculoRepository(BasePolizaRepository[PolizaVehiculo]):
    """
    Data Access Layer for PolizaVehiculo entities.
    
    Inherits common operations from BasePolizaRepository and
    provides specific operations for vehicle insurance policies.
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
        'valor_vehiculo_asegurado',
        'valor_accesorios_asegurado',
        'valor_rc_asegurado',
        'valor_cuota_3',
        'valor_cuota_5',
        'valor_cuota_8',
        'valor_cuota_11',
    ]
    
    def __init__(self):
        super().__init__(PolizaVehiculo, 'id_vehiculo')

    def update(self, poliza: PolizaVehiculo, data: dict) -> PolizaVehiculo:
        """
        Update a vehicle insurance policy.
        
        Args:
            poliza: The policy instance to update
            data: Dictionary with fields to update
            
        Returns:
            The updated policy instance
        """
        return super().update(poliza, data, self.UPDATABLE_FIELDS)

    def get_by_usuario_id(self, usuario_id: int) -> List[PolizaVehiculo]:
        """
        Retrieve all vehicle policies for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of vehicle policies for this user (through their vehicles)
        """
        from app.models.bienes.vehiculo import Vehiculo
        return PolizaVehiculo.query.join(Vehiculo).filter(
            Vehiculo.id_usuario == usuario_id
        ).all()

    def get_by_placa(self, placa: str) -> List[PolizaVehiculo]:
        """
        Retrieve all policies for a vehicle by license plate.
        
        Args:
            placa: The vehicle's license plate
            
        Returns:
            List of policies for this vehicle
        """
        from app.models.bienes.vehiculo import Vehiculo
        return PolizaVehiculo.query.join(Vehiculo).filter(
            Vehiculo.placa == placa
        ).all()


# Singleton instance for use in services
poliza_vehiculo_repository = PolizaVehiculoRepository()
