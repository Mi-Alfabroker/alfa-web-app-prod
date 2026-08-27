<script lang="ts">
	/**
	 * KpiRow - auto-fitting row of KPI tiles.
	 *
	 * @prop kpis - label / value / note triples; values render in the heading face
	 */
	export let kpis: { label: string; value: string; note?: string }[] = [];
</script>

{#if kpis.length}
	<div class="kpi-row">
		{#each kpis as kpi}
			<div class="kpi-card">
				<div class="kpi-label">{kpi.label}</div>
				<div class="kpi-value">{kpi.value}</div>
				{#if kpi.note}
					<div class="kpi-note">{kpi.note}</div>
				{/if}
			</div>
		{/each}
	</div>
{/if}
