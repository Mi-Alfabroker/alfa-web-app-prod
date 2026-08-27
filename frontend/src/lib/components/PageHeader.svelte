<script lang="ts">
	/**
	 * PageHeader - the design's in-content page header: optional back link,
	 * breadcrumb, title, subtitle, and right-aligned actions.
	 *
	 * Replaces the 64px `.page-header` bar that every route used to hand-roll.
	 *
	 * @prop title - page title
	 * @prop subtitle - one-line description under the title
	 * @prop crumb - breadcrumb text, e.g. "Inicio / Operación"
	 * @prop backHref - when set, renders a back link above the breadcrumb
	 * @prop backLabel - back link text
	 * @slot actions - buttons aligned to the right edge
	 */
	export let title: string;
	export let subtitle: string = '';
	export let crumb: string = '';
	export let backHref: string = '';
	export let backLabel: string = 'Volver';
</script>

<div class="page-header-block">
	<div class="min-w-0">
		{#if backHref}
			<a href={backHref} class="btn-ghost mb-1 !px-1.5 !py-0.5 text-[13px]">
				<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
					<path d="M15 6l-6 6 6 6" />
				</svg>
				{backLabel}
			</a>
		{/if}
		{#if crumb}
			<div class="page-crumb">{crumb}</div>
		{/if}
		<h1 class="page-header-title">{title}</h1>
		{#if subtitle}
			<p class="page-subtitle">{subtitle}</p>
		{/if}
	</div>

	<div class="flex gap-2 flex-wrap">
		<slot name="actions" />
	</div>
</div>
