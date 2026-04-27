<script lang="ts">
	import { APP_NAME } from '$lib/config';

	const reportTypes = [
		{ 
			title: 'Ventas por Período', 
			description: 'Análisis de ventas por mes/año',
			icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
			color: 'bg-blue-50 text-blue-600'
		},
		{ 
			title: 'Clientes por Aseguradora', 
			description: 'Distribución de clientes',
			icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
			color: 'bg-green-50 text-green-600'
		},
		{ 
			title: 'Propuestas Pendientes', 
			description: 'Estado de propuestas activas',
			icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
			color: 'bg-amber-50 text-amber-600'
		},
		{ 
			title: 'Comisiones', 
			description: 'Reporte de comisiones generadas',
			icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
			color: 'bg-purple-50 text-purple-600'
		}
	];
</script>

<svelte:head>
	<title>Reportes | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<h1 class="page-title">Reportes</h1>
</header>

<!-- Content -->
<div class="page-content">
	<div class="mb-6">
		<p class="text-secondary-500">Selecciona un tipo de reporte para generar</p>
	</div>

	<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 mb-8">
		{#each reportTypes as report}
			<button 
				class="card text-left hover:shadow-md transition-shadow cursor-pointer"
				type="button"
			>
				<div class="w-12 h-12 rounded-xl {report.color} flex items-center justify-center mb-4">
					<svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d={report.icon} />
					</svg>
				</div>
				<h3 class="font-semibold text-secondary-900">{report.title}</h3>
				<p class="text-sm text-secondary-500 mt-1">{report.description}</p>
			</button>
		{/each}
	</div>

	<!-- Report Content Area -->
	<div class="card">
		<div class="empty-state">
			<div class="empty-state-icon">📊</div>
			<p class="empty-state-title">Área de Reportes</p>
			<p class="empty-state-text">Selecciona un reporte para ver los resultados aquí</p>
		</div>
	</div>
</div>
