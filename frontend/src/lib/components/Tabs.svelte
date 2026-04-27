<script lang="ts">
	/**
	 * Tabs - Tab navigation component
	 * 
	 * @prop tabs - Array of tab definitions { id, label, count? }
	 * @prop activeTab - Currently active tab ID (bindable)
	 */

	type Tab = {
		id: string;
		label: string;
		count?: number;
	};

	export let tabs: Tab[] = [];
	export let activeTab: string = '';

	function selectTab(id: string) {
		activeTab = id;
	}
</script>

<div class="tabs">
	{#each tabs as tab}
		<button
			class="tab {activeTab === tab.id ? 'tab-active' : ''}"
			on:click={() => selectTab(tab.id)}
		>
			{tab.label}
			{#if tab.count !== undefined}
				<span class="tab-count">{tab.count}</span>
			{/if}
		</button>
	{/each}
	<slot name="actions" />
</div>
