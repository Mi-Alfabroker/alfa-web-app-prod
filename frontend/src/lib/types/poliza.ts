/**
 * Types for Polizas (Insurance Policies) module
 */

// Estados de póliza
export const ESTADOS_POLIZA = [
	{ value: 'PROSPECTO', label: 'Prospecto', color: 'blue' },
	{ value: 'VIGENTE', label: 'Vigente', color: 'green' },
	{ value: 'VENCIDA', label: 'Vencida', color: 'red' },
	{ value: 'CANCELADA', label: 'Cancelada', color: 'gray' }
] as const;

export type EstadoPoliza = 'PROSPECTO' | 'VIGENTE' | 'VENCIDA' | 'CANCELADA';

// Tipos de póliza (matching TipoBien)
export type TipoPoliza = 'HOGAR' | 'VEHICULO' | 'COPROPIEDAD' | 'OTRO';

// ============================================================================
// BASE POLIZA (campos comunes)
// ============================================================================
export interface BasePoliza {
	id: number;
	consecutivo: string;
	estado: EstadoPoliza;
	inicio_vigencia: string | null;
	fin_vigencia: string | null;
	
	// Primas de aseguradoras (hasta 5 opciones)
	valor_prima_aseg_1: number | null;
	valor_prima_aseg_2: number | null;
	valor_prima_aseg_3: number | null;
	valor_prima_aseg_4: number | null;
	valor_prima_aseg_5: number | null;
	
	// IDs de aseguradoras
	id_aseguradora_1: number | null;
	id_aseguradora_2: number | null;
	id_aseguradora_3: number | null;
	id_aseguradora_4: number | null;
	id_aseguradora_5: number | null;
	
	// Aseguradora seleccionada (1-5) cuando está vigente
	aseguradora_seleccionada: number | null;
	numero_poliza_aseguradora: string | null;
	
	// Valores financieros
	valor_prima_neta: number | null;
	valor_otros_costos: number | null;
	valor_iva: number | null;
	ingreso_comision_percibido: number | null;
	
	// Timestamps
	created_at: string | null;
	updated_at: string | null;
}

// ============================================================================
// POLIZA HOGAR
// ============================================================================
export interface PolizaHogar extends BasePoliza {
	id_hogar: number;
	valor_inmueble_asegurado: number | null;
	valor_contenidos_normales_asegurado: number | null;
	valor_contenidos_especiales_asegurado: number | null;
	valor_equipo_electronico_asegurado: number | null;
	valor_maquinaria_equipo_asegurado: number | null;
	valor_rc_asegurado: number | null;
}

export interface CreatePolizaHogarDto {
	id_hogar: number;
	fecha_consecutivo?: string;
	inicio_vigencia?: string;
	fin_vigencia?: string;
	id_aseguradora_1?: number;
	id_aseguradora_2?: number;
	id_aseguradora_3?: number;
	id_aseguradora_4?: number;
	id_aseguradora_5?: number;
	valor_prima_aseg_1?: number;
	valor_prima_aseg_2?: number;
	valor_prima_aseg_3?: number;
	valor_prima_aseg_4?: number;
	valor_prima_aseg_5?: number;
	valor_inmueble_asegurado?: number;
	valor_contenidos_normales_asegurado?: number;
	valor_contenidos_especiales_asegurado?: number;
	valor_equipo_electronico_asegurado?: number;
	valor_maquinaria_equipo_asegurado?: number;
	valor_rc_asegurado?: number;
	valor_prima_neta?: number;
	valor_otros_costos?: number;
	valor_iva?: number;
	ingreso_comision_percibido?: number;
}

// ============================================================================
// POLIZA VEHICULO
// ============================================================================
export interface PolizaVehiculo extends BasePoliza {
	id_vehiculo: number;
	valor_vehiculo_asegurado: number | null;
	valor_accesorios_asegurado: number | null;
	valor_rc_asegurado: number | null;
}

export interface CreatePolizaVehiculoDto {
	id_vehiculo: number;
	fecha_consecutivo?: string;
	inicio_vigencia?: string;
	fin_vigencia?: string;
	id_aseguradora_1?: number;
	id_aseguradora_2?: number;
	id_aseguradora_3?: number;
	id_aseguradora_4?: number;
	id_aseguradora_5?: number;
	valor_prima_aseg_1?: number;
	valor_prima_aseg_2?: number;
	valor_prima_aseg_3?: number;
	valor_prima_aseg_4?: number;
	valor_prima_aseg_5?: number;
	valor_vehiculo_asegurado?: number;
	valor_accesorios_asegurado?: number;
	valor_rc_asegurado?: number;
	valor_prima_neta?: number;
	valor_otros_costos?: number;
	valor_iva?: number;
	ingreso_comision_percibido?: number;
}

// ============================================================================
// POLIZA COPROPIEDAD
// ============================================================================
export interface PolizaCopropiedad extends BasePoliza {
	id_copropiedad: number;
	valor_area_comun_asegurado: number | null;
	valor_area_privada_asegurado: number | null;
	valor_maquinaria_equipo_asegurado: number | null;
	valor_equipo_electronico_asegurado: number | null;
	valor_muebles_asegurado: number | null;
	valor_directores_asegurado: number | null;
	valor_rce_asegurado: number | null;
	valor_manejo_asegurado: number | null;
	valor_transporte_valores_vigencia_asegurado: number | null;
	valor_transporte_valores_despacho_asegurado: number | null;
}

export interface CreatePolizaCopropiedadDto {
	id_copropiedad: number;
	fecha_consecutivo?: string;
	inicio_vigencia?: string;
	fin_vigencia?: string;
	id_aseguradora_1?: number;
	id_aseguradora_2?: number;
	id_aseguradora_3?: number;
	id_aseguradora_4?: number;
	id_aseguradora_5?: number;
	valor_prima_aseg_1?: number;
	valor_prima_aseg_2?: number;
	valor_prima_aseg_3?: number;
	valor_prima_aseg_4?: number;
	valor_prima_aseg_5?: number;
	valor_area_comun_asegurado?: number;
	valor_area_privada_asegurado?: number;
	valor_maquinaria_equipo_asegurado?: number;
	valor_equipo_electronico_asegurado?: number;
	valor_muebles_asegurado?: number;
	valor_directores_asegurado?: number;
	valor_rce_asegurado?: number;
	valor_manejo_asegurado?: number;
	valor_transporte_valores_vigencia_asegurado?: number;
	valor_transporte_valores_despacho_asegurado?: number;
	valor_prima_neta?: number;
	valor_otros_costos?: number;
	valor_iva?: number;
	ingreso_comision_percibido?: number;
}

// ============================================================================
// POLIZA OTRO BIEN
// ============================================================================
export interface PolizaOtroBien extends BasePoliza {
	id_otro_bien: number;
	valor_asegurado: number | null;
}

export interface CreatePolizaOtroBienDto {
	id_otro_bien: number;
	fecha_consecutivo?: string;
	inicio_vigencia?: string;
	fin_vigencia?: string;
	id_aseguradora_1?: number;
	id_aseguradora_2?: number;
	id_aseguradora_3?: number;
	id_aseguradora_4?: number;
	id_aseguradora_5?: number;
	valor_prima_aseg_1?: number;
	valor_prima_aseg_2?: number;
	valor_prima_aseg_3?: number;
	valor_prima_aseg_4?: number;
	valor_prima_aseg_5?: number;
	valor_asegurado?: number;
	valor_prima_neta?: number;
	valor_otros_costos?: number;
	valor_iva?: number;
	ingreso_comision_percibido?: number;
}

// ============================================================================
// TIPOS DE ACTUALIZACIÓN (Partial)
// ============================================================================
export type UpdatePolizaHogarDto = Partial<Omit<CreatePolizaHogarDto, 'id_hogar'>>;
export type UpdatePolizaVehiculoDto = Partial<Omit<CreatePolizaVehiculoDto, 'id_vehiculo'>>;
export type UpdatePolizaCopropiedadDto = Partial<Omit<CreatePolizaCopropiedadDto, 'id_copropiedad'>>;
export type UpdatePolizaOtroBienDto = Partial<Omit<CreatePolizaOtroBienDto, 'id_otro_bien'>>;

// ============================================================================
// CAMBIO DE ESTADO
// ============================================================================
export interface CambiarEstadoDto {
	estado: EstadoPoliza;
	aseguradora_seleccionada?: number;
}

// ============================================================================
// RESPUESTA UNIFICADA DE PÓLIZAS POR USUARIO
// ============================================================================
export interface PolizasUsuario {
	hogar: PolizaHogar[];
	vehiculo: PolizaVehiculo[];
	copropiedad: PolizaCopropiedad[];
	otro_bien: PolizaOtroBien[];
}

export interface PolizasCount {
	hogar: number;
	vehiculo: number;
	copropiedad: number;
	otro_bien: number;
	total: number;
}

// ============================================================================
// TIPO UNIÓN PARA CUALQUIER PÓLIZA
// ============================================================================
export type Poliza = PolizaHogar | PolizaVehiculo | PolizaCopropiedad | PolizaOtroBien;

// Helper para identificar el tipo de póliza
export function getTipoPoliza(poliza: Poliza): TipoPoliza {
	if ('id_hogar' in poliza) return 'HOGAR';
	if ('id_vehiculo' in poliza) return 'VEHICULO';
	if ('id_copropiedad' in poliza) return 'COPROPIEDAD';
	return 'OTRO';
}

// Helper para obtener color de estado
export function getEstadoColor(estado: EstadoPoliza): string {
	const found = ESTADOS_POLIZA.find(e => e.value === estado);
	return found?.color || 'gray';
}

// Helper para verificar si es propuesta (PROSPECTO)
export function esPropuesta(poliza: Poliza): boolean {
	return poliza.estado === 'PROSPECTO';
}

// Helper para verificar si es póliza activa
export function esPolizaActiva(poliza: Poliza): boolean {
	return poliza.estado === 'VIGENTE';
}
