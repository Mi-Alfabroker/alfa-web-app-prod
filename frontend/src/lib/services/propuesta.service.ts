/**
 * Service for proposal (propuesta) generation
 * Handles API calls to generate Excel proposals from templates
 */

import { API_BASE_URL, API_TIMEOUT } from '$lib/config';
import { getAccessToken } from '$lib/stores/auth';

export interface GenerateProposalRequest {
	template_name: string;
	variables: Record<string, string>;
	imagenes?: Record<string, string>;
}

export interface GenerateProposalResponse {
	success: boolean;
	filename: string;
	savedPath: string;
	blob: Blob;
}

export interface TemplatesResponse {
	success: boolean;
	data: string[];
	count: number;
}

class PropuestaService {
	private baseUrl: string;

	constructor(baseUrl: string = API_BASE_URL) {
		this.baseUrl = baseUrl;
	}

	/**
	 * Get available templates
	 */
	async getTemplates(): Promise<string[]> {
		const headers: Record<string, string> = {
			'Content-Type': 'application/json'
		};

		const token = getAccessToken();
		if (token) {
			headers.Authorization = `Bearer ${token}`;
		}

		const response = await fetch(`${this.baseUrl}/api/propuestas/templates`, {
			headers
		});
		
		if (!response.ok) {
			throw new Error('Error al obtener plantillas disponibles');
		}
		
		const data: TemplatesResponse = await response.json();
		return data.data;
	}

	/**
	 * Generate a proposal document from a template
	 * Returns the Excel file as a Blob for download
	 */
	async generate(request: GenerateProposalRequest): Promise<GenerateProposalResponse> {
		const controller = new AbortController();
		const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

		try {
			const headers: Record<string, string> = {
				'Content-Type': 'application/json'
			};

			const token = getAccessToken();
			if (token) {
				headers.Authorization = `Bearer ${token}`;
			}

			const response = await fetch(`${this.baseUrl}/api/propuestas/generate`, {
				method: 'POST',
				headers,
				body: JSON.stringify(request),
				signal: controller.signal
			});

			clearTimeout(timeoutId);

			if (!response.ok) {
				const error = await response.json().catch(() => ({ error: 'Error desconocido' }));
				throw new Error(error.error || `Error ${response.status}: ${response.statusText}`);
			}

			// Get the filename from Content-Disposition header or use default
			const contentDisposition = response.headers.get('Content-Disposition');
			let filename = `propuesta_${request.template_name}.xlsx`;
			
			if (contentDisposition) {
				const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
				if (filenameMatch && filenameMatch[1]) {
					filename = filenameMatch[1].replace(/['"]/g, '');
				}
			}

			// Get the saved path from custom header
			const savedPath = response.headers.get('X-Saved-Path') || '';

			// Get the blob
			const blob = await response.blob();

			return {
				success: true,
				filename,
				savedPath,
				blob
			};
		} catch (error) {
			clearTimeout(timeoutId);

			if (error instanceof Error && error.name === 'AbortError') {
				throw new Error('Tiempo de espera agotado al generar la propuesta');
			}

			throw error;
		}
	}

	/**
	 * Helper to download a blob as a file
	 */
	downloadBlob(blob: Blob, filename: string): void {
		const url = window.URL.createObjectURL(blob);
		const link = document.createElement('a');
		link.href = url;
		link.download = filename;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		window.URL.revokeObjectURL(url);
	}

	/**
	 * Generate and automatically download the proposal
	 */
	async generateAndDownload(request: GenerateProposalRequest): Promise<GenerateProposalResponse> {
		const result = await this.generate(request);
		this.downloadBlob(result.blob, result.filename);
		return result;
	}
}

// Singleton instance
export const propuestaService = new PropuestaService();
