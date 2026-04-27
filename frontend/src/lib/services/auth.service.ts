import { api } from './api';
import { clearSession, setSession, setAuthUser } from '$lib/stores/auth';
import type { ApiResponse } from '$lib/types';
import type { AuthUser, LoginResponse, RefreshResponse } from '$lib/types';

export const authService = {
	async login(usuario: string, clave: string): Promise<LoginResponse> {
		const response = await api.post<ApiResponse<LoginResponse>>(
			'/api/auth/login',
			{ usuario, clave },
			{ skipAuth: true }
		);

		setSession(response.data.user, response.data.tokens);
		return response.data;
	},

	async refresh(refreshToken: string): Promise<RefreshResponse> {
		const response = await api.post<ApiResponse<RefreshResponse>>(
			'/api/auth/refresh',
			{ refresh_token: refreshToken },
			{ skipAuth: true }
		);
		return response.data;
	},

	async me(): Promise<AuthUser> {
		const response = await api.get<ApiResponse<{ user: AuthUser }>>('/api/auth/me');
		setAuthUser(response.data.user);
		return response.data.user;
	},

	logout(): void {
		clearSession();
	}
};
