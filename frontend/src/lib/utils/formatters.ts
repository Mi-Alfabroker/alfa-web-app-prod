/**
 * Formatting utility functions
 */

/**
 * Format a date string to locale date
 */
export function formatDate(date: string | Date, locale: string = 'es-ES'): string {
	const d = typeof date === 'string' ? new Date(date) : date;
	return d.toLocaleDateString(locale, {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});
}

/**
 * Format a date string to locale date and time
 */
export function formatDateTime(date: string | Date, locale: string = 'es-ES'): string {
	const d = typeof date === 'string' ? new Date(date) : date;
	return d.toLocaleString(locale, {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit'
	});
}

/**
 * Format a number as currency
 */
export function formatCurrency(
	amount: number,
	currency: string = 'CLP',
	locale: string = 'es-CL'
): string {
	return new Intl.NumberFormat(locale, {
		style: 'currency',
		currency
	}).format(amount);
}
