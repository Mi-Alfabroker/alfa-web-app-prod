<script lang="ts">
	/**
	 * ListRowCard - the design's list primitive: a header line (lead tile, title,
	 * tags, right-aligned actions) above an auto-fitting metadata grid.
	 *
	 * Replaces table rows for the pólizas, clientes and aseguradoras lists.
	 *
	 * @prop fields - the metadata grid; entries with an empty value are dropped
	 * @slot lead - avatar or sigla tile
	 * @slot title - the row's headline (plain text or a link)
	 * @slot tags - status/type tags shown beside the title
	 * @slot actions - buttons pinned to the right of the header line
	 */
	export let fields: { label: string; value: string; strong?: boolean }[] = [];

	$: visibleFields = fields.filter((f) => f.value !== '' && f.value !== null && f.value !== undefined);
</script>

<div class="row-card">
	<div class="row-card-head">
		<slot name="lead" />
		<slot name="title" />
		<slot name="tags" />
		<div class="row-card-actions">
			<slot name="actions" />
		</div>
	</div>

	{#if visibleFields.length}
		<div class="field-grid">
			{#each visibleFields as field}
				<div>
					<div class="field-label">{field.label}</div>
					<div class="field-value" class:font-normal={!field.strong}>{field.value}</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
