/**
 * Service for Cliente (Usuario) API operations
 */

import { api } from './api';
import type { Cliente, CreateClienteDto, UpdateClienteDto } from '$lib/types/cliente';
import type { ApiResponse } from '$lib/types';

const ENDPOINT = '/api/usuarios';

export const clienteService = {
	/**
	 * Get all clientes (usuarios con tipo_usuario = CLIENTE)
	 */
	async getAll(): Promise<Cliente[]> {
		const response = await api.get<ApiResponse<Cliente[]>>(`${ENDPOINT}?tipo_usuario=CLIENTE`);
		return response.data;
	},

	/**
	 * Get all usuarios (sin filtro)
	 */
	async getAllUsuarios(): Promise<Cliente[]> {
		const response = await api.get<ApiResponse<Cliente[]>>(ENDPOINT);
		return response.data;
	},

	/**
	 * Get a single cliente by ID
	 */
	async getById(id: number): Promise<Cliente> {
		const response = await api.get<ApiResponse<Cliente>>(`${ENDPOINT}/${id}`);
		return response.data;
	},

	/**
	 * Create a new cliente
	 * Por defecto, tipo_usuario será 'CLIENTE'
	 */
	async create(data: CreateClienteDto): Promise<Cliente> {
		// Asegurar que tipo_usuario sea CLIENTE por defecto
		const payload: CreateClienteDto = {
			...data,
			tipo_usuario: data.tipo_usuario || 'CLIENTE'
		};
		const response = await api.post<ApiResponse<Cliente>>(ENDPOINT, payload);
		return response.data;
	},

	/**
	 * Update an existing cliente
	 */
	async update(id: number, data: UpdateClienteDto): Promise<Cliente> {
		const response = await api.put<ApiResponse<Cliente>>(`${ENDPOINT}/${id}`, data);
		return response.data;
	},

	/**
	 * Delete a cliente
	 */
	async delete(id: number): Promise<void> {
		await api.delete(`${ENDPOINT}/${id}`);
	}
};
