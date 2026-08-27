<script lang="ts">
	import { onMount } from 'svelte';
	import { APP_NAME } from '$lib/config';
	import { BarList, EmptyState, KpiRow, PageHeader, SkeletonRows, StatusBadge } from '$components';
	import { DOMAIN_ICONS } from '$constants';
	import { catalog, loadCatalog } from '$lib/stores/catalog';
	import {
		aseguradoraIds,
		buildPolizaRows,
		diasParaVencer,
		money,
		moneyShort,
		RUBROS
	} from '$utils';
	import type { PolizaRow } from '$utils';

	/** Window used for the "próximos a vencer" panel. */
	const DIAS_VENCIMIENTO = 60;

	/**
	 * Primary entry points. Each tile carries the glyph of the section it leads to
	 * (same map the sidebar uses), so the icon is a wayfinding cue rather than
	 * decoration: the tile and its nav item read as the same place.
	 */
	const quickActions = [
		{
			label: 'Nueva propuesta',
			href: '/propuestas/nueva',
			desc: 'Cotizar un bien',
			icon: DOMAIN_ICONS.polizas
		},
		{
			label: 'Nuevo cliente',
			href: '/clientes/nuevo',
			desc: 'Persona o empresa',
			icon: DOMAIN_ICONS.clientes
		},
		{
			label: 'Nuevo bien',
			href: '/bienes/nuevo',
			desc: 'Hogar, vehículo, copropiedad',
			icon: DOMAIN_ICONS.bienes
		},
		{
			label: 'Nueva aseguradora',
			href: '/aseguradoras/nueva',
			desc: 'Condiciones por rubro',
			icon: DOMAIN_ICONS.aseguradoras
		}
	];

	onMount(() => {
		void loadCatalog();
	});

	$: rows = buildPolizaRows($catalog);
	$: vigentes = rows.filter((r) => r.estado === 'VIGENTE');
	$: propuestas = rows.filter((r) => r.estado === 'PROSPECTO');
	$: primaVigente = vigentes.reduce((sum, r) => sum + (r.prima ?? 0), 0);

	/**
	 * Vigentes whose cover ends inside the window, plus anything already past its
	 * end date — both need someone to make a call. Soonest first.
	 */
	$: vencimientos = rows
		.filter((r) => r.estado === 'VIGENTE' || r.estado === 'VENCIDA')
		.map((r) => ({ row: r, dias: diasParaVencer(r.raw) }))
		.filter(
			(v): v is { row: PolizaRow; dias: number } => v.dias !== null && v.dias <= DIAS_VENCIMIENTO
		)
		.sort((a, b) => a.dias - b.dias);

	/** Open proposals, oldest first: the ones most at risk of going cold. */
	$: porCerrar = [...propuestas].sort((a, b) => {
		const at = a.raw.created_at ? Date.parse(a.raw.created_at) : 0;
		const bt = b.raw.created_at ? Date.parse(b.raw.created_at) : 0;
		return at - bt;
	});

	$: kpis = [
		{
			label: 'Pólizas vigentes',
			value: String(vigentes.length),
			note: `de ${rows.length} registros en cartera`
		},
		{
			label: `Vencen en ${DIAS_VENCIMIENTO} días`,
			value: String(vencimientos.filter((v) => v.dias >= 0).length),
			note: 'requieren contacto'
		},
		{
			label: 'Propuestas abiertas',
			value: String(propuestas.length),
			note: 'pendientes de emisión'
		},
		{
			label: 'Prima vigente',
			value: moneyShort(primaVigente),
			note: `${$catalog.clientes.length} clientes activos`
		}
	];

	/**
	 * Records per rubro. Counting records rather than prima keeps the bars readable
	 * while most of the cartera is still in proposal state and carries no bound
	 * prima; the prima rides along as the row note.
	 */
	$: porRubro = RUBROS.map((rubro) => {
		const delRubro = rows.filter((r) => r.tipo === rubro.tipo);
		const prima = delRubro
			.filter((r) => r.estado === 'VIGENTE')
			.reduce((sum, r) => sum + (r.prima ?? 0), 0);
		return {
			label: rubro.label,
			value: delRubro.length,
			valueLabel: String(delRubro.length),
			note: prima > 0 ? `${money(prima)} de prima vigente` : undefined,
			tooltip: `${rubro.label}: ${delRubro.length} registros · ${money(prima)} de prima vigente`
		};
	}).sort((a, b) => b.value - a.value);

	/** Pólizas actually placed with each aseguradora (bound slot only). */
	$: porAseguradora = $catalog.aseguradoras
		.map((aseguradora) => {
			const colocadas = rows.filter((r) => {
				const slot = r.raw.aseguradora_seleccionada;
				return slot ? aseguradoraIds(r.raw)[slot - 1] === aseguradora.id : false;
			});
			const prima = colocadas.reduce((sum, r) => sum + (r.prima ?? 0), 0);
			return {
				label: aseguradora.nombre,
				value: colocadas.length,
				valueLabel: String(colocadas.length),
				note: prima > 0 ? `${money(prima)} de prima` : undefined,
				tooltip: `${aseguradora.nombre}: ${colocadas.length} pólizas colocadas · ${money(prima)}`
			};
		})
		.sort((a, b) => b.value - a.value);

	$: cargando = $catalog.loading && !$catalog.loaded;

	function diasLabel(dias: number): string {
		if (dias < 0) return `Venció hace ${Math.abs(dias)} d`;
		if (dias === 0) return 'Vence hoy';
		return `En ${dias} d`;
	}
</script>

<svelte:head>
	<title>Dashboard | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader title="Dashboard" crumb="Inicio" subtitle="Indicadores de la cartera de {APP_NAME}" />

	<!-- Entry points first: these are the four things people come here to start. -->
	<div class="action-strip">
		{#each quickActions as action}
			<a href={action.href} class="action-tile">
				<span class="action-tile-icon">
					<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
						<path d={action.icon.d} />
						<path d={action.icon.d2} />
					</svg>
				</span>
				<span class="min-w-0">
					<span class="action-tile-label">{action.label}</span>
					<span class="action-tile-desc">{action.desc}</span>
				</span>
			</a>
		{/each}
	</div>

	<KpiRow {kpis} />

	{#if $catalog.error}
		<EmptyState title="No fue posible cargar la cartera" text={$catalog.error}>
			<button slot="action" type="button" class="btn-secondary" on:click={() => loadCatalog(true)}>
				Reintentar
			</button>
		</EmptyState>
	{:else}
		<!--
			Main column carries the actionable queues; the rail carries composition
			and shortcuts. Stacking by kind — rather than pairing one list with one
			chart per row — keeps the two column heights close, so neither side ends
			in a block of empty card.
		-->
		<div class="detail-grid">
			<!-- Main column: what someone has to act on -->
			<div class="flex flex-col gap-3.5 min-w-0">
				<div class="card">
					<div class="flex items-center gap-2 mb-1">
						<h3 class="card-heading !mb-0">Vencimientos próximos</h3>
						{#if vencimientos.length}
							<span class="tag tag-neutral">{vencimientos.length}</span>
						{/if}
					</div>
					<p class="text-xs mb-3" style="color: var(--color-text-55)">
						Pólizas vigentes cuya cobertura termina dentro de {DIAS_VENCIMIENTO} días, y las que ya
						vencieron. Primero las más urgentes.
					</p>

					{#if cargando}
						<SkeletonRows count={3} />
					{:else if !vencimientos.length}
						<p class="text-sm" style="color: var(--color-text-60)">
							Ninguna póliza vence en los próximos {DIAS_VENCIMIENTO} días.
						</p>
					{:else}
						<!--
							tabindex is deliberate and the a11y rule is over-broad here: it sees a
							plain div, but this one scrolls, and a scroll container that cannot take
							focus cannot be scrolled by keyboard (WCAG 2.1.1). role=region + tabindex=0
							is the documented pattern for a scrollable region.
						-->
						<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
						<div
							class="scroll-list flex flex-col gap-2.5"
							role="region"
							aria-label="Vencimientos próximos"
							tabindex="0"
						>
							{#each vencimientos as { row, dias } (row.tipo + row.id)}
								<div
									class="flex flex-wrap items-center gap-2.5 rounded-xl px-3 py-2.5 flex-none"
									style="border: 1px solid var(--color-divider)"
								>
									<a class="row-card-link !text-sm" href={row.href}>{row.consecutivo}</a>
									<StatusBadge status={row.estado} label={row.estadoLabel} />
									<span class="text-[13px]" style="color: var(--color-text-60)">
										{row.clienteNombre}
									</span>
									<span class="ml-auto text-[13px] font-medium whitespace-nowrap">
										{row.fin} · {diasLabel(dias)}
									</span>
								</div>
							{/each}
						</div>
					{/if}
				</div>

				<div class="card">
					<div class="flex items-center gap-2 mb-1">
						<h3 class="card-heading !mb-0">Propuestas por cerrar</h3>
						{#if porCerrar.length}
							<span class="tag tag-neutral">{porCerrar.length}</span>
						{/if}
					</div>
					<p class="text-xs mb-3" style="color: var(--color-text-55)">
						Cotizaciones sin emitir, de la más antigua a la más reciente.
					</p>

					{#if cargando}
						<SkeletonRows count={4} />
					{:else if !porCerrar.length}
						<p class="text-sm" style="color: var(--color-text-60)">No hay propuestas abiertas.</p>
					{:else}
						<!--
							The whole queue lives here and scrolls in place, rather than being
							truncated to a handful with a "see all" link: this is a work list,
							so every row should be reachable without leaving the dashboard.
						-->
						<!--
							tabindex is deliberate and the a11y rule is over-broad here: it sees a
							plain div, but this one scrolls, and a scroll container that cannot take
							focus cannot be scrolled by keyboard (WCAG 2.1.1). role=region + tabindex=0
							is the documented pattern for a scrollable region.
						-->
						<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
						<div
							class="scroll-list flex flex-col gap-2.5"
							role="region"
							aria-label="Propuestas por cerrar"
							tabindex="0"
						>
							{#each porCerrar as row (row.tipo + row.id)}
								<div
									class="flex flex-wrap items-center gap-2.5 rounded-xl px-3 py-2.5 flex-none"
									style="border: 1px solid var(--color-divider)"
								>
									<a class="row-card-link !text-sm" href={row.href}>{row.consecutivo}</a>
									<span class="tag tag-neutral">{row.rubroLabel}</span>
									<span class="text-[13px]" style="color: var(--color-text-60)">
										{row.clienteNombre}
									</span>
									<span class="ml-auto text-[13px] font-medium whitespace-nowrap">
										{row.primaLabel}
									</span>
								</div>
							{/each}
						</div>
						<a class="link-button mt-3" href="/propuestas">Abrir en la lista de pólizas</a>
					{/if}
				</div>
			</div>

			<!-- Rail: how the cartera is composed, plus shortcuts -->
			<div class="flex flex-col gap-3.5 min-w-0">
				<div class="card">
					<h3 class="card-heading">Registros por rubro</h3>
					<p class="text-xs mb-3.5" style="color: var(--color-text-55)">
						Pólizas y propuestas en cada ramo.
					</p>
					{#if cargando}
						<SkeletonRows count={4} />
					{:else}
						<BarList items={porRubro} emptyText="Todavía no hay pólizas registradas." />
					{/if}
				</div>

				<div class="card">
					<h3 class="card-heading">Colocación por aseguradora</h3>
					<p class="text-xs mb-3.5" style="color: var(--color-text-55)">
						Pólizas emitidas, contando solo la aseguradora elegida.
					</p>
					{#if cargando}
						<SkeletonRows count={3} />
					{:else}
						<BarList
							items={porAseguradora}
							emptyText="Aún no hay pólizas emitidas con aseguradora seleccionada."
						/>
					{/if}
				</div>

			</div>
		</div>
	{/if}
</div>
