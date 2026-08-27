<script lang="ts">
	/**
	 * StatusBadge - status indicator with a dot, drawn from the design system's
	 * four tag variants.
	 *
	 * The design has no six-hue status palette: states collapse onto
	 * accent (active), accent-2 (pending/informational), neutral (inert) and
	 * outline (terminal/negative). Every status key the app used before is
	 * still accepted, so callers need no changes.
	 *
	 * @prop status - Status key
	 * @prop label - Display label (optional, uses status if not provided)
	 */
	type TagVariant = 'accent' | 'accent-2' | 'neutral' | 'outline';

	export let status: string;
	export let label: string = '';

	const statusVariants: Record<string, TagVariant> = {
		// Active / positive
		vigente: 'accent',
		activo: 'accent',
		activa: 'accent',
		emision: 'accent',
		aceptada: 'accent',
		// Pending / informational
		prospecto: 'accent-2',
		cotizacion: 'accent-2',
		propuesta: 'accent-2',
		en_espera: 'accent-2',
		pendiente: 'accent-2',
		por_vencer: 'accent-2',
		enviada: 'accent-2',
		// Inert
		inactivo: 'neutral',
		inactiva: 'neutral',
		vencida: 'neutral',
		borrador: 'neutral',
		// Terminal / negative
		suspendida: 'outline',
		cancelada: 'outline',
		anulada: 'outline',
		rechazada: 'outline',
		bloqueado: 'outline'
	};

	// The dot reads as an intensity cue, so it tracks the variant rather than
	// carrying its own colour scale.
	const dotColors: Record<TagVariant, string> = {
		accent: 'var(--color-accent-600)',
		'accent-2': 'var(--color-accent-2-400)',
		neutral: 'color-mix(in srgb, var(--color-text) 38%, transparent)',
		outline: 'var(--color-accent-800)'
	};

	$: variant = statusVariants[status.toLowerCase()] ?? 'neutral';
	$: displayLabel = label || status;
</script>

<span class="tag tag-{variant} status-badge">
	<span class="status-badge-dot" style="background: {dotColors[variant]}"></span>
	{displayLabel}
</span>
