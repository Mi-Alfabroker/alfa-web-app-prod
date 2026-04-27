"""Base repository for Poliza (Insurance Policy) data access operations."""
from typing import Optional, TypeVar, Generic, Type, List
from datetime import date
from app.models import db
from app.models.polizas.base_poliza import EstadoPoliza

T = TypeVar('T', bound=db.Model)


class BasePolizaRepository(Generic[T]):
    """
    Generic Data Access Layer for Policy entities.
    
    Provides common CRUD operations for all policy types.
    Following the Repository Pattern to abstract data persistence.
    """
    
    def __init__(self, model_class: Type[T], bien_fk_field: str):
        """
        Initialize the repository.
        
        Args:
            model_class: The SQLAlchemy model class
            bien_fk_field: The name of the foreign key field to the asset (e.g., 'id_hogar')
        """
        self._model_class = model_class
        self._bien_fk_field = bien_fk_field

    def get_all(self) -> List[T]:
        """Retrieve all policies of this type."""
        return self._model_class.query.all()

    def get_by_id(self, poliza_id: int) -> Optional[T]:
        """Retrieve a policy by its ID."""
        return self._model_class.query.get(poliza_id)

    def get_by_consecutivo(self, consecutivo: str) -> Optional[T]:
        """Retrieve a policy by its consecutive identifier."""
        return self._model_class.query.filter_by(consecutivo=consecutivo).first()

    def get_by_bien_id(self, bien_id: int) -> List[T]:
        """Retrieve all policies belonging to a specific asset."""
        return self._model_class.query.filter(
            getattr(self._model_class, self._bien_fk_field) == bien_id
        ).all()

    def get_by_estado(self, estado: str) -> List[T]:
        """Retrieve all policies with a specific state."""
        return self._model_class.query.filter_by(estado=estado).all()

    def get_vigentes(self) -> List[T]:
        """Retrieve all active (VIGENTE) policies."""
        return self.get_by_estado(EstadoPoliza.VIGENTE.value)

    def get_prospectos(self) -> List[T]:
        """Retrieve all prospect (PROSPECTO) policies."""
        return self.get_by_estado(EstadoPoliza.PROSPECTO.value)

    def get_vencidas(self) -> List[T]:
        """Retrieve all expired (VENCIDA) policies."""
        return self.get_by_estado(EstadoPoliza.VENCIDA.value)

    def get_por_vencer(self, dias: int = 30) -> List[T]:
        """
        Retrieve policies that will expire within the specified days.
        
        Args:
            dias: Number of days to check for expiration
            
        Returns:
            List of policies about to expire
        """
        from datetime import timedelta
        fecha_limite = date.today() + timedelta(days=dias)
        return self._model_class.query.filter(
            self._model_class.estado == EstadoPoliza.VIGENTE.value,
            self._model_class.fin_vigencia <= fecha_limite,
            self._model_class.fin_vigencia >= date.today()
        ).all()

    def get_by_aseguradora(self, aseguradora_id: int) -> List[T]:
        """
        Retrieve all policies that include a specific insurance provider.
        
        Args:
            aseguradora_id: The insurance provider ID
            
        Returns:
            List of policies with this provider in any of the 5 options
        """
        from sqlalchemy import or_
        return self._model_class.query.filter(
            or_(
                self._model_class.id_aseguradora_1 == aseguradora_id,
                self._model_class.id_aseguradora_2 == aseguradora_id,
                self._model_class.id_aseguradora_3 == aseguradora_id,
                self._model_class.id_aseguradora_4 == aseguradora_id,
                self._model_class.id_aseguradora_5 == aseguradora_id,
            )
        ).all()

    def create(self, data: dict) -> T:
        """
        Create a new policy.
        
        Args:
            data: Dictionary with policy fields
            
        Returns:
            The created policy instance
        """
        poliza = self._model_class(**data)
        db.session.add(poliza)
        db.session.commit()
        return poliza

    def update(self, poliza: T, data: dict, updatable_fields: List[str]) -> T:
        """
        Update an existing policy.
        
        Args:
            poliza: The policy instance to update
            data: Dictionary with fields to update
            updatable_fields: List of field names that can be updated
            
        Returns:
            The updated policy instance
        """
        for field in updatable_fields:
            if field in data:
                setattr(poliza, field, data[field])
        
        db.session.commit()
        return poliza

    def update_estado(self, poliza: T, nuevo_estado: str) -> T:
        """
        Update the policy state.
        
        Args:
            poliza: The policy instance
            nuevo_estado: The new state value
            
        Returns:
            The updated policy instance
        """
        poliza.estado = nuevo_estado
        db.session.commit()
        return poliza

    def delete(self, poliza: T) -> bool:
        """
        Delete a policy.
        
        Args:
            poliza: The policy instance to delete
            
        Returns:
            True if deletion was successful
        """
        db.session.delete(poliza)
        db.session.commit()
        return True

    def exists_consecutivo(self, consecutivo: str) -> bool:
        """Check if a policy with this consecutive already exists."""
        return self._model_class.query.filter_by(consecutivo=consecutivo).first() is not None
