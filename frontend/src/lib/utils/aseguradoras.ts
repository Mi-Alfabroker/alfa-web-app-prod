/**
 * Aseguradora helpers.
 *
 * An aseguradora record carries the broker's negotiated conditions for each
 * rubro as flat, prefixed columns (`cop_*`, `hog_*`, `veh_*`, `otr_*`). The
 * prefix is the only thing that groups them, so these helpers read that prefix
 * rather than maintaining a second list that could drift from the type.
 */

import type { Aseguradora } from '$lib/types/aseguradora';

/** Column prefix per rubro, in the order the design tabs them. */
export const RUBRO_PREFIXES = [
	{ id: 'cop', label: 'Copropiedades', prefix: 'cop_' },
	{ id: 'hog', label: 'Hogar', prefix: 'hog_' },
	{ id: 'veh', label: 'Vehículos', prefix: 'veh_' },
	{ id: 'otr', label: 'Otros ramos', prefix: 'otr_' }
] as const;

export type RubroPrefixId = (typeof RUBRO_PREFIXES)[number]['id'];

const ALL_PREFIXES = RUBRO_PREFIXES.map((r) => r.prefix);

/** True when the key is one of the per-rubro condition columns. */
export function isRubroField(key: string): boolean {
	return ALL_PREFIXES.some((p) => key.startsWith(p));
}

/**
 * How many per-rubro conditions this aseguradora actually has on record.
 * Empty columns are not counted: the number is meant to say "how much of this
 * aseguradora is configured", not how wide the table is.
 */
export function valoresConfigurados(
	aseguradora: Aseguradora | Record<string, unknown>,
	prefix?: string
): number {
	return Object.entries(aseguradora).filter(([key, value]) => {
		if (prefix ? !key.startsWith(prefix) : !isRubroField(key)) return false;
		return value !== null && value !== undefined && value !== '';
	}).length;
}
