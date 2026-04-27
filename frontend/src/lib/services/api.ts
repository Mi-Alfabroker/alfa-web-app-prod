/**
 * Base API service for HTTP requests
 * Implements a simple HTTP client with error handling
 */

import { API_BASE_URL, API_TIMEOUT } from '$lib/config';
import type { ApiResponse, ApiError } from '$lib/types';
import { browser } from '$app/environment';
import { clearSession, getAccessToken, getRefreshToken, updateAccessToken } from '$lib/stores/auth';

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface RequestOptions {
	headers?: Record<string, string>;
	timeout?: number;
	skipAuth?: boolean;
	retryOnAuthFailure?: boolean;
}

class ApiService {
	private baseUrl: string;
	private defaultTimeout: number;

	constructor(baseUrl: string = API_BASE_URL, timeout: number = API_TIMEOUT) {
		this.baseUrl = baseUrl;
		this.defaultTimeout = timeout;
	}

	private async request<T>(
		method: HttpMethod,
		endpoint: string,
		data?: unknown,
		options: RequestOptions = {}
	): Promise<T> {
		const url = `${this.baseUrl}${endpoint}`;
		const shouldSkipAuth = options.skipAuth === true;
		const shouldRetry = options.retryOnAuthFailure !== false;
		const controller = new AbortController();
		const timeoutId = setTimeout(
			() => controller.abort(),
			options.timeout || this.defaultTimeout
		);

		try {
			const headers: Record<string, string> = {
				'Content-Type': 'application/json',
				...options.headers
			};

			if (!shouldSkipAuth) {
				const token = getAccessToken();
				if (token) {
					headers.Authorization = `Bearer ${token}`;
				}
			}

			const response = await fetch(url, {
				method,
				headers,
				body: data ? JSON.stringify(data) : undefined,
				signal: controller.signal
			});

			clearTimeout(timeoutId);

			if (response.status === 401 && !shouldSkipAuth && shouldRetry) {
				const refreshed = await this.refreshAccessToken();
				if (refreshed) {
					return this.request<T>(method, endpoint, data, {
						...options,
						retryOnAuthFailure: false
					});
				}
			}

			if (!response.ok) {
				const payload = await response.json().catch(() => null);
				const error: ApiError = {
					message:
						payload?.error?.message ||
						payload?.message ||
						`HTTP Error: ${response.status} ${response.statusText}`,
					code: payload?.error?.code || payload?.code
				};
				throw error;
			}

			return await response.json();
		} catch (error) {
			clearTimeout(timeoutId);

			if (error instanceof Error && error.name === 'AbortError') {
				throw { message: 'Request timeout', code: 'TIMEOUT' } as ApiError;
			}

			throw error;
		}
	}

	private async refreshAccessToken(): Promise<boolean> {
		const refreshToken = getRefreshToken();
		if (!refreshToken) {
			this.handleAuthFailure();
			return false;
		}

		try {
			const response = await fetch(`${this.baseUrl}/api/auth/refresh`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ refresh_token: refreshToken })
			});

			if (!response.ok) {
				this.handleAuthFailure();
				return false;
			}

			const payload = (await response.json()) as ApiResponse<{ access_token: string }>;
			if (!payload?.data?.access_token) {
				this.handleAuthFailure();
				return false;
			}

			updateAccessToken(payload.data.access_token);
			return true;
		} catch {
			this.handleAuthFailure();
			return false;
		}
	}

	private handleAuthFailure(): void {
		clearSession();
		if (browser && window.location.pathname !== '/login') {
			window.location.href = '/login';
		}
	}

	async get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
		return this.request<T>('GET', endpoint, undefined, options);
	}

	async post<T>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<T> {
		return this.request<T>('POST', endpoint, data, options);
	}

	async put<T>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<T> {
		return this.request<T>('PUT', endpoint, data, options);
	}

	async patch<T>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<T> {
		return this.request<T>('PATCH', endpoint, data, options);
	}

	async delete<T>(endpoint: string, options?: RequestOptions): Promise<T> {
		return this.request<T>('DELETE', endpoint, undefined, options);
	}
}

// Singleton instance
export const api = new ApiService();

// Export class for testing or custom instances
export { ApiService };
