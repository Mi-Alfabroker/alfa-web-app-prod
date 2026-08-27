<script lang="ts">
	/**
	 * FilterBar - search field, N dropdowns, a reset, and a record count.
	 *
	 * The parent owns the filter state; this component only reports changes, so
	 * a page can derive its filtered list however it likes.
	 *
	 * @prop query - bound search text
	 * @prop placeholder - search field placeholder
	 * @prop selects - dropdown definitions; `value` is bound back through `onChange`
	 * @prop count - number of records after filtering
	 * @prop countNoun - singular noun for the count, e.g. "póliza"
	 * @slot extra - additional controls, rendered before the reset button
	 */
	export let query: string = '';
	export let placeholder: string = 'Buscar…';
	export let selects: {
		value: string;
		options: { value: string; label: string }[];
		onChange: (value: string) => void;
		label?: string;
	}[] = [];
	export let count: number | null = null;
	export let countNoun: string = 'registro';
	export let onReset: () => void = () => {};

	$: hasActiveFilters = query.trim() !== '' || selects.some((s) => s.value !== '');
	$: countText =
		count === null ? '' : `${count} ${countNoun}${count === 1 ? '' : 's'}`;
</script>

<div class="filter-bar">
	<div class="relative flex-1 min-w-[200px]">
		<svg
			class="absolute left-3 top-1/2 -translate-y-1/2 opacity-50"
			width="16"
			height="16"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="1.5"
		>
			<circle cx="11" cy="11" r="6.5" />
			<path d="M16 16l4.5 4.5" />
		</svg>
		<input
			class="input !pl-9 !min-h-[38px]"
			type="search"
			bind:value={query}
			{placeholder}
			aria-label={placeholder}
		/>
	</div>

	{#each selects as select}
		<select
			class="select !w-auto !min-w-[158px] !min-h-[38px]"
			value={select.value}
			aria-label={select.label ?? 'Filtro'}
			on:change={(e) => select.onChange(e.currentTarget.value)}
		>
			{#each select.options as option}
				<option value={option.value}>{option.label}</option>
			{/each}
		</select>
	{/each}

	<slot name="extra" />

	{#if hasActiveFilters}
		<button type="button" class="btn-ghost !min-h-[38px]" on:click={onReset}>
			Limpiar filtros
		</button>
	{/if}

	{#if countText}
		<div class="ml-auto text-xs whitespace-nowrap" style="color: var(--color-text-55)">
			{countText}
		</div>
	{/if}
</div>
