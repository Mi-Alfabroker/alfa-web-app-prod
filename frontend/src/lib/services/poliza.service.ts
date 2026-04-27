/**
 * Service for Polizas (Insurance Policies) API operations
 */

import { api } from './api';
import type { ApiResponse } from '$lib/types';
import type {
	PolizaHogar, CreatePolizaHogarDto, UpdatePolizaHogarDto,
	PolizaVehiculo, CreatePolizaVehiculoDto, UpdatePolizaVehiculoDto,
	PolizaCopropiedad, CreatePolizaCopropiedadDto, UpdatePolizaCopropiedadDto,
	PolizaOtroBien, CreatePolizaOtroBienDto, UpdatePolizaOtroBienDto,
	PolizasUsuario, PolizasCount, CambiarEstadoDto, EstadoPoliza
} from '$lib/types/poliza';

const BASE_ENDPOINT = '/api/polizas';

// ============================================================================
// POLIZAS HOGAR SERVICE
// ============================================================================
export const polizaHogarService = {
	async getAll(params?: { hogar_id?: number; usuario_id?: number; estado?: EstadoPoliza }): Promise<PolizaHogar[]> {
		const queryParams = new URLSearchParams();
		if (params?.hogar_id) queryParams.append('hogar_id', String(params.hogar_id));
		if (params?.usuario_id) queryParams.append('usuario_id', String(params.usuario_id));
		if (params?.estado) queryParams.append('estado', params.estado);
		const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
		const response = await api.get<ApiResponse<PolizaHogar[]>>(`${BASE_ENDPOINT}/hogar${query}`);
		return response.data;
	},

	async getById(id: number): Promise<PolizaHogar> {
		const response = await api.get<ApiResponse<PolizaHogar>>(`${BASE_ENDPOINT}/hogar/${id}`);
		return response.data;
	},

	async getByConsecutivo(consecutivo: string): Promise<PolizaHogar> {
		const response = await api.get<ApiResponse<PolizaHogar>>(`${BASE_ENDPOINT}/hogar/consecutivo/${consecutivo}`);
		return response.data;
	},

	async create(data: CreatePolizaHogarDto): Promise<PolizaHogar> {
		const response = await api.post<ApiResponse<PolizaHogar>>(`${BASE_ENDPOINT}/hogar`, data);
		return response.data;
	},

	async update(id: number, data: UpdatePolizaHogarDto): Promise<PolizaHogar> {
		const response = await api.put<ApiResponse<PolizaHogar>>(`${BASE_ENDPOINT}/hogar/${id}`, data);
		return response.data;
	},

	async cambiarEstado(id: number, data: CambiarEstadoDto): Promise<PolizaHogar> {
		const response = await api.patch<ApiResponse<PolizaHogar>>(`${BASE_ENDPOINT}/hogar/${id}/estado`, data);
		return response.data;
	},

	async validar(id: number): Promise<{ is_valid: boolean; errores: string[] }> {
		const response = await api.get<ApiResponse<{ is_valid: boolean; errores: string[] }>>(`${BASE_ENDPOINT}/hogar/${id}/validar`);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/hogar/${id}`);
	},

	async entregar(id: number, datos: Record<string, any>): Promise<PolizaHogar> {
		const response = await api.post<ApiResponse<PolizaHogar>>(`${BASE_ENDPOINT}/hogar/${id}/entregar`, datos);
		return response.data;
	},

	async actualizarEntrega(id: number, datos: Record<string, any>): Promise<PolizaHogar> {
		const response = await api.patch<ApiResponse<PolizaHogar>>(`${BASE_ENDPOINT}/hogar/${id}/actualizar-entrega`, datos);
		return response.data;
	}
};

// ============================================================================
// POLIZAS VEHICULO SERVICE
// ============================================================================
export const polizaVehiculoService = {
	async getAll(params?: { vehiculo_id?: number; usuario_id?: number; estado?: EstadoPoliza; placa?: string }): Promise<PolizaVehiculo[]> {
		const queryParams = new URLSearchParams();
		if (params?.vehiculo_id) queryParams.append('vehiculo_id', String(params.vehiculo_id));
		if (params?.usuario_id) queryParams.append('usuario_id', String(params.usuario_id));
		if (params?.estado) queryParams.append('estado', params.estado);
		if (params?.placa) queryParams.append('placa', params.placa);
		const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
		const response = await api.get<ApiResponse<PolizaVehiculo[]>>(`${BASE_ENDPOINT}/vehiculo${query}`);
		return response.data;
	},

	async getById(id: number): Promise<PolizaVehiculo> {
		const response = await api.get<ApiResponse<PolizaVehiculo>>(`${BASE_ENDPOINT}/vehiculo/${id}`);
		return response.data;
	},

	async getByConsecutivo(consecutivo: string): Promise<PolizaVehiculo> {
		const response = await api.get<ApiResponse<PolizaVehiculo>>(`${BASE_ENDPOINT}/vehiculo/consecutivo/${consecutivo}`);
		return response.data;
	},

	async create(data: CreatePolizaVehiculoDto): Promise<PolizaVehiculo> {
		const response = await api.post<ApiResponse<PolizaVehiculo>>(`${BASE_ENDPOINT}/vehiculo`, data);
		return response.data;
	},

	async update(id: number, data: UpdatePolizaVehiculoDto): Promise<PolizaVehiculo> {
		const response = await api.put<ApiResponse<PolizaVehiculo>>(`${BASE_ENDPOINT}/vehiculo/${id}`, data);
		return response.data;
	},

	async cambiarEstado(id: number, data: CambiarEstadoDto): Promise<PolizaVehiculo> {
		const response = await api.patch<ApiResponse<PolizaVehiculo>>(`${BASE_ENDPOINT}/vehiculo/${id}/estado`, data);
		return response.data;
	},

	async validar(id: number): Promise<{ is_valid: boolean; errores: string[] }> {
		const response = await api.get<ApiResponse<{ is_valid: boolean; errores: string[] }>>(`${BASE_ENDPOINT}/vehiculo/${id}/validar`);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/vehiculo/${id}`);
	},

	async entregar(id: number, datos: Record<string, any>): Promise<PolizaVehiculo> {
		const response = await api.post<ApiResponse<PolizaVehiculo>>(`${BASE_ENDPOINT}/vehiculo/${id}/entregar`, datos);
		return response.data;
	},

	async actualizarEntrega(id: number, datos: Record<string, any>): Promise<PolizaVehiculo> {
		const response = await api.patch<ApiResponse<PolizaVehiculo>>(`${BASE_ENDPOINT}/vehiculo/${id}/actualizar-entrega`, datos);
		return response.data;
	}
};

// ============================================================================
// POLIZAS COPROPIEDAD SERVICE
// ============================================================================
export const polizaCopropiedadService = {
	async getAll(params?: { copropiedad_id?: number; usuario_id?: number; estado?: EstadoPoliza }): Promise<PolizaCopropiedad[]> {
		const queryParams = new URLSearchParams();
		if (params?.copropiedad_id) queryParams.append('copropiedad_id', String(params.copropiedad_id));
		if (params?.usuario_id) queryParams.append('usuario_id', String(params.usuario_id));
		if (params?.estado) queryParams.append('estado', params.estado);
		const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
		const response = await api.get<ApiResponse<PolizaCopropiedad[]>>(`${BASE_ENDPOINT}/copropiedad${query}`);
		return response.data;
	},

	async getById(id: number): Promise<PolizaCopropiedad> {
		const response = await api.get<ApiResponse<PolizaCopropiedad>>(`${BASE_ENDPOINT}/copropiedad/${id}`);
		return response.data;
	},

	async getByConsecutivo(consecutivo: string): Promise<PolizaCopropiedad> {
		const response = await api.get<ApiResponse<PolizaCopropiedad>>(`${BASE_ENDPOINT}/copropiedad/consecutivo/${consecutivo}`);
		return response.data;
	},

	async create(data: CreatePolizaCopropiedadDto): Promise<PolizaCopropiedad> {
		const response = await api.post<ApiResponse<PolizaCopropiedad>>(`${BASE_ENDPOINT}/copropiedad`, data);
		return response.data;
	},

	async update(id: number, data: UpdatePolizaCopropiedadDto): Promise<PolizaCopropiedad> {
		const response = await api.put<ApiResponse<PolizaCopropiedad>>(`${BASE_ENDPOINT}/copropiedad/${id}`, data);
		return response.data;
	},

	async cambiarEstado(id: number, data: CambiarEstadoDto): Promise<PolizaCopropiedad> {
		const response = await api.patch<ApiResponse<PolizaCopropiedad>>(`${BASE_ENDPOINT}/copropiedad/${id}/estado`, data);
		return response.data;
	},

	async validar(id: number): Promise<{ is_valid: boolean; errores: string[] }> {
		const response = await api.get<ApiResponse<{ is_valid: boolean; errores: string[] }>>(`${BASE_ENDPOINT}/copropiedad/${id}/validar`);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/copropiedad/${id}`);
	},

	async entregar(id: number, datos: Record<string, any>): Promise<PolizaCopropiedad> {
		const response = await api.post<ApiResponse<PolizaCopropiedad>>(`${BASE_ENDPOINT}/copropiedad/${id}/entregar`, datos);
		return response.data;
	},

	async actualizarEntrega(id: number, datos: Record<string, any>): Promise<PolizaCopropiedad> {
		const response = await api.patch<ApiResponse<PolizaCopropiedad>>(`${BASE_ENDPOINT}/copropiedad/${id}/actualizar-entrega`, datos);
		return response.data;
	}
};

// ============================================================================
// POLIZAS OTRO BIEN SERVICE
// ============================================================================
export const polizaOtroBienService = {
	async getAll(params?: { otro_bien_id?: number; usuario_id?: number; estado?: EstadoPoliza }): Promise<PolizaOtroBien[]> {
		const queryParams = new URLSearchParams();
		if (params?.otro_bien_id) queryParams.append('otro_bien_id', String(params.otro_bien_id));
		if (params?.usuario_id) queryParams.append('usuario_id', String(params.usuario_id));
		if (params?.estado) queryParams.append('estado', params.estado);
		const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
		const response = await api.get<ApiResponse<PolizaOtroBien[]>>(`${BASE_ENDPOINT}/otro-bien${query}`);
		return response.data;
	},

	async getById(id: number): Promise<PolizaOtroBien> {
		const response = await api.get<ApiResponse<PolizaOtroBien>>(`${BASE_ENDPOINT}/otro-bien/${id}`);
		return response.data;
	},

	async getByConsecutivo(consecutivo: string): Promise<PolizaOtroBien> {
		const response = await api.get<ApiResponse<PolizaOtroBien>>(`${BASE_ENDPOINT}/otro-bien/consecutivo/${consecutivo}`);
		return response.data;
	},

	async create(data: CreatePolizaOtroBienDto): Promise<PolizaOtroBien> {
		const response = await api.post<ApiResponse<PolizaOtroBien>>(`${BASE_ENDPOINT}/otro-bien`, data);
		return response.data;
	},

	async update(id: number, data: UpdatePolizaOtroBienDto): Promise<PolizaOtroBien> {
		const response = await api.put<ApiResponse<PolizaOtroBien>>(`${BASE_ENDPOINT}/otro-bien/${id}`, data);
		return response.data;
	},

	async cambiarEstado(id: number, data: CambiarEstadoDto): Promise<PolizaOtroBien> {
		const response = await api.patch<ApiResponse<PolizaOtroBien>>(`${BASE_ENDPOINT}/otro-bien/${id}/estado`, data);
		return response.data;
	},

	async validar(id: number): Promise<{ is_valid: boolean; errores: string[] }> {
		const response = await api.get<ApiResponse<{ is_valid: boolean; errores: string[] }>>(`${BASE_ENDPOINT}/otro-bien/${id}/validar`);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/otro-bien/${id}`);
	},

	async entregar(id: number, datos: Record<string, any>): Promise<PolizaOtroBien> {
		const response = await api.post<ApiResponse<PolizaOtroBien>>(`${BASE_ENDPOINT}/otro-bien/${id}/entregar`, datos);
		return response.data;
	},

	async actualizarEntrega(id: number, datos: Record<string, any>): Promise<PolizaOtroBien> {
		const response = await api.patch<ApiResponse<PolizaOtroBien>>(`${BASE_ENDPOINT}/otro-bien/${id}/actualizar-entrega`, datos);
		return response.data;
	}
};

// ============================================================================
// UNIFIED POLIZA SERVICE
// ============================================================================
export const polizaService = {
	/**
	 * Get all policies for a specific user/client
	 */
	async getAllByUsuario(usuarioId: number): Promise<{ data: PolizasUsuario; count: PolizasCount }> {
		const response = await api.get<ApiResponse<PolizasUsuario> & { count: PolizasCount }>(
			`${BASE_ENDPOINT}/usuario/${usuarioId}`
		);
		return { data: response.data, count: response.count };
	},

	/**
	 * Get policies about to expire
	 */
	async getPorVencer(dias: number = 30): Promise<{ data: PolizasUsuario; count: PolizasCount }> {
		const response = await api.get<ApiResponse<PolizasUsuario> & { count: PolizasCount; dias_consultados: number }>(
			`${BASE_ENDPOINT}/por-vencer?dias=${dias}`
		);
		return { data: response.data, count: response.count };
	},

	// Re-export individual services
	hogar: polizaHogarService,
	vehiculo: polizaVehiculoService,
	copropiedad: polizaCopropiedadService,
	otroBien: polizaOtroBienService
};
