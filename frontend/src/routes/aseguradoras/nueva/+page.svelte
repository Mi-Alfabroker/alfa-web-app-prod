<script lang="ts">
	import { APP_NAME } from '$lib/config';
	import { AseguradoraForm } from '$components';
</script>

<svelte:head>
	<title>Registrar aseguradora | {APP_NAME}</title>
</svelte:head>

<AseguradoraForm aseguradoraId={null} />
