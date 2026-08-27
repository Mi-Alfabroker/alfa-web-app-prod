<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { Avatar, KpiRow, PageHeader, PillTabs, Tag } from '$components';
	import { ASEGURADORA_GENERALES, ASEGURADORA_RUBROS } from '$constants';
	import { aseguradoraService } from '$services';
	import { valoresConfigurados } from '$utils';
	import type { Aseguradora } from '$lib/types/aseguradora';

	$: aseguradoraId = Number($page.params.id);

	let aseguradora: (Aseguradora & Record<string, unknown>) | null = null;
	let loading = true;
	let error: string | null = null;
	let activeTab: string = ASEGURADORA_RUBROS[0].id;

	$: void load(aseguradoraId);

	async function load(id: number) {
		if (!id) return;
		loading = true;
		error = null;
		try {
			aseguradora = (await aseguradoraService.getById(id)) as Aseguradora & Record<string, unknown>;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Error al cargar la aseguradora';
		} finally {
			loading = false;
		}
	}

	function value(key: string): string {
		const raw = aseguradora?.[key];
		if (raw === null || raw === undefined || raw === '') return '—';
		return String(raw);
	}

	$: activeRubro = ASEGURADORA_RUBROS.find((r) => r.id === activeTab) ?? ASEGURADORA_RUBROS[0];

	$: tabs = ASEGURADORA_RUBROS.map((r) => ({
		id: r.id,
		label: r.label,
		count: aseguradora ? valoresConfigurados(aseguradora, `${r.id}_`) : undefined
	}));

	$: kpis = aseguradora
		? [
				{
					label: 'Condiciones definidas',
					value: String(valoresConfigurados(aseguradora)),
					note: 'en los cuatro rubros'
				},
				...ASEGURADORA_RUBROS.map((r) => ({
					label: r.label,
					value: String(valoresConfigurados(aseguradora as Record<string, unknown>, `${r.id}_`)),
					note: 'condiciones definidas'
				}))
			]
		: [];
</script>

<svelte:head>
	<title>{aseguradora?.nombre ?? 'Aseguradora'} | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader
		title={aseguradora?.nombre ?? 'Aseguradora'}
		crumb="Inicio / Operación / Aseguradoras"
		subtitle={aseguradora?.respaldo_aseguradora
			? `Respaldo: ${aseguradora.respaldo_aseguradora}`
			: 'Condiciones negociadas por rubro'}
		backHref="/aseguradoras"
		backLabel="Volver a aseguradoras"
	>
		<a slot="actions" class="btn-primary !min-h-[38px]" href="/aseguradoras/{aseguradoraId}/editar">
			Editar aseguradora
		</a>
	</PageHeader>

	{#if loading}
		<div class="card flex items-center gap-3">
			<span
				class="block h-4 w-4 rounded-full"
				style="border: 2px solid var(--color-accent-200); border-top-color: var(--color-accent-600); animation: spin .7s linear infinite"
			></span>
			<span style="color: var(--color-text-60)">Cargando ficha…</span>
		</div>
	{:else if error}
		<div
			class="card"
			style="border-color: var(--color-accent-400); background: var(--color-accent-100)"
		>
			<p class="font-medium" style="color: var(--color-accent-900)">
				No fue posible cargar la aseguradora
			</p>
			<p class="text-sm" style="color: var(--color-accent-900)">{error}</p>
		</div>
	{:else if aseguradora}
		<KpiRow {kpis} />

		<div class="card mb-3.5">
			<div class="row-card-head !mb-3.5">
				<Avatar name={aseguradora.nombre} shape="square" strong />
				<span class="row-card-title">{aseguradora.nombre}</span>
				{#if aseguradora.respaldo_aseguradora}
					<Tag variant="neutral">{aseguradora.respaldo_aseguradora}</Tag>
				{/if}
			</div>
			<div class="field-grid">
				{#each ASEGURADORA_GENERALES.filter((f) => f.key !== 'nombre') as field}
					<div>
						<div class="field-label">{field.label}</div>
						<div class="field-value">{value(field.key)}</div>
					</div>
				{/each}
			</div>
		</div>

		<div class="flex flex-col gap-3.5">
			<PillTabs {tabs} bind:active={activeTab} />

			{#each activeRubro.sections as section}
				<div class="card">
					<h3 class="card-heading">{section.title}</h3>
					<div
						class="grid gap-2.5"
						style="grid-template-columns: repeat(auto-fit, minmax(248px, 1fr))"
					>
						{#each section.fields as field}
							<div class="rounded-xl px-3 py-2.5" style="border: 1px solid var(--color-divider)">
								<div class="field-label">{field.label}</div>
								<div class="mt-0.5 text-sm font-medium">{value(field.key)}</div>
							</div>
						{/each}
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
