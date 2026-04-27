export type UserRole = 'AGENTE' | 'ADMINISTRADOR' | 'SUPERADMIN' | 'CLIENTE';

export interface AuthUser {
	id: number;
	usuario: string;
	tipo_usuario: UserRole;
	nombre?: string;
	razon_social?: string;
	correo?: string;
}

export interface AuthTokens {
	access_token: string;
	refresh_token: string;
	token_type: 'Bearer';
	expires_in: number;
}

export interface LoginResponse {
	user: AuthUser;
	tokens: AuthTokens;
}

export interface RefreshResponse {
	access_token: string;
	token_type: 'Bearer';
	expires_in: number;
}
