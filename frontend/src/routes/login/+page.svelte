<script lang="ts">
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { authService } from '$lib/services/auth.service';
	import { RUBROS } from '$utils';

	let usuario = '';
	let clave = '';
	let showPass = false;
	let remember = true;
	let isSubmitting = false;
	let errorMessage = '';

	const REMEMBER_KEY = 'ab_login_usuario';

	// Prefill only the username; the password is never persisted.
	if (typeof localStorage !== 'undefined') {
		const saved = localStorage.getItem(REMEMBER_KEY);
		if (saved) {
			usuario = saved;
		} else {
			remember = false;
		}
	}

	async function onSubmit(event: SubmitEvent) {
		event.preventDefault();
		errorMessage = '';
		isSubmitting = true;

		try {
			await authService.login(usuario, clave);
			if (remember) {
				localStorage.setItem(REMEMBER_KEY, usuario);
			} else {
				localStorage.removeItem(REMEMBER_KEY);
			}
			await goto('/');
		} catch (error) {
			errorMessage = (error as { message?: string })?.message || 'No fue posible iniciar sesión';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<svelte:head>
	<title>Iniciar sesión | {APP_NAME}</title>
</svelte:head>

<div class="login">
	<!-- Brand panel: a full column on wide viewports, a header band on narrow. -->
	<div class="login-brand">
		<div class="flex items-center gap-3">
			<div class="login-brand-mark">AB</div>
			<div>
				<div class="login-brand-name">Alfabroker</div>
				<div class="text-xs opacity-70 mt-0.5">Gestión de pólizas</div>
			</div>
		</div>

		<div class="login-brand-pitch">
			<h2 class="login-brand-headline">Cada póliza, bajo control.</h2>
			<p class="text-[15px] opacity-75 max-w-[38ch] m-0">
				Clientes, pólizas, propuestas y aseguradoras de Hogar, Vehículos, Copropiedades y otros
				ramos en un solo lugar.
			</p>
		</div>

		<div class="login-brand-tiles">
			{#each RUBROS as rubro}
				<div class="login-brand-tile">
					<div class="login-brand-tile-sigla">{rubro.sigla}</div>
					<div class="text-xs opacity-70">{rubro.label}</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Form panel -->
	<div class="grid place-items-center flex-1 px-6 py-10">
		<div class="w-full max-w-[390px]">
			<h1 class="text-4xl mb-1.5">Iniciar sesión</h1>
			<p class="text-sm mb-6" style="color: var(--color-text-60)">
				Usa las credenciales corporativas asignadas por el administrador.
			</p>

			{#if errorMessage}
				<div class="login-alert" role="alert">
					<svg
						width="17"
						height="17"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="1.5"
						class="flex-none mt-px"
						style="color: var(--color-accent-800)"
					>
						<circle cx="12" cy="12" r="9" />
						<path d="M12 8v4M12 16h.01" />
					</svg>
					<div class="text-[13px] leading-relaxed" style="color: var(--color-accent-900)">
						{errorMessage}
					</div>
				</div>
			{/if}

			<form class="flex flex-col gap-3.5" on:submit={onSubmit}>
				<div>
					<label class="mb-1.5 block text-[13px] font-medium" for="usuario">Usuario</label>
					<input
						id="usuario"
						class="input !min-h-[42px]"
						bind:value={usuario}
						autocomplete="username"
						required
					/>
				</div>

				<div>
					<label class="mb-1.5 block text-[13px] font-medium" for="clave">Contraseña</label>
					<div class="relative">
						<!-- `type` is dynamic, so this cannot use bind:value (Svelte forbids
						     the combination). Toggling the attribute keeps the same DOM node,
						     so focus and caret survive the reveal. -->
						<input
							id="clave"
							type={showPass ? 'text' : 'password'}
							class="input !min-h-[42px] !pr-11"
							value={clave}
							on:input={(e) => (clave = e.currentTarget.value)}
							autocomplete="current-password"
							required
						/>
						<button
							type="button"
							class="absolute right-0.5 top-0.5 bottom-0.5 w-10 grid place-items-center rounded-lg border-0 bg-transparent"
							style="color: var(--color-text-60)"
							title={showPass ? 'Ocultar contraseña' : 'Mostrar contraseña'}
							aria-label={showPass ? 'Ocultar contraseña' : 'Mostrar contraseña'}
							on:click={() => (showPass = !showPass)}
						>
							{#if showPass}
								<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
									<path d="M3 3l18 18M10.6 10.6a2 2 0 0 0 2.8 2.8" />
									<path d="M6.7 6.8C4.6 8.2 3 10.4 2 12c1.7 3 5.3 6 10 6 1.7 0 3.2-.4 4.6-1.1" />
									<path d="M9.9 5.2A9.9 9.9 0 0 1 12 5c4.7 0 8.3 3 10 7-.6 1-1.5 2.2-2.6 3.2" />
								</svg>
							{:else}
								<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
									<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z" />
									<circle cx="12" cy="12" r="2.6" />
								</svg>
							{/if}
						</button>
					</div>
				</div>

				<label class="flex items-center gap-2 text-[13.5px] cursor-pointer">
					<input
						type="checkbox"
						class="checkbox"
						bind:checked={remember}
						style="accent-color: var(--color-accent-600)"
					/>
					Recordar mi usuario
				</label>

				<button class="btn-primary btn-block !min-h-[44px] !text-[15px] mt-1" disabled={isSubmitting}>
					{#if isSubmitting}
						<span class="login-spinner"></span>
						Verificando…
					{:else}
						Ingresar
					{/if}
				</button>
			</form>
		</div>
	</div>
</div>

<style>
	.login {
		min-height: 100vh;
		display: flex;
		flex-direction: row;
		background: var(--color-bg);
	}

	.login-brand {
		flex: 0 0 46%;
		padding: 44px 40px;
		background: linear-gradient(160deg, var(--color-accent-800), var(--color-accent-900));
		color: #f2f2f3;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 30px;
		border-radius: 0 28px 28px 0;
	}

	.login-brand-mark {
		width: 44px;
		height: 44px;
		border-radius: 12px;
		display: grid;
		place-items: center;
		background: color-mix(in srgb, #f2f2f3 16%, transparent);
		font-family: var(--font-heading);
		font-size: 19px;
		flex: none;
	}

	.login-brand-name {
		font-family: var(--font-heading);
		font-size: 24px;
		line-height: 1;
	}

	.login-brand-headline {
		font-size: 40px;
		line-height: 1.05;
		max-width: 15ch;
		margin: 0 0 14px;
	}

	.login-brand-tiles {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 12px;
	}

	.login-brand-tile {
		background: color-mix(in srgb, #f2f2f3 12%, transparent);
		border-radius: 12px;
		padding: 14px 16px;
	}

	.login-brand-tile-sigla {
		font-family: var(--font-heading);
		font-size: 26px;
		line-height: 1;
	}

	.login-alert {
		display: flex;
		gap: 9px;
		align-items: flex-start;
		border: 1px solid var(--color-accent-400);
		border-radius: 10px;
		padding: 10px 12px;
		margin-bottom: 16px;
		background: var(--color-accent-100);
	}

	.login-spinner {
		width: 15px;
		height: 15px;
		border: 2px solid color-mix(in srgb, var(--color-accent-ink) 30%, transparent);
		border-top-color: var(--color-accent-ink);
		border-radius: 50%;
		display: block;
		animation: spin 0.7s linear infinite;
	}

	/* Narrow: the brand column becomes a compact header band and the pitch and
	   tiles drop away, exactly as the design specifies. */
	@media (max-width: 767px) {
		.login {
			flex-direction: column;
		}

		.login-brand {
			flex: none;
			padding: 20px;
			border-radius: 0;
		}

		.login-brand-pitch,
		.login-brand-tiles {
			display: none;
		}
	}
</style>
