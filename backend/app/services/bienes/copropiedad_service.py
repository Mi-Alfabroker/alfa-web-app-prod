"""Business logic service for Copropiedad (Co-ownership) operations."""
from typing import Optional
from app.models.bienes.copropiedad import Copropiedad
from app.repositories.bienes import copropiedad_repository
from app.repositories.usuario_repository import UsuarioRepository


class CopropiedadService:
    """
    Business Logic Layer for Copropiedad operations.
    
    Orchestrates business rules and delegates data access to the repository.
    """

    @staticmethod
    def get_all() -> list[dict]:
        """
        Get all co-ownership assets.
        
        Returns:
            List of co-ownerships as dictionaries
        """
        copropiedades = copropiedad_repository.get_all()
        return [c.to_dict() for c in copropiedades]

    @staticmethod
    def get_by_id(copropiedad_id: int) -> Optional[dict]:
        """
        Get a co-ownership asset by ID.
        
        Args:
            copropiedad_id: The unique identifier
            
        Returns:
            Co-ownership as dictionary or None if not found
        """
        copropiedad = copropiedad_repository.get_by_id(copropiedad_id)
        return copropiedad.to_dict() if copropiedad else None

    @staticmethod
    def get_by_usuario_id(usuario_id: int) -> list[dict]:
        """
        Get all co-ownership assets for a specific user/client.
        
        Args:
            usuario_id: The user's unique identifier
            
        Returns:
            List of co-ownerships as dictionaries
        """
        copropiedades = copropiedad_repository.get_by_usuario_id(usuario_id)
        return [c.to_dict() for c in copropiedades]

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new co-ownership asset.
        
        Args:
            data: Dictionary with co-ownership fields
            
        Returns:
            Tuple of (created co-ownership dict, error message or None)
        """
        # Validate required fields
        if not data.get('id_usuario'):
            return {}, "Field 'id_usuario' is required"
        
        # Validate user exists
        usuario = UsuarioRepository.get_by_id(data['id_usuario'])
        if not usuario:
            return {}, f"Usuario with ID {data['id_usuario']} not found"
        
        copropiedad = copropiedad_repository.create(data)
        return copropiedad.to_dict(), None

    @staticmethod
    def update(copropiedad_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """
        Update an existing co-ownership asset.
        
        Args:
            copropiedad_id: The ID of the co-ownership to update
            data: Dictionary with fields to update
            
        Returns:
            Tuple of (updated co-ownership dict, error message or None)
        """
        copropiedad = copropiedad_repository.get_by_id(copropiedad_id)
        if not copropiedad:
            return {}, f"Copropiedad with ID {copropiedad_id} not found"
        
        updated = copropiedad_repository.update(copropiedad, data)
        return updated.to_dict(), None

    @staticmethod
    def delete(copropiedad_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete a co-ownership asset.
        
        Args:
            copropiedad_id: The ID of the co-ownership to delete
            
        Returns:
            Tuple of (success boolean, error message or None)
        """
        copropiedad = copropiedad_repository.get_by_id(copropiedad_id)
        if not copropiedad:
            return False, f"Copropiedad with ID {copropiedad_id} not found"
        
        copropiedad_repository.delete(copropiedad)
        return True, None
