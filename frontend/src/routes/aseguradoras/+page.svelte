<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME } from '$lib/config';
	import { DataTable, Modal } from '$components';
	import { goto } from '$app/navigation';
	import { api } from '$lib/services/api';
	import { AseguradoraFields } from '$constants';
	import type { Aseguradora } from '$types/aseguradora';

	// Alias para mayor legibilidad
	const F = AseguradoraFields;

	// Table columns usando constantes
	const columns = [
		{ key: F.id.db, label: F.id.label, sortable: true },
		{ key: F.nombre.db, label: F.nombre.label, sortable: true },
		{ key: F.respaldo_aseguradora.db, label: F.respaldo_aseguradora.label, sortable: true },
		{ key: F.contacto_asignado.db, label: F.contacto_asignado.label, sortable: true },
		{ key: F.numeral_asistencia.db, label: F.numeral_asistencia.label, sortable: false },
		{ key: F.correo_comercial.db, label: F.correo_comercial.label, sortable: true },
		{ key: 'acciones', label: 'Acciones', sortable: false }
	];

	// Data from API
	let data: Record<string, unknown>[] = [];
	let loading = true;
	let error: string | null = null;

	// Modal state
	let showModal = false;
	let selectedAseguradora: Aseguradora | null = null;

	// Secciones colapsables del modal
	let modalSections = {
		general: true,
		contacto: true,
		asistencia: false,
		danosMateriales: false,
		danosInternos: false,
		sustraccion: false,
		directores: false,
		rceDeducibles: false,
		rceSublimites: false,
		manejoTransporte: false
	};

	function toggleModalSection(key: keyof typeof modalSections) {
		modalSections[key] = !modalSections[key];
	}

	// Load aseguradoras from API
	onMount(async () => {
		try {
			const response = await api.get<{ data: Record<string, unknown>[] }>('/api/aseguradoras');
			console.log('✅ Aseguradoras Response:', response);
			// Ordenar del más nuevo al más antiguo (ID descendente)
			data = (response.data || []).sort((a, b) => Number(b.id) - Number(a.id));
		} catch (err) {
			console.error('❌ Error loading aseguradoras:', err);
			error = err instanceof Error ? err.message : 'Error al cargar aseguradoras';
		} finally {
			loading = false;
		}
	});

	// Handle view action
	function viewAseguradora(row: Record<string, unknown>) {
		selectedAseguradora = row as unknown as Aseguradora;
		showModal = true;
	}

	// Handle edit action
	function editAseguradora(id: number) {
		goto(`/aseguradoras/${id}/editar`);
	}

	// Helper para mostrar valor o placeholder
	function displayValue(value: unknown): string {
		if (value === null || value === undefined || value === '') {
			return '—';
		}
		return String(value);
	}
</script>

<svelte:head>
	<title>Aseguradoras | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<h1 class="page-title">Aseguradoras</h1>
</header>

<!-- Content -->
<div class="page-content">
	<div class="card">
		<!-- Toolbar -->
		<div class="flex items-center justify-between mb-4">
			<a href="/aseguradoras/nueva" class="btn btn-primary flex items-center gap-1.5">
				<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
				</svg>
				Nueva Aseguradora
			</a>

			<!-- Toolbar Actions -->
			<div class="table-toolbar-actions">
				<button class="table-toolbar-btn" title="Buscar">
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
					</svg>
				</button>
				<button class="table-toolbar-btn" title="Filtros">
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h7" />
					</svg>
				</button>
				<button class="table-toolbar-btn" title="Ordenar">
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
					</svg>
				</button>
				<button class="table-toolbar-btn" title="Más opciones">
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
					</svg>
				</button>
			</div>
		</div>

		<!-- Data Table -->
		<DataTable 
			{columns} 
			{data}
			showActions={false}
		>
			<svelte:fragment slot="cell" let:row let:column let:value>
				{#if column.key === F.id.db}
					<span class="data-table-id">#{value}</span>
				{:else if column.key === F.nombre.db}
					<span class="font-medium text-secondary-900">{value}</span>
				{:else if column.key === F.correo_comercial.db}
					<a href="mailto:{value}" class="text-primary-600 hover:text-primary-700 hover:underline">
						{value}
					</a>
				{:else if column.key === 'acciones'}
					<div class="flex items-center gap-1">
						<button 
							type="button"
							class="p-1.5 text-secondary-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
							title="Ver detalles"
							on:click|stopPropagation={() => viewAseguradora(row)}
						>
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
							</svg>
						</button>
						<button 
							type="button"
							class="p-1.5 text-secondary-500 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
							title="Editar"
							on:click|stopPropagation={() => editAseguradora(Number(row.id))}
						>
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
							</svg>
						</button>
					</div>
				{:else}
					{value}
				{/if}
			</svelte:fragment>

			<svelte:fragment slot="empty">
				<div class="empty-state">
					<div class="empty-state-icon">🏢</div>
					<p class="empty-state-title">No hay aseguradoras</p>
					<p class="empty-state-text">Agrega una nueva aseguradora para comenzar</p>
				</div>
			</svelte:fragment>
		</DataTable>
	</div>
</div>

<!-- Modal de Visualización -->
<Modal bind:open={showModal} title={selectedAseguradora?.nombre || 'Detalles de Aseguradora'} size="xl">
	{#if selectedAseguradora}
		<div class="space-y-4">
			<!-- Información General -->
			<div class="border border-secondary-200 rounded-lg overflow-hidden">
				<button 
					type="button"
					class="w-full flex items-center justify-between px-4 py-3 bg-secondary-50 text-left text-sm font-semibold text-secondary-900 hover:bg-secondary-100 transition-colors"
					on:click={() => toggleModalSection('general')}
				>
					<span>Información General</span>
					<svg class="w-5 h-5 transition-transform {modalSections.general ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if modalSections.general}
					<div class="px-4 py-4 bg-white border-t border-secondary-200">
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.id.label}</p>
								<p class="text-sm font-medium text-secondary-900">#{selectedAseguradora.id}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.nombre.label}</p>
								<p class="text-sm font-medium text-secondary-900">{displayValue(selectedAseguradora.nombre)}</p>
							</div>
							<div class="col-span-2">
								<p class="text-xs text-secondary-500 mb-1">{F.respaldo_aseguradora.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedAseguradora.respaldo_aseguradora)}</p>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Información de Contacto -->
			<div class="border border-secondary-200 rounded-lg overflow-hidden">
				<button 
					type="button"
					class="w-full flex items-center justify-between px-4 py-3 bg-secondary-50 text-left text-sm font-semibold text-secondary-900 hover:bg-secondary-100 transition-colors"
					on:click={() => toggleModalSection('contacto')}
				>
					<span>Información de Contacto</span>
					<svg class="w-5 h-5 transition-transform {modalSections.contacto ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if modalSections.contacto}
					<div class="px-4 py-4 bg-white border-t border-secondary-200">
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.numeral_asistencia.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedAseguradora.numeral_asistencia)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.contacto_asignado.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedAseguradora.contacto_asignado)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.correo_comercial.label}</p>
								<p class="text-sm text-secondary-700">
									{#if selectedAseguradora.correo_comercial}
										<a href="mailto:{selectedAseguradora.correo_comercial}" class="text-primary-600 hover:underline">
											{selectedAseguradora.correo_comercial}
										</a>
									{:else}
										—
									{/if}
								</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.correo_reclamaciones.label}</p>
								<p class="text-sm text-secondary-700">
									{#if selectedAseguradora.correo_reclamaciones}
										<a href="mailto:{selectedAseguradora.correo_reclamaciones}" class="text-primary-600 hover:underline">
											{selectedAseguradora.correo_reclamaciones}
										</a>
									{:else}
										—
									{/if}
								</p>
							</div>
							<div class="col-span-2">
								<p class="text-xs text-secondary-500 mb-1">{F.direccion_oficina.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedAseguradora.direccion_oficina)}</p>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Sección: Configuración Copropiedad -->
			<div class="border-t border-secondary-300 pt-4 mt-4">
				<h3 class="text-sm font-bold text-secondary-800 mb-3">Configuración Copropiedad</h3>
				
				<!-- Asistencia -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('asistencia')}
					>
						<span>Asistencia</span>
						<svg class="w-5 h-5 transition-transform {modalSections.asistencia ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.asistencia}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_asistencia_area_comun.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_asistencia_area_comun)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_asistencia_area_privada.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_asistencia_area_privada)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- Daños Materiales -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('danosMateriales')}
					>
						<span>Daños Materiales</span>
						<svg class="w-5 h-5 transition-transform {modalSections.danosMateriales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.danosMateriales}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_dm_deducible_terremoto.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_dm_deducible_terremoto)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_dm_deducible_inundacion.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_dm_deducible_inundacion)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_dm_deducible_incendio.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_dm_deducible_incendio)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_dm_deducible_amit.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_dm_deducible_amit)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_dm_deducible_tuberia_vidrio.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_dm_deducible_tuberia_vidrio)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- Daños Internos -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('danosInternos')}
					>
						<span>Daños Internos</span>
						<svg class="w-5 h-5 transition-transform {modalSections.danosInternos ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.danosInternos}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_di_deducible_maq_equipo.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_di_deducible_maq_equipo)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_di_deducible_equipo_electronico.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_di_deducible_equipo_electronico)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- Sustracción con Violencia -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('sustraccion')}
					>
						<span>Sustracción con Violencia</span>
						<svg class="w-5 h-5 transition-transform {modalSections.sustraccion ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.sustraccion}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_scv_deducible_maq_equipo.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_scv_deducible_maq_equipo)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_scv_deducible_equipo_electronico.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_scv_deducible_equipo_electronico)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_scv_deducible_dineros.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_scv_deducible_dineros)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_scv_deducible_muebles.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_scv_deducible_muebles)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- Directores y Administradores -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('directores')}
					>
						<span>Directores y Administradores</span>
						<svg class="w-5 h-5 transition-transform {modalSections.directores ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.directores}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_da_deducible_amparo_basico.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_da_deducible_amparo_basico)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- RCE Deducibles -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('rceDeducibles')}
					>
						<span>RCE - Deducibles</span>
						<svg class="w-5 h-5 transition-transform {modalSections.rceDeducibles ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.rceDeducibles}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_deducible_contratistas.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_deducible_contratistas)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_deducible_cruzada.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_deducible_cruzada)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_deducible_patronal.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_deducible_patronal)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_deducible_parqueaderos.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_deducible_parqueaderos)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_deducible_gastos_medicos.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_deducible_gastos_medicos)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- RCE Sublímites -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('rceSublimites')}
					>
						<span>RCE - Sublímites</span>
						<svg class="w-5 h-5 transition-transform {modalSections.rceSublimites ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.rceSublimites}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_sublimite_contratistas.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_sublimite_contratistas)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_sublimite_cruzada.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_sublimite_cruzada)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_sublimite_patronal.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_sublimite_patronal)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_sublimite_parqueaderos.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_sublimite_parqueaderos)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_rce_sublimite_gastos_medicos.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_rce_sublimite_gastos_medicos)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- Manejo y Transporte -->
				<div class="cop-subsection">
					<button 
						type="button"
						class="cop-subsection-header"
						on:click={() => toggleModalSection('manejoTransporte')}
					>
						<span>Manejo y Transporte de Valores</span>
						<svg class="w-5 h-5 transition-transform {modalSections.manejoTransporte ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.manejoTransporte}
						<div class="cop-subsection-content">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_manejo_deducible_amparo_basico.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_manejo_deducible_amparo_basico)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.cop_tv_deducible_amparo_basico.label}</p>
									<p class="text-sm text-secondary-700 font-mono">{displayValue(selectedAseguradora.cop_tv_deducible_amparo_basico)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}

	<svelte:fragment slot="footer">
		<div class="flex justify-end gap-3">
			<button 
				type="button" 
				class="btn btn-secondary"
				on:click={() => showModal = false}
			>
				Cerrar
			</button>
			<button 
				type="button" 
				class="btn btn-primary"
				on:click={() => { showModal = false; editAseguradora(selectedAseguradora?.id || 0); }}
			>
				Editar
			</button>
		</div>
	</svelte:fragment>
</Modal>
