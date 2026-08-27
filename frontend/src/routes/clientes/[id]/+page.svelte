<script lang="ts">
	/**
	 * There is no read-only cliente detail screen: the list opens a ficha modal
	 * and all editing happens on /clientes/[id]/editar. This route only ever
	 * held a placeholder, so it forwards to the editor — which is where links
	 * such as the topbar search results expect to land.
	 */
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	onMount(() => {
		void goto(`/clientes/${$page.params.id}/editar`, { replaceState: true });
	});
</script>
