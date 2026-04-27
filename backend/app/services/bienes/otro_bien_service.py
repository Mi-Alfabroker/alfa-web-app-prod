"""Business logic service for OtroBien (Other Asset) operations."""
from typing import Optional
from app.models.bienes.otro_bien import OtroBien
from app.repositories.bienes import otro_bien_repository
from app.repositories.usuario_repository import UsuarioRepository


class OtroBienService:
    """
    Business Logic Layer for OtroBien operations.
    
    Orchestrates business rules and delegates data access to the repository.
    """

    @staticmethod
    def get_all() -> list[dict]:
        """
        Get all other assets.
        
        Returns:
            List of other assets as dictionaries
        """
        otros_bienes = otro_bien_repository.get_all()
        return [o.to_dict() for o in otros_bienes]

    @staticmethod
    def get_by_id(otro_bien_id: int) -> Optional[dict]:
        """
        Get an other asset by ID.
        
        Args:
            otro_bien_id: The unique identifier
            
        Returns:
            Other asset as dictionary or None if not found
        """
        otro_bien = otro_bien_repository.get_by_id(otro_bien_id)
        return otro_bien.to_dict() if otro_bien else None

    @staticmethod
    def get_by_usuario_id(usuario_id: int) -> list[dict]:
        """
        Get all other assets for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of other assets as dictionaries
        """
        otros_bienes = otro_bien_repository.get_by_usuario_id(usuario_id)
        return [o.to_dict() for o in otros_bienes]

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new other asset.
        
        Args:
            data: Dictionary with other asset fields
            
        Returns:
            Tuple of (created other asset dict, error message or None)
        """
        # Validate required fields
        if not data.get('id_usuario'):
            return {}, "Field 'id_usuario' is required"
        
        # Validate user exists
        usuario = UsuarioRepository.get_by_id(data['id_usuario'])
        if not usuario:
            return {}, f"Usuario with ID {data['id_usuario']} not found"
        
        otro_bien = otro_bien_repository.create(data)
        return otro_bien.to_dict(), None

    @staticmethod
    def update(otro_bien_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """
        Update an existing other asset.
        
        Args:
            otro_bien_id: The ID of the other asset to update
            data: Dictionary with fields to update
            
        Returns:
            Tuple of (updated other asset dict, error message or None)
        """
        otro_bien = otro_bien_repository.get_by_id(otro_bien_id)
        if not otro_bien:
            return {}, f"OtroBien with ID {otro_bien_id} not found"
        
        updated = otro_bien_repository.update(otro_bien, data)
        return updated.to_dict(), None

    @staticmethod
    def delete(otro_bien_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete an other asset.
        
        Args:
            otro_bien_id: The ID of the other asset to delete
            
        Returns:
            Tuple of (success boolean, error message or None)
        """
        otro_bien = otro_bien_repository.get_by_id(otro_bien_id)
        if not otro_bien:
            return False, f"OtroBien with ID {otro_bien_id} not found"
        
        otro_bien_repository.delete(otro_bien)
        return True, None
