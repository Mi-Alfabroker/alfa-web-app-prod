<script lang="ts">
	/**
	 * TopBar - sticky application header: drawer toggle on narrow viewports,
	 * global search over clientes and pólizas, and the environment tag.
	 *
	 * @prop narrow - viewport is below the drawer breakpoint
	 * @prop ambiente - environment label shown on the right
	 */
	import { goto } from '$app/navigation';
	import { catalog, loadCatalog } from '$lib/stores/catalog';
	import { buildPolizaRows, clienteDocumento, clienteNombre, initials } from '$utils';
	import { debounce } from '$utils/timing';
	import Avatar from './Avatar.svelte';

	export let narrow: boolean = false;
	export let ambiente: string = '';
	/** Opens the navigation drawer; only reachable on narrow viewports. */
	export let onOpenDrawer: () => void = () => {};

	const MIN_QUERY = 2;
	const MAX_PER_GROUP = 4;

	let query = '';
	let debounced = '';
	let open = false;

	const setDebounced = debounce((value: string) => {
		debounced = value;
	}, 200);

	function onInput(event: Event) {
		query = (event.target as HTMLInputElement).value;
		open = true;
		setDebounced(query.trim().toLowerCase());
		// The catalog backs the search; load it on the first real keystroke
		// rather than on app boot.
		if (query.trim().length >= MIN_QUERY) void loadCatalog();
	}

	type Result = {
		lead: string;
		titulo: string;
		sub: string;
		tipo: string;
		shape: 'circle' | 'square';
		href: string;
	};

	$: results = ((): Result[] => {
		const q = debounced;
		if (q.length < MIN_QUERY) return [];

		const clientes: Result[] = $catalog.clientes
			.filter((c) => {
				const nombre = clienteNombre(c).toLowerCase();
				const doc = clienteDocumento(c).toLowerCase();
				return nombre.includes(q) || doc.includes(q) || (c.correo ?? '').toLowerCase().includes(q);
			})
			.slice(0, MAX_PER_GROUP)
			.map((c) => ({
				lead: initials(clienteNombre(c)),
				titulo: clienteNombre(c),
				sub: [clienteDocumento(c), c.ciudad].filter(Boolean).join(' · '),
				tipo: 'Cliente',
				shape: 'circle' as const,
				href: `/clientes/${c.id}`
			}));

		const polizas: Result[] = buildPolizaRows($catalog)
			.filter(
				(p) =>
					p.consecutivo.toLowerCase().includes(q) ||
					p.clienteNombre.toLowerCase().includes(q) ||
					p.documento.toLowerCase().includes(q)
			)
			.slice(0, MAX_PER_GROUP + 1)
			.map((p) => ({
				lead: p.sigla,
				titulo: p.consecutivo,
				sub: [p.clienteNombre, p.documento].filter((s) => s && s !== '—').join(' · '),
				tipo: 'Póliza',
				shape: 'square' as const,
				href: p.href
			}));

		return [...clientes, ...polizas];
	})();

	$: showPanel = open && query.trim().length >= MIN_QUERY;

	async function pick(href: string) {
		open = false;
		query = '';
		debounced = '';
		await goto(href);
	}

	function onKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			open = false;
		}
	}
</script>

<header class="topbar">
	{#if narrow}
		<button
			type="button"
			class="btn-secondary btn-icon"
			aria-label="Abrir menú"
			on:click={onOpenDrawer}
		>
			<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
				<path d="M4 7h16M4 12h16M4 17h16" />
			</svg>
		</button>
	{/if}

	<div class="relative flex-1 min-w-0 max-w-[460px]">
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
			class="input !pl-9 !min-h-[38px]"
			type="search"
			value={query}
			placeholder="Buscar cliente, documento o póliza…"
			aria-label="Búsqueda global"
			on:input={onInput}
			on:focus={() => (open = true)}
			on:keydown={onKeydown}
		/>

		{#if showPanel}
			<!-- Click-away catcher, below the panel. -->
			<div class="fixed inset-0 z-[65]" role="presentation" on:click={() => (open = false)}></div>
			<div
				class="absolute left-0 right-0 top-[calc(100%+6px)] z-[70] max-h-[340px] overflow-y-auto p-1.5"
				style="background: var(--color-bg); border: 1px solid var(--color-divider); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg)"
			>
				{#if $catalog.loading && !results.length}
					<div class="px-3 py-3.5 text-sm" style="color: var(--color-text-55)">Buscando…</div>
				{:else if results.length}
					{#each results as r}
						<button
							type="button"
							class="menu-item w-full"
							on:click={() => pick(r.href)}
						>
							<Avatar text={r.lead} shape={r.shape} />
							<span class="flex-1 min-w-0 block text-left">
								<span class="block text-sm font-medium">{r.titulo}</span>
								<span
									class="block text-xs overflow-hidden text-ellipsis whitespace-nowrap"
									style="color: var(--color-text-55)">{r.sub}</span
								>
							</span>
							<span class="tag tag-neutral flex-none !text-[10.5px]">{r.tipo}</span>
						</button>
					{/each}
				{:else}
					<div class="px-3 py-3.5 text-sm" style="color: var(--color-text-55)">
						Sin coincidencias por nombre, documento o número de póliza.
					</div>
				{/if}
			</div>
		{/if}
	</div>

	<div class="flex-1"></div>

	{#if ambiente}
		<span class="tag tag-neutral whitespace-nowrap">{ambiente}</span>
	{/if}
</header>
