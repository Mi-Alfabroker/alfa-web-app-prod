import { browser } from '$app/environment';
import { writable } from 'svelte/store';
import type { AuthTokens, AuthUser, UserRole } from '$lib/types';

const ACCESS_TOKEN_KEY = 'ab_access_token';
const REFRESH_TOKEN_KEY = 'ab_refresh_token';
const USER_KEY = 'ab_auth_user';

export interface AuthState {
	user: AuthUser | null;
	isAuthenticated: boolean;
}

function loadUser(): AuthUser | null {
	if (!browser) return null;
	const raw = localStorage.getItem(USER_KEY);
	if (!raw) return null;
	try {
		return JSON.parse(raw) as AuthUser;
	} catch {
		return null;
	}
}

const initialUser = loadUser();
const initialAccessToken = browser ? localStorage.getItem(ACCESS_TOKEN_KEY) : null;

export const auth = writable<AuthState>({
	user: initialUser,
	isAuthenticated: Boolean(initialUser && initialAccessToken)
});

export function getAccessToken(): string | null {
	if (!browser) return null;
	return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
	if (!browser) return null;
	return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getAuthUser(): AuthUser | null {
	return loadUser();
}

export function setAuthTokens(tokens: AuthTokens): void {
	if (!browser) return;
	localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
	localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}

export function updateAccessToken(accessToken: string): void {
	if (!browser) return;
	localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
}

export function setAuthUser(user: AuthUser): void {
	if (browser) {
		localStorage.setItem(USER_KEY, JSON.stringify(user));
	}
	auth.set({ user, isAuthenticated: Boolean(getAccessToken()) });
}

export function setSession(user: AuthUser, tokens: AuthTokens): void {
	setAuthTokens(tokens);
	setAuthUser(user);
}

export function clearSession(): void {
	if (browser) {
		localStorage.removeItem(ACCESS_TOKEN_KEY);
		localStorage.removeItem(REFRESH_TOKEN_KEY);
		localStorage.removeItem(USER_KEY);
	}
	auth.set({ user: null, isAuthenticated: false });
}

export function hasAnyRole(role: UserRole | UserRole[]): boolean {
	const current = loadUser();
	if (!current) return false;
	const allowed = Array.isArray(role) ? role : [role];
	return allowed.includes(current.tipo_usuario);
}
