<script lang="ts">
	/**
	 * PillTabs - rounded tab set with optional counts, used by the aseguradora
	 * form and ficha. Distinct from Tabs.svelte, which is the underline variant
	 * used for the bienes rubro switcher.
	 *
	 * @prop tabs - id / label / optional count
	 * @prop active - bound id of the selected tab
	 */
	export let tabs: { id: string; label: string; count?: number | string }[] = [];
	export let active: string = '';
</script>

<div class="pill-tabs" role="tablist">
	{#each tabs as tab}
		<button
			type="button"
			role="tab"
			aria-selected={tab.id === active}
			class="pill-tab {tab.id === active ? 'pill-tab-active' : ''}"
			on:click={() => (active = tab.id)}
		>
			{tab.label}
			{#if tab.count !== undefined && tab.count !== ''}
				<span class="pill-tab-count">{tab.count}</span>
			{/if}
		</button>
	{/each}
</div>
