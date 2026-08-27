/**
 * Formatting utility functions
 */

const DATE_ONLY = /^(\d{4})-(\d{2})-(\d{2})$/;

/**
 * Parse a value coming from the API into a Date.
 *
 * Date-only columns (`inicio_vigencia`, `fin_vigencia`, …) arrive as
 * "2026-01-31". `new Date()` reads that as UTC midnight, which in Colombia
 * (UTC-5) renders as the 30th — a vigencia would display one day early. Those
 * are calendar dates with no time zone, so they are built from their parts at
 * local midnight instead. Full timestamps keep normal parsing.
 */
export function parseApiDate(date: string | Date | null | undefined): Date | null {
	if (!date) return null;
	if (date instanceof Date) return Number.isNaN(date.getTime()) ? null : date;
	const parts = DATE_ONLY.exec(date);
	if (parts) {
		return new Date(Number(parts[1]), Number(parts[2]) - 1, Number(parts[3]));
	}
	const parsed = new Date(date);
	return Number.isNaN(parsed.getTime()) ? null : parsed;
}

/**
 * Format a date string to locale date
 */
export function formatDate(date: string | Date, locale: string = 'es-CO'): string {
	const d = parseApiDate(date);
	if (!d) return '—';
	return d.toLocaleDateString(locale, {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});
}

/**
 * Format a date string to locale date and time
 */
export function formatDateTime(date: string | Date, locale: string = 'es-CO'): string {
	const d = parseApiDate(date);
	if (!d) return '—';
	return d.toLocaleString(locale, {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit'
	});
}

const MESES_CORTOS = [
	'ene',
	'feb',
	'mar',
	'abr',
	'may',
	'jun',
	'jul',
	'ago',
	'sep',
	'oct',
	'nov',
	'dic'
];

/**
 * Short date, e.g. "01 feb 2026" — the form used across list and detail views.
 *
 * Assembled by hand rather than through Intl: es-CO's `month: 'short'` renders
 * "30 de ene de 2026", which is too long for a table cell or a row card.
 */
export function formatDateShort(date: string | Date | null | undefined): string {
	const d = parseApiDate(date);
	if (!d) return '—';
	const day = String(d.getDate()).padStart(2, '0');
	return `${day} ${MESES_CORTOS[d.getMonth()]} ${d.getFullYear()}`;
}

/**
 * Format a number as currency. Colombian pesos, which is what the backend
 * stores and what every proposal template is denominated in.
 */
export function formatCurrency(
	amount: number,
	currency: string = 'COP',
	locale: string = 'es-CO'
): string {
	return new Intl.NumberFormat(locale, {
		style: 'currency',
		currency,
		maximumFractionDigits: 0
	}).format(amount);
}

/**
 * Compact peso amount, e.g. "$4.820.000". No currency code, es-CO grouping —
 * the form the design uses in tables, row cards and metrics.
 */
export function money(amount: number | null | undefined): string {
	if (amount === null || amount === undefined || Number.isNaN(Number(amount))) return '—';
	return '$' + Math.round(Number(amount)).toLocaleString('es-CO');
}

/**
 * Peso amount abbreviated to millions, for KPI tiles: 4820000 -> "$4,8 M".
 */
export function moneyShort(amount: number | null | undefined): string {
	if (amount === null || amount === undefined || Number.isNaN(Number(amount))) return '—';
	const n = Number(amount);
	if (Math.abs(n) >= 1_000_000) {
		return '$' + (n / 1_000_000).toLocaleString('es-CO', { maximumFractionDigits: 1 }) + ' M';
	}
	if (Math.abs(n) >= 1_000) {
		return '$' + (n / 1_000).toLocaleString('es-CO', { maximumFractionDigits: 0 }) + ' K';
	}
	return money(n);
}

/**
 * Up to two initials from a name, skipping short connector words
 * ("Familia Restrepo Uribe" -> "RU", "Global Re" -> "GL").
 */
export function initials(name: string | null | undefined): string {
	if (!name) return '—';
	const words = name.trim().split(/\s+/).filter((w) => w.length > 2);
	const source = words.length ? words : name.trim().split(/\s+/);
	const letters = source.map((w) => w[0]).slice(0, 2).join('');
	return (letters || name.slice(0, 2)).toUpperCase();
}
