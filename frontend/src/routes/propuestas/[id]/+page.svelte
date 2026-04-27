<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';

	$: id = $page.params.id;
</script>

<svelte:head>
	<title>Propuesta #{id} | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<a href="/propuestas" class="page-back-link">
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
			</svg>
			<span>Volver</span>
		</a>
		<h1 class="page-title">Propuesta #{id}</h1>
	</div>
	<span class="badge badge-warning">En proceso</span>
</header>

<!-- Content -->
<div class="page-content">
	<div class="card max-w-4xl mx-auto">
		<div class="empty-state">
			<div class="empty-state-icon">📋</div>
			<p class="empty-state-title">Detalle de Propuesta</p>
			<p class="empty-state-text">ID: {id}</p>
			<p class="empty-state-text">Aquí se mostrará el formulario de edición</p>
		</div>
	</div>
</div>
