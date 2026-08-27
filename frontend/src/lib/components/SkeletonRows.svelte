<script lang="ts">
	/**
	 * SkeletonRows - placeholder rows shown while a list loads, shaped like the
	 * row cards that replace them so the layout does not jump.
	 */
	export let count: number = 5;

	// Varying widths so the block reads as content rather than a progress bar.
	const widths = ['44%', '38%', '52%', '34%', '46%', '40%'];
</script>

<div class="row-list" aria-busy="true" aria-live="polite">
	{#each Array(count) as _, i}
		<div class="sk-row">
			<span class="sk-bar flex-none rounded-full" style="width: 38px; height: 38px"></span>
			<span class="block flex-1">
				<span
					class="sk-bar rounded-md"
					style="width: {widths[i % widths.length]}; height: 11px"
				></span>
				<span
					class="sk-bar rounded"
					style="width: 62%; height: 9px; margin-top: 8px; opacity: .7"
				></span>
			</span>
			<span class="sk-bar flex-none rounded-full" style="width: 96px; height: 22px"></span>
		</div>
	{/each}
	<span class="sr-only">Cargando…</span>
</div>
