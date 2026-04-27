<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME } from '$lib/config';
	import { DataTable, Modal } from '$components';
	import { goto } from '$app/navigation';
	import { clienteService } from '$services';
	import { ClienteFields } from '$constants';
	import type { Cliente } from '$lib/types/cliente';

	// Alias para mayor legibilidad
	const F = ClienteFields;

	// Table columns usando constantes
	const columns = [
		{ key: F.id.db, label: F.id.label, sortable: true },
		{ key: 'documento', label: 'Documento', sortable: true },
		{ key: 'display_name', label: 'Nombre / Razón Social', sortable: true },
		{ key: F.tipo_persona.db, label: F.tipo_persona.label, sortable: true },
		{ key: F.correo.db, label: F.correo.label, sortable: true },
		{ key: F.telefono_movil.db, label: F.telefono_movil.label, sortable: false },
		{ key: F.ciudad.db, label: F.ciudad.label, sortable: true },
		{ key: 'acciones', label: 'Acciones', sortable: false }
	];

	// Data from API
	let allData: Record<string, unknown>[] = [];
	let data: Record<string, unknown>[] = [];
	let loading = true;
	let error: string | null = null;

	// Filtro por documento
	let documentoFilter: string = '';

	// Modal state
	let showModal = false;
	let selectedCliente: Cliente | null = null;

	// Secciones colapsables del modal
	let modalSections = {
		general: true,
		contacto: true,
		persona: false,
		empresa: false
	};

	function toggleModalSection(key: keyof typeof modalSections) {
		modalSections[key] = !modalSections[key];
	}

	// Load clientes from API
	onMount(async () => {
		try {
			const response = await clienteService.getAll();
			console.log('✅ Clientes Response:', response);
			// Agregar campos display_name y documento para la tabla
			allData = (response || []).map((cliente: Cliente) => ({
				...cliente,
				display_name: cliente.tipo_persona === 'PERSONA' 
					? cliente.nombre 
					: cliente.razon_social,
				documento: cliente.tipo_persona === 'PERSONA'
					? cliente.numero_documento
					: cliente.nit
			}));
			// Ordenar del más nuevo al más antiguo (ID descendente)
			allData.sort((a, b) => Number(b.id) - Number(a.id));
			data = allData;
		} catch (err) {
			console.error('❌ Error loading clientes:', err);
			error = err instanceof Error ? err.message : 'Error al cargar clientes';
		} finally {
			loading = false;
		}
	});

	// Filtrar por documento
	function filterByDocumento() {
		if (!documentoFilter.trim()) {
			data = allData;
			return;
		}
		const searchTerm = documentoFilter.trim().toLowerCase();
		data = allData.filter(cliente => {
			const doc = String(cliente.documento || '').toLowerCase();
			return doc.includes(searchTerm);
		});
	}

	// Limpiar filtro
	function clearFilter() {
		documentoFilter = '';
		data = allData;
	}

	// Manejar Enter en búsqueda
	function handleSearchKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			filterByDocumento();
		}
	}

	// Handle view action
	function viewCliente(row: Record<string, unknown>) {
		selectedCliente = row as unknown as Cliente;
		showModal = true;
	}

	// Handle edit action
	function editCliente(id: number) {
		goto(`/clientes/${id}/editar`);
	}

	// Helper para mostrar valor o placeholder
	function displayValue(value: unknown): string {
		if (value === null || value === undefined || value === '') {
			return '—';
		}
		return String(value);
	}

	// Helper para badge de tipo persona
	function getTipoPersonaBadge(tipo: string) {
		return tipo === 'PERSONA' 
			? { text: 'Persona', class: 'bg-blue-100 text-blue-700' }
			: { text: 'Empresa', class: 'bg-purple-100 text-purple-700' };
	}
</script>

<svelte:head>
	<title>Clientes | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<h1 class="page-title">Clientes</h1>
</header>

<!-- Content -->
<div class="page-content">
	<div class="card">
		<!-- Toolbar -->
		<div class="flex flex-wrap items-center justify-between gap-4 mb-4">
			<a href="/clientes/nuevo" class="btn btn-primary flex items-center gap-1.5">
				<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
				</svg>
				Nuevo Cliente
			</a>

			<!-- Filtro por documento -->
			<div class="flex items-center gap-2">
				<label for="documento-filter" class="text-sm text-secondary-600 whitespace-nowrap">Buscar por documento:</label>
				<div class="relative">
					<input
						id="documento-filter"
						type="text"
						class="input w-48 pr-8"
						placeholder="CC o NIT..."
						bind:value={documentoFilter}
						on:keydown={handleSearchKeydown}
					/>
					{#if documentoFilter}
						<button
							type="button"
							class="absolute right-2 top-1/2 -translate-y-1/2 text-secondary-400 hover:text-secondary-600"
							on:click={clearFilter}
						>
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					{/if}
				</div>
				<button
					class="btn btn-secondary flex items-center gap-1"
					on:click={filterByDocumento}
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
					</svg>
					Buscar
				</button>
			</div>
		</div>

		<!-- Loading State -->
		{#if loading}
			<div class="flex items-center justify-center py-12">
				<div class="flex flex-col items-center gap-4">
					<svg class="animate-spin h-8 w-8 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
					</svg>
					<p class="text-secondary-600">Cargando clientes...</p>
				</div>
			</div>
		{:else if error}
			<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
				<p class="font-medium">Error</p>
				<p class="text-sm">{error}</p>
			</div>
		{:else}
			<!-- Data Table -->
			<DataTable 
				{columns} 
				{data}
				showActions={false}
			>
				<svelte:fragment slot="cell" let:row let:column let:value>
					{#if column.key === F.id.db}
						<span class="data-table-id">#{value}</span>
					{:else if column.key === 'documento'}
						<span class="font-mono text-sm text-secondary-700">{displayValue(value)}</span>
					{:else if column.key === 'display_name'}
						<span class="font-medium text-secondary-900">{displayValue(value)}</span>
					{:else if column.key === F.tipo_persona.db}
						{@const badge = getTipoPersonaBadge(String(value))}
						<span class="px-2 py-1 text-xs font-medium rounded-full {badge.class}">
							{badge.text}
						</span>
					{:else if column.key === F.correo.db}
						{#if value}
							<a href="mailto:{value}" class="text-primary-600 hover:text-primary-700 hover:underline">
								{value}
							</a>
						{:else}
							<span class="text-secondary-400">—</span>
						{/if}
					{:else if column.key === 'acciones'}
						<div class="flex items-center gap-1">
							<button 
								type="button"
								class="p-1.5 text-secondary-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
								title="Ver detalles"
								on:click|stopPropagation={() => viewCliente(row)}
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
								on:click|stopPropagation={() => editCliente(Number(row.id))}
							>
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
								</svg>
							</button>
						</div>
					{:else}
						{displayValue(value)}
					{/if}
				</svelte:fragment>

				<svelte:fragment slot="empty">
					<div class="empty-state">
						<div class="empty-state-icon">👥</div>
						<p class="empty-state-title">No hay clientes</p>
						<p class="empty-state-text">Agrega un nuevo cliente para comenzar</p>
					</div>
				</svelte:fragment>
			</DataTable>
		{/if}
	</div>
</div>

<!-- Modal de Visualización -->
<Modal 
	bind:open={showModal} 
	title={selectedCliente?.tipo_persona === 'PERSONA' ? selectedCliente?.nombre : selectedCliente?.razon_social || 'Detalles del Cliente'} 
	size="lg"
>
	{#if selectedCliente}
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
								<p class="text-sm font-medium text-secondary-900">#{selectedCliente.id}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.tipo_persona.label}</p>
								{#if selectedCliente.tipo_persona === 'PERSONA'}
									<span class="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-700">
										Persona
									</span>
								{:else}
									<span class="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-700">
										Empresa
									</span>
								{/if}
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.usuario.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedCliente.usuario)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.tipo_usuario.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedCliente.tipo_usuario)}</p>
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
								<p class="text-xs text-secondary-500 mb-1">{F.correo.label}</p>
								<p class="text-sm text-secondary-700">
									{#if selectedCliente.correo}
										<a href="mailto:{selectedCliente.correo}" class="text-primary-600 hover:underline">
											{selectedCliente.correo}
										</a>
									{:else}
										—
									{/if}
								</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.telefono_movil.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedCliente.telefono_movil)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{F.ciudad.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedCliente.ciudad)}</p>
							</div>
							<div class="col-span-2">
								<p class="text-xs text-secondary-500 mb-1">{F.direccion.label}</p>
								<p class="text-sm text-secondary-700">{displayValue(selectedCliente.direccion)}</p>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Datos Persona Natural (solo si es PERSONA) -->
			{#if selectedCliente.tipo_persona === 'PERSONA'}
				<div class="border border-secondary-200 rounded-lg overflow-hidden">
					<button 
						type="button"
						class="w-full flex items-center justify-between px-4 py-3 bg-secondary-50 text-left text-sm font-semibold text-secondary-900 hover:bg-secondary-100 transition-colors"
						on:click={() => toggleModalSection('persona')}
					>
						<span>Datos Personales</span>
						<svg class="w-5 h-5 transition-transform {modalSections.persona ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.persona}
						<div class="px-4 py-4 bg-white border-t border-secondary-200">
							<div class="grid grid-cols-2 gap-4">
								<div class="col-span-2">
									<p class="text-xs text-secondary-500 mb-1">{F.nombre.label}</p>
									<p class="text-sm font-medium text-secondary-900">{displayValue(selectedCliente.nombre)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.tipo_documento.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.tipo_documento)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.numero_documento.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.numero_documento)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.edad.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.edad)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>
			{/if}

			<!-- Datos Empresa (solo si es EMPRESA) -->
			{#if selectedCliente.tipo_persona === 'EMPRESA'}
				<div class="border border-secondary-200 rounded-lg overflow-hidden">
					<button 
						type="button"
						class="w-full flex items-center justify-between px-4 py-3 bg-secondary-50 text-left text-sm font-semibold text-secondary-900 hover:bg-secondary-100 transition-colors"
						on:click={() => toggleModalSection('empresa')}
					>
						<span>Datos de la Empresa</span>
						<svg class="w-5 h-5 transition-transform {modalSections.empresa ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
						</svg>
					</button>
					{#if modalSections.empresa}
						<div class="px-4 py-4 bg-white border-t border-secondary-200">
							<div class="grid grid-cols-2 gap-4">
								<div class="col-span-2">
									<p class="text-xs text-secondary-500 mb-1">{F.razon_social.label}</p>
									<p class="text-sm font-medium text-secondary-900">{displayValue(selectedCliente.razon_social)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.nit.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.nit)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.nombre_rep_legal.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.nombre_rep_legal)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.documento_rep_legal.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.documento_rep_legal)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.telefono_rep_legal.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.telefono_rep_legal)}</p>
								</div>
								<div>
									<p class="text-xs text-secondary-500 mb-1">{F.correo_rep_legal.label}</p>
									<p class="text-sm text-secondary-700">
										{#if selectedCliente.correo_rep_legal}
											<a href="mailto:{selectedCliente.correo_rep_legal}" class="text-primary-600 hover:underline">
												{selectedCliente.correo_rep_legal}
											</a>
										{:else}
											—
										{/if}
									</p>
								</div>
								<div class="col-span-2">
									<p class="text-xs text-secondary-500 mb-1">{F.contacto_alternativo.label}</p>
									<p class="text-sm text-secondary-700">{displayValue(selectedCliente.contacto_alternativo)}</p>
								</div>
							</div>
						</div>
					{/if}
				</div>
			{/if}
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
				on:click={() => { showModal = false; editCliente(selectedCliente?.id || 0); }}
			>
				Editar
			</button>
		</div>
	</svelte:fragment>
</Modal>
