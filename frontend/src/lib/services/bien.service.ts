/**
 * Service for Bienes (Assets) API operations
 */

import { api } from './api';
import type { ApiResponse } from '$lib/types';
import type {
	Hogar, CreateHogarDto, UpdateHogarDto,
	Vehiculo, CreateVehiculoDto, UpdateVehiculoDto,
	Copropiedad, CreateCopropiedadDto, UpdateCopropiedadDto,
	OtroBien, CreateOtroBienDto, UpdateOtroBienDto,
	BienesUsuario, BienesCount
} from '$lib/types/bien';

const BASE_ENDPOINT = '/api/bienes';

// ============================================================================
// HOGARES SERVICE
// ============================================================================
export const hogarService = {
	async getAll(usuarioId?: number): Promise<Hogar[]> {
		const params = usuarioId ? `?usuario_id=${usuarioId}` : '';
		const response = await api.get<ApiResponse<Hogar[]>>(`${BASE_ENDPOINT}/hogares${params}`);
		return response.data;
	},

	async getById(id: number): Promise<Hogar> {
		const response = await api.get<ApiResponse<Hogar>>(`${BASE_ENDPOINT}/hogares/${id}`);
		return response.data;
	},

	async create(data: CreateHogarDto): Promise<Hogar> {
		const response = await api.post<ApiResponse<Hogar>>(`${BASE_ENDPOINT}/hogares`, data);
		return response.data;
	},

	async update(id: number, data: UpdateHogarDto): Promise<Hogar> {
		const response = await api.put<ApiResponse<Hogar>>(`${BASE_ENDPOINT}/hogares/${id}`, data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/hogares/${id}`);
	}
};

// ============================================================================
// VEHICULOS SERVICE
// ============================================================================
export const vehiculoService = {
	async getAll(usuarioId?: number): Promise<Vehiculo[]> {
		const params = usuarioId ? `?usuario_id=${usuarioId}` : '';
		const response = await api.get<ApiResponse<Vehiculo[]>>(`${BASE_ENDPOINT}/vehiculos${params}`);
		return response.data;
	},

	async getById(id: number): Promise<Vehiculo> {
		const response = await api.get<ApiResponse<Vehiculo>>(`${BASE_ENDPOINT}/vehiculos/${id}`);
		return response.data;
	},

	async getByPlaca(placa: string): Promise<Vehiculo> {
		const response = await api.get<ApiResponse<Vehiculo>>(`${BASE_ENDPOINT}/vehiculos/placa/${placa}`);
		return response.data;
	},

	async create(data: CreateVehiculoDto): Promise<Vehiculo> {
		const response = await api.post<ApiResponse<Vehiculo>>(`${BASE_ENDPOINT}/vehiculos`, data);
		return response.data;
	},

	async update(id: number, data: UpdateVehiculoDto): Promise<Vehiculo> {
		const response = await api.put<ApiResponse<Vehiculo>>(`${BASE_ENDPOINT}/vehiculos/${id}`, data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/vehiculos/${id}`);
	}
};

// ============================================================================
// COPROPIEDADES SERVICE
// ============================================================================
export const copropiedadService = {
	async getAll(usuarioId?: number): Promise<Copropiedad[]> {
		const params = usuarioId ? `?usuario_id=${usuarioId}` : '';
		const response = await api.get<ApiResponse<Copropiedad[]>>(`${BASE_ENDPOINT}/copropiedades${params}`);
		return response.data;
	},

	async getById(id: number): Promise<Copropiedad> {
		const response = await api.get<ApiResponse<Copropiedad>>(`${BASE_ENDPOINT}/copropiedades/${id}`);
		return response.data;
	},

	async create(data: CreateCopropiedadDto): Promise<Copropiedad> {
		const response = await api.post<ApiResponse<Copropiedad>>(`${BASE_ENDPOINT}/copropiedades`, data);
		return response.data;
	},

	async update(id: number, data: UpdateCopropiedadDto): Promise<Copropiedad> {
		const response = await api.put<ApiResponse<Copropiedad>>(`${BASE_ENDPOINT}/copropiedades/${id}`, data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/copropiedades/${id}`);
	}
};

// ============================================================================
// OTROS BIENES SERVICE
// ============================================================================
export const otroBienService = {
	async getAll(usuarioId?: number): Promise<OtroBien[]> {
		const params = usuarioId ? `?usuario_id=${usuarioId}` : '';
		const response = await api.get<ApiResponse<OtroBien[]>>(`${BASE_ENDPOINT}/otros${params}`);
		return response.data;
	},

	async getById(id: number): Promise<OtroBien> {
		const response = await api.get<ApiResponse<OtroBien>>(`${BASE_ENDPOINT}/otros/${id}`);
		return response.data;
	},

	async create(data: CreateOtroBienDto): Promise<OtroBien> {
		const response = await api.post<ApiResponse<OtroBien>>(`${BASE_ENDPOINT}/otros`, data);
		return response.data;
	},

	async update(id: number, data: UpdateOtroBienDto): Promise<OtroBien> {
		const response = await api.put<ApiResponse<OtroBien>>(`${BASE_ENDPOINT}/otros/${id}`, data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`${BASE_ENDPOINT}/otros/${id}`);
	}
};

// ============================================================================
// UNIFIED BIENES SERVICE
// ============================================================================
export const bienService = {
	/**
	 * Get all assets for a specific user/client
	 */
	async getAllByUsuario(usuarioId: number): Promise<{ data: BienesUsuario; count: BienesCount }> {
		const response = await api.get<ApiResponse<BienesUsuario> & { count: BienesCount }>(
			`${BASE_ENDPOINT}/usuario/${usuarioId}`
		);
		return { data: response.data, count: response.count };
	},

	// Re-export individual services for convenience
	hogares: hogarService,
	vehiculos: vehiculoService,
	copropiedades: copropiedadService,
	otros: otroBienService
};
