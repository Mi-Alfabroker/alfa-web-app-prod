<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME } from '$lib/config';
	import { DataTable, StatusBadge, Modal } from '$components';
	import { goto } from '$app/navigation';
	import { polizaService, clienteService, bienService, aseguradoraService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import type { Cliente } from '$lib/types/cliente';
	import type { Aseguradora } from '$lib/types/aseguradora';
	import type { Hogar, Vehiculo, Copropiedad, OtroBien, TipoBien } from '$lib/types/bien';
	import type { 
		PolizaHogar, PolizaVehiculo, PolizaCopropiedad, PolizaOtroBien, 
		Poliza, TipoPoliza, EstadoPoliza, ESTADOS_POLIZA 
	} from '$lib/types/poliza';

	// Data state
	let polizasHogar: PolizaHogar[] = [];
	let polizasVehiculo: PolizaVehiculo[] = [];
	let polizasCopropiedad: PolizaCopropiedad[] = [];
	let polizasOtroBien: PolizaOtroBien[] = [];
	
	let clientes: Cliente[] = [];
	let aseguradoras: Aseguradora[] = [];
	let hogares: Hogar[] = [];
	let vehiculos: Vehiculo[] = [];
	let copropiedades: Copropiedad[] = [];
	let otrosBienes: OtroBien[] = [];
	
	// UI state
	let loading = true;
	let error: string | null = null;
	let activeTab: TipoPoliza = 'HOGAR';
	
	// Filtros
	let filtroEstado: 'todos' | 'propuestas' | 'polizas' = 'todos';
	
	// Modal de crear propuesta
	let showNuevaModal = false;
	let selectedTipoBien: TipoBien = 'HOGAR';
	
	// Tab items
	const tabs = [
		{ id: 'HOGAR', label: 'Hogares', icon: '🏠' },
		{ id: 'VEHICULO', label: 'Vehículos', icon: '🚗' },
		{ id: 'COPROPIEDAD', label: 'Copropiedades', icon: '🏢' },
		{ id: 'OTRO', label: 'Otros', icon: '📦' }
	];

	// Filtros de estado
	const filtrosEstado = [
		{ id: 'todos', label: 'Todos' },
		{ id: 'propuestas', label: 'Solo Propuestas' },
		{ id: 'polizas', label: 'Solo Pólizas' }
	];

	// Column definitions
	const baseColumns = [
		{ key: 'consecutivo', label: 'Consecutivo', sortable: true },
		{ key: 'bien', label: 'Bien', sortable: true },
		{ key: 'cliente', label: 'Cliente', sortable: true },
		{ key: 'inicio_vigencia', label: 'Inicio', sortable: true },
		{ key: 'fin_vigencia', label: 'Fin', sortable: true },
		{ key: 'estado', label: 'Estado', sortable: true },
		{ key: 'acciones', label: 'Acciones', sortable: false }
	];

	// Cargar datos
	onMount(async () => {
		await Promise.all([
			loadClientes(),
			loadAseguradoras(),
			loadBienes(),
			loadPolizas()
		]);
		loading = false;
	});

	async function loadClientes() {
		try {
			clientes = await clienteService.getAll();
		} catch (err) {
			console.error('Error loading clientes:', err);
		}
	}

	async function loadAseguradoras() {
		try {
			aseguradoras = await aseguradoraService.getAll();
		} catch (err) {
			console.error('Error loading aseguradoras:', err);
		}
	}

	async function loadBienes() {
		try {
			const [h, v, c, o] = await Promise.all([
				bienService.hogares.getAll(),
				bienService.vehiculos.getAll(),
				bienService.copropiedades.getAll(),
				bienService.otros.getAll()
			]);
			hogares = h;
			vehiculos = v;
			copropiedades = c;
			otrosBienes = o;
		} catch (err) {
			console.error('Error loading bienes:', err);
		}
	}

	async function loadPolizas() {
		loading = true;
		error = null;
		try {
			const [ph, pv, pc, po] = await Promise.all([
				polizaService.hogar.getAll(),
				polizaService.vehiculo.getAll(),
				polizaService.copropiedad.getAll(),
				polizaService.otroBien.getAll()
			]);
			polizasHogar = ph.sort((a, b) => b.id - a.id);
			polizasVehiculo = pv.sort((a, b) => b.id - a.id);
			polizasCopropiedad = pc.sort((a, b) => b.id - a.id);
			polizasOtroBien = po.sort((a, b) => b.id - a.id);
		} catch (err) {
			console.error('Error loading polizas:', err);
			error = err instanceof Error ? err.message : 'Error al cargar las pólizas';
		} finally {
			loading = false;
		}
	}

	// Helpers para obtener nombres
	function getClienteName(idUsuario: number): string {
		const cliente = clientes.find(c => c.id === idUsuario);
		if (!cliente) return `#${idUsuario}`;
		return cliente.tipo_persona === 'PERSONA' 
			? cliente.nombre || `#${idUsuario}`
			: cliente.razon_social || `#${idUsuario}`;
	}

	function getHogarDesc(id: number): string {
		const hogar = hogares.find(h => h.id === id);
		if (!hogar) return `Hogar #${id}`;
		return `${hogar.tipo_inmueble || 'Hogar'} - ${hogar.ciudad_inmueble || ''}`;
	}

	function getVehiculoDesc(id: number): string {
		const vehiculo = vehiculos.find(v => v.id === id);
		if (!vehiculo) return `Vehículo #${id}`;
		return `${vehiculo.marca || ''} ${vehiculo.placa || ''}`.trim() || `Vehículo #${id}`;
	}

	function getCopropiedadDesc(id: number): string {
		const cop = copropiedades.find(c => c.id === id);
		if (!cop) return `Copropiedad #${id}`;
		return `${cop.tipo_copropiedad || 'Copropiedad'} - ${cop.ciudad || ''}`;
	}

	function getOtroBienDesc(id: number): string {
		const otro = otrosBienes.find(o => o.id === id);
		if (!otro) return `Otro Bien #${id}`;
		return otro.bien_asegurado || `Otro Bien #${id}`;
	}

	function getClienteIdFromBien(tipo: TipoPoliza, bienId: number): number {
		if (tipo === 'HOGAR') {
			return hogares.find(h => h.id === bienId)?.id_usuario || 0;
		} else if (tipo === 'VEHICULO') {
			return vehiculos.find(v => v.id === bienId)?.id_usuario || 0;
		} else if (tipo === 'COPROPIEDAD') {
			return copropiedades.find(c => c.id === bienId)?.id_usuario || 0;
		} else {
			return otrosBienes.find(o => o.id === bienId)?.id_usuario || 0;
		}
	}

	function formatDate(dateStr: unknown): string {
		if (!dateStr) return '—';
		try {
			return new Date(String(dateStr)).toLocaleDateString('es-CO', {
				day: '2-digit',
				month: 'short',
				year: 'numeric'
			});
		} catch {
			return String(dateStr);
		}
	}

	// Aplicar filtros de estado
	function applyEstadoFilter<T extends { estado: EstadoPoliza }>(items: T[]): T[] {
		if (filtroEstado === 'propuestas') {
			return items.filter(p => p.estado === 'PROSPECTO');
		} else if (filtroEstado === 'polizas') {
			return items.filter(p => p.estado !== 'PROSPECTO');
		}
		return items;
	}

	// Datos activos según tab y filtros
	$: activeData = (() => {
		let data: Poliza[] = [];
		if (activeTab === 'HOGAR') {
			data = applyEstadoFilter(polizasHogar);
		} else if (activeTab === 'VEHICULO') {
			data = applyEstadoFilter(polizasVehiculo);
		} else if (activeTab === 'COPROPIEDAD') {
			data = applyEstadoFilter(polizasCopropiedad);
		} else {
			data = applyEstadoFilter(polizasOtroBien);
		}
		return data;
	})();

	// Transformar datos para la tabla
	$: tableData = activeData.map(poliza => {
		let bienDesc = '';
		let bienId = 0;
		let clienteId = 0;

		if ('id_hogar' in poliza) {
			bienId = poliza.id_hogar;
			bienDesc = getHogarDesc(bienId);
			clienteId = getClienteIdFromBien('HOGAR', bienId);
		} else if ('id_vehiculo' in poliza) {
			bienId = poliza.id_vehiculo;
			bienDesc = getVehiculoDesc(bienId);
			clienteId = getClienteIdFromBien('VEHICULO', bienId);
		} else if ('id_copropiedad' in poliza) {
			bienId = poliza.id_copropiedad;
			bienDesc = getCopropiedadDesc(bienId);
			clienteId = getClienteIdFromBien('COPROPIEDAD', bienId);
		} else if ('id_otro_bien' in poliza) {
			bienId = poliza.id_otro_bien;
			bienDesc = getOtroBienDesc(bienId);
			clienteId = getClienteIdFromBien('OTRO', bienId);
		}

		return {
			id: poliza.id,
			consecutivo: poliza.consecutivo,
			bien: bienDesc,
			bienId,
			cliente: getClienteName(clienteId),
			clienteId,
			inicio_vigencia: poliza.inicio_vigencia,
			fin_vigencia: poliza.fin_vigencia,
			estado: poliza.estado,
			raw: poliza
		};
	});

	// Conteos
	$: counts = {
		HOGAR: { total: polizasHogar.length, propuestas: polizasHogar.filter(p => p.estado === 'PROSPECTO').length },
		VEHICULO: { total: polizasVehiculo.length, propuestas: polizasVehiculo.filter(p => p.estado === 'PROSPECTO').length },
		COPROPIEDAD: { total: polizasCopropiedad.length, propuestas: polizasCopropiedad.filter(p => p.estado === 'PROSPECTO').length },
		OTRO: { total: polizasOtroBien.length, propuestas: polizasOtroBien.filter(p => p.estado === 'PROSPECTO').length },
		totalGeneral: polizasHogar.length + polizasVehiculo.length + polizasCopropiedad.length + polizasOtroBien.length
	};

	function setActiveTab(tabId: string) {
		activeTab = tabId as TipoPoliza;
	}

	function setFiltroEstado(filtroId: string) {
		filtroEstado = filtroId as typeof filtroEstado;
	}

	function getTabCount(tabId: string): number {
		return counts[tabId as TipoPoliza]?.total || 0;
	}

	// Navegar a ver detalle
	function viewPoliza(tipo: TipoPoliza, id: number) {
		goto(`/propuestas/${tipo.toLowerCase()}/${id}`);
	}

	// Obtener color de badge según estado
	function getStatusColor(estado: EstadoPoliza): 'blue' | 'green' | 'red' | 'gray' | 'yellow' {
		switch(estado) {
			case 'PROSPECTO': return 'blue';
			case 'VIGENTE': return 'green';
			case 'VENCIDA': return 'red';
			case 'CANCELADA': return 'gray';
			default: return 'gray';
		}
	}

	// Abrir modal de nueva propuesta
	function openNuevaModal() {
		selectedTipoBien = activeTab as TipoBien;
		showNuevaModal = true;
	}

	// Helper para seleccionar tipo de bien
	function setSelectedTipoBien(tipo: string) {
		selectedTipoBien = tipo as TipoBien;
	}

	// Ir al formulario de crear propuesta
	function irAFormulario() {
		showNuevaModal = false;
		goto(`/propuestas/nueva/${selectedTipoBien.toLowerCase()}`);
	}
</script>

<svelte:head>
	<title>Pólizas y Propuestas | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<h1 class="page-title">Pólizas y Propuestas</h1>
	<p class="text-secondary-500 text-sm mt-1">
		{counts.totalGeneral} registro{counts.totalGeneral !== 1 ? 's' : ''} en total
	</p>
</header>

<!-- Content -->
<div class="page-content">
	<div class="card">
		<!-- Toolbar -->
		<div class="flex flex-wrap items-center justify-between gap-4 mb-6">
			<!-- Filtro por estado -->
			<div class="flex items-center gap-2">
				<span class="text-sm text-secondary-600">Mostrar:</span>
				<div class="flex rounded-lg border border-secondary-200 overflow-hidden">
					{#each filtrosEstado as filtro}
						<button
							type="button"
							class="px-3 py-1.5 text-sm font-medium transition-colors
								{filtroEstado === filtro.id 
									? 'bg-primary-500 text-white' 
									: 'bg-white text-secondary-600 hover:bg-secondary-50'}"
							on:click={() => setFiltroEstado(filtro.id)}
						>
							{filtro.label}
						</button>
					{/each}
				</div>
			</div>

			<!-- Acciones -->
			<div class="flex items-center gap-3">
				<button 
					type="button"
					class="btn btn-primary flex items-center gap-1.5"
					on:click={openNuevaModal}
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
					</svg>
					Nueva Propuesta
				</button>
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
						<span class="ml-1 px-2 py-0.5 text-xs rounded-full 
							{activeTab === tab.id ? 'bg-primary-100 text-primary-700' : 'bg-secondary-100 text-secondary-600'}">
							{getTabCount(tab.id)}
						</span>
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
					<p class="text-secondary-600">Cargando pólizas...</p>
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
				columns={baseColumns} 
				data={tableData}
				showActions={false}
			>
				<svelte:fragment slot="cell" let:row let:column let:value>
					{#if column.key === 'consecutivo'}
						<span class="font-mono text-sm font-medium text-primary-600">{value}</span>
					{:else if column.key === 'bien'}
						<span class="text-sm text-secondary-900">{value}</span>
					{:else if column.key === 'cliente'}
						<span class="text-sm">{value}</span>
					{:else if column.key === 'inicio_vigencia' || column.key === 'fin_vigencia'}
						<span class="text-sm text-secondary-600">{formatDate(value)}</span>
					{:else if column.key === 'estado'}
						<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
							{value === 'PROSPECTO' ? 'bg-blue-100 text-blue-800' : ''}
							{value === 'VIGENTE' ? 'bg-green-100 text-green-800' : ''}
							{value === 'VENCIDA' ? 'bg-red-100 text-red-800' : ''}
							{value === 'CANCELADA' ? 'bg-gray-100 text-gray-800' : ''}
						">
							{value === 'PROSPECTO' ? 'Propuesta' : value}
						</span>
					{:else if column.key === 'acciones'}
						<div class="flex items-center gap-1">
							<button 
								type="button"
								class="p-1.5 text-secondary-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
								title="Ver detalles"
								on:click|stopPropagation={() => viewPoliza(activeTab, row.id)}
							>
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
								</svg>
							</button>
						</div>
					{:else}
						{value ?? '—'}
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
							No hay {filtroEstado === 'propuestas' ? 'propuestas' : filtroEstado === 'polizas' ? 'pólizas' : 'registros'}
						</p>
						<p class="text-secondary-500 text-center max-w-sm mb-4">
							{#if filtroEstado === 'propuestas'}
								No hay propuestas para {activeTab === 'HOGAR' ? 'hogares' : activeTab === 'VEHICULO' ? 'vehículos' : activeTab === 'COPROPIEDAD' ? 'copropiedades' : 'otros bienes'}.
							{:else if filtroEstado === 'polizas'}
								No hay pólizas emitidas para este rubro.
							{:else}
								Crea una propuesta desde la sección de Bienes.
							{/if}
						</p>
						<a href="/bienes" class="btn btn-primary">
							Ir a Bienes
						</a>
					</div>
				</svelte:fragment>
			</DataTable>
		{/if}
	</div>
</div>

<!-- Modal Nueva Propuesta -->
<Modal 
	bind:open={showNuevaModal} 
	title="Nueva Propuesta"
	size="md"
>
	<div class="space-y-6">
		<p class="text-secondary-600">
			Selecciona el tipo de bien para el cual deseas crear una nueva propuesta de seguro.
		</p>

		<!-- Selector de tipo de bien -->
		<div class="grid grid-cols-2 gap-3">
			{#each [
				{ id: 'HOGAR', label: 'Hogar', icon: '🏠', desc: 'Casas, apartamentos' },
				{ id: 'VEHICULO', label: 'Vehículo', icon: '🚗', desc: 'Autos, motos' },
				{ id: 'COPROPIEDAD', label: 'Copropiedad', icon: '🏢', desc: 'Edificios, conjuntos' },
				{ id: 'OTRO', label: 'Otro Bien', icon: '📦', desc: 'Otros activos' }
			] as tipo}
				<button
					type="button"
					class="flex items-center gap-3 p-4 rounded-lg border-2 transition-all text-left
						{selectedTipoBien === tipo.id 
							? 'border-primary-500 bg-primary-50' 
							: 'border-secondary-200 hover:border-secondary-300'}"
					on:click={() => setSelectedTipoBien(tipo.id)}
				>
					<span class="text-3xl">{tipo.icon}</span>
					<div>
						<p class="font-medium {selectedTipoBien === tipo.id ? 'text-primary-700' : 'text-secondary-900'}">{tipo.label}</p>
						<p class="text-xs text-secondary-500">{tipo.desc}</p>
					</div>
				</button>
			{/each}
		</div>

		<!-- Info -->
		<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
			<div class="flex items-start gap-3">
				<svg class="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				<div>
					<p class="text-sm text-blue-800">
						En el siguiente paso podrás seleccionar el bien específico y llenar todos los valores de la propuesta.
					</p>
				</div>
			</div>
		</div>
	</div>

	<svelte:fragment slot="footer">
		<div class="flex justify-end gap-3">
			<button 
				type="button" 
				class="btn btn-secondary"
				on:click={() => { showNuevaModal = false; }}
			>
				Cancelar
			</button>
			<button 
				type="button" 
				class="btn btn-primary flex items-center gap-2"
				on:click={irAFormulario}
			>
				<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
				</svg>
				Continuar
			</button>
		</div>
	</svelte:fragment>
</Modal>
