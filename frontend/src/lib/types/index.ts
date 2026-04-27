/**
 * Shared TypeScript types and interfaces
 */

// API Response types
export interface ApiResponse<T> {
	data: T;
	message?: string;
	success: boolean;
}

export interface ApiError {
	message: string;
	code?: string;
	details?: Record<string, unknown>;
}

export interface PaginatedResponse<T> {
	items: T[];
	total: number;
	page: number;
	pageSize: number;
	totalPages: number;
}

// Common entity types
export interface BaseEntity {
	id: number;
	created_at?: string;
	updated_at?: string;
}

// Entity types
export * from './aseguradora';
export * from './cliente';
export * from './bien';
export * from './poliza';
export * from './auth';
