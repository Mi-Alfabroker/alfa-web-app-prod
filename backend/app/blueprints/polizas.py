"""Blueprint for Polizas (Insurance Policies) API endpoints."""
from flask import Blueprint, jsonify, request, make_response
from app.services.polizas import (
    PolizaHogarService,
    PolizaVehiculoService,
    PolizaCopropiedadService,
    PolizaOtroBienService
)
from app.security.decorators import authorize_request
from app.security.roles import ADMIN_ROLES, STAFF_ROLES

polizas_bp = Blueprint('polizas', __name__, url_prefix='/api/polizas')


@polizas_bp.before_request
def authorize_polizas_access():
    if request.method == 'OPTIONS':
        # Return empty response for CORS preflight
        response = make_response()
        response.status_code = 200
        return response
    if request.method == 'DELETE':
        return authorize_request(ADMIN_ROLES)
    return authorize_request(STAFF_ROLES)


# List of numeric fields that should be converted to integers
NUMERIC_FIELDS = [
    'valor_prima_aseg_1', 'valor_prima_aseg_2', 'valor_prima_aseg_3',
    'valor_prima_aseg_4', 'valor_prima_aseg_5',
    'id_aseguradora_1', 'id_aseguradora_2', 'id_aseguradora_3',
    'id_aseguradora_4', 'id_aseguradora_5',
    'aseguradora_seleccionada',
    'valor_prima_neta', 'valor_otros_costos', 'valor_iva', 'ingreso_comision_percibido',
    'valor_inmueble_asegurado', 'valor_contenidos_normales_asegurado',
    'valor_contenidos_especiales_asegurado', 'valor_equipo_electronico_asegurado',
    'valor_maquinaria_equipo_asegurado', 'valor_rc_asegurado',
    'valor_vehiculo_asegurado', 'valor_accesorios_asegurado',
    'valor_area_comun_asegurado', 'valor_area_privada_asegurado',
    'valor_muebles_asegurado', 'valor_directores_asegurado',
    'valor_rce_asegurado', 'valor_manejo_asegurado',
    'valor_transporte_valores_vigencia_asegurado', 'valor_transporte_valores_despacho_asegurado',
    'valor_bien_asegurado',
    # Delivery/Entrega fields
    'valor_total_prima',
    'financiacion_num_cuotas', 'financiacion_cuota_actual', 'financiacion_valor_cuota',
    'valor_cuota_3', 'valor_cuota_5', 'valor_cuota_8', 'valor_cuota_11',
]


def sanitize_numeric_fields(data: dict) -> dict:
    """
    Sanitize numeric fields in the data dictionary.
    Converts empty strings and invalid values to None,
    and ensures numeric values are integers.
    """
    sanitized = data.copy()
    for field in NUMERIC_FIELDS:
        if field in sanitized:
            value = sanitized[field]
            if value is None or value == '' or value == 'undefined':
                sanitized[field] = None
            elif isinstance(value, str):
                try:
                    sanitized[field] = int(value)
                except (ValueError, TypeError):
                    sanitized[field] = None
            elif isinstance(value, (int, float)):
                sanitized[field] = int(value)
    return sanitized


# =============================================================================
# POLIZAS HOGAR (Home Insurance Policies) Endpoints
# =============================================================================

@polizas_bp.route('/hogar', methods=['GET'])
def get_all_polizas_hogar():
    """
    Get all home insurance policies.
    
    Query params:
        - hogar_id: Optional filter by home asset ID
        - usuario_id: Optional filter by user ID
        - estado: Optional filter by state (PROSPECTO, VIGENTE, VENCIDA, CANCELADA)
    
    Returns:
        JSON list of all home policies
    """
    hogar_id = request.args.get('hogar_id', type=int)
    usuario_id = request.args.get('usuario_id', type=int)
    estado = request.args.get('estado', type=str)
    
    if hogar_id:
        polizas = PolizaHogarService.get_by_hogar_id(hogar_id)
    elif usuario_id:
        polizas = PolizaHogarService.get_by_usuario_id(usuario_id)
    elif estado:
        polizas = PolizaHogarService.get_by_estado(estado)
    else:
        polizas = PolizaHogarService.get_all()
    
    return jsonify({
        'success': True,
        'data': polizas,
        'count': len(polizas)
    }), 200


@polizas_bp.route('/hogar/<int:poliza_id>', methods=['GET'])
def get_poliza_hogar_by_id(poliza_id: int):
    """Get a specific home insurance policy by ID."""
    poliza = PolizaHogarService.get_by_id(poliza_id)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaHogar with ID {poliza_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/hogar/consecutivo/<string:consecutivo>', methods=['GET'])
def get_poliza_hogar_by_consecutivo(consecutivo: str):
    """Get a home insurance policy by consecutive identifier."""
    poliza = PolizaHogarService.get_by_consecutivo(consecutivo)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaHogar with consecutivo {consecutivo} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/hogar', methods=['POST'])
def create_poliza_hogar():
    """
    Create a new home insurance policy.
    
    Expected JSON body:
        - id_hogar (required): Home asset ID
        - fecha_consecutivo: Optional date for consecutive generation (defaults to today)
        - inicio_vigencia: Start date of coverage
        - fin_vigencia: End date of coverage
        - id_aseguradora_1 to id_aseguradora_5: Insurance provider IDs
        - valor_prima_aseg_1 to valor_prima_aseg_5: Premium values
        - valor_inmueble_asegurado: Insured property value
        - valor_contenidos_normales_asegurado: Normal contents insured value
        - valor_contenidos_especiales_asegurado: Special contents insured value
        - valor_equipo_electronico_asegurado: Electronic equipment insured value
        - valor_maquinaria_equipo_asegurado: Machinery insured value
        - valor_rc_asegurado: RC insured value
        - valor_prima_neta: Net premium value
        - valor_otros_costos: Other costs
        - valor_iva: IVA value
        - ingreso_comision_percibido: Commission income
        
    Returns:
        JSON with created policy or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaHogarService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaHogar created successfully'
    }), 201


@polizas_bp.route('/hogar/<int:poliza_id>', methods=['PUT'])
def update_poliza_hogar(poliza_id: int):
    """Update an existing home insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaHogarService.update(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaHogar updated successfully'
    }), 200


@polizas_bp.route('/hogar/<int:poliza_id>/estado', methods=['PATCH'])
def cambiar_estado_poliza_hogar(poliza_id: int):
    """
    Change the state of a home insurance policy.
    
    Expected JSON body:
        - estado (required): New state (PROSPECTO, VIGENTE, VENCIDA, CANCELADA)
        - aseguradora_seleccionada: Required when changing to VIGENTE (1-5)
    """
    data = request.get_json()
    
    if not data or 'estado' not in data:
        return jsonify({
            'success': False,
            'error': 'Field estado is required'
        }), 400
    
    poliza, error = PolizaHogarService.cambiar_estado(
        poliza_id, 
        data['estado'],
        data.get('aseguradora_seleccionada')
    )
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': f'PolizaHogar state changed to {data["estado"]} successfully'
    }), 200


@polizas_bp.route('/hogar/<int:poliza_id>/validar', methods=['GET'])
def validar_poliza_hogar(poliza_id: int):
    """Validate insured values against appraisal values for a home policy."""
    is_valid, errores = PolizaHogarService.validar_valores_asegurados(poliza_id)
    
    return jsonify({
        'success': True,
        'data': {
            'is_valid': is_valid,
            'errores': errores
        }
    }), 200


@polizas_bp.route('/hogar/<int:poliza_id>/entregar', methods=['POST', 'OPTIONS'])
def entregar_poliza_hogar(poliza_id: int):
    """Deliver a home insurance policy (PROSPECTO -> VIGENTE)."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaHogarService.entregar_poliza(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaHogar entregada exitosamente'
    }), 200


@polizas_bp.route('/hogar/<int:poliza_id>/actualizar-entrega', methods=['PATCH', 'OPTIONS'])
def actualizar_entrega_hogar(poliza_id: int):
    """Update delivery data for a home insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaHogarService.actualizar_entrega(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'Datos de entrega actualizados exitosamente'
    }), 200


@polizas_bp.route('/hogar/<int:poliza_id>', methods=['DELETE'])
def delete_poliza_hogar(poliza_id: int):
    """Delete a home insurance policy."""
    success, error = PolizaHogarService.delete(poliza_id)
    
    if not success:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'message': f'PolizaHogar with ID {poliza_id} deleted successfully'
    }), 200


# =============================================================================
# POLIZAS VEHICULO (Vehicle Insurance Policies) Endpoints
# =============================================================================

@polizas_bp.route('/vehiculo', methods=['GET'])
def get_all_polizas_vehiculo():
    """
    Get all vehicle insurance policies.
    
    Query params:
        - vehiculo_id: Optional filter by vehicle asset ID
        - usuario_id: Optional filter by user ID
        - estado: Optional filter by state
        - placa: Optional filter by license plate
    """
    vehiculo_id = request.args.get('vehiculo_id', type=int)
    usuario_id = request.args.get('usuario_id', type=int)
    estado = request.args.get('estado', type=str)
    placa = request.args.get('placa', type=str)
    
    if vehiculo_id:
        polizas = PolizaVehiculoService.get_by_vehiculo_id(vehiculo_id)
    elif usuario_id:
        polizas = PolizaVehiculoService.get_by_usuario_id(usuario_id)
    elif estado:
        polizas = PolizaVehiculoService.get_by_estado(estado)
    elif placa:
        polizas = PolizaVehiculoService.get_by_placa(placa)
    else:
        polizas = PolizaVehiculoService.get_all()
    
    return jsonify({
        'success': True,
        'data': polizas,
        'count': len(polizas)
    }), 200


@polizas_bp.route('/vehiculo/<int:poliza_id>', methods=['GET'])
def get_poliza_vehiculo_by_id(poliza_id: int):
    """Get a specific vehicle insurance policy by ID."""
    poliza = PolizaVehiculoService.get_by_id(poliza_id)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaVehiculo with ID {poliza_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/vehiculo/consecutivo/<string:consecutivo>', methods=['GET'])
def get_poliza_vehiculo_by_consecutivo(consecutivo: str):
    """Get a vehicle insurance policy by consecutive identifier."""
    poliza = PolizaVehiculoService.get_by_consecutivo(consecutivo)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaVehiculo with consecutivo {consecutivo} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/vehiculo', methods=['POST'])
def create_poliza_vehiculo():
    """
    Create a new vehicle insurance policy.
    
    Expected JSON body:
        - id_vehiculo (required): Vehicle asset ID
        - All other fields as for home policy, plus:
        - valor_vehiculo_asegurado: Insured vehicle value
        - valor_accesorios_asegurado: Insured accessories value
        - valor_rc_asegurado: RC insured value
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaVehiculoService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaVehiculo created successfully'
    }), 201


@polizas_bp.route('/vehiculo/<int:poliza_id>', methods=['PUT'])
def update_poliza_vehiculo(poliza_id: int):
    """Update an existing vehicle insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaVehiculoService.update(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaVehiculo updated successfully'
    }), 200


@polizas_bp.route('/vehiculo/<int:poliza_id>/estado', methods=['PATCH'])
def cambiar_estado_poliza_vehiculo(poliza_id: int):
    """Change the state of a vehicle insurance policy."""
    data = request.get_json()
    
    if not data or 'estado' not in data:
        return jsonify({
            'success': False,
            'error': 'Field estado is required'
        }), 400
    
    poliza, error = PolizaVehiculoService.cambiar_estado(
        poliza_id, 
        data['estado'],
        data.get('aseguradora_seleccionada')
    )
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': f'PolizaVehiculo state changed to {data["estado"]} successfully'
    }), 200


@polizas_bp.route('/vehiculo/<int:poliza_id>/validar', methods=['GET'])
def validar_poliza_vehiculo(poliza_id: int):
    """Validate insured values against appraisal values for a vehicle policy."""
    is_valid, errores = PolizaVehiculoService.validar_valores_asegurados(poliza_id)
    
    return jsonify({
        'success': True,
        'data': {
            'is_valid': is_valid,
            'errores': errores
        }
    }), 200


@polizas_bp.route('/vehiculo/<int:poliza_id>/entregar', methods=['POST', 'OPTIONS'])
def entregar_poliza_vehiculo(poliza_id: int):
    """Deliver a vehicle insurance policy (PROSPECTO -> VIGENTE)."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaVehiculoService.entregar_poliza(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaVehiculo entregada exitosamente'
    }), 200


@polizas_bp.route('/vehiculo/<int:poliza_id>/actualizar-entrega', methods=['PATCH', 'OPTIONS'])
def actualizar_entrega_vehiculo(poliza_id: int):
    """Update delivery data for a vehicle insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaVehiculoService.actualizar_entrega(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'Datos de entrega actualizados exitosamente'
    }), 200


@polizas_bp.route('/vehiculo/<int:poliza_id>', methods=['DELETE'])
def delete_poliza_vehiculo(poliza_id: int):
    """Delete a vehicle insurance policy."""
    success, error = PolizaVehiculoService.delete(poliza_id)
    
    if not success:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'message': f'PolizaVehiculo with ID {poliza_id} deleted successfully'
    }), 200


# =============================================================================
# POLIZAS COPROPIEDAD (Co-ownership Insurance Policies) Endpoints
# =============================================================================

@polizas_bp.route('/copropiedad', methods=['GET'])
def get_all_polizas_copropiedad():
    """
    Get all co-ownership insurance policies.
    
    Query params:
        - copropiedad_id: Optional filter by co-ownership asset ID
        - usuario_id: Optional filter by user ID
        - estado: Optional filter by state
    """
    copropiedad_id = request.args.get('copropiedad_id', type=int)
    usuario_id = request.args.get('usuario_id', type=int)
    estado = request.args.get('estado', type=str)
    
    if copropiedad_id:
        polizas = PolizaCopropiedadService.get_by_copropiedad_id(copropiedad_id)
    elif usuario_id:
        polizas = PolizaCopropiedadService.get_by_usuario_id(usuario_id)
    elif estado:
        polizas = PolizaCopropiedadService.get_by_estado(estado)
    else:
        polizas = PolizaCopropiedadService.get_all()
    
    return jsonify({
        'success': True,
        'data': polizas,
        'count': len(polizas)
    }), 200


@polizas_bp.route('/copropiedad/<int:poliza_id>', methods=['GET'])
def get_poliza_copropiedad_by_id(poliza_id: int):
    """Get a specific co-ownership insurance policy by ID."""
    poliza = PolizaCopropiedadService.get_by_id(poliza_id)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaCopropiedad with ID {poliza_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/copropiedad/consecutivo/<string:consecutivo>', methods=['GET'])
def get_poliza_copropiedad_by_consecutivo(consecutivo: str):
    """Get a co-ownership insurance policy by consecutive identifier."""
    poliza = PolizaCopropiedadService.get_by_consecutivo(consecutivo)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaCopropiedad with consecutivo {consecutivo} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/copropiedad', methods=['POST'])
def create_poliza_copropiedad():
    """
    Create a new co-ownership insurance policy.
    
    Expected JSON body:
        - id_copropiedad (required): Co-ownership asset ID
        - All common policy fields, plus:
        - valor_area_comun_asegurado: Insured common area value
        - valor_area_privada_asegurado: Insured private area value
        - valor_maquinaria_equipo_asegurado: Insured machinery value
        - valor_equipo_electronico_asegurado: Insured electronic equipment value
        - valor_muebles_asegurado: Insured furniture value
        - valor_directores_asegurado: Insured directors value
        - valor_rce_asegurado: Insured RCE value
        - valor_manejo_asegurado: Insured management value
        - valor_transporte_valores_vigencia_asegurado: Value transport insured (validity)
        - valor_transporte_valores_despacho_asegurado: Value transport insured (dispatch)
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaCopropiedadService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaCopropiedad created successfully'
    }), 201


@polizas_bp.route('/copropiedad/<int:poliza_id>', methods=['PUT'])
def update_poliza_copropiedad(poliza_id: int):
    """Update an existing co-ownership insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaCopropiedadService.update(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaCopropiedad updated successfully'
    }), 200


@polizas_bp.route('/copropiedad/<int:poliza_id>/estado', methods=['PATCH'])
def cambiar_estado_poliza_copropiedad(poliza_id: int):
    """Change the state of a co-ownership insurance policy."""
    data = request.get_json()
    
    if not data or 'estado' not in data:
        return jsonify({
            'success': False,
            'error': 'Field estado is required'
        }), 400
    
    poliza, error = PolizaCopropiedadService.cambiar_estado(
        poliza_id, 
        data['estado'],
        data.get('aseguradora_seleccionada')
    )
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': f'PolizaCopropiedad state changed to {data["estado"]} successfully'
    }), 200


@polizas_bp.route('/copropiedad/<int:poliza_id>/validar', methods=['GET'])
def validar_poliza_copropiedad(poliza_id: int):
    """Validate insured values against appraisal values for a co-ownership policy."""
    is_valid, errores = PolizaCopropiedadService.validar_valores_asegurados(poliza_id)
    
    return jsonify({
        'success': True,
        'data': {
            'is_valid': is_valid,
            'errores': errores
        }
    }), 200


@polizas_bp.route('/copropiedad/<int:poliza_id>/entregar', methods=['POST', 'OPTIONS'])
def entregar_poliza_copropiedad(poliza_id: int):
    """Deliver a co-ownership insurance policy (PROSPECTO -> VIGENTE)."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaCopropiedadService.entregar_poliza(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaCopropiedad entregada exitosamente'
    }), 200


@polizas_bp.route('/copropiedad/<int:poliza_id>/actualizar-entrega', methods=['PATCH', 'OPTIONS'])
def actualizar_entrega_copropiedad(poliza_id: int):
    """Update delivery data for a co-ownership insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaCopropiedadService.actualizar_entrega(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'Datos de entrega actualizados exitosamente'
    }), 200


@polizas_bp.route('/copropiedad/<int:poliza_id>', methods=['DELETE'])
def delete_poliza_copropiedad(poliza_id: int):
    """Delete a co-ownership insurance policy."""
    success, error = PolizaCopropiedadService.delete(poliza_id)
    
    if not success:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'message': f'PolizaCopropiedad with ID {poliza_id} deleted successfully'
    }), 200


# =============================================================================
# POLIZAS OTRO BIEN (Other Asset Insurance Policies) Endpoints
# =============================================================================

@polizas_bp.route('/otro-bien', methods=['GET'])
def get_all_polizas_otro_bien():
    """
    Get all other asset insurance policies.
    
    Query params:
        - otro_bien_id: Optional filter by other asset ID
        - usuario_id: Optional filter by user ID
        - estado: Optional filter by state
    """
    otro_bien_id = request.args.get('otro_bien_id', type=int)
    usuario_id = request.args.get('usuario_id', type=int)
    estado = request.args.get('estado', type=str)
    
    if otro_bien_id:
        polizas = PolizaOtroBienService.get_by_otro_bien_id(otro_bien_id)
    elif usuario_id:
        polizas = PolizaOtroBienService.get_by_usuario_id(usuario_id)
    elif estado:
        polizas = PolizaOtroBienService.get_by_estado(estado)
    else:
        polizas = PolizaOtroBienService.get_all()
    
    return jsonify({
        'success': True,
        'data': polizas,
        'count': len(polizas)
    }), 200


@polizas_bp.route('/otro-bien/<int:poliza_id>', methods=['GET'])
def get_poliza_otro_bien_by_id(poliza_id: int):
    """Get a specific other asset insurance policy by ID."""
    poliza = PolizaOtroBienService.get_by_id(poliza_id)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaOtroBien with ID {poliza_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/otro-bien/consecutivo/<string:consecutivo>', methods=['GET'])
def get_poliza_otro_bien_by_consecutivo(consecutivo: str):
    """Get an other asset insurance policy by consecutive identifier."""
    poliza = PolizaOtroBienService.get_by_consecutivo(consecutivo)
    
    if not poliza:
        return jsonify({
            'success': False,
            'error': f'PolizaOtroBien with consecutivo {consecutivo} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': poliza
    }), 200


@polizas_bp.route('/otro-bien', methods=['POST'])
def create_poliza_otro_bien():
    """
    Create a new other asset insurance policy.
    
    Expected JSON body:
        - id_otro_bien (required): Other asset ID
        - All common policy fields, plus:
        - valor_asegurado: Insured value
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaOtroBienService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaOtroBien created successfully'
    }), 201


@polizas_bp.route('/otro-bien/<int:poliza_id>', methods=['PUT'])
def update_poliza_otro_bien(poliza_id: int):
    """Update an existing other asset insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaOtroBienService.update(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaOtroBien updated successfully'
    }), 200


@polizas_bp.route('/otro-bien/<int:poliza_id>/estado', methods=['PATCH'])
def cambiar_estado_poliza_otro_bien(poliza_id: int):
    """Change the state of an other asset insurance policy."""
    data = request.get_json()
    
    if not data or 'estado' not in data:
        return jsonify({
            'success': False,
            'error': 'Field estado is required'
        }), 400
    
    poliza, error = PolizaOtroBienService.cambiar_estado(
        poliza_id, 
        data['estado'],
        data.get('aseguradora_seleccionada')
    )
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': f'PolizaOtroBien state changed to {data["estado"]} successfully'
    }), 200


@polizas_bp.route('/otro-bien/<int:poliza_id>/validar', methods=['GET'])
def validar_poliza_otro_bien(poliza_id: int):
    """Validate insured values against appraisal values for an other asset policy."""
    is_valid, errores = PolizaOtroBienService.validar_valores_asegurados(poliza_id)
    
    return jsonify({
        'success': True,
        'data': {
            'is_valid': is_valid,
            'errores': errores
        }
    }), 200


@polizas_bp.route('/otro-bien/<int:poliza_id>/entregar', methods=['POST', 'OPTIONS'])
def entregar_poliza_otro_bien(poliza_id: int):
    """Deliver an other asset insurance policy (PROSPECTO -> VIGENTE)."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaOtroBienService.entregar_poliza(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'PolizaOtroBien entregada exitosamente'
    }), 200


@polizas_bp.route('/otro-bien/<int:poliza_id>/actualizar-entrega', methods=['PATCH', 'OPTIONS'])
def actualizar_entrega_otro_bien(poliza_id: int):
    """Update delivery data for an other asset insurance policy."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    data = sanitize_numeric_fields(data)
    poliza, error = PolizaOtroBienService.actualizar_entrega(poliza_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': poliza,
        'message': 'Datos de entrega actualizados exitosamente'
    }), 200


@polizas_bp.route('/otro-bien/<int:poliza_id>', methods=['DELETE'])
def delete_poliza_otro_bien(poliza_id: int):
    """Delete an other asset insurance policy."""
    success, error = PolizaOtroBienService.delete(poliza_id)
    
    if not success:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'message': f'PolizaOtroBien with ID {poliza_id} deleted successfully'
    }), 200


# =============================================================================
# UNIFIED ENDPOINTS: Cross-type policy queries
# =============================================================================

@polizas_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def get_all_polizas_by_usuario(usuario_id: int):
    """
    Get all policies of all types for a specific user.
    
    Args:
        usuario_id: The user's unique identifier
        
    Returns:
        JSON with all policies grouped by type
    """
    polizas_hogar = PolizaHogarService.get_by_usuario_id(usuario_id)
    polizas_vehiculo = PolizaVehiculoService.get_by_usuario_id(usuario_id)
    polizas_copropiedad = PolizaCopropiedadService.get_by_usuario_id(usuario_id)
    polizas_otro_bien = PolizaOtroBienService.get_by_usuario_id(usuario_id)
    
    total = len(polizas_hogar) + len(polizas_vehiculo) + len(polizas_copropiedad) + len(polizas_otro_bien)
    
    return jsonify({
        'success': True,
        'data': {
            'hogar': polizas_hogar,
            'vehiculo': polizas_vehiculo,
            'copropiedad': polizas_copropiedad,
            'otro_bien': polizas_otro_bien
        },
        'count': {
            'hogar': len(polizas_hogar),
            'vehiculo': len(polizas_vehiculo),
            'copropiedad': len(polizas_copropiedad),
            'otro_bien': len(polizas_otro_bien),
            'total': total
        }
    }), 200


@polizas_bp.route('/por-vencer', methods=['GET'])
def get_polizas_por_vencer():
    """
    Get all policies about to expire across all types.
    
    Query params:
        - dias: Number of days to look ahead (default: 30)
        
    Returns:
        JSON with policies about to expire grouped by type
    """
    dias = request.args.get('dias', default=30, type=int)
    
    polizas_hogar = PolizaHogarService.get_por_vencer(dias)
    polizas_vehiculo = PolizaVehiculoService.get_por_vencer(dias)
    polizas_copropiedad = PolizaCopropiedadService.get_por_vencer(dias)
    polizas_otro_bien = PolizaOtroBienService.get_por_vencer(dias)
    
    total = len(polizas_hogar) + len(polizas_vehiculo) + len(polizas_copropiedad) + len(polizas_otro_bien)
    
    return jsonify({
        'success': True,
        'data': {
            'hogar': polizas_hogar,
            'vehiculo': polizas_vehiculo,
            'copropiedad': polizas_copropiedad,
            'otro_bien': polizas_otro_bien
        },
        'count': {
            'hogar': len(polizas_hogar),
            'vehiculo': len(polizas_vehiculo),
            'copropiedad': len(polizas_copropiedad),
            'otro_bien': len(polizas_otro_bien),
            'total': total
        },
        'dias_consultados': dias
    }), 200
