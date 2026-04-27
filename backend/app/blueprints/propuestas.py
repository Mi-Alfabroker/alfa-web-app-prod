"""Blueprint for Propuestas (Insurance Proposals) API endpoints."""
from flask import Blueprint, jsonify, request, send_file
from app.services.propuestas import PropuestaService
from app.security.decorators import authorize_request
from app.security.roles import STAFF_ROLES

propuestas_bp = Blueprint('propuestas', __name__, url_prefix='/api/propuestas')


@propuestas_bp.before_request
def authorize_propuestas_access():
    if request.method == 'OPTIONS':
        return  # Let Flask-CORS handle preflight
    return authorize_request(STAFF_ROLES)


@propuestas_bp.route('/templates', methods=['GET'])
def get_templates():
    """
    Get available proposal templates.
    
    Returns:
        JSON list of available template names
    """
    templates = PropuestaService.get_available_templates()
    return jsonify({
        'success': True,
        'data': templates,
        'count': len(templates)
    }), 200


@propuestas_bp.route('/generate', methods=['POST'])
def generate_proposal():
    """
    Generate a proposal document from a template.
    
    Expected JSON body:
        - template_name (required): Name of template to use (e.g., 'copropiedades')
        - variables (required): Dictionary of variables to replace
          Format: {"[key]": "value", "[2]": "2026-2027", ...}
        - imagenes (optional): Dictionary of images to replace by alternative text
          Format: {"logo_aseg_1": "mapfre", "bandera_aseg_2": "sura", ...}
          Keys should match image alternative text in Excel (e.g., logo_aseg_X, bandera_aseg_X)
          Values are the image name (lowercase, without extension). 
          Images are searched in:
            - logos_aseguradoras/{value}.png for keys starting with 'logo_aseg'
            - banderas_aseguradoras/{value}.png for keys starting with 'bandera_aseg'
    
    Returns:
        Excel file as attachment or JSON error
    
    Example request body:
        {
            "template_name": "copropiedades",
            "variables": {
                "[2]": "2026-2027",
                "[3]": "Juan Pérez García",
                "[4]": "1234567890"
            },
            "imagenes": {
                "logo_aseg_1": "mapfre",
                "logo_aseg_2": "sura",
                "bandera_aseg_1": "mapfre",
                "bandera_aseg_2": "sura"
            }
        }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    # Extract and validate required fields
    template_name = data.get('template_name')
    if not template_name:
        return jsonify({
            'success': False,
            'error': "Field 'template_name' is required"
        }), 400
    
    variables = data.get('variables')
    if not variables:
        return jsonify({
            'success': False,
            'error': "Field 'variables' is required"
        }), 400
    
    # Extract optional images
    imagenes = data.get('imagenes')
    
    # Validate variables format
    is_valid, validation_error = PropuestaService.validate_variables(variables)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': validation_error
        }), 400
    
    # Generate the proposal
    file_buffer, filename, saved_path, error = PropuestaService.generate_proposal(
        template_name=template_name,
        variables=variables,
        imagenes=imagenes
    )
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    # Return the generated file
    response = send_file(
        file_buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )
    
    # Add custom header with saved path info
    response.headers['X-Saved-Path'] = saved_path
    
    return response


@propuestas_bp.route('/preview', methods=['POST'])
def preview_proposal():
    """
    Preview which variables would be replaced without generating the file.
    
    Useful for debugging and validation purposes.
    
    Expected JSON body:
        - template_name (required): Name of template to use
        - variables (required): Dictionary of variables to replace
        
    Returns:
        JSON with validation status and variable summary
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    template_name = data.get('template_name')
    variables = data.get('variables', {})
    
    # Validate template
    available_templates = PropuestaService.get_available_templates()
    template_exists = template_name in available_templates
    
    # Validate variables
    is_valid, validation_error = PropuestaService.validate_variables(variables)
    
    return jsonify({
        'success': True,
        'data': {
            'template_name': template_name,
            'template_exists': template_exists,
            'available_templates': available_templates,
            'variables_count': len(variables) if variables else 0,
            'variables_valid': is_valid,
            'validation_error': validation_error,
            'sample_variables': dict(list(variables.items())[:5]) if variables else {}
        }
    }), 200
