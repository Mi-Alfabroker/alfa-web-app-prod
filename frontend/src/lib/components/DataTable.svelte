<script lang="ts">
	/**
	 * DataTable - Reusable data table component
	 * 
	 * @prop columns - Array of column definitions
	 * @prop data - Array of data rows
	 * @prop selectable - Enable row selection with checkboxes
	 * @prop selectedIds - Array of selected row IDs (bindable)
	 */

	import { createEventDispatcher } from 'svelte';

	type Column = {
		key: string;
		label: string;
		sortable?: boolean;
		width?: string;
	};

	export let columns: Column[] = [];
	export let data: Record<string, unknown>[] = [];
	export let selectable: boolean = false;
	export let selectedIds: (string | number)[] = [];
	export let showActions: boolean = true;

	const dispatch = createEventDispatcher();

	let sortKey: string = '';
	let sortDirection: 'asc' | 'desc' = 'asc';

	$: allSelected = data.length > 0 && selectedIds.length === data.length;

	function getRowId(row: Record<string, unknown>): string | number {
		return row.id as string | number;
	}

	function toggleAll() {
		if (allSelected) {
			selectedIds = [];
		} else {
			selectedIds = data.map(row => getRowId(row));
		}
	}

	function toggleRow(id: string | number) {
		if (selectedIds.includes(id)) {
			selectedIds = selectedIds.filter(i => i !== id);
		} else {
			selectedIds = [...selectedIds, id];
		}
	}

	function isSelected(row: Record<string, unknown>): boolean {
		return selectedIds.includes(getRowId(row));
	}

	function handleSort(key: string) {
		if (sortKey === key) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDirection = 'asc';
		}
		dispatch('sort', { key: sortKey, direction: sortDirection });
	}

	function handleRowClick(row: Record<string, unknown>) {
		dispatch('rowClick', row);
	}

	function handleAction(action: string, row: Record<string, unknown>) {
		dispatch('action', { action, row });
	}
</script>

<div class="data-table-container">
	<table class="data-table">
		<thead>
			<tr>
				{#if selectable}
					<th class="data-table-checkbox-cell">
						<input 
							type="checkbox" 
							class="data-table-checkbox"
							checked={allSelected}
							on:change={toggleAll}
						/>
					</th>
				{/if}
				{#each columns as column}
					<th 
						class="data-table-header-cell"
						style={column.width ? `width: ${column.width}` : ''}
					>
						{#if column.sortable}
							<button 
								class="data-table-sort-btn"
								on:click={() => handleSort(column.key)}
							>
								{column.label}
								{#if sortKey === column.key}
									<svg class="w-4 h-4 ml-1 {sortDirection === 'desc' ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
									</svg>
								{/if}
							</button>
						{:else}
							{column.label}
						{/if}
					</th>
				{/each}
				{#if showActions}
					<th class="data-table-header-cell text-right">Acciones</th>
				{/if}
			</tr>
		</thead>
		<tbody>
			{#each data as row}
				<tr 
					class="data-table-row"
					on:click={() => handleRowClick(row)}
				>
					{#if selectable}
						<td class="data-table-checkbox-cell" on:click|stopPropagation>
							<input 
								type="checkbox" 
								class="data-table-checkbox"
								checked={isSelected(row)}
								on:change={() => toggleRow(getRowId(row))}
							/>
						</td>
					{/if}
					{#each columns as column}
						<td class="data-table-cell">
							<slot name="cell" {row} {column} value={row[column.key]}>
								{row[column.key]}
							</slot>
						</td>
					{/each}
					{#if showActions}
						<td class="data-table-cell text-right" on:click|stopPropagation>
							<div class="data-table-actions">
								<button 
									class="data-table-action-btn"
									title="Editar"
									on:click={() => handleAction('edit', row)}
								>
									<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
									</svg>
								</button>
								<button 
									class="data-table-action-btn"
									title="Duplicar"
									on:click={() => handleAction('duplicate', row)}
								>
									<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
									</svg>
								</button>
							</div>
						</td>
					{/if}
				</tr>
			{/each}
		</tbody>
	</table>

	{#if data.length === 0}
		<div class="data-table-empty">
			<slot name="empty">
				<p>No hay datos para mostrar</p>
			</slot>
		</div>
	{/if}
</div>
