<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME, API_BASE_URL } from '$lib/config';
	import { api } from '$lib/services/api';

	const stats = [
		{ label: 'Aseguradoras', value: '—', href: '/aseguradoras', color: 'bg-blue-50 text-blue-600' },
		{ label: 'Clientes', value: '—', href: '/clientes', color: 'bg-green-50 text-green-600' },
		{ label: 'Propuestas', value: '—', href: '/propuestas', color: 'bg-amber-50 text-amber-600' },
		{ label: 'Reportes', value: '—', href: '/reportes', color: 'bg-purple-50 text-purple-600' }
	];

	const quickActions = [
		{ label: 'Nueva Aseguradora', href: '/aseguradoras/nueva' },
		{ label: 'Nuevo Cliente', href: '/clientes/nuevo' },
		{ label: 'Nueva Propuesta', href: '/propuestas/nueva' }
	];

	// Test API connection on mount
	onMount(async () => {
		console.log('🔗 API Base URL:', API_BASE_URL);
		
		try {
			// Test health endpoint
			const healthResponse = await api.get('/health');
			console.log('✅ Health Check Response:', healthResponse);
		} catch (error) {
			console.error('❌ API Error:', error);
		}
	});
</script>

<svelte:head>
	<title>Dashboard | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<h1 class="page-title">Dashboard</h1>
</header>

<!-- Content -->
<div class="page-content">
	<!-- Welcome -->
	<div class="mb-8">
		<h2 class="text-2xl font-bold text-secondary-900 mb-2">
			Bienvenido a {APP_NAME}
		</h2>
		<p class="text-secondary-500">
			Panel de administración de seguros
		</p>
	</div>

	<!-- Stats Grid -->
	<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 mb-8">
		{#each stats as stat}
			<a href={stat.href} class="card hover:shadow-md transition-shadow">
				<div class="flex items-center gap-4">
					<div class="w-12 h-12 rounded-xl {stat.color} flex items-center justify-center">
						<span class="text-xl font-bold">{stat.value}</span>
					</div>
					<div>
						<p class="text-sm text-secondary-500">{stat.label}</p>
						<p class="text-lg font-semibold text-secondary-900">Total</p>
					</div>
				</div>
			</a>
		{/each}
	</div>

	<!-- Quick Actions -->
	<div class="card">
		<h3 class="text-lg font-semibold text-secondary-900 mb-4">Acciones rápidas</h3>
		<div class="flex flex-wrap gap-3">
			{#each quickActions as action}
				<a href={action.href} class="btn btn-primary">
					+ {action.label}
				</a>
			{/each}
		</div>
	</div>
</div>
