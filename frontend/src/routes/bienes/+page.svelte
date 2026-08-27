<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME } from '$lib/config';
	import {
		Avatar,
		DropdownMenu,
		EmptyState,
		ListRowCard,
		Modal,
		PageHeader,
		SkeletonRows,
		Tag
	} from '$components';
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

	// Helper para cambiar tab (evita casting en template)
	function setActiveTab(tabId: string) {
		activeTab = tabId as TipoBien;
	}

	/**
	 * Derived rather than called per tab from the template. A template call like
	 * `getTabCount(tab.id)` only re-evaluates when a name inside that expression
	 * changes, so a helper reading `counts` internally would stay frozen at the
	 * zeros it saw before the lists loaded.
	 */
	$: tabsWithCounts = tabs.map((tab) => ({
		...tab,
		count: counts[tab.id as TipoBien] ?? 0
	}));

	// Helper para formatear valor numérico
	function formatValue(value: unknown): string {
		return formatCurrency(value as number);
	}

	/**
	 * Row-card shape per rubro. Each collection has its own columns, so the
	 * headline, the tag and the metadata grid are chosen per type; the cliente
	 * is included in all four (the old table did not show the owner at all).
	 */
	interface BienRow {
		id: number;
		sigla: string;
		titulo: string;
		tipo: string;
		fields: { label: string; value: string; strong?: boolean }[];
		raw: Record<string, unknown>;
	}

	function num(value: number | null | undefined): string {
		return value === null || value === undefined ? '—' : String(value);
	}

	/**
	 * Derived rather than called from the template, and every source is named in
	 * the reactive expression below — including `clientes`, which is only read
	 * indirectly through `getClienteName`. Left implicit, the owner column would
	 * keep showing `#id` whenever clientes resolved after the bien lists.
	 */
	$: bienRows = buildBienRows(
		activeTab,
		hogares,
		vehiculos,
		copropiedades,
		otrosBienes,
		clientes
	);

	function buildBienRows(
		activeTab: TipoBien,
		hogares: Hogar[],
		vehiculos: Vehiculo[],
		copropiedades: Copropiedad[],
		otrosBienes: OtroBien[],
		// Named so the reactive statement above depends on it; read via getClienteName.
		_clientes: Cliente[]
	): BienRow[] {
		if (activeTab === 'HOGAR') {
			return hogares.map((h) => ({
				id: h.id,
				sigla: 'HOG',
				titulo: h.direccion_inmueble || `Hogar #${h.id}`,
				tipo: h.tipo_inmueble || 'Hogar',
				raw: h as unknown as Record<string, unknown>,
				fields: [
					{ label: 'Cliente', value: getClienteName(h.id_usuario), strong: true },
					{ label: HogarFields.ciudad_inmueble.label, value: displayValue(h.ciudad_inmueble) },
					{ label: 'Valor avalúo', value: formatValue(h.valor_inmueble_avaluo), strong: true },
					{ label: HogarFields.numero_pisos.label, value: num(h.numero_pisos) },
					{ label: HogarFields.ano_construccion.label, value: num(h.ano_construccion) }
				]
			}));
		}
		if (activeTab === 'VEHICULO') {
			return vehiculos.map((v) => ({
				id: v.id,
				sigla: 'AUT',
				titulo: v.placa || `Vehículo #${v.id}`,
				tipo: v.tipo_vehiculo || 'Vehículo',
				raw: v as unknown as Record<string, unknown>,
				fields: [
					{ label: 'Cliente', value: getClienteName(v.id_usuario), strong: true },
					{ label: VehiculoFields.marca.label, value: displayValue(v.marca) },
					{ label: VehiculoFields.ano_modelo.label, value: num(v.ano_modelo) },
					{ label: VehiculoFields.serie_referencia.label, value: displayValue(v.serie_referencia) },
					{ label: 'Valor vehículo', value: formatValue(v.valor_vehiculo), strong: true },
					{ label: VehiculoFields.codigo_fasecolda.label, value: displayValue(v.codigo_fasecolda) }
				]
			}));
		}
		if (activeTab === 'COPROPIEDAD') {
			return copropiedades.map((c) => ({
				id: c.id,
				sigla: 'COP',
				titulo: c.direccion || `Copropiedad #${c.id}`,
				tipo: c.tipo_copropiedad || 'Copropiedad',
				raw: c as unknown as Record<string, unknown>,
				fields: [
					{ label: 'Cliente', value: getClienteName(c.id_usuario), strong: true },
					{ label: CopropiedadFields.ciudad.label, value: displayValue(c.ciudad) },
					{ label: CopropiedadFields.estrato.label, value: num(c.estrato) },
					{ label: 'Torres', value: num(c.numero_torres) },
					{
						label: 'Valor área común',
						value: formatValue(c.valor_edificio_area_comun_avaluo),
						strong: true
					},
					{ label: CopropiedadFields.ano_construccion.label, value: num(c.ano_construccion) }
				]
			}));
		}
		return otrosBienes.map((o) => ({
			id: o.id,
			sigla: 'OTR',
			titulo: o.bien_asegurado || `Otro bien #${o.id}`,
			tipo: o.tipo_seguro || 'Otro',
			raw: o as unknown as Record<string, unknown>,
			fields: [
				{ label: 'Cliente', value: getClienteName(o.id_usuario), strong: true },
				{ label: 'Valor a asegurar', value: formatValue(o.valor_bien_asegurar), strong: true },
				{ label: OtroBienFields.detalles_bien_asegurado.label, value: displayValue(o.detalles_bien_asegurado) }
			]
		}));
	}

	$: rubroSingular =
		activeTab === 'HOGAR'
			? 'hogar'
			: activeTab === 'VEHICULO'
				? 'vehículo'
				: activeTab === 'COPROPIEDAD'
					? 'copropiedad'
					: 'otro bien';

	$: rubroPlural =
		activeTab === 'HOGAR'
			? 'hogares'
			: activeTab === 'VEHICULO'
				? 'vehículos'
				: activeTab === 'COPROPIEDAD'
					? 'copropiedades'
					: 'otros bienes';
</script>

<svelte:head>
	<title>Bienes | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader
		title="Bienes"
		crumb="Inicio / Operación"
		subtitle="Hogares, vehículos, copropiedades y otros bienes asegurables"
	>
		<button slot="actions" type="button" class="btn-primary !min-h-[38px]" on:click={handleNuevoBien}>
			Nuevo bien
		</button>
	</PageHeader>

	<!-- Cliente lookup: the backend filters bienes by owner, so this searches
	     the cliente by document first and then reloads the lists. -->
	<div class="filter-bar">
		<div class="relative flex-1 min-w-[200px]">
			<svg
				class="absolute left-3 top-1/2 -translate-y-1/2 opacity-50"
				width="16"
				height="16"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="1.5"
			>
				<circle cx="11" cy="11" r="6.5" />
				<path d="M16 16l4.5 4.5" />
			</svg>
			<input
				id="documento-filter"
				type="search"
				class="input !pl-9 !min-h-[38px]"
				placeholder="Filtrar por documento del cliente (CC o NIT)…"
				aria-label="Filtrar por documento del cliente"
				bind:value={documentoFilter}
				on:keydown={handleSearchKeydown}
			/>
		</div>

		<button
			type="button"
			class="btn-secondary !min-h-[38px]"
			on:click={searchByDocumento}
			disabled={searchingCliente}
		>
			{searchingCliente ? 'Buscando…' : 'Buscar'}
		</button>

		{#if filteredCliente}
			<Tag variant="accent">
				{filteredCliente.tipo_persona === 'PERSONA'
					? filteredCliente.nombre
					: filteredCliente.razon_social}
			</Tag>
			<button type="button" class="btn-ghost !min-h-[38px]" on:click={clearFilter}>
				Limpiar filtros
			</button>
		{:else if documentoFilter && !searchingCliente}
			<Tag variant="outline">Cliente no encontrado</Tag>
		{/if}

		<div class="ml-auto text-xs whitespace-nowrap" style="color: var(--color-text-55)">
			{counts.total} bien{counts.total !== 1 ? 'es' : ''}
		</div>
	</div>

	<!-- Tabs -->
	<div class="tabs mb-3.5">
		{#each tabsWithCounts as tab}
			<button
				type="button"
				class="tab {activeTab === tab.id ? 'tab-active' : ''}"
				on:click={() => setActiveTab(tab.id)}
			>
				{tab.label}
				<span class="tab-count">{tab.count}</span>
			</button>
		{/each}
	</div>

	{#if loading}
		<SkeletonRows count={4} />
	{:else if error}
		<EmptyState title="No fue posible cargar los bienes" text={error}>
			<button slot="action" type="button" class="btn-secondary" on:click={loadBienes}>
				Reintentar
			</button>
		</EmptyState>
	{:else if !bienRows.length}
		<EmptyState
			title="No hay {rubroPlural}"
			text={selectedClienteId
				? 'Este cliente no tiene bienes de este tipo registrados.'
				: 'Todavía no se han registrado bienes de este tipo.'}
		>
			<button slot="action" type="button" class="btn-primary" on:click={handleNuevoBien}>
				Registrar {rubroSingular}
			</button>
		</EmptyState>
	{:else}
		<div class="row-list">
			{#each bienRows as bien (bien.id)}
				<ListRowCard fields={bien.fields}>
					<Avatar slot="lead" text={bien.sigla} shape="square" />

					<button
						slot="title"
						type="button"
						class="row-card-link"
						on:click={() => viewBien(activeTab, bien.raw)}
					>
						{bien.titulo}
					</button>

					<svelte:fragment slot="tags">
						<Tag variant="accent">{bien.tipo}</Tag>
						<Tag variant="neutral">#{bien.id}</Tag>
					</svelte:fragment>

					<svelte:fragment slot="actions">
						<button
							type="button"
							class="btn-secondary !h-8 !py-0 !px-3 !text-xs"
							on:click={() => irACrearPropuesta(activeTab, bien.raw)}
						>
							Crear propuesta
						</button>
						<DropdownMenu width={210} height={150}>
							<button type="button" class="menu-item" on:click={() => viewBien(activeTab, bien.raw)}>
								Ver detalle
							</button>
							<button type="button" class="menu-item" on:click={() => editBien(activeTab, bien.id)}>
								Editar bien
							</button>
							<button
								type="button"
								class="menu-item"
								on:click={() => irACrearPropuesta(activeTab, bien.raw)}
							>
								Crear propuesta
							</button>
						</DropdownMenu>
					</svelte:fragment>
				</ListRowCard>
			{/each}
		</div>
	{/if}
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

