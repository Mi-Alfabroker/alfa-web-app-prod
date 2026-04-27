"""Business logic service for Usuario operations."""
from typing import Optional
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.security import hash_password


# Valid values for tipo_persona and tipo_usuario
VALID_TIPOS_PERSONA = ['PERSONA', 'EMPRESA']
VALID_TIPOS_USUARIO = ['CLIENTE', 'AGENTE', 'ADMINISTRADOR', 'SUPERADMIN']


class UsuarioService:
    """
    Business Logic Layer for Usuario operations.
    
    Orchestrates business rules and delegates data access to the repository.
    """

    @staticmethod
    def get_all() -> list[dict]:
        """
        Get all users.
        
        Returns:
            List of usuarios as dictionaries
        """
        usuarios = UsuarioRepository.get_all()
        return [u.to_dict() for u in usuarios]

    @staticmethod
    def get_by_id(usuario_id: int) -> Optional[dict]:
        """
        Get a user by ID.
        
        Args:
            usuario_id: The unique identifier
            
        Returns:
            Usuario as dictionary or None if not found
        """
        usuario = UsuarioRepository.get_by_id(usuario_id)
        return usuario.to_dict() if usuario else None

    @staticmethod
    def get_by_tipo_usuario(tipo_usuario: str) -> list[dict]:
        """
        Get all users of a specific type.
        
        Args:
            tipo_usuario: User type (CLIENTE, AGENTE, ADMINISTRADOR, SUPERADMIN)
            
        Returns:
            List of usuarios as dictionaries
        """
        usuarios = UsuarioRepository.get_by_tipo_usuario(tipo_usuario.upper())
        return [u.to_dict() for u in usuarios]

    @staticmethod
    def _validate_required_fields(data: dict) -> Optional[str]:
        """Validate required fields are present."""
        required = ['tipo_persona', 'usuario', 'clave', 'tipo_usuario']
        missing = [field for field in required if not data.get(field)]
        
        if missing:
            return f"Required fields missing: {', '.join(missing)}"
        return None

    @staticmethod
    def _validate_tipo_values(data: dict) -> Optional[str]:
        """Validate tipo_persona and tipo_usuario values."""
        tipo_persona = data.get('tipo_persona', '').upper()
        tipo_usuario = data.get('tipo_usuario', '').upper()
        
        if tipo_persona and tipo_persona not in VALID_TIPOS_PERSONA:
            return f"tipo_persona must be one of: {', '.join(VALID_TIPOS_PERSONA)}"
        
        if tipo_usuario and tipo_usuario not in VALID_TIPOS_USUARIO:
            return f"tipo_usuario must be one of: {', '.join(VALID_TIPOS_USUARIO)}"
        
        return None

    @staticmethod
    def _validate_persona_fields(data: dict) -> Optional[str]:
        """Validate required fields for persona natural."""
        tipo_persona = data.get('tipo_persona', '').upper()
        
        if tipo_persona == 'PERSONA':
            if not data.get('nombre'):
                return "Field 'nombre' is required for PERSONA"
        
        if tipo_persona == 'EMPRESA':
            if not data.get('razon_social'):
                return "Field 'razon_social' is required for EMPRESA"
        
        return None

    @staticmethod
    def create(data: dict) -> tuple[dict, Optional[str]]:
        """
        Create a new user.
        
        Args:
            data: Dictionary with usuario fields
            
        Returns:
            Tuple of (created usuario dict, error message or None)
        """
        # Validate required fields
        error = UsuarioService._validate_required_fields(data)
        if error:
            return {}, error
        
        # Validate tipo values
        error = UsuarioService._validate_tipo_values(data)
        if error:
            return {}, error
        
        # Validate persona-specific fields
        error = UsuarioService._validate_persona_fields(data)
        if error:
            return {}, error
        
        # Check for duplicate username
        existing = UsuarioRepository.get_by_usuario(data['usuario'])
        if existing:
            return {}, f"Username '{data['usuario']}' already exists"
        
        # Check for duplicate email if provided
        if data.get('correo'):
            existing = UsuarioRepository.get_by_correo(data['correo'])
            if existing:
                return {}, f"Email '{data['correo']}' already exists"
        
        # Normalize tipo values to uppercase
        data['tipo_persona'] = data['tipo_persona'].upper()
        data['tipo_usuario'] = data['tipo_usuario'].upper()
        data['clave'] = hash_password(data['clave'])
        
        usuario = UsuarioRepository.create(data)
        return usuario.to_dict(), None

    @staticmethod
    def update(usuario_id: int, data: dict) -> tuple[dict, Optional[str]]:
        """
        Update an existing user.
        
        Args:
            usuario_id: The ID of the usuario to update
            data: Dictionary with fields to update
            
        Returns:
            Tuple of (updated usuario dict, error message or None)
        """
        usuario = UsuarioRepository.get_by_id(usuario_id)
        if not usuario:
            return {}, f"Usuario with ID {usuario_id} not found"
        
        # Validate tipo values if provided
        error = UsuarioService._validate_tipo_values(data)
        if error:
            return {}, error
        
        # If updating username, check for duplicates
        if 'usuario' in data and data['usuario'] != usuario.usuario:
            existing = UsuarioRepository.get_by_usuario(data['usuario'])
            if existing:
                return {}, f"Username '{data['usuario']}' already exists"
        
        # If updating email, check for duplicates
        if 'correo' in data and data['correo'] != usuario.correo:
            existing = UsuarioRepository.get_by_correo(data['correo'])
            if existing:
                return {}, f"Email '{data['correo']}' already exists"
        
        # Normalize tipo values if provided
        if 'tipo_persona' in data:
            data['tipo_persona'] = data['tipo_persona'].upper()
        if 'tipo_usuario' in data:
            data['tipo_usuario'] = data['tipo_usuario'].upper()
        if 'clave' in data and data['clave']:
            data['clave'] = hash_password(data['clave'])
        
        updated = UsuarioRepository.update(usuario, data)
        return updated.to_dict(), None

    @staticmethod
    def delete(usuario_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete a user.
        
        Args:
            usuario_id: The ID of the usuario to delete
            
        Returns:
            Tuple of (success boolean, error message or None)
        """
        usuario = UsuarioRepository.get_by_id(usuario_id)
        if not usuario:
            return False, f"Usuario with ID {usuario_id} not found"
        
        UsuarioRepository.delete(usuario)
        return True, None
