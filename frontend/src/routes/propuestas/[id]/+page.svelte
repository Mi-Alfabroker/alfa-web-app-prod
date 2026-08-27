<script lang="ts">
	/**
	 * A póliza id alone does not identify a póliza: the four rubros have separate
	 * tables and separate id sequences, so /propuestas/7 is ambiguous. The real
	 * detail routes are /propuestas/{hogar,vehiculo,copropiedad,otro}/[id]. This
	 * route was a placeholder; it now sends the visitor back to the list, where
	 * the search box resolves a consecutivo to the right rubro.
	 */
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		void goto('/propuestas', { replaceState: true });
	});
</script>
