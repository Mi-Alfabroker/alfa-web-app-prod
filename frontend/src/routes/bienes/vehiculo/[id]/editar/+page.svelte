<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select, CurrencyInput } from '$components';
	import { bienService, clienteService } from '$services';
	import { VehiculoFields } from '$constants';
	import type { Cliente } from '$lib/types/cliente';
	import type { Vehiculo, UpdateVehiculoDto } from '$lib/types/bien';
	import { TIPOS_VEHICULO } from '$lib/types/bien';

	const id = Number($page.params.id);

	let vehiculo: Vehiculo | null = null;
	let cliente: Cliente | null = null;
	let formData: UpdateVehiculoDto = {};
	let loading = true;
	let saving = false;
	let error: string | null = null;

	let sections = {
		cliente: { open: true },
		datos: { open: true },
		valores: { open: true }
	};

	const tipoVehiculoOptions = TIPOS_VEHICULO.map(t => ({ value: t.value, label: t.label }));

	onMount(async () => {
		try {
			vehiculo = await bienService.vehiculos.getById(id);
			if (vehiculo) {
				formData = {
					tipo_vehiculo: vehiculo.tipo_vehiculo || '',
					placa: vehiculo.placa || '',
					marca: vehiculo.marca || '',
					serie_referencia: vehiculo.serie_referencia || '',
					ano_modelo: vehiculo.ano_modelo || undefined,
					ano_nacimiento_conductor: vehiculo.ano_nacimiento_conductor || undefined,
					codigo_fasecolda: vehiculo.codigo_fasecolda || '',
					valor_vehiculo: vehiculo.valor_vehiculo || undefined,
					valor_accesorios_avaluo: vehiculo.valor_accesorios_avaluo || undefined
				};
				const clientes = await clienteService.getAll();
				cliente = clientes.find(c => c.id === vehiculo?.id_usuario) || null;
			}
		} catch (err) {
			console.error('Error loading vehiculo:', err);
			error = 'Error al cargar el vehículo';
		} finally {
			loading = false;
		}
	});

	async function handleSubmit() {
		saving = true;
		error = null;
		try {
			await bienService.vehiculos.update(id, formData);
			goto('/bienes');
		} catch (err: unknown) {
			console.error('Error updating vehiculo:', err);
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
	<title>Editar Vehículo | {APP_NAME}</title>
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
		{:else if !vehiculo}
			<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
				<p class="font-medium">Vehículo no encontrado</p>
			</div>
		{:else}
			<form class="form-container" on:submit|preventDefault={handleSubmit}>
				<h1 class="form-title">Editar Vehículo #{id}</h1>

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

				<FormSection title="Datos del Vehículo" bind:open={sections.datos.open}>
					<div class="space-y-4">
						<FormField label={VehiculoFields.tipo_vehiculo.label}>
							<Select bind:value={formData.tipo_vehiculo} options={tipoVehiculoOptions} disabled={saving} />
						</FormField>
						<FormField label={VehiculoFields.placa.label}>
							<Input bind:value={formData.placa} maxlength="10" disabled={saving} />
						</FormField>
						<FormField label={VehiculoFields.marca.label}>
							<Input bind:value={formData.marca} disabled={saving} />
						</FormField>
						<FormField label={VehiculoFields.serie_referencia.label}>
							<Input bind:value={formData.serie_referencia} disabled={saving} />
						</FormField>
						<FormField label={VehiculoFields.ano_modelo.label}>
							<Input type="number" bind:value={formData.ano_modelo} min="1950" disabled={saving} />
						</FormField>
						<FormField label={VehiculoFields.codigo_fasecolda.label}>
							<Input bind:value={formData.codigo_fasecolda} disabled={saving} />
						</FormField>
						<FormField label={VehiculoFields.ano_nacimiento_conductor.label}>
							<Input type="number" bind:value={formData.ano_nacimiento_conductor} min="1920" disabled={saving} />
						</FormField>
					</div>
				</FormSection>

				<FormSection title="Valores" bind:open={sections.valores.open}>
					<div class="space-y-4">
						<FormField label={VehiculoFields.valor_vehiculo.label}>
							<CurrencyInput bind:value={formData.valor_vehiculo} disabled={saving} />
						</FormField>
						<FormField label={VehiculoFields.valor_accesorios_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_accesorios_avaluo} disabled={saving} />
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
