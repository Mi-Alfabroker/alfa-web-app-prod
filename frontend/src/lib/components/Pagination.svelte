<script lang="ts">
	/**
	 * Pagination - range text plus prev / numbered pages / next.
	 *
	 * @prop total - total rows across all pages
	 * @prop perPage - rows per page
	 * @prop page - current 1-based page (bound)
	 * @prop noun - plural noun for the range text
	 */
	export let total: number = 0;
	export let perPage: number = 10;
	export let page: number = 1;
	export let noun: string = 'registros';

	$: pages = Math.max(1, Math.ceil(total / perPage));
	$: current = Math.min(Math.max(1, page), pages);
	$: start = (current - 1) * perPage;
	$: shown = Math.min(perPage, total - start);
	$: rangeText = `Mostrando ${total ? start + 1 : 0}–${start + Math.max(0, shown)} de ${total} ${noun}`;

	function go(n: number) {
		page = Math.min(pages, Math.max(1, n));
	}
</script>

{#if total > perPage}
	<div class="flex flex-wrap items-center gap-3.5 px-0.5 py-1">
		<span class="text-xs" style="color: var(--color-text-60)">{rangeText}</span>

		<div class="ml-auto flex items-center gap-1.5">
			<button
				type="button"
				class="btn-secondary btn-icon !w-8 !h-8"
				disabled={current <= 1}
				aria-label="Página anterior"
				on:click={() => go(current - 1)}
			>
				<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
					<path d="M15 6l-6 6 6 6" />
				</svg>
			</button>

			{#each Array(pages) as _, i}
				<button
					type="button"
					class="min-w-8 h-8 rounded-lg text-sm font-medium transition-colors"
					style={i + 1 === current
						? 'background: var(--color-accent); color: var(--color-accent-ink); border: 1px solid var(--color-accent)'
						: 'background: var(--color-bg); border: 1px solid var(--color-divider)'}
					aria-current={i + 1 === current ? 'page' : undefined}
					on:click={() => go(i + 1)}
				>
					{i + 1}
				</button>
			{/each}

			<button
				type="button"
				class="btn-secondary btn-icon !w-8 !h-8"
				disabled={current >= pages}
				aria-label="Página siguiente"
				on:click={() => go(current + 1)}
			>
				<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
					<path d="M9 6l6 6-6 6" />
				</svg>
			</button>
		</div>
	</div>
{/if}
