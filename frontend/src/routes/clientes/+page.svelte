<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import {
		Avatar,
		DropdownMenu,
		EmptyState,
		FilterBar,
		ListRowCard,
		Modal,
		PageHeader,
		SkeletonRows,
		Tag
	} from '$components';
	import { ClienteFields } from '$constants';
	import { catalog, loadCatalog } from '$lib/stores/catalog';
	import { buildPolizaRows, clienteDocumento, clienteNombre } from '$utils';
	import type { Cliente } from '$lib/types/cliente';

	const F = ClienteFields;

	// Filters
	let query = '';
	let filtroTipo = '';
	let filtroCiudad = '';

	// Detail modal
	let showModal = false;
	let selectedCliente: Cliente | null = null;

	onMount(() => {
		void loadCatalog();
	});

	/** Póliza counts per cliente, so a row can show how much business it holds. */
	$: polizasPorCliente = buildPolizaRows($catalog).reduce<Record<number, number>>((acc, row) => {
		if (row.clienteId) acc[row.clienteId] = (acc[row.clienteId] ?? 0) + 1;
		return acc;
	}, {});

	/** Bien counts per cliente, across the four collections. */
	$: bienesPorCliente = [
		...$catalog.hogares,
		...$catalog.vehiculos,
		...$catalog.copropiedades,
		...$catalog.otrosBienes
	].reduce<Record<number, number>>((acc, bien) => {
		acc[bien.id_usuario] = (acc[bien.id_usuario] ?? 0) + 1;
		return acc;
	}, {});

	$: ciudades = Array.from(
		new Set($catalog.clientes.map((c) => c.ciudad).filter((c): c is string => !!c))
	).sort((a, b) => a.localeCompare(b, 'es'));

	$: filtered = $catalog.clientes.filter((c) => {
		const q = query.trim().toLowerCase();
		const matchesQuery =
			!q ||
			clienteNombre(c).toLowerCase().includes(q) ||
			clienteDocumento(c).toLowerCase().includes(q) ||
			(c.correo ?? '').toLowerCase().includes(q);
		return (
			matchesQuery &&
			(!filtroTipo || c.tipo_persona === filtroTipo) &&
			(!filtroCiudad || c.ciudad === filtroCiudad)
		);
	});

	function resetFilters() {
		query = '';
		filtroTipo = '';
		filtroCiudad = '';
	}

	function viewCliente(cliente: Cliente) {
		selectedCliente = cliente;
		showModal = true;
	}

	function displayValue(value: unknown): string {
		if (value === null || value === undefined || value === '') return '—';
		return String(value);
	}

	function fieldsFor(c: Cliente) {
		return [
			{ label: 'Documento', value: clienteDocumento(c), strong: true },
			{ label: F.ciudad.label, value: displayValue(c.ciudad) },
			{ label: F.correo.label, value: displayValue(c.correo) },
			{ label: F.telefono_movil.label, value: displayValue(c.telefono_movil) },
			{ label: 'Bienes asegurados', value: String(bienesPorCliente[c.id] ?? 0) },
			{ label: F.direccion.label, value: displayValue(c.direccion) }
		];
	}
</script>

<svelte:head>
	<title>Clientes | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader
		title="Clientes"
		crumb="Inicio / Operación"
		subtitle="Personas y empresas con bienes asegurados"
	>
		<a slot="actions" href="/clientes/nuevo" class="btn-primary !min-h-[38px]">Nuevo cliente</a>
	</PageHeader>

	<FilterBar
		bind:query
		placeholder="Buscar por nombre, documento o correo…"
		selects={[
			{
				value: filtroTipo,
				label: 'Tipo de persona',
				options: [
					{ value: '', label: 'Personas y empresas' },
					{ value: 'PERSONA', label: 'Persona natural' },
					{ value: 'EMPRESA', label: 'Empresa' }
				],
				onChange: (v) => (filtroTipo = v)
			},
			{
				value: filtroCiudad,
				label: 'Ciudad',
				options: [
					{ value: '', label: 'Todas las ciudades' },
					...ciudades.map((c) => ({ value: c, label: c }))
				],
				onChange: (v) => (filtroCiudad = v)
			}
		]}
		count={filtered.length}
		countNoun="cliente"
		onReset={resetFilters}
	/>

	{#if $catalog.loading && !$catalog.loaded}
		<SkeletonRows count={5} />
	{:else if $catalog.error}
		<EmptyState title="No fue posible cargar los clientes" text={$catalog.error}>
			<button slot="action" type="button" class="btn-secondary" on:click={() => loadCatalog(true)}>
				Reintentar
			</button>
		</EmptyState>
	{:else if !filtered.length}
		<EmptyState
			title={$catalog.clientes.length ? 'Sin resultados' : 'Aún no hay clientes'}
			text={$catalog.clientes.length
				? 'Ningún cliente coincide con la búsqueda o los filtros aplicados. Puedes buscar por nombre, documento o correo.'
				: 'Registra el primer cliente para empezar a crear bienes y propuestas.'}
		>
			<svelte:fragment slot="action">
				{#if $catalog.clientes.length}
					<button type="button" class="btn-secondary" on:click={resetFilters}>
						Limpiar filtros
					</button>
				{:else}
					<a href="/clientes/nuevo" class="btn-primary">Nuevo cliente</a>
				{/if}
			</svelte:fragment>
		</EmptyState>
	{:else}
		<div class="row-list">
			{#each filtered as cliente (cliente.id)}
				<ListRowCard fields={fieldsFor(cliente)}>
					<Avatar slot="lead" name={clienteNombre(cliente)} shape="circle" />

					<span slot="title" class="row-card-title">{clienteNombre(cliente)}</span>

					<svelte:fragment slot="tags">
						<Tag variant={cliente.tipo_persona === 'PERSONA' ? 'accent-2' : 'accent'}>
							{cliente.tipo_persona === 'PERSONA' ? 'Persona natural' : 'Empresa'}
						</Tag>
						<Tag variant="neutral">
							{polizasPorCliente[cliente.id] ?? 0}
							{(polizasPorCliente[cliente.id] ?? 0) === 1 ? 'póliza' : 'pólizas'}
						</Tag>
					</svelte:fragment>

					<svelte:fragment slot="actions">
						<a
							class="btn-secondary !h-8 !py-0 !px-3 !text-xs"
							href="/propuestas?q={encodeURIComponent(clienteNombre(cliente))}"
						>
							Ver pólizas
						</a>
						<DropdownMenu width={210} height={150}>
							<button type="button" class="menu-item" on:click={() => viewCliente(cliente)}>
								Ver ficha
							</button>
							<a class="menu-item" href="/clientes/{cliente.id}/editar">Editar cliente</a>
							<a class="menu-item" href="/bienes?cliente={cliente.id}">Ver bienes</a>
						</DropdownMenu>
					</svelte:fragment>
				</ListRowCard>
			{/each}
		</div>
	{/if}
</div>

<!-- Detail modal -->
<Modal
	bind:open={showModal}
	title={selectedCliente ? clienteNombre(selectedCliente) : 'Detalles del cliente'}
	size="lg"
>
	{#if selectedCliente}
		<div class="space-y-4">
			<div class="card-flat !p-0">
				<div class="field-grid p-4">
					<div>
						<div class="field-label">{F.id.label}</div>
						<div class="field-value">#{selectedCliente.id}</div>
					</div>
					<div>
						<div class="field-label">{F.tipo_persona.label}</div>
						<Tag variant={selectedCliente.tipo_persona === 'PERSONA' ? 'accent-2' : 'accent'}>
							{selectedCliente.tipo_persona === 'PERSONA' ? 'Persona natural' : 'Empresa'}
						</Tag>
					</div>
					<div>
						<div class="field-label">{F.usuario.label}</div>
						<div class="field-value">{displayValue(selectedCliente.usuario)}</div>
					</div>
					<div>
						<div class="field-label">{F.tipo_usuario.label}</div>
						<div class="field-value">{displayValue(selectedCliente.tipo_usuario)}</div>
					</div>
				</div>
			</div>

			<div>
				<h3 class="card-heading">Contacto</h3>
				<div class="field-grid">
					<div>
						<div class="field-label">{F.correo.label}</div>
						<div class="field-value">
							{#if selectedCliente.correo}
								<a href="mailto:{selectedCliente.correo}">{selectedCliente.correo}</a>
							{:else}
								—
							{/if}
						</div>
					</div>
					<div>
						<div class="field-label">{F.telefono_movil.label}</div>
						<div class="field-value">{displayValue(selectedCliente.telefono_movil)}</div>
					</div>
					<div>
						<div class="field-label">{F.ciudad.label}</div>
						<div class="field-value">{displayValue(selectedCliente.ciudad)}</div>
					</div>
					<div>
						<div class="field-label">{F.direccion.label}</div>
						<div class="field-value">{displayValue(selectedCliente.direccion)}</div>
					</div>
				</div>
			</div>

			{#if selectedCliente.tipo_persona === 'PERSONA'}
				<div>
					<h3 class="card-heading">Datos personales</h3>
					<div class="field-grid">
						<div>
							<div class="field-label">{F.nombre.label}</div>
							<div class="field-value">{displayValue(selectedCliente.nombre)}</div>
						</div>
						<div>
							<div class="field-label">{F.tipo_documento.label}</div>
							<div class="field-value">{displayValue(selectedCliente.tipo_documento)}</div>
						</div>
						<div>
							<div class="field-label">{F.numero_documento.label}</div>
							<div class="field-value">{displayValue(selectedCliente.numero_documento)}</div>
						</div>
						<div>
							<div class="field-label">{F.edad.label}</div>
							<div class="field-value">{displayValue(selectedCliente.edad)}</div>
						</div>
					</div>
				</div>
			{:else}
				<div>
					<h3 class="card-heading">Datos de la empresa</h3>
					<div class="field-grid">
						<div>
							<div class="field-label">{F.razon_social.label}</div>
							<div class="field-value">{displayValue(selectedCliente.razon_social)}</div>
						</div>
						<div>
							<div class="field-label">{F.nit.label}</div>
							<div class="field-value">{displayValue(selectedCliente.nit)}</div>
						</div>
						<div>
							<div class="field-label">{F.nombre_rep_legal.label}</div>
							<div class="field-value">{displayValue(selectedCliente.nombre_rep_legal)}</div>
						</div>
						<div>
							<div class="field-label">{F.documento_rep_legal.label}</div>
							<div class="field-value">{displayValue(selectedCliente.documento_rep_legal)}</div>
						</div>
						<div>
							<div class="field-label">{F.telefono_rep_legal.label}</div>
							<div class="field-value">{displayValue(selectedCliente.telefono_rep_legal)}</div>
						</div>
						<div>
							<div class="field-label">{F.correo_rep_legal.label}</div>
							<div class="field-value">
								{#if selectedCliente.correo_rep_legal}
									<a href="mailto:{selectedCliente.correo_rep_legal}">
										{selectedCliente.correo_rep_legal}
									</a>
								{:else}
									—
								{/if}
							</div>
						</div>
						<div>
							<div class="field-label">{F.contacto_alternativo.label}</div>
							<div class="field-value">{displayValue(selectedCliente.contacto_alternativo)}</div>
						</div>
					</div>
				</div>
			{/if}
		</div>
	{/if}

	<svelte:fragment slot="footer">
		<div class="flex justify-end gap-2">
			<button type="button" class="btn-secondary" on:click={() => (showModal = false)}>
				Cerrar
			</button>
			<button
				type="button"
				class="btn-primary"
				on:click={() => {
					showModal = false;
					void goto(`/clientes/${selectedCliente?.id ?? 0}/editar`);
				}}
			>
				Editar
			</button>
		</div>
	</svelte:fragment>
</Modal>
