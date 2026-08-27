<script lang="ts">
	import { APP_NAME } from '$lib/config';
	import { EmptyState, PageHeader } from '$components';

	/**
	 * Reports are not implemented on the backend: there are no aggregate
	 * endpoints behind any of these. They are listed so the intended scope is
	 * visible, and the page states plainly that nothing runs yet rather than
	 * offering buttons that do nothing.
	 */
	const reportTypes = [
		{ title: 'Producción por período', description: 'Primas emitidas por mes y por rubro' },
		{ title: 'Cartera por aseguradora', description: 'Distribución de pólizas colocadas' },
		{ title: 'Propuestas pendientes', description: 'Cotizaciones sin emitir y su antigüedad' },
		{ title: 'Comisiones', description: 'Comisión percibida por póliza y por ejecutivo' }
	];
</script>

<svelte:head>
	<title>Reportes | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader
		title="Reportes"
		crumb="Inicio / Administración"
		subtitle="Producción, cartera y comisiones"
	/>

	<div class="kpi-row">
		{#each reportTypes as report}
			<div class="kpi-card">
				<div class="text-sm font-medium">{report.title}</div>
				<div class="kpi-note mt-1">{report.description}</div>
			</div>
		{/each}
	</div>

	<EmptyState
		title="Módulo en construcción"
		text="Los reportes todavía no tienen endpoints de agregación en el backend. Mientras tanto, el dashboard resume la cartera y las listas de Pólizas y Aseguradoras permiten filtrar y exportar manualmente."
	>
		<svelte:fragment slot="icon">
			<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
				<path d="M4 20V4M4 20h16" />
				<path d="M8 17v-6h3v6zM14 17V7h3v10z" />
			</svg>
		</svelte:fragment>
		<svelte:fragment slot="action">
			<div class="flex gap-2 flex-wrap justify-center">
				<a href="/" class="btn-secondary">Ir al dashboard</a>
				<a href="/propuestas" class="btn-primary">Ir a Pólizas</a>
			</div>
		</svelte:fragment>
	</EmptyState>
</div>
