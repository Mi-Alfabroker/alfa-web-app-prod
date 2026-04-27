"""Blueprint for Bienes (Assets) API endpoints."""
from flask import Blueprint, jsonify, request
from app.services.bienes import (
    HogarService, 
    VehiculoService, 
    CopropiedadService, 
    OtroBienService
)
from app.security.decorators import authorize_request
from app.security.roles import ADMIN_ROLES, STAFF_ROLES

bienes_bp = Blueprint('bienes', __name__, url_prefix='/api/bienes')


@bienes_bp.before_request
def authorize_bienes_access():
    if request.method == 'OPTIONS':
        return  # Let Flask-CORS handle preflight
    if request.method == 'DELETE':
        return authorize_request(ADMIN_ROLES)
    return authorize_request(STAFF_ROLES)


# =============================================================================
# HOGARES (Homes) Endpoints
# =============================================================================

@bienes_bp.route('/hogares', methods=['GET'])
def get_all_hogares():
    """
    Get all home assets.
    
    Query params:
        - usuario_id: Optional filter by user ID
    
    Returns:
        JSON list of all homes
    """
    usuario_id = request.args.get('usuario_id', type=int)
    
    if usuario_id:
        hogares = HogarService.get_by_usuario_id(usuario_id)
    else:
        hogares = HogarService.get_all()
    
    return jsonify({
        'success': True,
        'data': hogares,
        'count': len(hogares)
    }), 200


@bienes_bp.route('/hogares/<int:hogar_id>', methods=['GET'])
def get_hogar_by_id(hogar_id: int):
    """
    Get a specific home asset by ID.
    
    Args:
        hogar_id: The unique identifier
        
    Returns:
        JSON with home data or 404 error
    """
    hogar = HogarService.get_by_id(hogar_id)
    
    if not hogar:
        return jsonify({
            'success': False,
            'error': f'Hogar with ID {hogar_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': hogar
    }), 200


@bienes_bp.route('/hogares', methods=['POST'])
def create_hogar():
    """
    Create a new home asset.
    
    Expected JSON body:
        - id_usuario (required): Owner user ID
        - tipo_inmueble: Type of property
        - ciudad_inmueble: City
        - direccion_inmueble: Address
        - numero_pisos: Number of floors
        - ano_construccion: Year of construction
        - valor_inmueble_avaluo: Property value
        - valor_contenidos_normales_avaluo: Normal contents value
        - valor_contenidos_especiales_avaluo: Special contents value
        - valor_equipo_electronico_avaluo: Electronic equipment value
        - valor_maquinaria_equipo_avaluo: Machinery/equipment value
        
    Returns:
        JSON with created home or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    hogar, error = HogarService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': hogar,
        'message': 'Hogar created successfully'
    }), 201


@bienes_bp.route('/hogares/<int:hogar_id>', methods=['PUT'])
def update_hogar(hogar_id: int):
    """
    Update an existing home asset.
    
    Args:
        hogar_id: The ID of the home to update
        
    Returns:
        JSON with updated home or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    hogar, error = HogarService.update(hogar_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': hogar,
        'message': 'Hogar updated successfully'
    }), 200


@bienes_bp.route('/hogares/<int:hogar_id>', methods=['DELETE'])
def delete_hogar(hogar_id: int):
    """
    Delete a home asset.
    
    Args:
        hogar_id: The ID of the home to delete
        
    Returns:
        JSON with success message or error
    """
    success, error = HogarService.delete(hogar_id)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'Hogar with ID {hogar_id} deleted successfully'
    }), 200


# =============================================================================
# VEHICULOS (Vehicles) Endpoints
# =============================================================================

@bienes_bp.route('/vehiculos', methods=['GET'])
def get_all_vehiculos():
    """
    Get all vehicle assets.
    
    Query params:
        - usuario_id: Optional filter by user ID
    
    Returns:
        JSON list of all vehicles
    """
    usuario_id = request.args.get('usuario_id', type=int)
    
    if usuario_id:
        vehiculos = VehiculoService.get_by_usuario_id(usuario_id)
    else:
        vehiculos = VehiculoService.get_all()
    
    return jsonify({
        'success': True,
        'data': vehiculos,
        'count': len(vehiculos)
    }), 200


@bienes_bp.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def get_vehiculo_by_id(vehiculo_id: int):
    """
    Get a specific vehicle asset by ID.
    
    Args:
        vehiculo_id: The unique identifier
        
    Returns:
        JSON with vehicle data or 404 error
    """
    vehiculo = VehiculoService.get_by_id(vehiculo_id)
    
    if not vehiculo:
        return jsonify({
            'success': False,
            'error': f'Vehiculo with ID {vehiculo_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': vehiculo
    }), 200


@bienes_bp.route('/vehiculos/placa/<string:placa>', methods=['GET'])
def get_vehiculo_by_placa(placa: str):
    """
    Get a vehicle by its license plate.
    
    Args:
        placa: The license plate number
        
    Returns:
        JSON with vehicle data or 404 error
    """
    vehiculo = VehiculoService.get_by_placa(placa)
    
    if not vehiculo:
        return jsonify({
            'success': False,
            'error': f'Vehiculo with plate {placa} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': vehiculo
    }), 200


@bienes_bp.route('/vehiculos', methods=['POST'])
def create_vehiculo():
    """
    Create a new vehicle asset.
    
    Expected JSON body:
        - id_usuario (required): Owner user ID
        - tipo_vehiculo: Type of vehicle
        - placa: License plate
        - marca: Brand
        - serie_referencia: Series/Reference
        - ano_modelo: Model year
        - ano_nacimiento_conductor: Driver's birth year
        - codigo_fasecolda: Fasecolda code
        - valor_vehiculo: Vehicle value
        - valor_accesorios_avaluo: Accessories value
        
    Returns:
        JSON with created vehicle or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    vehiculo, error = VehiculoService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': vehiculo,
        'message': 'Vehiculo created successfully'
    }), 201


@bienes_bp.route('/vehiculos/<int:vehiculo_id>', methods=['PUT'])
def update_vehiculo(vehiculo_id: int):
    """
    Update an existing vehicle asset.
    
    Args:
        vehiculo_id: The ID of the vehicle to update
        
    Returns:
        JSON with updated vehicle or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    vehiculo, error = VehiculoService.update(vehiculo_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': vehiculo,
        'message': 'Vehiculo updated successfully'
    }), 200


@bienes_bp.route('/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def delete_vehiculo(vehiculo_id: int):
    """
    Delete a vehicle asset.
    
    Args:
        vehiculo_id: The ID of the vehicle to delete
        
    Returns:
        JSON with success message or error
    """
    success, error = VehiculoService.delete(vehiculo_id)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'Vehiculo with ID {vehiculo_id} deleted successfully'
    }), 200


# =============================================================================
# COPROPIEDADES (Co-ownerships) Endpoints
# =============================================================================

@bienes_bp.route('/copropiedades', methods=['GET'])
def get_all_copropiedades():
    """
    Get all co-ownership assets.
    
    Query params:
        - usuario_id: Optional filter by user ID
    
    Returns:
        JSON list of all co-ownerships
    """
    usuario_id = request.args.get('usuario_id', type=int)
    
    if usuario_id:
        copropiedades = CopropiedadService.get_by_usuario_id(usuario_id)
    else:
        copropiedades = CopropiedadService.get_all()
    
    return jsonify({
        'success': True,
        'data': copropiedades,
        'count': len(copropiedades)
    }), 200


@bienes_bp.route('/copropiedades/<int:copropiedad_id>', methods=['GET'])
def get_copropiedad_by_id(copropiedad_id: int):
    """
    Get a specific co-ownership asset by ID.
    
    Args:
        copropiedad_id: The unique identifier
        
    Returns:
        JSON with co-ownership data or 404 error
    """
    copropiedad = CopropiedadService.get_by_id(copropiedad_id)
    
    if not copropiedad:
        return jsonify({
            'success': False,
            'error': f'Copropiedad with ID {copropiedad_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': copropiedad
    }), 200


@bienes_bp.route('/copropiedades', methods=['POST'])
def create_copropiedad():
    """
    Create a new co-ownership asset.
    
    Expected JSON body:
        - id_usuario (required): Owner user ID
        - tipo_copropiedad: Type of co-ownership
        - ciudad: City
        - direccion: Address
        - estrato: Socioeconomic stratum
        - ano_construccion: Year of construction
        - numero_torres: Number of towers
        - numero_maximo_pisos: Maximum number of floors
        - numero_maximo_sotanos: Maximum number of basements
        - cantidad_unidades_casa: Number of house units
        - cantidad_unidades_apartamentos: Number of apartment units
        - cantidad_unidades_locales: Number of commercial units
        - cantidad_unidades_oficinas: Number of office units
        - cantidad_unidades_otros: Number of other units
        - valor_edificio_area_comun_avaluo: Common area building value
        - valor_edificio_area_privada_avaluo: Private area building value
        - valor_maquinaria_equipo_avaluo: Machinery/equipment value
        - valor_equipo_electrico_electronico_avaluo: Electronic equipment value
        - valor_muebles_avaluo: Furniture value
        
    Returns:
        JSON with created co-ownership or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    copropiedad, error = CopropiedadService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': copropiedad,
        'message': 'Copropiedad created successfully'
    }), 201


@bienes_bp.route('/copropiedades/<int:copropiedad_id>', methods=['PUT'])
def update_copropiedad(copropiedad_id: int):
    """
    Update an existing co-ownership asset.
    
    Args:
        copropiedad_id: The ID of the co-ownership to update
        
    Returns:
        JSON with updated co-ownership or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    copropiedad, error = CopropiedadService.update(copropiedad_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': copropiedad,
        'message': 'Copropiedad updated successfully'
    }), 200


@bienes_bp.route('/copropiedades/<int:copropiedad_id>', methods=['DELETE'])
def delete_copropiedad(copropiedad_id: int):
    """
    Delete a co-ownership asset.
    
    Args:
        copropiedad_id: The ID of the co-ownership to delete
        
    Returns:
        JSON with success message or error
    """
    success, error = CopropiedadService.delete(copropiedad_id)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'Copropiedad with ID {copropiedad_id} deleted successfully'
    }), 200


# =============================================================================
# OTROS BIENES (Other Assets) Endpoints
# =============================================================================

@bienes_bp.route('/otros', methods=['GET'])
def get_all_otros_bienes():
    """
    Get all other assets.
    
    Query params:
        - usuario_id: Optional filter by user ID
    
    Returns:
        JSON list of all other assets
    """
    usuario_id = request.args.get('usuario_id', type=int)
    
    if usuario_id:
        otros_bienes = OtroBienService.get_by_usuario_id(usuario_id)
    else:
        otros_bienes = OtroBienService.get_all()
    
    return jsonify({
        'success': True,
        'data': otros_bienes,
        'count': len(otros_bienes)
    }), 200


@bienes_bp.route('/otros/<int:otro_bien_id>', methods=['GET'])
def get_otro_bien_by_id(otro_bien_id: int):
    """
    Get a specific other asset by ID.
    
    Args:
        otro_bien_id: The unique identifier
        
    Returns:
        JSON with other asset data or 404 error
    """
    otro_bien = OtroBienService.get_by_id(otro_bien_id)
    
    if not otro_bien:
        return jsonify({
            'success': False,
            'error': f'OtroBien with ID {otro_bien_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': otro_bien
    }), 200


@bienes_bp.route('/otros', methods=['POST'])
def create_otro_bien():
    """
    Create a new other asset.
    
    Expected JSON body:
        - id_usuario (required): Owner user ID
        - tipo_seguro: Type of insurance
        - bien_asegurado: Asset description
        - valor_bien_asegurar: Asset value
        - detalles_bien_asegurado: Additional details
        
    Returns:
        JSON with created other asset or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    otro_bien, error = OtroBienService.create(data)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': otro_bien,
        'message': 'OtroBien created successfully'
    }), 201


@bienes_bp.route('/otros/<int:otro_bien_id>', methods=['PUT'])
def update_otro_bien(otro_bien_id: int):
    """
    Update an existing other asset.
    
    Args:
        otro_bien_id: The ID of the other asset to update
        
    Returns:
        JSON with updated other asset or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    otro_bien, error = OtroBienService.update(otro_bien_id, data)
    
    if error:
        status_code = 404 if 'not found' in error.lower() else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'data': otro_bien,
        'message': 'OtroBien updated successfully'
    }), 200


@bienes_bp.route('/otros/<int:otro_bien_id>', methods=['DELETE'])
def delete_otro_bien(otro_bien_id: int):
    """
    Delete an other asset.
    
    Args:
        otro_bien_id: The ID of the other asset to delete
        
    Returns:
        JSON with success message or error
    """
    success, error = OtroBienService.delete(otro_bien_id)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'OtroBien with ID {otro_bien_id} deleted successfully'
    }), 200


# =============================================================================
# UNIFIED ENDPOINT: Get all assets for a user
# =============================================================================

@bienes_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def get_all_bienes_by_usuario(usuario_id: int):
    """
    Get all assets of all types for a specific user.
    
    Args:
        usuario_id: The user's unique identifier
        
    Returns:
        JSON with all assets grouped by type
    """
    hogares = HogarService.get_by_usuario_id(usuario_id)
    vehiculos = VehiculoService.get_by_usuario_id(usuario_id)
    copropiedades = CopropiedadService.get_by_usuario_id(usuario_id)
    otros_bienes = OtroBienService.get_by_usuario_id(usuario_id)
    
    total = len(hogares) + len(vehiculos) + len(copropiedades) + len(otros_bienes)
    
    return jsonify({
        'success': True,
        'data': {
            'hogares': hogares,
            'vehiculos': vehiculos,
            'copropiedades': copropiedades,
            'otros_bienes': otros_bienes
        },
        'count': {
            'hogares': len(hogares),
            'vehiculos': len(vehiculos),
            'copropiedades': len(copropiedades),
            'otros_bienes': len(otros_bienes),
            'total': total
        }
    }), 200
