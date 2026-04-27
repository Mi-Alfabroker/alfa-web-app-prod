<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select, CurrencyInput } from '$components';
	import { bienService, clienteService } from '$services';
	import { HogarFields } from '$constants';
	import type { Cliente } from '$lib/types/cliente';
	import type { Hogar, UpdateHogarDto } from '$lib/types/bien';
	import { TIPOS_INMUEBLE } from '$lib/types/bien';

	const id = Number($page.params.id);

	// Data
	let hogar: Hogar | null = null;
	let cliente: Cliente | null = null;

	// Form state
	let formData: UpdateHogarDto = {};
	let loading = true;
	let saving = false;
	let error: string | null = null;

	// Section states
	let sections = {
		cliente: { open: true },
		datos: { open: true },
		valores: { open: true }
	};

	// Options
	const tipoInmuebleOptions = TIPOS_INMUEBLE.map(t => ({ value: t.value, label: t.label }));

	onMount(async () => {
		try {
			hogar = await bienService.hogares.getById(id);
			if (hogar) {
				formData = {
					tipo_inmueble: hogar.tipo_inmueble || '',
					ciudad_inmueble: hogar.ciudad_inmueble || '',
					direccion_inmueble: hogar.direccion_inmueble || '',
					numero_pisos: hogar.numero_pisos || undefined,
					ano_construccion: hogar.ano_construccion || undefined,
					valor_inmueble_avaluo: hogar.valor_inmueble_avaluo || undefined,
					valor_contenidos_normales_avaluo: hogar.valor_contenidos_normales_avaluo || undefined,
					valor_contenidos_especiales_avaluo: hogar.valor_contenidos_especiales_avaluo || undefined,
					valor_equipo_electronico_avaluo: hogar.valor_equipo_electronico_avaluo || undefined,
					valor_maquinaria_equipo_avaluo: hogar.valor_maquinaria_equipo_avaluo || undefined
				};
				// Cargar info del cliente
				const clientes = await clienteService.getAll();
				cliente = clientes.find(c => c.id === hogar?.id_usuario) || null;
			}
		} catch (err) {
			console.error('Error loading hogar:', err);
			error = 'Error al cargar el hogar';
		} finally {
			loading = false;
		}
	});

	async function handleSubmit() {
		saving = true;
		error = null;

		try {
			await bienService.hogares.update(id, formData);
			goto('/bienes');
		} catch (err: unknown) {
			console.error('Error updating hogar:', err);
			if (err && typeof err === 'object' && 'error' in err) {
				error = (err as { error: string }).error;
			} else {
				error = 'Error al actualizar el hogar';
			}
		} finally {
			saving = false;
		}
	}

	function getClienteName(): string {
		if (!cliente) return 'Cliente no encontrado';
		return cliente.tipo_persona === 'PERSONA' 
			? cliente.nombre || 'Sin nombre'
			: cliente.razon_social || 'Sin razón social';
	}
</script>

<svelte:head>
	<title>Editar Hogar | {APP_NAME}</title>
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
		{:else if !hogar}
			<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
				<p class="font-medium">Hogar no encontrado</p>
			</div>
		{:else}
			<form class="form-container" on:submit|preventDefault={handleSubmit}>
				<h1 class="form-title">Editar Hogar #{id}</h1>

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

				<FormSection title="Datos del Hogar" bind:open={sections.datos.open}>
					<div class="space-y-4">
						<FormField label={HogarFields.tipo_inmueble.label}>
							<Select 
								bind:value={formData.tipo_inmueble}
								options={tipoInmuebleOptions}
								disabled={saving}
							/>
						</FormField>
						<FormField label={HogarFields.ciudad_inmueble.label}>
							<Input bind:value={formData.ciudad_inmueble} disabled={saving} />
						</FormField>
						<FormField label={HogarFields.direccion_inmueble.label}>
							<Input bind:value={formData.direccion_inmueble} disabled={saving} />
						</FormField>
						<FormField label={HogarFields.numero_pisos.label}>
							<Input type="number" bind:value={formData.numero_pisos} min="1" disabled={saving} />
						</FormField>
						<FormField label={HogarFields.ano_construccion.label}>
							<Input type="number" bind:value={formData.ano_construccion} min="1900" disabled={saving} />
						</FormField>
					</div>
				</FormSection>

				<FormSection title="Valores de Avalúo" bind:open={sections.valores.open}>
					<div class="space-y-4">
						<FormField label={HogarFields.valor_inmueble_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_inmueble_avaluo} disabled={saving} />
						</FormField>
						<FormField label={HogarFields.valor_contenidos_normales_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_contenidos_normales_avaluo} disabled={saving} />
						</FormField>
						<FormField label={HogarFields.valor_contenidos_especiales_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_contenidos_especiales_avaluo} disabled={saving} />
						</FormField>
						<FormField label={HogarFields.valor_equipo_electronico_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_equipo_electronico_avaluo} disabled={saving} />
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
