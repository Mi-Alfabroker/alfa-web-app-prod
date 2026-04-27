<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, CurrencyInput } from '$components';
	import { bienService, clienteService } from '$services';
	import { OtroBienFields } from '$constants';
	import type { Cliente } from '$lib/types/cliente';
	import type { OtroBien, UpdateOtroBienDto } from '$lib/types/bien';

	const id = Number($page.params.id);

	let otroBien: OtroBien | null = null;
	let cliente: Cliente | null = null;
	let formData: UpdateOtroBienDto = {};
	let loading = true;
	let saving = false;
	let error: string | null = null;

	let sections = {
		cliente: { open: true },
		datos: { open: true }
	};

	onMount(async () => {
		try {
			otroBien = await bienService.otros.getById(id);
			if (otroBien) {
				formData = {
					tipo_seguro: otroBien.tipo_seguro || '',
					bien_asegurado: otroBien.bien_asegurado || '',
					valor_bien_asegurar: otroBien.valor_bien_asegurar || undefined,
					detalles_bien_asegurado: otroBien.detalles_bien_asegurado || ''
				};
				const clientes = await clienteService.getAll();
				cliente = clientes.find(c => c.id === otroBien?.id_usuario) || null;
			}
		} catch (err) {
			console.error('Error loading otro bien:', err);
			error = 'Error al cargar el bien';
		} finally {
			loading = false;
		}
	});

	async function handleSubmit() {
		saving = true;
		error = null;
		try {
			await bienService.otros.update(id, formData);
			goto('/bienes');
		} catch (err: unknown) {
			console.error('Error updating otro bien:', err);
			error = err instanceof Error ? err.message : 'Error al actualizar';
		} finally {
			saving = false;
		}
	}

	function getClienteName(): string {
		if (!cliente) return 'Cliente no encontrado';
		return cliente.tipo_persona === 'PERSONA' ? cliente.nombre || 'Sin nombre' : cliente.razon_social || 'Sin razón social';
	}
</script>

<svelte:head>
	<title>Editar Bien | {APP_NAME}</title>
</svelte:head>

<header class="page-header">
	<div class="flex items-center gap-4">
		<a href="/bienes" class="page-back-link">
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
			</svg>
			<span>Volver</span>
		</a>
	</div>
</header>

<div class="page-content">
	<div class="max-w-4xl mx-auto">
		{#if loading}
			<div class="flex items-center justify-center py-12">
				<svg class="animate-spin h-8 w-8 text-primary-500" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
				</svg>
			</div>
		{:else if !otroBien}
			<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
				<p class="font-medium">Bien no encontrado</p>
			</div>
		{:else}
			<form class="form-container" on:submit|preventDefault={handleSubmit}>
				<h1 class="form-title">Editar Bien #{id}</h1>

				{#if error}
					<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
						<span>{error}</span>
					</div>
				{/if}

				<FormSection title="Cliente" bind:open={sections.cliente.open}>
					<div class="bg-secondary-50 rounded-lg p-4">
						<p class="text-sm text-secondary-500">Propietario</p>
						<p class="font-medium text-secondary-900">{getClienteName()}</p>
					</div>
				</FormSection>

				<FormSection title="Datos del Bien" bind:open={sections.datos.open}>
					<div class="space-y-4">
						<FormField label={OtroBienFields.tipo_seguro.label}>
							<Input bind:value={formData.tipo_seguro} disabled={saving} />
						</FormField>
						<FormField label={OtroBienFields.bien_asegurado.label}>
							<Input bind:value={formData.bien_asegurado} disabled={saving} />
						</FormField>
						<FormField label={OtroBienFields.valor_bien_asegurar.label}>
							<CurrencyInput bind:value={formData.valor_bien_asegurar} disabled={saving} />
						</FormField>
						<FormField label={OtroBienFields.detalles_bien_asegurado.label}>
							<textarea
								bind:value={formData.detalles_bien_asegurado}
								class="input min-h-[100px]"
								disabled={saving}
							></textarea>
						</FormField>
					</div>
				</FormSection>

				<div class="form-actions">
					<a href="/bienes" class="btn btn-secondary">Cancelar</a>
					<button type="submit" class="btn btn-primary" disabled={saving}>
						{saving ? 'Guardando...' : 'Guardar Cambios'}
					</button>
				</div>
			</form>
		{/if}
	</div>
</div>
