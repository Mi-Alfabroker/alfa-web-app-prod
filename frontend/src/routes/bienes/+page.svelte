<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME } from '$lib/config';
	import { DataTable, Modal, Tabs } from '$components';
	import { goto } from '$app/navigation';
	import { bienService, clienteService } from '$services';
	import { HogarFields, VehiculoFields, CopropiedadFields, OtroBienFields } from '$constants';
	import type { Cliente } from '$lib/types/cliente';
	import type { Hogar, Vehiculo, Copropiedad, OtroBien, TipoBien } from '$lib/types/bien';
	import { TIPOS_BIEN } from '$lib/types/bien';

	// Data state
	let clientes: Cliente[] = [];
	let hogares: Hogar[] = [];
	let vehiculos: Vehiculo[] = [];
	let copropiedades: Copropiedad[] = [];
	let otrosBienes: OtroBien[] = [];
	
	// UI state
	let loading = true;
	let error: string | null = null;
	let selectedClienteId: number | null = null;
	let activeTab: TipoBien = 'HOGAR';
	
	// Filtro por documento
	let documentoFilter: string = '';
	let filteredCliente: Cliente | null = null;
	let searchingCliente: boolean = false;

	// Modal state
	let showModal = false;
	let modalTipo: TipoBien = 'HOGAR';
	let modalData: Hogar | Vehiculo | Copropiedad | OtroBien | null = null;
	

	// Tab items
	const tabs = [
		{ id: 'HOGAR', label: 'Hogares', icon: '🏠' },
		{ id: 'VEHICULO', label: 'Vehículos', icon: '🚗' },
		{ id: 'COPROPIEDAD', label: 'Copropiedades', icon: '🏢' },
		{ id: 'OTRO', label: 'Otros', icon: '📦' }
	];

	// Column definitions
	const hogarColumns = [
		{ key: HogarFields.id.db, label: HogarFields.id.label, sortable: true },
		{ key: HogarFields.tipo_inmueble.db, label: HogarFields.tipo_inmueble.label, sortable: true },
		{ key: HogarFields.ciudad_inmueble.db, label: HogarFields.ciudad_inmueble.label, sortable: true },
		{ key: HogarFields.direccion_inmueble.db, label: HogarFields.direccion_inmueble.label, sortable: false },
		{ key: HogarFields.valor_inmueble_avaluo.db, label: 'Valor', sortable: true },
		{ key: 'acciones', label: 'Acciones', sortable: false }
	];

	const vehiculoColumns = [
		{ key: VehiculoFields.id.db, label: VehiculoFields.id.label, sortable: true },
		{ key: VehiculoFields.tipo_vehiculo.db, label: VehiculoFields.tipo_vehiculo.label, sortable: true },
		{ key: VehiculoFields.placa.db, label: VehiculoFields.placa.label, sortable: true },
		{ key: VehiculoFields.marca.db, label: VehiculoFields.marca.label, sortable: true },
		{ key: VehiculoFields.ano_modelo.db, label: VehiculoFields.ano_modelo.label, sortable: true },
		{ key: VehiculoFields.valor_vehiculo.db, label: 'Valor', sortable: true },
		{ key: 'acciones', label: 'Acciones', sortable: false }
	];

	const copropiedadColumns = [
		{ key: CopropiedadFields.id.db, label: CopropiedadFields.id.label, sortable: true },
		{ key: CopropiedadFields.tipo_copropiedad.db, label: CopropiedadFields.tipo_copropiedad.label, sortable: true },
		{ key: CopropiedadFields.ciudad.db, label: CopropiedadFields.ciudad.label, sortable: true },
		{ key: CopropiedadFields.direccion.db, label: CopropiedadFields.direccion.label, sortable: false },
		{ key: CopropiedadFields.numero_torres.db, label: 'Torres', sortable: true },
		{ key: 'acciones', label: 'Acciones', sortable: false }
	];

	const otroBienColumns = [
		{ key: OtroBienFields.id.db, label: OtroBienFields.id.label, sortable: true },
		{ key: OtroBienFields.tipo_seguro.db, label: OtroBienFields.tipo_seguro.label, sortable: true },
		{ key: OtroBienFields.bien_asegurado.db, label: OtroBienFields.bien_asegurado.label, sortable: true },
		{ key: OtroBienFields.valor_bien_asegurar.db, label: 'Valor', sortable: true },
		{ key: 'acciones', label: 'Acciones', sortable: false }
	];

	// Cargar datos
	onMount(async () => {
		await loadClientes();
		await loadBienes();
	});

	async function loadClientes() {
		try {
			clientes = await clienteService.getAll();
		} catch (err) {
			console.error('Error loading clientes:', err);
		}
	}

	async function loadBienes() {
		loading = true;
		error = null;
		try {
			// Cargar todos los tipos de bienes
			const [h, v, c, o] = await Promise.all([
				bienService.hogares.getAll(selectedClienteId || undefined),
				bienService.vehiculos.getAll(selectedClienteId || undefined),
				bienService.copropiedades.getAll(selectedClienteId || undefined),
				bienService.otros.getAll(selectedClienteId || undefined)
			]);
			// Ordenar del más nuevo al más antiguo (ID descendente)
			hogares = h.sort((a, b) => b.id - a.id);
			vehiculos = v.sort((a, b) => b.id - a.id);
			copropiedades = c.sort((a, b) => b.id - a.id);
			otrosBienes = o.sort((a, b) => b.id - a.id);
		} catch (err) {
			console.error('Error loading bienes:', err);
			error = err instanceof Error ? err.message : 'Error al cargar los bienes';
		} finally {
			loading = false;
		}
	}

	// Buscar cliente por documento
	async function searchByDocumento() {
		if (!documentoFilter.trim()) {
			// Si el campo está vacío, limpiar filtro
			filteredCliente = null;
			selectedClienteId = null;
			await loadBienes();
			return;
		}

		searchingCliente = true;
		const doc = documentoFilter.trim();
		
		// Buscar cliente por número de documento o NIT
		const cliente = clientes.find(c => 
			c.numero_documento === doc || c.nit === doc
		);

		if (cliente) {
			filteredCliente = cliente;
			selectedClienteId = cliente.id;
			await loadBienes();
		} else {
			filteredCliente = null;
			selectedClienteId = null;
			// Limpiar bienes si no se encuentra cliente
			hogares = [];
			vehiculos = [];
			copropiedades = [];
			otrosBienes = [];
		}
		
		searchingCliente = false;
	}

	// Limpiar filtro
	function clearFilter() {
		documentoFilter = '';
		filteredCliente = null;
		selectedClienteId = null;
		loadBienes();
	}

	// Manejar Enter en el campo de búsqueda
	function handleSearchKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			searchByDocumento();
		}
	}

	// Navegar a crear nuevo bien
	function handleNuevoBien() {
		goto(`/bienes/nuevo?tipo=${activeTab}`);
	}

	// Ver detalle
	function viewBien(tipo: TipoBien, bien: Record<string, unknown>) {
		modalTipo = tipo;
		modalData = bien as unknown as Hogar | Vehiculo | Copropiedad | OtroBien;
		showModal = true;
	}

	// Editar bien
	function editBien(tipo: TipoBien, id: number) {
		goto(`/bienes/${tipo.toLowerCase()}/${id}/editar`);
	}

	// Ir al formulario de crear propuesta
	function irACrearPropuesta(tipo: TipoBien, bien: Record<string, unknown>) {
		const id = bien.id as number;
		goto(`/propuestas/nueva/${tipo.toLowerCase()}?bien_id=${id}`);
	}

	// Obtener nombre del cliente
	function getClienteName(idUsuario: number): string {
		const cliente = clientes.find(c => c.id === idUsuario);
		if (!cliente) return `#${idUsuario}`;
		return cliente.tipo_persona === 'PERSONA' 
			? cliente.nombre || `#${idUsuario}`
			: cliente.razon_social || `#${idUsuario}`;
	}

	// Formatear moneda
	function formatCurrency(value: number | null): string {
		if (value === null || value === undefined) return '—';
		return new Intl.NumberFormat('es-CO', {
			style: 'currency',
			currency: 'COP',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(value);
	}

	// Helper para mostrar valor o placeholder
	function displayValue(value: unknown): string {
		if (value === null || value === undefined || value === '') return '—';
		return String(value);
	}

	// Contar bienes por tipo
	$: counts = {
		HOGAR: hogares.length,
		VEHICULO: vehiculos.length,
		COPROPIEDAD: copropiedades.length,
		OTRO: otrosBienes.length,
		total: hogares.length + vehiculos.length + copropiedades.length + otrosBienes.length
	};

	// Datos activos según tab
	$: activeData = activeTab === 'HOGAR' ? hogares
		: activeTab === 'VEHICULO' ? vehiculos
		: activeTab === 'COPROPIEDAD' ? copropiedades
		: otrosBienes;

	$: activeColumns = activeTab === 'HOGAR' ? hogarColumns
		: activeTab === 'VEHICULO' ? vehiculoColumns
		: activeTab === 'COPROPIEDAD' ? copropiedadColumns
		: otroBienColumns;

	// Helper para cambiar tab (evita casting en template)
	function setActiveTab(tabId: string) {
		activeTab = tabId as TipoBien;
	}

	// Helper para formatear valor numérico
	function formatValue(value: unknown): string {
		return formatCurrency(value as number);
	}
</script>

<svelte:head>
	<title>Bienes | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<h1 class="page-title">Bienes</h1>
	<p class="text-secondary-500 text-sm mt-1">
		{counts.total} bien{counts.total !== 1 ? 'es' : ''} registrado{counts.total !== 1 ? 's' : ''}
	</p>
</header>

<!-- Content -->
<div class="page-content">
	<div class="card">
		<!-- Toolbar -->
		<div class="flex flex-wrap items-center justify-between gap-4 mb-6">
			<div class="flex items-center gap-4">
				<button 
					class="btn btn-primary flex items-center gap-1.5"
					on:click={handleNuevoBien}
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
					</svg>
					Nuevo Bien
				</button>
			</div>

			<!-- Filtro por documento -->
			<div class="flex items-center gap-3">
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
						on:click={searchByDocumento}
						disabled={searchingCliente}
					>
						{#if searchingCliente}
							<svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
							</svg>
						{:else}
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						{/if}
						Buscar
					</button>
				</div>
				
				<!-- Info del cliente encontrado -->
				{#if filteredCliente}
					<div class="flex items-center gap-2 px-3 py-1.5 bg-primary-50 border border-primary-200 rounded-lg text-sm">
						<span class="text-primary-700 font-medium">
							{filteredCliente.tipo_persona === 'PERSONA' ? filteredCliente.nombre : filteredCliente.razon_social}
						</span>
						<button
							type="button"
							class="text-primary-400 hover:text-primary-600"
							on:click={clearFilter}
							title="Quitar filtro"
						>
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					</div>
				{:else if documentoFilter && !searchingCliente}
					<span class="text-sm text-amber-600">Cliente no encontrado</span>
				{/if}
			</div>
		</div>

		<!-- Tabs -->
		<div class="border-b border-secondary-200 mb-6">
			<nav class="flex gap-1 -mb-px">
				{#each tabs as tab}
					<button
						type="button"
						class="px-4 py-3 text-sm font-medium border-b-2 transition-colors flex items-center gap-2
							{activeTab === tab.id 
								? 'border-primary-500 text-primary-600' 
								: 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-secondary-300'}"
						on:click={() => setActiveTab(tab.id)}
					>
						<span>{tab.icon}</span>
						<span>{tab.label}</span>
					</button>
				{/each}
			</nav>
		</div>

		<!-- Loading State -->
		{#if loading}
			<div class="flex items-center justify-center py-12">
				<div class="flex flex-col items-center gap-4">
					<svg class="animate-spin h-8 w-8 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
					</svg>
					<p class="text-secondary-600">Cargando bienes...</p>
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
				columns={activeColumns} 
				data={activeData}
				showActions={false}
			>
				<svelte:fragment slot="cell" let:row let:column let:value>
					{#if column.key === 'id'}
						<span class="data-table-id">#{value}</span>
					{:else if column.key === 'valor_inmueble_avaluo' || column.key === 'valor_vehiculo' || column.key === 'valor_bien_asegurar'}
						<span class="font-medium text-secondary-900">{formatValue(value)}</span>
					{:else if column.key === 'placa'}
						<span class="font-mono font-medium text-secondary-900">{displayValue(value)}</span>
					{:else if column.key === 'tipo_inmueble' || column.key === 'tipo_vehiculo' || column.key === 'tipo_copropiedad' || column.key === 'tipo_seguro'}
						<span class="px-2 py-1 text-xs font-medium rounded-full bg-primary-100 text-primary-700">
							{displayValue(value)}
						</span>
					{:else if column.key === 'acciones'}
						<div class="flex items-center gap-1">
							<button 
								type="button"
								class="p-1.5 text-secondary-500 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
								title="Crear propuesta"
								on:click|stopPropagation={() => irACrearPropuesta(activeTab, row)}
							>
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
								</svg>
							</button>
							<button 
								type="button"
								class="p-1.5 text-secondary-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
								title="Ver detalles"
								on:click|stopPropagation={() => viewBien(activeTab, row)}
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
								on:click|stopPropagation={() => editBien(activeTab, Number(row.id))}
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
					<div class="flex flex-col items-center justify-center py-12">
						<div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
							<span class="text-3xl">
								{activeTab === 'HOGAR' ? '🏠' : activeTab === 'VEHICULO' ? '🚗' : activeTab === 'COPROPIEDAD' ? '🏢' : '📦'}
							</span>
						</div>
						<p class="text-lg font-medium text-secondary-900 mb-2">
							No hay {activeTab === 'HOGAR' ? 'hogares' : activeTab === 'VEHICULO' ? 'vehículos' : activeTab === 'COPROPIEDAD' ? 'copropiedades' : 'otros bienes'}
						</p>
						<p class="text-secondary-500 text-center max-w-sm mb-4">
							{selectedClienteId ? 'Este cliente no tiene bienes de este tipo registrados.' : 'No se han registrado bienes de este tipo.'}
						</p>
						<button 
							class="btn btn-primary"
							on:click={handleNuevoBien}
						>
							Registrar {activeTab === 'HOGAR' ? 'Hogar' : activeTab === 'VEHICULO' ? 'Vehículo' : activeTab === 'COPROPIEDAD' ? 'Copropiedad' : 'Otro Bien'}
						</button>
					</div>
				</svelte:fragment>
			</DataTable>
		{/if}
	</div>
</div>

<!-- Modal de Visualización -->
<Modal 
	bind:open={showModal} 
	title={modalTipo === 'HOGAR' ? 'Detalle del Hogar' 
		: modalTipo === 'VEHICULO' ? 'Detalle del Vehículo'
		: modalTipo === 'COPROPIEDAD' ? 'Detalle de Copropiedad'
		: 'Detalle del Bien'}
	size="lg"
>
	{#if modalData}
		<div class="space-y-4">
			<!-- Info Cliente -->
			<div class="bg-secondary-50 rounded-lg p-4">
				<p class="text-xs text-secondary-500 mb-1">Cliente</p>
				<p class="font-medium text-secondary-900">{getClienteName(modalData.id_usuario)}</p>
			</div>

			<!-- Detalles según tipo -->
			{#if modalTipo === 'HOGAR' && 'tipo_inmueble' in modalData}
				<div class="grid grid-cols-2 gap-4">
					<div>
						<p class="text-xs text-secondary-500 mb-1">{HogarFields.tipo_inmueble.label}</p>
						<p class="text-sm font-medium">{displayValue(modalData.tipo_inmueble)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{HogarFields.ciudad_inmueble.label}</p>
						<p class="text-sm">{displayValue(modalData.ciudad_inmueble)}</p>
					</div>
					<div class="col-span-2">
						<p class="text-xs text-secondary-500 mb-1">{HogarFields.direccion_inmueble.label}</p>
						<p class="text-sm">{displayValue(modalData.direccion_inmueble)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{HogarFields.numero_pisos.label}</p>
						<p class="text-sm">{displayValue(modalData.numero_pisos)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{HogarFields.ano_construccion.label}</p>
						<p class="text-sm">{displayValue(modalData.ano_construccion)}</p>
					</div>
					<div class="col-span-2 border-t pt-4 mt-2">
						<h4 class="text-sm font-semibold text-secondary-700 mb-3">Valores de Avalúo</h4>
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">{HogarFields.valor_inmueble_avaluo.label}</p>
								<p class="text-sm font-medium text-primary-600">{formatCurrency(modalData.valor_inmueble_avaluo)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{HogarFields.valor_contenidos_normales_avaluo.label}</p>
								<p class="text-sm">{formatCurrency(modalData.valor_contenidos_normales_avaluo)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{HogarFields.valor_contenidos_especiales_avaluo.label}</p>
								<p class="text-sm">{formatCurrency(modalData.valor_contenidos_especiales_avaluo)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{HogarFields.valor_equipo_electronico_avaluo.label}</p>
								<p class="text-sm">{formatCurrency(modalData.valor_equipo_electronico_avaluo)}</p>
							</div>
						</div>
					</div>
				</div>
			{:else if modalTipo === 'VEHICULO' && 'placa' in modalData}
				<div class="grid grid-cols-2 gap-4">
					<div>
						<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.tipo_vehiculo.label}</p>
						<p class="text-sm font-medium">{displayValue(modalData.tipo_vehiculo)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.placa.label}</p>
						<p class="text-sm font-mono font-bold">{displayValue(modalData.placa)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.marca.label}</p>
						<p class="text-sm">{displayValue(modalData.marca)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.serie_referencia.label}</p>
						<p class="text-sm">{displayValue(modalData.serie_referencia)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.ano_modelo.label}</p>
						<p class="text-sm">{displayValue(modalData.ano_modelo)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.codigo_fasecolda.label}</p>
						<p class="text-sm font-mono">{displayValue(modalData.codigo_fasecolda)}</p>
					</div>
					<div class="col-span-2 border-t pt-4 mt-2">
						<h4 class="text-sm font-semibold text-secondary-700 mb-3">Valores</h4>
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.valor_vehiculo.label}</p>
								<p class="text-sm font-medium text-primary-600">{formatCurrency(modalData.valor_vehiculo)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{VehiculoFields.valor_accesorios_avaluo.label}</p>
								<p class="text-sm">{formatCurrency(modalData.valor_accesorios_avaluo)}</p>
							</div>
						</div>
					</div>
				</div>
			{:else if modalTipo === 'COPROPIEDAD' && 'tipo_copropiedad' in modalData}
				<div class="grid grid-cols-2 gap-4">
					<div>
						<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.tipo_copropiedad.label}</p>
						<p class="text-sm font-medium">{displayValue(modalData.tipo_copropiedad)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.estrato.label}</p>
						<p class="text-sm">{displayValue(modalData.estrato)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.ciudad.label}</p>
						<p class="text-sm">{displayValue(modalData.ciudad)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.ano_construccion.label}</p>
						<p class="text-sm">{displayValue(modalData.ano_construccion)}</p>
					</div>
					<div class="col-span-2">
						<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.direccion.label}</p>
						<p class="text-sm">{displayValue(modalData.direccion)}</p>
					</div>
					<div class="col-span-2 border-t pt-4 mt-2">
						<h4 class="text-sm font-semibold text-secondary-700 mb-3">Estructura</h4>
						<div class="grid grid-cols-3 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.numero_torres.label}</p>
								<p class="text-sm">{displayValue(modalData.numero_torres)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.numero_maximo_pisos.label}</p>
								<p class="text-sm">{displayValue(modalData.numero_maximo_pisos)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">{CopropiedadFields.numero_maximo_sotanos.label}</p>
								<p class="text-sm">{displayValue(modalData.numero_maximo_sotanos)}</p>
							</div>
						</div>
					</div>
				</div>
			{:else if modalTipo === 'OTRO' && 'bien_asegurado' in modalData}
				<div class="grid grid-cols-2 gap-4">
					<div>
						<p class="text-xs text-secondary-500 mb-1">{OtroBienFields.tipo_seguro.label}</p>
						<p class="text-sm font-medium">{displayValue(modalData.tipo_seguro)}</p>
					</div>
					<div>
						<p class="text-xs text-secondary-500 mb-1">{OtroBienFields.valor_bien_asegurar.label}</p>
						<p class="text-sm font-medium text-primary-600">{formatCurrency(modalData.valor_bien_asegurar)}</p>
					</div>
					<div class="col-span-2">
						<p class="text-xs text-secondary-500 mb-1">{OtroBienFields.bien_asegurado.label}</p>
						<p class="text-sm">{displayValue(modalData.bien_asegurado)}</p>
					</div>
					<div class="col-span-2">
						<p class="text-xs text-secondary-500 mb-1">{OtroBienFields.detalles_bien_asegurado.label}</p>
						<p class="text-sm whitespace-pre-wrap">{displayValue(modalData.detalles_bien_asegurado)}</p>
					</div>
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
				on:click={() => { showModal = false; editBien(modalTipo, modalData?.id || 0); }}
			>
				Editar
			</button>
		</div>
	</svelte:fragment>
</Modal>

