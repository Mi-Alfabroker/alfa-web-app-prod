/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				// Alfabroker brand gold color palette
				// Base color: #E5B94E
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
					950: '#4a3912'
				},
				// Neutral gray palette for text and backgrounds
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
				}
			},
			fontFamily: {
				sans: ['Inter', 'system-ui', 'sans-serif']
			}
		}
	},
	plugins: []
};
