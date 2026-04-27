/**
 * Service for Aseguradora API operations
 */

import { api } from './api';
import type { Aseguradora, CreateAseguradoraDto, UpdateAseguradoraDto } from '$lib/types/aseguradora';
import type { ApiResponse, PaginatedResponse } from '$lib/types';

const ENDPOINT = '/api/aseguradoras';

export const aseguradoraService = {
	/**
	 * Get all aseguradoras
	 */
	async getAll(): Promise<Aseguradora[]> {
		const response = await api.get<ApiResponse<Aseguradora[]>>(ENDPOINT);
		return response.data;
	},

	/**
	 * Get paginated aseguradoras
	 */
	async getPaginated(page: number = 1, pageSize: number = 10): Promise<PaginatedResponse<Aseguradora>> {
		return api.get<PaginatedResponse<Aseguradora>>(`${ENDPOINT}?page=${page}&pageSize=${pageSize}`);
	},

	/**
	 * Get a single aseguradora by ID
	 */
	async getById(id: number): Promise<Aseguradora> {
		const response = await api.get<ApiResponse<Aseguradora>>(`${ENDPOINT}/${id}`);
		return response.data;
	},

	/**
	 * Get minimal data for policy delivery (nombre, numeral_asistencia)
	 */
	async getDatosEntrega(id: number): Promise<{ id: number; nombre: string; numeral_asistencia: string | null }> {
		const response = await api.get<ApiResponse<{ id: number; nombre: string; numeral_asistencia: string | null }>>(`${ENDPOINT}/${id}/datos-entrega`);
		return response.data;
	},

	/**
	 * Create a new aseguradora
	 */
	async create(data: CreateAseguradoraDto): Promise<Aseguradora> {
		const response = await api.post<ApiResponse<Aseguradora>>(ENDPOINT, data);
		return response.data;
	},

	/**
	 * Update an existing aseguradora
	 */
	async update(id: number, data: UpdateAseguradoraDto): Promise<Aseguradora> {
		const response = await api.put<ApiResponse<Aseguradora>>(`${ENDPOINT}/${id}`, data);
		return response.data;
	},

	/**
	 * Delete an aseguradora
	 */
	async delete(id: number): Promise<void> {
		await api.delete(`${ENDPOINT}/${id}`);
	}
};
