"""Business logic service for Aseguradora operations."""
from typing import Optional
from app.models.aseguradora import Aseguradora
from app.repositories.aseguradora_repository import AseguradoraRepository


class AseguradoraService:
    """
    Business Logic Layer for Aseguradora operations.
    
    Orchestrates business rules and delegates data access to the repository.
    """

    @staticmethod
    def get_all() -> list[dict]:
        """
        Get all insurance providers.
        
        Returns:
            List of aseguradoras as dictionaries
        """
        aseguradoras = AseguradoraRepository.get_all()
        return [a.to_dict() for a in aseguradoras]

    @staticmethod
    def get_by_id(aseguradora_id: int) -> Optional[dict]:
        """
        Get an insurance provider by ID.
        
        Args:
            aseguradora_id: The unique identifier
            
        Returns:
            Aseguradora as dictionary or None if not found
        """
        aseguradora = AseguradoraRepository.get_by_id(aseguradora_id)
        return aseguradora.to_dict() if aseguradora else None

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new insurance provider.
        
        Args:
            data: Dictionary with aseguradora fields
            
        Returns:
            Tuple of (created aseguradora dict, error message or None)
        """
        # Validate required fields
        if not data.get('nombre'):
            return {}, "Field 'nombre' is required"
        
        # Check for duplicate name
        existing = AseguradoraRepository.get_by_nombre(data['nombre'])
        if existing:
            return {}, f"Aseguradora with name '{data['nombre']}' already exists"
        
        aseguradora = AseguradoraRepository.create(data)
        return aseguradora.to_dict(), None

    @staticmethod
    def update(aseguradora_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """
        Update an existing insurance provider.
        
        Args:
            aseguradora_id: The ID of the aseguradora to update
            data: Dictionary with fields to update
            
        Returns:
            Tuple of (updated aseguradora dict, error message or None)
        """
        aseguradora = AseguradoraRepository.get_by_id(aseguradora_id)
        if not aseguradora:
            return {}, f"Aseguradora with ID {aseguradora_id} not found"
        
        # If updating name, check for duplicates
        if 'nombre' in data and data['nombre'] != aseguradora.nombre:
            existing = AseguradoraRepository.get_by_nombre(data['nombre'])
            if existing:
                return {}, f"Aseguradora with name '{data['nombre']}' already exists"
        
        updated = AseguradoraRepository.update(aseguradora, data)
        return updated.to_dict(), None

    @staticmethod
    def delete(aseguradora_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete an insurance provider.
        
        Args:
            aseguradora_id: The ID of the aseguradora to delete
            
        Returns:
            Tuple of (success boolean, error message or None)
        """
        aseguradora = AseguradoraRepository.get_by_id(aseguradora_id)
        if not aseguradora:
            return False, f"Aseguradora with ID {aseguradora_id} not found"
        
        AseguradoraRepository.delete(aseguradora)
        return True, None
