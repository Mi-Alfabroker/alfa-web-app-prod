<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import {
		Avatar,
		DropdownMenu,
		EmptyState,
		FilterBar,
		KpiRow,
		ListRowCard,
		Modal,
		PageHeader,
		SkeletonRows,
		StatusBadge
	} from '$components';
	import { catalog, loadCatalog } from '$lib/stores/catalog';
	import { buildPolizaRows, flujoPoliza, moneyShort, RUBROS, rubroBySlug, rubroByTipo } from '$utils';
	import type { PolizaRow } from '$utils';
	import type { TipoBien } from '$lib/types/bien';
	import type { EstadoPoliza, TipoPoliza } from '$lib/types/poliza';

	// Filters. The rubro lives in the URL (?rubro=) so the sidebar submenu, the
	// dropdown and a shared link all agree on one source of truth.
	let query = '';
	let filtroEstado = '';

	// Nueva propuesta modal
	let showNuevaModal = false;
	let selectedTipoBien: TipoBien = 'HOGAR';

	/**
	 * `EMITIDAS` is not a stored estado: it means "anything that is no longer a
	 * proposal", which the previous version offered as a one-click "Solo Pólizas"
	 * filter. Kept so that capability does not disappear behind four separate
	 * estado selections.
	 */
	const ESTADO_OPTIONS: { value: '' | EstadoPoliza | 'EMITIDAS'; label: string }[] = [
		{ value: '', label: 'Todos los estados' },
		{ value: 'PROSPECTO', label: 'Solo propuestas' },
		{ value: 'EMITIDAS', label: 'Solo pólizas emitidas' },
		{ value: 'VIGENTE', label: 'Vigente' },
		{ value: 'VENCIDA', label: 'Vencida' },
		{ value: 'CANCELADA', label: 'Cancelada' }
	];

	onMount(() => {
		void loadCatalog();
		// Deep links from elsewhere (e.g. "Ver pólizas" on a cliente row) seed the
		// search box through ?q=.
		const q = $page.url.searchParams.get('q');
		if (q) query = q;
	});

	$: filtroRubro = rubroBySlug($page.url.searchParams.get('rubro'))?.tipo ?? '';

	function setRubro(tipo: string) {
		const slug = RUBROS.find((r) => r.tipo === tipo)?.slug;
		const url = new URL($page.url);
		if (slug) {
			url.searchParams.set('rubro', slug);
		} else {
			url.searchParams.delete('rubro');
		}
		void goto(url, { replaceState: true, noScroll: true, keepFocus: true });
	}

	$: rows = buildPolizaRows($catalog);

	$: filtered = rows.filter((r) => {
		const q = query.trim().toLowerCase();
		const matchesQuery =
			!q ||
			r.consecutivo.toLowerCase().includes(q) ||
			r.clienteNombre.toLowerCase().includes(q) ||
			r.documento.toLowerCase().includes(q) ||
			r.bienDesc.toLowerCase().includes(q);
		const matchesEstado =
			!filtroEstado ||
			(filtroEstado === 'EMITIDAS' ? r.estado !== 'PROSPECTO' : r.estado === filtroEstado);
		return matchesQuery && (!filtroRubro || r.tipo === filtroRubro) && matchesEstado;
	});

	$: vigentes = rows.filter((r) => r.estado === 'VIGENTE').length;
	$: propuestas = rows.filter((r) => r.estado === 'PROSPECTO').length;
	$: primaTotal = rows
		.filter((r) => r.estado === 'VIGENTE')
		.reduce((sum, r) => sum + (r.prima ?? 0), 0);

	$: kpis = [
		{ label: 'Vigentes', value: String(vigentes), note: `de ${rows.length} registros` },
		{ label: 'Propuestas abiertas', value: String(propuestas), note: 'pendientes de emisión' },
		{ label: 'Prima vigente', value: moneyShort(primaTotal), note: 'cartera emitida' },
		{
			label: 'Aseguradoras',
			value: String($catalog.aseguradoras.length),
			note: 'registradas'
		}
	];

	function resetFilters() {
		query = '';
		filtroEstado = '';
		void goto('/propuestas', { replaceState: true, noScroll: true, keepFocus: true });
	}

	function openNuevaModal() {
		selectedTipoBien = (filtroRubro || 'HOGAR') as TipoBien;
		showNuevaModal = true;
	}

	function irAFormulario() {
		showNuevaModal = false;
		void goto(`/propuestas/nueva/${selectedTipoBien.toLowerCase()}`);
	}

	// Kept in the script: TypeScript is only transpiled inside <script>, so a
	// cast written in a template expression is a parse error.
	function selectRubro(tipo: TipoPoliza) {
		selectedTipoBien = tipo as TipoBien;
	}

	function fieldsFor(row: PolizaRow) {
		return [
			{ label: 'Cliente', value: row.clienteNombre, strong: true },
			{ label: 'Documento', value: row.documento },
			{ label: 'Bien asegurado', value: row.bienDesc },
			{ label: 'Vigencia', value: row.vigencia },
			{ label: 'Prima', value: row.primaLabel, strong: true },
			{ label: 'Aseguradora', value: row.aseguradoraNombre }
		];
	}
</script>

<svelte:head>
	<title>Pólizas y Propuestas | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader
		title="Pólizas"
		crumb="Inicio / Operación"
		subtitle="Cartera de Hogar, Vehículos, Copropiedades y otros ramos"
	>
		<svelte:fragment slot="actions">
			<button type="button" class="btn-primary !min-h-[38px]" on:click={openNuevaModal}>
				Nueva propuesta
			</button>
		</svelte:fragment>
	</PageHeader>

	<KpiRow {kpis} />

	<FilterBar
		bind:query
		placeholder="Buscar por consecutivo, cliente o documento…"
		selects={[
			{
				value: filtroRubro,
				label: 'Rubro',
				options: [
					{ value: '', label: 'Todos los rubros' },
					...RUBROS.map((r) => ({ value: r.tipo, label: r.label }))
				],
				onChange: setRubro
			},
			{
				value: filtroEstado,
				label: 'Estado',
				options: ESTADO_OPTIONS,
				onChange: (v) => (filtroEstado = v)
			}
		]}
		count={filtered.length}
		countNoun="registro"
		onReset={resetFilters}
	/>

	{#if $catalog.loading && !$catalog.loaded}
		<SkeletonRows count={5} />
	{:else if $catalog.error}
		<EmptyState title="No fue posible cargar las pólizas" text={$catalog.error}>
			<button slot="action" type="button" class="btn-secondary" on:click={() => loadCatalog(true)}>
				Reintentar
			</button>
		</EmptyState>
	{:else if !filtered.length}
		<EmptyState
			title="Sin resultados"
			text="Ningún registro coincide con la búsqueda o los filtros aplicados. Puedes buscar por consecutivo, por nombre del cliente o por su documento."
		>
			<button slot="action" type="button" class="btn-secondary" on:click={resetFilters}>
				Limpiar filtros
			</button>
		</EmptyState>
	{:else}
		<div class="row-list">
			{#each filtered as row (row.tipo + row.id)}
				<ListRowCard fields={fieldsFor(row)}>
					<Avatar slot="lead" text={row.sigla} shape="square" />

					<a slot="title" class="row-card-link" href={row.href}>{row.consecutivo}</a>

					<svelte:fragment slot="tags">
						<StatusBadge status={row.estado} label={row.estadoLabel} />
						<span class="tag tag-neutral">{row.rubroLabel}</span>
					</svelte:fragment>

					<svelte:fragment slot="actions">
						<a class="btn-secondary !h-8 !py-0 !px-3 !text-xs" href={row.href}>Ver detalle</a>
						<DropdownMenu width={230} height={180}>
							<a class="menu-item" href={row.href}>Ver detalle</a>
							<!--
								Mismo flujoPoliza que el detalle. Sin esto la lista sería una
								puerta trasera al orden que el detalle sí respeta.
							-->
							{#each flujoPoliza(row.raw, rubroByTipo(row.tipo).slug).pasos.filter((p) => p.id === 'propuesta' || p.id === 'entrega') as paso}
								{@const etiqueta =
									paso.id === 'propuesta' ? 'Generar propuesta' : 'Entregar póliza'}
								{#if paso.enabled && paso.href}
									<a class="menu-item" href={paso.href}>{etiqueta}</a>
								{:else}
									<span
										class="menu-item opacity-50 cursor-not-allowed"
										title={paso.blockedReason}
									>
										{etiqueta}
									</span>
								{/if}
							{/each}
						</DropdownMenu>
					</svelte:fragment>
				</ListRowCard>
			{/each}
		</div>
	{/if}
</div>

<Modal bind:open={showNuevaModal} title="Nueva propuesta" size="md">
	<div class="space-y-5">
		<p style="color: var(--color-text-60)">
			Selecciona el rubro para el cual deseas crear una nueva propuesta de seguro.
		</p>

		<div class="grid grid-cols-2 gap-2.5">
			{#each RUBROS as rubro}
				<button
					type="button"
					class="flex items-center gap-3 rounded-xl p-3.5 text-left transition-colors"
					style={selectedTipoBien === rubro.tipo
						? 'border: 1px solid var(--color-accent); background: var(--color-accent-100)'
						: 'border: 1px solid var(--color-divider)'}
					on:click={() => selectRubro(rubro.tipo)}
				>
					<Avatar text={rubro.sigla} shape="square" />
					<span class="font-medium">{rubro.label}</span>
				</button>
			{/each}
		</div>

		<p class="text-xs" style="color: var(--color-text-55)">
			En el siguiente paso podrás seleccionar el bien específico y registrar los valores de la
			propuesta.
		</p>
	</div>

	<svelte:fragment slot="footer">
		<div class="flex justify-end gap-2">
			<button type="button" class="btn-secondary" on:click={() => (showNuevaModal = false)}>
				Cancelar
			</button>
			<button type="button" class="btn-primary" on:click={irAFormulario}>Continuar</button>
		</div>
	</svelte:fragment>
</Modal>
