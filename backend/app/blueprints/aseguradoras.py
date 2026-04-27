"""Blueprint for Aseguradora (Insurance Provider) API endpoints."""
from flask import Blueprint, jsonify, request
from app.services.aseguradoras import AseguradoraService
from app.security.decorators import authorize_request
from app.security.roles import ADMIN_ROLES, STAFF_ROLES

aseguradoras_bp = Blueprint('aseguradoras', __name__, url_prefix='/api/aseguradoras')


@aseguradoras_bp.before_request
def authorize_aseguradoras_access():
    if request.method == 'OPTIONS':
        return  # Let Flask-CORS handle preflight
    if request.method == 'GET':
        return authorize_request(STAFF_ROLES)
    return authorize_request(ADMIN_ROLES)


@aseguradoras_bp.route('', methods=['GET'])
def get_all():
    """
    Get all insurance providers.
    
    Returns:
        JSON list of all aseguradoras
    """
    aseguradoras = AseguradoraService.get_all()
    return jsonify({
        'success': True,
        'data': aseguradoras,
        'count': len(aseguradoras)
    }), 200


@aseguradoras_bp.route('/<int:aseguradora_id>', methods=['GET'])
def get_by_id(aseguradora_id: int):
    """
    Get a specific insurance provider by ID.
    
    Args:
        aseguradora_id: The unique identifier
        
    Returns:
        JSON with aseguradora data or 404 error
    """
    aseguradora = AseguradoraService.get_by_id(aseguradora_id)
    
    if not aseguradora:
        return jsonify({
            'success': False,
            'error': f'Aseguradora with ID {aseguradora_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': aseguradora
    }), 200


@aseguradoras_bp.route('/<int:aseguradora_id>/datos-entrega', methods=['GET'])
def get_datos_entrega(aseguradora_id: int):
    """
    Get insurance provider data for policy delivery form.
    
    Returns only the essential fields needed for auto-filling
    the policy delivery form (nombre, numeral_asistencia).
    
    Args:
        aseguradora_id: The unique identifier
        
    Returns:
        JSON with essential aseguradora data or 404 error
    """
    aseguradora = AseguradoraService.get_by_id(aseguradora_id)
    
    if not aseguradora:
        return jsonify({
            'success': False,
            'error': f'Aseguradora with ID {aseguradora_id} not found'
        }), 404
    
    # Return only essential fields for delivery form
    return jsonify({
        'success': True,
        'data': {
            'id': aseguradora.get('id'),
            'nombre': aseguradora.get('nombre'),
            'numeral_asistencia': aseguradora.get('numeral_asistencia'),
        }
    }), 200


@aseguradoras_bp.route('', methods=['POST'])
def create():
    """
    Create a new insurance provider.
    
    Expected JSON body:
        - nombre (required): Name of the insurance provider
        - numeral_asistencia: Assistance phone number
        - correo_comercial: Commercial email
        - correo_reclamaciones: Claims email
        - direccion_oficina: Office address
        - contacto_asignado: Assigned contact person
        - ruta_logo: Path to logo image
        - ruta_pais_logo: Path to country flag image
        - respaldo_aseguradora: Backing company information
        
    Returns:
        JSON with created aseguradora or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    aseguradora, error = AseguradoraService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': aseguradora,
        'message': 'Aseguradora created successfully'
    }), 201


@aseguradoras_bp.route('/<int:aseguradora_id>', methods=['PUT'])
def update(aseguradora_id: int):
    """
    Update an existing insurance provider.
    
    Args:
        aseguradora_id: The ID of the aseguradora to update
        
    Expected JSON body:
        Any of the aseguradora fields to update
        
    Returns:
        JSON with updated aseguradora or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    aseguradora, error = AseguradoraService.update(aseguradora_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': aseguradora,
        'message': 'Aseguradora updated successfully'
    }), 200


@aseguradoras_bp.route('/<int:aseguradora_id>', methods=['DELETE'])
def delete(aseguradora_id: int):
    """
    Delete an insurance provider.
    
    Args:
        aseguradora_id: The ID of the aseguradora to delete
        
    Returns:
        JSON with success message or error
    """
    success, error = AseguradoraService.delete(aseguradora_id)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'Aseguradora with ID {aseguradora_id} deleted successfully'
    }), 200
