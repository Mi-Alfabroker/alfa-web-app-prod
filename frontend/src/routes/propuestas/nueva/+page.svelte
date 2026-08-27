<script lang="ts">
	/**
	 * Rubro chooser for a new propuesta.
	 *
	 * This route used to hold a generic "Nueva Propuesta" form with invented
	 * fields (título, tipoSeguro, primaTotal…) that only wrote to local state and
	 * never reached the API. The real creation flow is per rubro, at
	 * /propuestas/nueva/[tipo], because the insured values differ by rubro — so
	 * this page now just routes the user into the right one.
	 */
	import { APP_NAME } from '$lib/config';
	import { Avatar, PageHeader } from '$components';
	import { RUBROS } from '$utils';
</script>

<svelte:head>
	<title>Nueva propuesta | {APP_NAME}</title>
</svelte:head>

<div class="page-shell">
	<PageHeader
		title="Nueva propuesta"
		crumb="Inicio / Operación / Pólizas"
		subtitle="Elige el rubro del bien que vas a cotizar"
		backHref="/propuestas"
		backLabel="Volver a pólizas"
	/>

	<div class="grid gap-3" style="grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))">
		{#each RUBROS as rubro}
			<a
				href="/propuestas/nueva/{rubro.slug}"
				class="card !p-4 flex items-center gap-3 transition-colors hover:border-[var(--color-accent-400)]"
				style="color: inherit"
			>
				<Avatar text={rubro.sigla} shape="square" />
				<span class="block">
					<span class="block font-medium">{rubro.label}</span>
					<span class="block text-xs" style="color: var(--color-text-55)">
						Selecciona el bien y registra hasta cinco cotizaciones
					</span>
				</span>
			</a>
		{/each}
	</div>
</div>
