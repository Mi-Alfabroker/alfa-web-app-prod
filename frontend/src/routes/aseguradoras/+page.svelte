<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME } from '$lib/config';
	import {
		Avatar,
		DropdownMenu,
		EmptyState,
		FilterBar,
		KpiRow,
		ListRowCard,
		PageHeader,
		SkeletonRows,
		Tag
	} from '$components';
	import { AseguradoraFields } from '$constants';
	import { catalog, loadCatalog } from '$lib/stores/catalog';
	import { aseguradoraIds, RUBROS, valoresConfigurados } from '$utils';
	import type { Aseguradora } from '$types/aseguradora';

	const F = AseguradoraFields;

	let query = '';

	onMount(() => {
		void loadCatalog();
	});

	/**
	 * Pólizas placed with each aseguradora — counted from the bound slot, so a
	 * quote that never won does not inflate the number.
	 */
	$: polizasPorAseguradora = [
		...$catalog.polizasHogar,
		...$catalog.polizasVehiculo,
		...$catalog.polizasCopropiedad,
		...$catalog.polizasOtroBien
	].reduce<Record<number, number>>((acc, poliza) => {
		const slot = poliza.aseguradora_seleccionada;
		if (!slot) return acc;
		const id = aseguradoraIds(poliza)[slot - 1];
		if (id) acc[id] = (acc[id] ?? 0) + 1;
		return acc;
	}, {});

	$: filtered = $catalog.aseguradoras.filter((a) => {
		const q = query.trim().toLowerCase();
		if (!q) return true;
		return (
			a.nombre.toLowerCase().includes(q) ||
			(a.respaldo_aseguradora ?? '').toLowerCase().includes(q) ||
			(a.contacto_asignado ?? '').toLowerCase().includes(q)
		);
	});

	$: totalValores = $catalog.aseguradoras.reduce((sum, a) => sum + valoresConfigurados(a), 0);

	$: kpis = [
		{
			label: 'Aseguradoras',
			value: String($catalog.aseguradoras.length),
			note: 'aliados registrados'
		},
		{
			label: 'Valores configurados',
			value: String(totalValores),
			note: 'condiciones por rubro'
		},
		{ label: 'Rubros cubiertos', value: String(RUBROS.length), note: RUBROS.map((r) => r.label).join(', ') },
		{
			label: 'Pólizas colocadas',
			value: String(Object.values(polizasPorAseguradora).reduce((a, b) => a + b, 0)),
			note: 'con aseguradora seleccionada'
		}
	];

	function displayValue(value: unknown): string {
		if (value === null || value === undefined || value === '') return '—';
		return String(value);
	}

	function fieldsFor(a: Aseguradora) {
		return [
			{ label: F.numeral_asistencia.label, value: displayValue(a.numeral_asistencia), strong: true },
			{ label: F.correo_comercial.label, value: displayValue(a.correo_comercial) },
			{ label: F.correo_reclamaciones.label, value: displayValue(a.correo_reclamaciones) },
			{ label: F.contacto_asignado.label, value: displayValue(a.contacto_asignado) },
			{ label: F.direccion_oficina.label, value: displayValue(a.direccion_oficina) },
			{
				label: 'Pólizas colocadas',
				value: String(polizasPorAseguradora[a.id] ?? 0)
			}
		];
	}
</script>

<svelte:head>
	<title>Aseguradoras | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader
		title="Aseguradoras"
		crumb="Inicio / Operación"
		subtitle="Aliados, condiciones y valores precargados por rubro"
	>
		<a slot="actions" href="/aseguradoras/nueva" class="btn-primary !min-h-[38px]">
			Registrar aseguradora
		</a>
	</PageHeader>

	<KpiRow {kpis} />

	<FilterBar
		bind:query
		placeholder="Buscar aseguradora, respaldo o contacto…"
		count={filtered.length}
		countNoun="aseguradora"
		onReset={() => (query = '')}
	/>

	{#if $catalog.loading && !$catalog.loaded}
		<SkeletonRows count={4} />
	{:else if $catalog.error}
		<EmptyState title="No fue posible cargar las aseguradoras" text={$catalog.error}>
			<button slot="action" type="button" class="btn-secondary" on:click={() => loadCatalog(true)}>
				Reintentar
			</button>
		</EmptyState>
	{:else if !filtered.length}
		<EmptyState
			title={$catalog.aseguradoras.length ? 'Sin resultados' : 'Aún no hay aseguradoras'}
			text={$catalog.aseguradoras.length
				? 'Ninguna aseguradora coincide con la búsqueda.'
				: 'Registra la primera aseguradora para poder cotizar propuestas.'}
		>
			<svelte:fragment slot="action">
				{#if $catalog.aseguradoras.length}
					<button type="button" class="btn-secondary" on:click={() => (query = '')}>
						Limpiar filtros
					</button>
				{:else}
					<a href="/aseguradoras/nueva" class="btn-primary">Registrar aseguradora</a>
				{/if}
			</svelte:fragment>
		</EmptyState>
	{:else}
		<div class="row-list">
			{#each filtered as aseguradora (aseguradora.id)}
				<ListRowCard fields={fieldsFor(aseguradora)}>
					<Avatar slot="lead" name={aseguradora.nombre} shape="square" strong />

					<span slot="title" class="row-card-title">{aseguradora.nombre}</span>

					<svelte:fragment slot="tags">
						<Tag variant="accent">{valoresConfigurados(aseguradora)} valores</Tag>
						{#if aseguradora.respaldo_aseguradora}
							<Tag variant="neutral">{aseguradora.respaldo_aseguradora}</Tag>
						{/if}
					</svelte:fragment>

					<svelte:fragment slot="actions">
						<a
							class="btn-secondary !h-8 !py-0 !px-3 !text-xs"
							href="/aseguradoras/{aseguradora.id}"
						>
							Ver ficha
						</a>
						<a
							class="btn-secondary !h-8 !py-0 !px-3 !text-xs"
							href="/aseguradoras/{aseguradora.id}/editar"
						>
							Editar
						</a>
						<DropdownMenu width={210} height={130}>
							<a class="menu-item" href="/aseguradoras/{aseguradora.id}">Ver ficha</a>
							<a class="menu-item" href="/aseguradoras/{aseguradora.id}/editar">
								Editar aseguradora
							</a>
						</DropdownMenu>
					</svelte:fragment>
				</ListRowCard>
			{/each}
		</div>
	{/if}
</div>
