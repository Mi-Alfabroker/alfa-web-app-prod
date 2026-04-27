"""Business logic service for Hogar (Home) operations."""
from typing import Optional
from app.models.bienes.hogar import Hogar
from app.repositories.bienes import hogar_repository
from app.repositories.usuario_repository import UsuarioRepository


class HogarService:
    """
    Business Logic Layer for Hogar operations.
    
    Orchestrates business rules and delegates data access to the repository.
    """

    @staticmethod
    def get_all() -> list[dict]:
        """
        Get all home assets.
        
        Returns:
            List of homes as dictionaries
        """
        hogares = hogar_repository.get_all()
        return [h.to_dict() for h in hogares]

    @staticmethod
    def get_by_id(hogar_id: int) -> Optional[dict]:
        """
        Get a home asset by ID.
        
        Args:
            hogar_id: The unique identifier
            
        Returns:
            Home as dictionary or None if not found
        """
        hogar = hogar_repository.get_by_id(hogar_id)
        return hogar.to_dict() if hogar else None

    @staticmethod
    def get_by_usuario_id(usuario_id: int) -> list[dict]:
        """
        Get all home assets for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of homes as dictionaries
        """
        hogares = hogar_repository.get_by_usuario_id(usuario_id)
        return [h.to_dict() for h in hogares]

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new home asset.
        
        Args:
            data: Dictionary with home fields
            
        Returns:
            Tuple of (created home dict, error message or None)
        """
        # Validate required fields
        if not data.get('id_usuario'):
            return {}, "Field 'id_usuario' is required"
        
        # Validate user exists
        usuario = UsuarioRepository.get_by_id(data['id_usuario'])
        if not usuario:
            return {}, f"Usuario with ID {data['id_usuario']} not found"
        
        hogar = hogar_repository.create(data)
        return hogar.to_dict(), None

    @staticmethod
    def update(hogar_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """
        Update an existing home asset.
        
        Args:
            hogar_id: The ID of the home to update
            data: Dictionary with fields to update
            
        Returns:
            Tuple of (updated home dict, error message or None)
        """
        hogar = hogar_repository.get_by_id(hogar_id)
        if not hogar:
            return {}, f"Hogar with ID {hogar_id} not found"
        
        updated = hogar_repository.update(hogar, data)
        return updated.to_dict(), None

    @staticmethod
    def delete(hogar_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete a home asset.
        
        Args:
            hogar_id: The ID of the home to delete
            
        Returns:
            Tuple of (success boolean, error message or None)
        """
        hogar = hogar_repository.get_by_id(hogar_id)
        if not hogar:
            return False, f"Hogar with ID {hogar_id} not found"
        
        hogar_repository.delete(hogar)
        return True, None
