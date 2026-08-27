<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { authService } from '$lib/services/auth.service';
	import { auth, clearSession, getAccessToken, getAuthUser } from '$lib/stores/auth';
	import { invalidateCatalog } from '$lib/stores/catalog';
	import type { UserRole } from '$lib/types';
	import { Notifications, TopBar } from '$lib/components';
	import { initials, RUBROS } from '$utils';
	import { DOMAIN_ICONS } from '$constants';
	import type { DomainIcon } from '$constants';

	const COLLAPSE_KEY = 'ab_sidebar_collapsed';
	const NARROW_BREAKPOINT = 768;

	// Sidebar state
	let collapsed = false;
	let drawerOpen = false;
	let width = 1280;
	let subOpen = false;
	let userMenuOpen = false;
	let tip: { label: string; top: string; left: string } | null = null;

	/** `d` / `d2` are the two SVG paths of a DOMAIN_ICONS glyph. */
	type NavigationItem = DomainIcon & {
		href: string;
		label: string;
		roles: UserRole[];
		/** Renders the Pólizas rubro submenu underneath. */
		rubros?: boolean;
	};

	type NavigationGroup = {
		label?: string;
		items: NavigationItem[];
	};

	const ALL: UserRole[] = ['AGENTE', 'ADMINISTRADOR', 'SUPERADMIN', 'CLIENTE'];
	const STAFF: UserRole[] = ['AGENTE', 'ADMINISTRADOR', 'SUPERADMIN'];
	const ADMIN: UserRole[] = ['ADMINISTRADOR', 'SUPERADMIN'];

	// Glyphs come from DOMAIN_ICONS so a dashboard action tile and the nav item it
	// leads to always show the same icon.
	const navigationGroups: NavigationGroup[] = [
		{
			items: [
				{ href: '/', label: 'Dashboard', ...DOMAIN_ICONS.dashboard, roles: ALL },
				{ href: '/clientes', label: 'Clientes', ...DOMAIN_ICONS.clientes, roles: STAFF },
				{ href: '/propuestas', label: 'Pólizas', ...DOMAIN_ICONS.polizas, roles: STAFF, rubros: true },
				{ href: '/bienes', label: 'Bienes', ...DOMAIN_ICONS.bienes, roles: STAFF },
				{ href: '/aseguradoras', label: 'Aseguradoras', ...DOMAIN_ICONS.aseguradoras, roles: STAFF }
			]
		},
		{
			label: 'Administración',
			items: [{ href: '/reportes', label: 'Reportes', ...DOMAIN_ICONS.reportes, roles: ADMIN }]
		}
	];

	/** Flat list, for the role guard and the fallback path. */
	const navigation: NavigationItem[] = navigationGroups.flatMap((g) => g.items);

	$: isLoginRoute = $page.url.pathname.startsWith('/login');
	$: currentRole = $auth.user?.tipo_usuario;
	$: narrow = width < NARROW_BREAKPOINT;
	// On narrow viewports the sidebar is a full-width drawer, never collapsed.
	$: expanded = narrow ? true : !collapsed;
	$: allowedGroups = currentRole
		? navigationGroups
				.map((g) => ({ ...g, items: g.items.filter((i) => i.roles.includes(currentRole)) }))
				.filter((g) => g.items.length > 0)
		: [];
	$: activeRubro = $page.url.searchParams.get('rubro');
	$: if (!isLoginRoute && $auth.user && !canAccessPath($page.url.pathname, $auth.user.tipo_usuario)) {
		const fallbackPath = getFallbackPath($auth.user.tipo_usuario);
		if ($page.url.pathname !== fallbackPath) {
			void goto(fallbackPath);
		}
	}
	// Close transient shell UI whenever the route changes.
	$: if ($page.url.pathname) {
		drawerOpen = false;
		userMenuOpen = false;
		tip = null;
	}

	onMount(async () => {
		collapsed = localStorage.getItem(COLLAPSE_KEY) === '1';

		if (isLoginRoute) {
			if (getAccessToken()) {
				await goto('/');
			}
			return;
		}

		const token = getAccessToken();
		if (!token) {
			await goto('/login');
			return;
		}

		const storedUser = getAuthUser();
		if (!storedUser) {
			try {
				await authService.me();
			} catch {
				clearSession();
				await goto('/login');
			}
		}
	});

	function isActive(href: string, currentPath: string): boolean {
		if (href === '/') return currentPath === '/';
		return currentPath.startsWith(href);
	}

	function canAccessPath(pathname: string, role: UserRole): boolean {
		const [basePath] = pathname.split('/').filter(Boolean);
		const normalizedPath = basePath ? `/${basePath}` : '/';
		const navItem = navigation.find((item) => item.href === normalizedPath);

		// Keep unknown routes accessible; route files can implement additional guards.
		if (!navItem) return true;
		return navItem.roles.includes(role);
	}

	function getFallbackPath(role: UserRole): string {
		const firstAllowedItem = navigation.find((item) => item.roles.includes(role));
		return firstAllowedItem?.href ?? '/login';
	}

	function toggleSidebar() {
		collapsed = !collapsed;
		userMenuOpen = false;
		tip = null;
		localStorage.setItem(COLLAPSE_KEY, collapsed ? '1' : '0');
	}

	/** Expanding a submenu needs labels, so a collapsed rail expands first. */
	function togglePolizas(event: MouseEvent) {
		if (!narrow && collapsed) {
			event.preventDefault();
			collapsed = false;
			localStorage.setItem(COLLAPSE_KEY, '0');
			subOpen = true;
			tip = null;
			return;
		}
		subOpen = !subOpen;
	}

	function showTip(event: MouseEvent, label: string) {
		if (narrow || !collapsed) return;
		const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
		tip = {
			label,
			top: rect.top + rect.height / 2 + 'px',
			left: rect.right + 12 + 'px'
		};
	}

	async function logout() {
		clearSession();
		invalidateCatalog();
		await goto('/login');
	}

	$: userLabel = $auth.user
		? $auth.user.nombre || $auth.user.razon_social || $auth.user.usuario
		: '';
</script>

<svelte:window bind:innerWidth={width} />

{#if isLoginRoute}
	<slot />
{:else}
	<div class="flex min-h-screen items-stretch">
		{#if narrow && drawerOpen}
			<div
				class="fixed inset-0 z-[35]"
				style="background: color-mix(in srgb, #1d1f20 45%, transparent)"
				role="presentation"
				on:click={() => (drawerOpen = false)}
			></div>
		{/if}

		<aside
			class="sidebar {expanded ? 'sidebar-expanded' : 'sidebar-collapsed'}"
			class:fixed={narrow}
			class:sticky={!narrow}
			style="top: 0; height: 100vh; z-index: 40; {narrow
				? `left: ${drawerOpen ? '0' : '-272px'}`
				: ''}"
		>
			<!-- 64px, matching the topbar so the two align across the divider. -->
			<div class="sidebar-header" class:justify-center={!expanded}>
				<div class="sidebar-logo">AB</div>
				{#if expanded}
					<div class="min-w-0 flex-1">
						<div class="sidebar-logo-text">Alfabroker</div>
						<div class="sidebar-logo-sub">Gestión de pólizas</div>
					</div>
					<button
						type="button"
						class="btn-secondary btn-icon !w-[30px] !h-[30px]"
						title={narrow ? 'Cerrar menú' : 'Colapsar menú'}
						aria-label={narrow ? 'Cerrar menú' : 'Colapsar menú'}
						on:click={narrow ? () => (drawerOpen = false) : toggleSidebar}
					>
						{#if narrow}
							<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
								<path d="M6 6l12 12M18 6 6 18" />
							</svg>
						{:else}
							<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
								<path d="M15 6l-6 6 6 6" />
							</svg>
						{/if}
					</button>
				{/if}
			</div>

			<nav class="sidebar-nav">
				<!-- Collapsed, the header has no room for the toggle beside the logo,
				     so it takes the rail's own icon-row idiom (tooltip included). -->
				{#if !expanded}
					<button
						type="button"
						class="sidebar-item"
						title="Expandir menú"
						aria-label="Expandir menú"
						on:click={toggleSidebar}
						on:mouseenter={(e) => showTip(e, 'Expandir menú')}
						on:mouseleave={() => (tip = null)}
					>
						<span class="sidebar-item-bar"></span>
						<svg
							class="sidebar-item-icon"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="1.5"
							style="transform: rotate(180deg)"
						>
							<path d="M15 6l-6 6 6 6" />
						</svg>
					</button>
				{/if}

				{#each allowedGroups as group}
					{#if group.label}
						<div class="sidebar-group-label" style="opacity: {expanded ? 1 : 0}">{group.label}</div>
					{/if}

					{#each group.items as item}
						<a
							href={item.href}
							class="sidebar-item {isActive(item.href, $page.url.pathname) ? 'sidebar-item-active' : ''}"
							on:mouseenter={(e) => showTip(e, item.label)}
							on:mouseleave={() => (tip = null)}
							on:click={item.rubros ? togglePolizas : undefined}
						>
							<span class="sidebar-item-bar"></span>
							<svg
								class="sidebar-item-icon"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.5"
							>
								<path d={item.d} />
								<path d={item.d2} />
							</svg>
							<span class="sidebar-item-label" style="opacity: {expanded ? 1 : 0}">{item.label}</span>
							{#if item.rubros && expanded}
								<svg
									class="flex-none"
									width="15"
									height="15"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="1.5"
									style="transform: rotate({subOpen ? 0 : -90}deg)"
								>
									<path d="M6 9l6 6 6-6" />
								</svg>
							{/if}
						</a>

						{#if item.rubros && subOpen && expanded}
							<div class="sidebar-submenu">
								{#each RUBROS as rubro}
									<a
										href="/propuestas?rubro={rubro.slug}"
										class="sidebar-subitem {isActive('/propuestas', $page.url.pathname) &&
										activeRubro === rubro.slug
											? 'sidebar-subitem-active'
											: ''}"
									>
										{rubro.label}
									</a>
								{/each}
							</div>
						{/if}
					{/each}
				{/each}
			</nav>

			<div class="sidebar-footer">
				{#if userMenuOpen}
					<div
						class="fixed inset-0 z-[55]"
						role="presentation"
						on:click={() => (userMenuOpen = false)}
					></div>
					<div
						class="absolute left-2.5 right-2.5 bottom-[calc(100%-2px)] z-[60] flex flex-col p-1.5"
						style="background: var(--color-bg); border: 1px solid var(--color-divider); border-radius: var(--radius-lg); box-shadow: var(--shadow-md)"
					>
						<div class="px-2.5 py-2 text-xs" style="color: var(--color-text-55)">
							{$auth.user?.usuario ?? ''}
						</div>
						<div class="menu-divider"></div>
						<button type="button" class="menu-item menu-item-danger" on:click={logout}>
							Cerrar sesión
						</button>
					</div>
				{/if}

				<button
					type="button"
					class="flex w-full items-center gap-2.5 rounded-xl p-1.5 text-left transition-colors hover:bg-[var(--color-accent-100)]"
					aria-expanded={userMenuOpen}
					on:click={() => (userMenuOpen = !userMenuOpen)}
				>
					<span class="avatar avatar-circle">{initials(userLabel)}</span>
					<span class="flex-1 min-w-0 block" style="opacity: {expanded ? 1 : 0}">
						<span class="block text-sm font-medium overflow-hidden text-ellipsis whitespace-nowrap">
							{userLabel}
						</span>
						<span class="block text-xs" style="color: var(--color-text-55)">
							{$auth.user?.tipo_usuario ?? ''}
						</span>
					</span>
				</button>
			</div>
		</aside>

		<main class="flex-1 min-w-0 flex flex-col">
			<TopBar {narrow} onOpenDrawer={() => (drawerOpen = true)} />
			<slot />
		</main>
	</div>

	{#if tip}
		<div class="sidebar-tip" style="top: {tip.top}; left: {tip.left}">{tip.label}</div>
	{/if}

	<Notifications />
{/if}
