"""Repository for Usuario data access operations."""
from typing import Optional
from app.models import db
from app.models.usuario import Usuario


class UsuarioRepository:
    """
    Data Access Layer for Usuario entities.
    
    Handles all database CRUD operations for users.
    Following the Repository Pattern to abstract data persistence.
    """

    @staticmethod
    def get_all() -> list[Usuario]:
        """Retrieve all users."""
        return Usuario.query.all()

    @staticmethod
    def get_by_id(usuario_id: int) -> Optional[Usuario]:
        """Retrieve a user by its ID."""
        return Usuario.query.get(usuario_id)

    @staticmethod
    def get_by_usuario(usuario: str) -> Optional[Usuario]:
        """Retrieve a user by username."""
        return Usuario.query.filter_by(usuario=usuario).first()

    @staticmethod
    def get_by_correo(correo: str) -> Optional[Usuario]:
        """Retrieve a user by email."""
        return Usuario.query.filter_by(correo=correo).first()

    @staticmethod
    def get_by_tipo_usuario(tipo_usuario: str) -> list[Usuario]:
        """Retrieve all users of a specific type."""
        return Usuario.query.filter_by(tipo_usuario=tipo_usuario).all()

    @staticmethod
    def get_by_tipo_persona(tipo_persona: str) -> list[Usuario]:
        """Retrieve all users of a specific person type."""
        return Usuario.query.filter_by(tipo_persona=tipo_persona).all()

    @staticmethod
    def create(data: dict) -> Usuario:
        """
        Create a new user.
        
        Args:
            data: Dictionary with usuario fields
            
        Returns:
            The created Usuario instance
        """
        usuario = Usuario(
            # Required fields
            tipo_persona=data.get('tipo_persona'),
            usuario=data.get('usuario'),
            clave=data.get('clave'),
            tipo_usuario=data.get('tipo_usuario'),
            # Common fields
            ciudad=data.get('ciudad'),
            direccion=data.get('direccion'),
            telefono_movil=data.get('telefono_movil'),
            correo=data.get('correo'),
            # Persona natural fields
            tipo_documento=data.get('tipo_documento'),
            numero_documento=data.get('numero_documento'),
            nombre=data.get('nombre'),
            edad=data.get('edad'),
            # Empresa fields
            nit=data.get('nit'),
            razon_social=data.get('razon_social'),
            nombre_rep_legal=data.get('nombre_rep_legal'),
            documento_rep_legal=data.get('documento_rep_legal'),
            telefono_rep_legal=data.get('telefono_rep_legal'),
            correo_rep_legal=data.get('correo_rep_legal'),
            contacto_alternativo=data.get('contacto_alternativo'),
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def update(usuario: Usuario, data: dict) -> Usuario:
        """
        Update an existing user.
        
        Args:
            usuario: The Usuario instance to update
            data: Dictionary with fields to update
            
        Returns:
            The updated Usuario instance
        """
        updatable_fields = [
            # Type fields
            'tipo_persona', 'tipo_usuario',
            # Common fields
            'ciudad', 'direccion', 'telefono_movil', 'correo',
            'usuario', 'clave',
            # Persona natural fields
            'tipo_documento', 'numero_documento', 'nombre', 'edad',
            # Empresa fields
            'nit', 'razon_social', 'nombre_rep_legal', 'documento_rep_legal',
            'telefono_rep_legal', 'correo_rep_legal', 'contacto_alternativo',
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(usuario, field, data[field])
        
        db.session.commit()
        return usuario

    @staticmethod
    def delete(usuario: Usuario) -> bool:
        """
        Delete a user.
        
        Args:
            usuario: The Usuario instance to delete
            
        Returns:
            True if deletion was successful
        """
        db.session.delete(usuario)
        db.session.commit()
        return True
