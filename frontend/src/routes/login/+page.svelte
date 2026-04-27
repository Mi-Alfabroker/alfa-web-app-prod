<script lang="ts">
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { authService } from '$lib/services/auth.service';

	let usuario = '';
	let clave = '';
	let isSubmitting = false;
	let errorMessage = '';

	async function onSubmit(event: SubmitEvent) {
		event.preventDefault();
		errorMessage = '';
		isSubmitting = true;

		try {
			await authService.login(usuario, clave);
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

<div class="min-h-screen bg-secondary-100 flex items-center justify-center p-6">
	<div class="w-full max-w-md card">
		<div class="mb-6 text-center">
			<h1 class="text-2xl font-semibold text-secondary-900">{APP_NAME}</h1>
			<p class="text-secondary-500 mt-1">Inicia sesión para continuar</p>
		</div>

		<form class="space-y-4" on:submit={onSubmit}>
			<div>
				<label class="form-label mb-1 block" for="usuario">Usuario</label>
				<input id="usuario" class="input" bind:value={usuario} autocomplete="username" required />
			</div>

			<div>
				<label class="form-label mb-1 block" for="clave">Contraseña</label>
				<input
					id="clave"
					type="password"
					class="input"
					bind:value={clave}
					autocomplete="current-password"
					required
				/>
			</div>

			{#if errorMessage}
				<p class="input-error-text">{errorMessage}</p>
			{/if}

			<button class="btn btn-primary w-full" disabled={isSubmitting}>
				{isSubmitting ? 'Ingresando...' : 'Ingresar'}
			</button>
		</form>
	</div>
</div>
