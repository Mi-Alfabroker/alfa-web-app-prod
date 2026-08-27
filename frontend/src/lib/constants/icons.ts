/**
 * Domain icons — one glyph per section, used everywhere that section is named.
 *
 * The sidebar and the dashboard's quick-action strip draw from this map so an
 * action tile carries the *same* glyph as the nav item it leads to. That is what
 * makes the dashboard readable as a map of the app instead of a set of unrelated
 * panels; duplicating the paths per screen would let the two drift apart.
 *
 * All glyphs are two-path, 24×24, 1.5 stroke, no fill — matching the design
 * system's icon style.
 */

export interface DomainIcon {
	/** Primary path. */
	d: string;
	/** Secondary path; every glyph here has one. */
	d2: string;
}

export const DOMAIN_ICONS: Record<string, DomainIcon> = {
	dashboard: {
		d: 'M4 13h6V4H4zM14 20h6v-9h-6z',
		d2: 'M14 8h6V4h-6zM4 20h6v-4H4z'
	},
	clientes: {
		d: 'M16 19v-1.5A3.5 3.5 0 0 0 12.5 14h-5A3.5 3.5 0 0 0 4 17.5V19',
		d2: 'M20 19v-1.5a3.5 3.5 0 0 0-2.6-3.4M10 4.8a3.2 3.2 0 1 1 0 6.4 3.2 3.2 0 0 1 0-6.4'
	},
	polizas: {
		d: 'M5 4h9l5 5v11a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1Z',
		d2: 'M14 4v5h5M8 13h8M8 17h5'
	},
	bienes: {
		d: 'M4 8.5 12 4l8 4.5v7L12 20l-8-4.5z',
		d2: 'M4 8.5 12 13l8-4.5M12 13v7'
	},
	aseguradoras: {
		d: 'M12 3l7 3v6c0 4.2-2.9 7.6-7 9-4.1-1.4-7-4.8-7-9V6z',
		d2: 'M9.5 12l1.8 1.8L15 10'
	},
	reportes: {
		d: 'M4 20V4M4 20h16',
		d2: 'M8 17v-6h3v6zM14 17V7h3v10z'
	}
};
