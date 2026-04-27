/**
 * Field definitions for Bienes (Assets) module
 * Centralized labels and database field mappings
 */

// ============================================================================
// COMMON FIELDS
// ============================================================================
const CommonFields = {
	id: { db: 'id', label: 'ID' },
	id_usuario: { db: 'id_usuario', label: 'Cliente' },
	created_at: { db: 'created_at', label: 'Fecha Creación' },
	updated_at: { db: 'updated_at', label: 'Última Actualización' }
};

// ============================================================================
// HOGAR FIELDS
// ============================================================================
export const HogarFields = {
	...CommonFields,
	tipo_inmueble: { db: 'tipo_inmueble', label: 'Tipo de Inmueble' },
	ciudad_inmueble: { db: 'ciudad_inmueble', label: 'Ciudad' },
	direccion_inmueble: { db: 'direccion_inmueble', label: 'Dirección' },
	numero_pisos: { db: 'numero_pisos', label: 'Número de Pisos' },
	ano_construccion: { db: 'ano_construccion', label: 'Año de Construcción' },
	valor_inmueble_avaluo: { db: 'valor_inmueble_avaluo', label: 'Valor Inmueble (Avalúo)' },
	valor_contenidos_normales_avaluo: { db: 'valor_contenidos_normales_avaluo', label: 'Valor Contenidos Normales' },
	valor_contenidos_especiales_avaluo: { db: 'valor_contenidos_especiales_avaluo', label: 'Valor Contenidos Especiales' },
	valor_equipo_electronico_avaluo: { db: 'valor_equipo_electronico_avaluo', label: 'Valor Equipo Electrónico' },
	valor_maquinaria_equipo_avaluo: { db: 'valor_maquinaria_equipo_avaluo', label: 'Valor Maquinaria/Equipo' }
};

// ============================================================================
// VEHICULO FIELDS
// ============================================================================
export const VehiculoFields = {
	...CommonFields,
	tipo_vehiculo: { db: 'tipo_vehiculo', label: 'Tipo de Vehículo' },
	placa: { db: 'placa', label: 'Placa' },
	marca: { db: 'marca', label: 'Marca' },
	serie_referencia: { db: 'serie_referencia', label: 'Serie/Referencia' },
	ano_modelo: { db: 'ano_modelo', label: 'Año del Modelo' },
	ano_nacimiento_conductor: { db: 'ano_nacimiento_conductor', label: 'Año Nacimiento Conductor' },
	codigo_fasecolda: { db: 'codigo_fasecolda', label: 'Código Fasecolda' },
	valor_vehiculo: { db: 'valor_vehiculo', label: 'Valor del Vehículo' },
	valor_accesorios_avaluo: { db: 'valor_accesorios_avaluo', label: 'Valor Accesorios' }
};

// ============================================================================
// COPROPIEDAD FIELDS
// ============================================================================
export const CopropiedadFields = {
	...CommonFields,
	tipo_copropiedad: { db: 'tipo_copropiedad', label: 'Tipo de Copropiedad' },
	ciudad: { db: 'ciudad', label: 'Ciudad' },
	direccion: { db: 'direccion', label: 'Dirección' },
	estrato: { db: 'estrato', label: 'Estrato' },
	ano_construccion: { db: 'ano_construccion', label: 'Año Construcción' },
	numero_torres: { db: 'numero_torres', label: 'Torres' },
	numero_maximo_pisos: { db: 'numero_maximo_pisos', label: 'Pisos Máx.' },
	numero_maximo_sotanos: { db: 'numero_maximo_sotanos', label: 'Sótanos Máx.' },
	cantidad_unidades_casa: { db: 'cantidad_unidades_casa', label: 'Casas' },
	cantidad_unidades_apartamentos: { db: 'cantidad_unidades_apartamentos', label: 'Apartamentos' },
	cantidad_unidades_locales: { db: 'cantidad_unidades_locales', label: 'Locales' },
	cantidad_unidades_oficinas: { db: 'cantidad_unidades_oficinas', label: 'Oficinas' },
	cantidad_unidades_otros: { db: 'cantidad_unidades_otros', label: 'Otros' },
	valor_edificio_area_comun_avaluo: { db: 'valor_edificio_area_comun_avaluo', label: 'Área Común' },
	valor_edificio_area_privada_avaluo: { db: 'valor_edificio_area_privada_avaluo', label: 'Área Privada' },
	valor_maquinaria_equipo_avaluo: { db: 'valor_maquinaria_equipo_avaluo', label: 'Maquinaria/Equipo' },
	valor_equipo_electrico_electronico_avaluo: { db: 'valor_equipo_electrico_electronico_avaluo', label: 'Equipo Electrónico' },
	valor_muebles_avaluo: { db: 'valor_muebles_avaluo', label: 'Muebles' }
};

// ============================================================================
// OTRO BIEN FIELDS
// ============================================================================
export const OtroBienFields = {
	...CommonFields,
	tipo_seguro: { db: 'tipo_seguro', label: 'Tipo de Seguro' },
	bien_asegurado: { db: 'bien_asegurado', label: 'Bien a Asegurar' },
	valor_bien_asegurar: { db: 'valor_bien_asegurar', label: 'Valor del Bien' },
	detalles_bien_asegurado: { db: 'detalles_bien_asegurado', label: 'Detalles' }
};

// ============================================================================
// UNIFIED EXPORT
// ============================================================================
export const BienFields = {
	Hogar: HogarFields,
	Vehiculo: VehiculoFields,
	Copropiedad: CopropiedadFields,
	OtroBien: OtroBienFields
};
