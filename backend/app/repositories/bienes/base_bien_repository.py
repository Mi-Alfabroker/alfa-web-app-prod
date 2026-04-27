"""Base repository for Bien (Asset) data access operations."""
from typing import Optional, TypeVar, Generic, Type
from app.models import db

T = TypeVar('T', bound=db.Model)


class BaseBienRepository(Generic[T]):
    """
    Generic Data Access Layer for Asset entities.
    
    Provides common CRUD operations for all asset types.
    Following the Repository Pattern to abstract data persistence.
    """
    
    def __init__(self, model_class: Type[T]):
        self._model_class = model_class

    def get_all(self) -> list[T]:
        """Retrieve all assets of this type."""
        return self._model_class.query.all()

    def get_by_id(self, bien_id: int) -> Optional[T]:
        """Retrieve an asset by its ID."""
        return self._model_class.query.get(bien_id)

    def get_by_usuario_id(self, usuario_id: int) -> list[T]:
        """Retrieve all assets belonging to a specific user/client."""
        return self._model_class.query.filter_by(id_usuario=usuario_id).all()

    def create(self, data: dict) -> T:
        """
        Create a new asset.
        
        Args:
            data: Dictionary with asset fields
            
        Returns:
            The created asset instance
        """
        bien = self._model_class(**data)
        db.session.add(bien)
        db.session.commit()
        return bien

    def update(self, bien: T, data: dict, updatable_fields: list[str]) -> T:
        """
        Update an existing asset.
        
        Args:
            bien: The asset instance to update
            data: Dictionary with fields to update
            updatable_fields: List of field names that can be updated
            
        Returns:
            The updated asset instance
        """
        for field in updatable_fields:
            if field in data:
                setattr(bien, field, data[field])
        
        db.session.commit()
        return bien

    def delete(self, bien: T) -> bool:
        """
        Delete an asset.
        
        Args:
            bien: The asset instance to delete
            
        Returns:
            True if deletion was successful
        """
        db.session.delete(bien)
        db.session.commit()
        return True
