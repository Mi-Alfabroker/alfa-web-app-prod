/**
 * Global loading state store
 */

import { writable } from 'svelte/store';

export const loading = writable<boolean>(false);

export function setLoading(value: boolean): void {
	loading.set(value);
}

/**
 * Utility to wrap async operations with loading state
 */
export async function withLoading<T>(operation: () => Promise<T>): Promise<T> {
	setLoading(true);
	try {
		return await operation();
	} finally {
		setLoading(false);
	}
}
