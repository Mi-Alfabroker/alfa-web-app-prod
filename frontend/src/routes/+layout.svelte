<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { authService } from '$lib/services/auth.service';
	import { auth, clearSession, getAccessToken, getAuthUser } from '$lib/stores/auth';
	import type { UserRole } from '$lib/types';
	import { Notifications } from '$lib/components';

	// Sidebar state
	let collapsed = false;

	type NavigationItem = {
		href: string;
		label: string;
		icon: string;
		roles: UserRole[];
	};

	const navigation: NavigationItem[] = [
		{ 
			href: '/', 
			label: 'Dashboard', 
			icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
			roles: ['AGENTE', 'ADMINISTRADOR', 'SUPERADMIN', 'CLIENTE']
		},
		{ 
			href: '/aseguradoras', 
			label: 'Aseguradoras', 
			icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
			roles: ['AGENTE', 'ADMINISTRADOR', 'SUPERADMIN']
		},
		{ 
			href: '/clientes', 
			label: 'Clientes', 
			icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
			roles: ['AGENTE', 'ADMINISTRADOR', 'SUPERADMIN']
		},
		{ 
			href: '/bienes', 
			label: 'Bienes', 
			icon: 'M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12',
			roles: ['AGENTE', 'ADMINISTRADOR', 'SUPERADMIN']
		},
		{ 
			href: '/propuestas', 
			label: 'Pólizas', 
			icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
			roles: ['AGENTE', 'ADMINISTRADOR', 'SUPERADMIN']
		},
		{ 
			href: '/reportes', 
			label: 'Reportes', 
			icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
			roles: ['ADMINISTRADOR', 'SUPERADMIN']
		}
	];

	$: isLoginRoute = $page.url.pathname.startsWith('/login');
	$: currentRole = $auth.user?.tipo_usuario;
	$: allowedNavigation = currentRole ? navigation.filter((item) => item.roles.includes(currentRole)) : [];
	$: if (!isLoginRoute && $auth.user && !canAccessPath($page.url.pathname, $auth.user.tipo_usuario)) {
		const fallbackPath = getFallbackPath($auth.user.tipo_usuario);
		if ($page.url.pathname !== fallbackPath) {
			void goto(fallbackPath);
		}
	}

	onMount(async () => {
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
	}

	async function logout() {
		clearSession();
		await goto('/login');
	}
</script>

{#if isLoginRoute}
	<slot />
{:else}
<div class="min-h-screen flex bg-secondary-100">
	<!-- Sidebar -->
	<aside 
		class="sidebar {collapsed ? 'sidebar-collapsed' : 'sidebar-expanded'}"
	>
		<!-- Logo -->
		<div class="sidebar-header">
			<div class="sidebar-logo">
				<svg class="w-6 h-6 text-primary-950" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
				</svg>
			</div>
			{#if !collapsed}
				<span class="sidebar-logo-text">{APP_NAME}</span>
			{/if}
		</div>

		<!-- Navigation -->
		<nav class="sidebar-nav">
			<ul class="space-y-1">
				{#each allowedNavigation as item}
					<li>
						<a
							href={item.href}
							class="sidebar-item {isActive(item.href, $page.url.pathname) ? 'sidebar-item-active' : ''}"
							title={collapsed ? item.label : ''}
						>
							<svg class="sidebar-item-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d={item.icon} />
							</svg>
							{#if !collapsed}
								<span class="sidebar-item-label">{item.label}</span>
							{/if}
						</a>
					</li>
				{/each}
			</ul>
		</nav>

		<!-- Footer with Settings -->
		<div class="sidebar-footer">
			{#if $auth.user}
				<div class="px-3 py-2 mb-2 text-xs text-secondary-500">
					<div class="font-medium text-secondary-700">{$auth.user.usuario}</div>
					<div>{$auth.user.tipo_usuario}</div>
				</div>
			{/if}

			<button
				class="sidebar-item"
				on:click={logout}
				title={collapsed ? 'Cerrar sesión' : ''}
			>
				<svg class="sidebar-item-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6A2.25 2.25 0 005.25 5.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
				</svg>
				{#if !collapsed}
					<span class="sidebar-item-label">Cerrar sesión</span>
				{/if}
			</button>

			<button
				class="sidebar-item"
				on:click={toggleSidebar}
				title={collapsed ? 'Expandir' : 'Colapsar'}
			>
				<svg 
					class="sidebar-item-icon transition-transform duration-200 {collapsed ? 'rotate-180' : ''}" 
					fill="none" 
					viewBox="0 0 24 24" 
					stroke="currentColor" 
					stroke-width="1.5"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
				</svg>
				{#if !collapsed}
					<span class="sidebar-item-label">Colapsar</span>
				{/if}
			</button>
		</div>
	</aside>

	<!-- Main Content -->
	<main class="flex-1 flex flex-col min-w-0 overflow-auto">
		<slot />
	</main>
</div>
<Notifications />
{/if}
