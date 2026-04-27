"""Blueprint for Usuario (User) API endpoints."""
from flask import Blueprint, jsonify, request
from app.services.usuarios import UsuarioService
from app.security.decorators import authorize_request
from app.security.roles import ADMIN_ROLES, STAFF_ROLES

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')


@usuarios_bp.before_request
def authorize_usuarios_access():
    if request.method == 'OPTIONS':
        return  # Let Flask-CORS handle preflight
    if request.method == 'GET':
        return authorize_request(STAFF_ROLES)
    return authorize_request(ADMIN_ROLES)


@usuarios_bp.route('', methods=['GET'])
def get_all():
    """
    Get all users.
    
    Query Parameters:
        tipo_usuario (optional): Filter by user type (CLIENTE, AGENTE, ADMINISTRADOR, SUPERADMIN)
    
    Returns:
        JSON list of all usuarios
    """
    # Check for tipo_usuario filter
    tipo_usuario = request.args.get('tipo_usuario')
    
    if tipo_usuario:
        usuarios = UsuarioService.get_by_tipo_usuario(tipo_usuario)
    else:
        usuarios = UsuarioService.get_all()
    
    return jsonify({
        'success': True,
        'data': usuarios,
        'count': len(usuarios)
    }), 200


@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def get_by_id(usuario_id: int):
    """
    Get a specific user by ID.
    
    Args:
        usuario_id: The unique identifier
        
    Returns:
        JSON with usuario data or 404 error
    """
    usuario = UsuarioService.get_by_id(usuario_id)
    
    if not usuario:
        return jsonify({
            'success': False,
            'error': f'Usuario with ID {usuario_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': usuario
    }), 200


@usuarios_bp.route('', methods=['POST'])
def create():
    """
    Create a new user.
    
    Expected JSON body:
        Required:
        - tipo_persona: 'PERSONA' or 'EMPRESA'
        - usuario: Username (unique)
        - clave: Password
        - tipo_usuario: 'CLIENTE', 'AGENTE', 'ADMINISTRADOR', or 'SUPERADMIN'
        
        Common (optional):
        - ciudad: City
        - direccion: Address
        - telefono_movil: Mobile phone
        - correo: Email (unique)
        
        For PERSONA:
        - nombre: Full name (required for PERSONA)
        - tipo_documento: Document type
        - numero_documento: Document number
        - edad: Age
        
        For EMPRESA:
        - razon_social: Company name (required for EMPRESA)
        - nit: Tax ID
        - nombre_rep_legal: Legal representative name
        - documento_rep_legal: Legal representative document
        - telefono_rep_legal: Legal representative phone
        - correo_rep_legal: Legal representative email
        - contacto_alternativo: Alternative contact
        
    Returns:
        JSON with created usuario or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    usuario, error = UsuarioService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': usuario,
        'message': 'Usuario created successfully'
    }), 201


@usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])
def update(usuario_id: int):
    """
    Update an existing user.
    
    Args:
        usuario_id: The ID of the usuario to update
        
    Expected JSON body:
        Any of the usuario fields to update
        
    Returns:
        JSON with updated usuario or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    usuario, error = UsuarioService.update(usuario_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': usuario,
        'message': 'Usuario updated successfully'
    }), 200


@usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])
def delete(usuario_id: int):
    """
    Delete a user.
    
    Args:
        usuario_id: The ID of the usuario to delete
        
    Returns:
        JSON with success message or error
    """
    success, error = UsuarioService.delete(usuario_id)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'Usuario with ID {usuario_id} deleted successfully'
    }), 200
