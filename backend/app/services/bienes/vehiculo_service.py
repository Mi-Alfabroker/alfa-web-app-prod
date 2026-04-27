"""Business logic service for Vehiculo (Vehicle) operations."""
from typing import Optional
from app.models.bienes.vehiculo import Vehiculo
from app.repositories.bienes import vehiculo_repository
from app.repositories.usuario_repository import UsuarioRepository


class VehiculoService:
    """
    Business Logic Layer for Vehiculo operations.
    
    Orchestrates business rules and delegates data access to the repository.
    """

    @staticmethod
    def get_all() -> list[dict]:
        """
        Get all vehicle assets.
        
        Returns:
            List of vehicles as dictionaries
        """
        vehiculos = vehiculo_repository.get_all()
        return [v.to_dict() for v in vehiculos]

    @staticmethod
    def get_by_id(vehiculo_id: int) -> Optional[dict]:
        """
        Get a vehicle asset by ID.
        
        Args:
            vehiculo_id: The unique identifier
            
        Returns:
            Vehicle as dictionary or None if not found
        """
        vehiculo = vehiculo_repository.get_by_id(vehiculo_id)
        return vehiculo.to_dict() if vehiculo else None

    @staticmethod
    def get_by_usuario_id(usuario_id: int) -> list[dict]:
        """
        Get all vehicle assets for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of vehicles as dictionaries
        """
        vehiculos = vehiculo_repository.get_by_usuario_id(usuario_id)
        return [v.to_dict() for v in vehiculos]

    @staticmethod
    def get_by_placa(placa: str) -> Optional[dict]:
        """
        Get a vehicle by its license plate.
        
        Args:
            placa: The license plate number
            
        Returns:
            Vehicle as dictionary or None if not found
        """
        vehiculo = vehiculo_repository.get_by_placa(placa)
        return vehiculo.to_dict() if vehiculo else None

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new vehicle asset.
        
        Args:
            data: Dictionary with vehicle fields
            
        Returns:
            Tuple of (created vehicle dict, error message or None)
        """
        # Validate required fields
        if not data.get('id_usuario'):
            return {}, "Field 'id_usuario' is required"
        
        # Validate user exists
        usuario = UsuarioRepository.get_by_id(data['id_usuario'])
        if not usuario:
            return {}, f"Usuario with ID {data['id_usuario']} not found"
        
        # Check for duplicate plate if provided
        if data.get('placa'):
            existing = vehiculo_repository.get_by_placa(data['placa'])
            if existing:
                return {}, f"Vehicle with plate '{data['placa']}' already exists"
        
        vehiculo = vehiculo_repository.create(data)
        return vehiculo.to_dict(), None

    @staticmethod
    def update(vehiculo_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """
        Update an existing vehicle asset.
        
        Args:
            vehiculo_id: The ID of the vehicle to update
            data: Dictionary with fields to update
            
        Returns:
            Tuple of (updated vehicle dict, error message or None)
        """
        vehiculo = vehiculo_repository.get_by_id(vehiculo_id)
        if not vehiculo:
            return {}, f"Vehiculo with ID {vehiculo_id} not found"
        
        # Check for duplicate plate if updating plate
        if 'placa' in data and data['placa'] != vehiculo.placa:
            existing = vehiculo_repository.get_by_placa(data['placa'])
            if existing:
                return {}, f"Vehicle with plate '{data['placa']}' already exists"
        
        updated = vehiculo_repository.update(vehiculo, data)
        return updated.to_dict(), None

    @staticmethod
    def delete(vehiculo_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete a vehicle asset.
        
        Args:
            vehiculo_id: The ID of the vehicle to delete
            
        Returns:
            Tuple of (success boolean, error message or None)
        """
        vehiculo = vehiculo_repository.get_by_id(vehiculo_id)
        if not vehiculo:
            return False, f"Vehiculo with ID {vehiculo_id} not found"
        
        vehiculo_repository.delete(vehiculo)
        return True, None
