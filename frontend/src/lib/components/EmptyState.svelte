<script lang="ts">
	/**
	 * EmptyState - card shown when a list has no rows or no matches.
	 *
	 * @prop title - heading
	 * @prop text - explanatory copy (max 42ch by design)
	 * @slot icon - overrides the default magnifier tile
	 * @slot action - optional button, e.g. "Limpiar filtros"
	 */
	export let title: string = 'Sin resultados';
	export let text: string = '';
</script>

<div class="empty-state">
	<div class="empty-state-icon">
		<slot name="icon">
			<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
				<circle cx="11" cy="11" r="6.5" />
				<path d="M16 16l4.5 4.5M8.5 11h5" />
			</svg>
		</slot>
	</div>
	<h3 class="empty-state-title">{title}</h3>
	{#if text}
		<p class="empty-state-text">{text}</p>
	{/if}
	<slot name="action" />
</div>
