/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				// Alfabroker brand gold color palette
				// Base color: #E5B94E
				// Steps 100-900 double as the design-system accent ramp
				// (--color-accent-*), so both access paths resolve to the same hexes.
				primary: {
					50: '#fefdf7',
					100: '#fdf9e9',
					200: '#fbf0c8',
					300: '#f7e4a0',
					400: '#f0ce6f',
					500: '#E5B94E',  // Base gold color
					600: '#d4a53b',
					700: '#b08a2e',
					800: '#8d6e25',
					900: '#735a1f',
					950: '#4a3912'   // Ink on gold fills (--color-accent-ink)
				},
				// Neutral gray palette for text and backgrounds.
				// Also the accent-2 ramp: the design system collapses accent and
				// accent-2 to the same gold, which makes the "active" and
				// "pending" tags indistinguishable. Slate keeps them apart.
				secondary: {
					50: '#f8fafc',
					100: '#f1f5f9',
					200: '#e2e8f0',
					300: '#cbd5e1',
					400: '#94a3b8',
					500: '#64748b',
					600: '#475569',
					700: '#334155',
					800: '#1e293b',
					900: '#0f172a',
					950: '#020617'
				},
				// Design-system surfaces. Cards/sidebar/topbar (surface-raised) sit
				// LIGHTER than the page (surface-sunken).
				surface: {
					raised: '#f2f2f3',
					sunken: '#e9e9ea'
				},
				ink: '#1d1f20'
			},
			fontFamily: {
				sans: ['Barlow', 'system-ui', 'sans-serif'],
				heading: ['Barlow Condensed', 'system-ui', 'sans-serif']
			},
			// Retuned to the design's radii. Deliberately global: every existing
			// rounded-lg control and rounded-2xl card picks these up at once.
			borderRadius: {
				lg: '9px',
				xl: '10px',
				'2xl': '14px',
				'3xl': '16px'
			},
			// Ink-tinted elevation from the design system.
			boxShadow: {
				sm: '0 1px 2px color-mix(in srgb, #2b2b2d 14%, transparent)',
				DEFAULT: '0 1px 2px color-mix(in srgb, #2b2b2d 14%, transparent)',
				md: '0 3px 10px color-mix(in srgb, #2b2b2d 16%, transparent)',
				lg: '0 12px 32px color-mix(in srgb, #2b2b2d 22%, transparent)'
			}
		}
	},
	plugins: []
};
