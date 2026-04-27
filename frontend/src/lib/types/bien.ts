/**
 * Types for Bienes (Assets) module
 */

// Enum para tipos de bien
export const TIPOS_BIEN = [
	{ value: 'HOGAR', label: 'Hogar' },
	{ value: 'VEHICULO', label: 'Vehículo' },
	{ value: 'COPROPIEDAD', label: 'Copropiedad' },
	{ value: 'OTRO', label: 'Otro Bien' }
] as const;

export type TipoBien = 'HOGAR' | 'VEHICULO' | 'COPROPIEDAD' | 'OTRO';

// Opciones para tipos de inmueble (hogar)
export const TIPOS_INMUEBLE = [
	{ value: 'Casa', label: 'Casa' },
	{ value: 'Apartamento', label: 'Apartamento' },
	{ value: 'Finca', label: 'Finca' },
	{ value: 'Local', label: 'Local Comercial' },
	{ value: 'Oficina', label: 'Oficina' },
	{ value: 'Bodega', label: 'Bodega' },
	{ value: 'Otro', label: 'Otro' }
] as const;

// Opciones para tipos de vehículo
export const TIPOS_VEHICULO = [
	{ value: 'Automóvil', label: 'Automóvil' },
	{ value: 'Camioneta', label: 'Camioneta' },
	{ value: 'Motocicleta', label: 'Motocicleta' },
	{ value: 'Camión', label: 'Camión' },
	{ value: 'Bus', label: 'Bus' },
	{ value: 'Taxi', label: 'Taxi' },
	{ value: 'Otro', label: 'Otro' }
] as const;

// Opciones para tipos de copropiedad
export const TIPOS_COPROPIEDAD = [
	{ value: 'Residencial', label: 'Residencial' },
	{ value: 'Comercial', label: 'Comercial' },
	{ value: 'Mixto', label: 'Mixto' },
	{ value: 'Industrial', label: 'Industrial' }
] as const;

// ============================================================================
// HOGAR
// ============================================================================
export interface Hogar {
	id: number;
	id_usuario: number;
	tipo_inmueble: string | null;
	ciudad_inmueble: string | null;
	direccion_inmueble: string | null;
	numero_pisos: number | null;
	ano_construccion: number | null;
	valor_inmueble_avaluo: number | null;
	valor_contenidos_normales_avaluo: number | null;
	valor_contenidos_especiales_avaluo: number | null;
	valor_equipo_electronico_avaluo: number | null;
	valor_maquinaria_equipo_avaluo: number | null;
	created_at: string | null;
	updated_at: string | null;
}

export interface CreateHogarDto {
	id_usuario: number;
	tipo_inmueble?: string;
	ciudad_inmueble?: string;
	direccion_inmueble?: string;
	numero_pisos?: number;
	ano_construccion?: number;
	valor_inmueble_avaluo?: number;
	valor_contenidos_normales_avaluo?: number;
	valor_contenidos_especiales_avaluo?: number;
	valor_equipo_electronico_avaluo?: number;
	valor_maquinaria_equipo_avaluo?: number;
}

export type UpdateHogarDto = Partial<Omit<CreateHogarDto, 'id_usuario'>>;

// ============================================================================
// VEHICULO
// ============================================================================
export interface Vehiculo {
	id: number;
	id_usuario: number;
	tipo_vehiculo: string | null;
	placa: string | null;
	marca: string | null;
	serie_referencia: string | null;
	ano_modelo: number | null;
	ano_nacimiento_conductor: number | null;
	codigo_fasecolda: string | null;
	valor_vehiculo: number | null;
	valor_accesorios_avaluo: number | null;
	created_at: string | null;
	updated_at: string | null;
}

export interface CreateVehiculoDto {
	id_usuario: number;
	tipo_vehiculo?: string;
	placa?: string;
	marca?: string;
	serie_referencia?: string;
	ano_modelo?: number;
	ano_nacimiento_conductor?: number;
	codigo_fasecolda?: string;
	valor_vehiculo?: number;
	valor_accesorios_avaluo?: number;
}

export type UpdateVehiculoDto = Partial<Omit<CreateVehiculoDto, 'id_usuario'>>;

// ============================================================================
// COPROPIEDAD
// ============================================================================
export interface Copropiedad {
	id: number;
	id_usuario: number;
	tipo_copropiedad: string | null;
	ciudad: string | null;
	direccion: string | null;
	estrato: number | null;
	ano_construccion: number | null;
	numero_torres: number | null;
	numero_maximo_pisos: number | null;
	numero_maximo_sotanos: number | null;
	cantidad_unidades_casa: number | null;
	cantidad_unidades_apartamentos: number | null;
	cantidad_unidades_locales: number | null;
	cantidad_unidades_oficinas: number | null;
	cantidad_unidades_otros: number | null;
	valor_edificio_area_comun_avaluo: number | null;
	valor_edificio_area_privada_avaluo: number | null;
	valor_maquinaria_equipo_avaluo: number | null;
	valor_equipo_electrico_electronico_avaluo: number | null;
	valor_muebles_avaluo: number | null;
	created_at: string | null;
	updated_at: string | null;
}

export interface CreateCopropiedadDto {
	id_usuario: number;
	tipo_copropiedad?: string;
	ciudad?: string;
	direccion?: string;
	estrato?: number;
	ano_construccion?: number;
	numero_torres?: number;
	numero_maximo_pisos?: number;
	numero_maximo_sotanos?: number;
	cantidad_unidades_casa?: number;
	cantidad_unidades_apartamentos?: number;
	cantidad_unidades_locales?: number;
	cantidad_unidades_oficinas?: number;
	cantidad_unidades_otros?: number;
	valor_edificio_area_comun_avaluo?: number;
	valor_edificio_area_privada_avaluo?: number;
	valor_maquinaria_equipo_avaluo?: number;
	valor_equipo_electrico_electronico_avaluo?: number;
	valor_muebles_avaluo?: number;
}

export type UpdateCopropiedadDto = Partial<Omit<CreateCopropiedadDto, 'id_usuario'>>;

// ============================================================================
// OTRO BIEN
// ============================================================================
export interface OtroBien {
	id: number;
	id_usuario: number;
	tipo_seguro: string | null;
	bien_asegurado: string | null;
	valor_bien_asegurar: number | null;
	detalles_bien_asegurado: string | null;
	created_at: string | null;
	updated_at: string | null;
}

export interface CreateOtroBienDto {
	id_usuario: number;
	tipo_seguro?: string;
	bien_asegurado?: string;
	valor_bien_asegurar?: number;
	detalles_bien_asegurado?: string;
}

export type UpdateOtroBienDto = Partial<Omit<CreateOtroBienDto, 'id_usuario'>>;

// ============================================================================
// RESPUESTA UNIFICADA DE BIENES POR USUARIO
// ============================================================================
export interface BienesUsuario {
	hogares: Hogar[];
	vehiculos: Vehiculo[];
	copropiedades: Copropiedad[];
	otros_bienes: OtroBien[];
}

export interface BienesCount {
	hogares: number;
	vehiculos: number;
	copropiedades: number;
	otros_bienes: number;
	total: number;
}

// Tipo unión para cualquier bien
export type Bien = Hogar | Vehiculo | Copropiedad | OtroBien;

// Helper para identificar el tipo de bien en runtime
export function getTipoBien(bien: Bien): TipoBien {
	if ('tipo_inmueble' in bien) return 'HOGAR';
	if ('placa' in bien) return 'VEHICULO';
	if ('tipo_copropiedad' in bien) return 'COPROPIEDAD';
	return 'OTRO';
}

// Helper para obtener descripción del bien
export function getBienDescription(bien: Bien): string {
	if ('tipo_inmueble' in bien) {
		return `${bien.tipo_inmueble || 'Hogar'} - ${bien.direccion_inmueble || 'Sin dirección'}`;
	}
	if ('placa' in bien) {
		return `${bien.marca || ''} ${bien.tipo_vehiculo || 'Vehículo'} - ${bien.placa || 'Sin placa'}`;
	}
	if ('tipo_copropiedad' in bien) {
		return `${bien.tipo_copropiedad || 'Copropiedad'} - ${bien.direccion || 'Sin dirección'}`;
	}
	return (bien as OtroBien).bien_asegurado || 'Otro bien';
}
