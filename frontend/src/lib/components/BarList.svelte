<script lang="ts">
	/**
	 * BarList - compact horizontal bar list for magnitude comparison across a few
	 * named categories (cartera por rubro, por aseguradora).
	 *
	 * Single series, so every bar carries the SAME hue: the categories are nominal
	 * (swapping their order changes nothing), and colouring them individually would
	 * spend the identity channel re-encoding what bar length already shows.
	 * One series also means no legend — the card heading names the measure.
	 *
	 * The gold ramp cannot reach 3:1 against this light surface without losing its
	 * chroma, so the bar fill sits at the highest-chroma step that clears the
	 * lightness band (accent-700, 2.88:1) and **every row is directly labelled**,
	 * which is the relief that makes a sub-3:1 mark legitimate.
	 *
	 * @prop items - rows; `value` drives the bar, `valueLabel` is the visible text
	 * @prop emptyText - shown when there is nothing to plot
	 */
	export let items: {
		label: string;
		value: number;
		valueLabel: string;
		note?: string;
		tooltip?: string;
	}[] = [];
	export let emptyText: string = 'Sin datos para mostrar.';

	// Bars are normalised to the largest row, not to a total: this compares
	// magnitudes, it is not a part-to-whole.
	$: max = items.reduce((m, i) => Math.max(m, i.value), 0);

	function widthOf(value: number): string {
		if (max <= 0 || value <= 0) return '0%';
		// Floor so a small-but-nonzero row stays visible instead of vanishing.
		return `max(3%, ${(value / max) * 100}%)`;
	}
</script>

{#if !items.length}
	<p class="text-sm" style="color: var(--color-text-60)">{emptyText}</p>
{:else}
	<div class="flex flex-col gap-3">
		{#each items as item}
			<div title={item.tooltip ?? `${item.label}: ${item.valueLabel}`}>
				<div class="flex items-baseline gap-2 mb-1.5">
					<span class="text-[13px] truncate">{item.label}</span>
					<span class="ml-auto text-[13px] font-semibold whitespace-nowrap">
						{item.valueLabel}
					</span>
				</div>
				<div class="bar-track">
					{#if item.value > 0}
						<div class="bar-fill" style="width: {widthOf(item.value)}"></div>
					{/if}
				</div>
				{#if item.note}
					<div class="text-xs mt-1" style="color: var(--color-text-55)">{item.note}</div>
				{/if}
			</div>
		{/each}
	</div>
{/if}
