<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select, CurrencyInput } from '$components';
	import { bienService, clienteService } from '$services';
	import { CopropiedadFields } from '$constants';
	import type { Cliente } from '$lib/types/cliente';
	import type { Copropiedad, UpdateCopropiedadDto } from '$lib/types/bien';
	import { TIPOS_COPROPIEDAD } from '$lib/types/bien';

	const id = Number($page.params.id);

	let copropiedad: Copropiedad | null = null;
	let cliente: Cliente | null = null;
	let formData: UpdateCopropiedadDto = {};
	let loading = true;
	let saving = false;
	let error: string | null = null;

	let sections = {
		cliente: { open: true },
		datos: { open: true },
		estructura: { open: false },
		valores: { open: false }
	};

	const tipoCopropiedadOptions = TIPOS_COPROPIEDAD.map(t => ({ value: t.value, label: t.label }));
	const estratoOptions = [1, 2, 3, 4, 5, 6].map(e => ({ value: String(e), label: `Estrato ${e}` }));

	onMount(async () => {
		try {
			copropiedad = await bienService.copropiedades.getById(id);
			if (copropiedad) {
				formData = {
					tipo_copropiedad: copropiedad.tipo_copropiedad || '',
					ciudad: copropiedad.ciudad || '',
					direccion: copropiedad.direccion || '',
					estrato: copropiedad.estrato || undefined,
					ano_construccion: copropiedad.ano_construccion || undefined,
					numero_torres: copropiedad.numero_torres || undefined,
					numero_maximo_pisos: copropiedad.numero_maximo_pisos || undefined,
					numero_maximo_sotanos: copropiedad.numero_maximo_sotanos || undefined,
					cantidad_unidades_casa: copropiedad.cantidad_unidades_casa || undefined,
					cantidad_unidades_apartamentos: copropiedad.cantidad_unidades_apartamentos || undefined,
					cantidad_unidades_locales: copropiedad.cantidad_unidades_locales || undefined,
					cantidad_unidades_oficinas: copropiedad.cantidad_unidades_oficinas || undefined,
					cantidad_unidades_otros: copropiedad.cantidad_unidades_otros || undefined,
					valor_edificio_area_comun_avaluo: copropiedad.valor_edificio_area_comun_avaluo || undefined,
					valor_edificio_area_privada_avaluo: copropiedad.valor_edificio_area_privada_avaluo || undefined,
					valor_maquinaria_equipo_avaluo: copropiedad.valor_maquinaria_equipo_avaluo || undefined,
					valor_equipo_electrico_electronico_avaluo: copropiedad.valor_equipo_electrico_electronico_avaluo || undefined,
					valor_muebles_avaluo: copropiedad.valor_muebles_avaluo || undefined
				};
				const clientes = await clienteService.getAll();
				cliente = clientes.find(c => c.id === copropiedad?.id_usuario) || null;
			}
		} catch (err) {
			console.error('Error loading copropiedad:', err);
			error = 'Error al cargar la copropiedad';
		} finally {
			loading = false;
		}
	});

	async function handleSubmit() {
		saving = true;
		error = null;
		try {
			await bienService.copropiedades.update(id, formData);
			goto('/bienes');
		} catch (err: unknown) {
			console.error('Error updating copropiedad:', err);
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
	<title>Editar Copropiedad | {APP_NAME}</title>
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
		{:else if !copropiedad}
			<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
				<p class="font-medium">Copropiedad no encontrada</p>
			</div>
		{:else}
			<form class="form-container" on:submit|preventDefault={handleSubmit}>
				<h1 class="form-title">Editar Copropiedad #{id}</h1>

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

				<FormSection title="Datos de la Copropiedad" bind:open={sections.datos.open}>
					<div class="space-y-4">
						<FormField label={CopropiedadFields.tipo_copropiedad.label}>
							<Select bind:value={formData.tipo_copropiedad} options={tipoCopropiedadOptions} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.estrato.label}>
							<Select bind:value={formData.estrato} options={estratoOptions} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.ciudad.label}>
							<Input bind:value={formData.ciudad} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.direccion.label}>
							<Input bind:value={formData.direccion} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.ano_construccion.label}>
							<Input type="number" bind:value={formData.ano_construccion} min="1900" disabled={saving} />
						</FormField>
					</div>
				</FormSection>

				<FormSection title="Estructura" bind:open={sections.estructura.open}>
					<div class="space-y-4">
						<FormField label={CopropiedadFields.numero_torres.label}>
							<Input type="number" bind:value={formData.numero_torres} min="0" disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.numero_maximo_pisos.label}>
							<Input type="number" bind:value={formData.numero_maximo_pisos} min="0" disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.numero_maximo_sotanos.label}>
							<Input type="number" bind:value={formData.numero_maximo_sotanos} min="0" disabled={saving} />
						</FormField>
					</div>
					<div class="border-t pt-4 mt-4">
						<h4 class="text-sm font-semibold text-secondary-700 mb-4">Unidades</h4>
						<div class="space-y-4">
							<FormField label={CopropiedadFields.cantidad_unidades_casa.label}>
								<Input type="number" bind:value={formData.cantidad_unidades_casa} min="0" disabled={saving} />
							</FormField>
							<FormField label={CopropiedadFields.cantidad_unidades_apartamentos.label}>
								<Input type="number" bind:value={formData.cantidad_unidades_apartamentos} min="0" disabled={saving} />
							</FormField>
							<FormField label={CopropiedadFields.cantidad_unidades_locales.label}>
								<Input type="number" bind:value={formData.cantidad_unidades_locales} min="0" disabled={saving} />
							</FormField>
							<FormField label={CopropiedadFields.cantidad_unidades_oficinas.label}>
								<Input type="number" bind:value={formData.cantidad_unidades_oficinas} min="0" disabled={saving} />
							</FormField>
							<FormField label={CopropiedadFields.cantidad_unidades_otros.label}>
								<Input type="number" bind:value={formData.cantidad_unidades_otros} min="0" disabled={saving} />
							</FormField>
						</div>
					</div>
				</FormSection>

				<FormSection title="Valores de Avalúo" bind:open={sections.valores.open}>
					<div class="space-y-4">
						<FormField label={CopropiedadFields.valor_edificio_area_comun_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_edificio_area_comun_avaluo} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.valor_edificio_area_privada_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_edificio_area_privada_avaluo} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.valor_maquinaria_equipo_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_maquinaria_equipo_avaluo} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.valor_equipo_electrico_electronico_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_equipo_electrico_electronico_avaluo} disabled={saving} />
						</FormField>
						<FormField label={CopropiedadFields.valor_muebles_avaluo.label}>
							<CurrencyInput bind:value={formData.valor_muebles_avaluo} disabled={saving} />
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
