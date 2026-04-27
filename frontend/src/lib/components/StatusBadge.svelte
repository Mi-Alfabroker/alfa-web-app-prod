<script lang="ts">
	/**
	 * StatusBadge - Status indicator with colored dot and label
	 * 
	 * @prop status - Status key
	 * @prop label - Display label (optional, uses status if not provided)
	 */

	export let status: string;
	export let label: string = '';

	// Status color mappings
	const statusColors: Record<string, { bg: string; text: string; dot: string }> = {
		// Propuestas
		prospecto: { bg: 'bg-secondary-100', text: 'text-secondary-700', dot: 'bg-secondary-400' },
		cotizacion: { bg: 'bg-amber-50', text: 'text-amber-700', dot: 'bg-amber-400' },
		propuesta: { bg: 'bg-blue-50', text: 'text-blue-700', dot: 'bg-blue-400' },
		en_espera: { bg: 'bg-orange-50', text: 'text-orange-700', dot: 'bg-orange-400' },
		emision: { bg: 'bg-purple-50', text: 'text-purple-700', dot: 'bg-purple-400' },
		vigente: { bg: 'bg-green-50', text: 'text-green-700', dot: 'bg-green-500' },
		vencida: { bg: 'bg-red-50', text: 'text-red-700', dot: 'bg-red-500' },
		por_vencer: { bg: 'bg-yellow-50', text: 'text-yellow-700', dot: 'bg-yellow-500' },
		pendiente: { bg: 'bg-amber-50', text: 'text-amber-700', dot: 'bg-amber-400' },
		// Generic states
		activo: { bg: 'bg-green-50', text: 'text-green-700', dot: 'bg-green-500' },
		inactivo: { bg: 'bg-secondary-100', text: 'text-secondary-600', dot: 'bg-secondary-400' },
		// Aseguradoras
		activa: { bg: 'bg-green-50', text: 'text-green-700', dot: 'bg-green-500' },
		inactiva: { bg: 'bg-secondary-100', text: 'text-secondary-600', dot: 'bg-secondary-400' },
		suspendida: { bg: 'bg-red-50', text: 'text-red-700', dot: 'bg-red-500' }
	};

	$: colors = statusColors[status.toLowerCase()] || statusColors.prospecto;
	$: displayLabel = label || status;
</script>

<span class="status-badge {colors.bg} {colors.text}">
	<span class="status-badge-dot {colors.dot}"></span>
	{displayLabel}
</span>
