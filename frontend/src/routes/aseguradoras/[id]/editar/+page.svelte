<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { AseguradoraForm } from '$components';

	$: aseguradoraId = Number($page.params.id);
</script>

<svelte:head>
	<title>Editar aseguradora | {APP_NAME}</title>
</svelte:head>

<AseguradoraForm {aseguradoraId} />
