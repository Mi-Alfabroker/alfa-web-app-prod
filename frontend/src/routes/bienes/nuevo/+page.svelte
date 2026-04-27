<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select, CurrencyInput } from '$components';
	import { bienService, clienteService } from '$services';
	import { HogarFields, VehiculoFields, CopropiedadFields, OtroBienFields } from '$constants';
	import type { Cliente } from '$lib/types/cliente';
	import type { TipoBien, CreateHogarDto, CreateVehiculoDto, CreateCopropiedadDto, CreateOtroBienDto } from '$lib/types/bien';
	import { TIPOS_BIEN, TIPOS_INMUEBLE, TIPOS_VEHICULO, TIPOS_COPROPIEDAD } from '$lib/types/bien';
	import { addNotification } from '$lib/stores/notifications';

	// Obtener tipo de bien desde query param
	let tipoBien: TipoBien = ($page.url.searchParams.get('tipo') as TipoBien) || 'HOGAR';

	// Clientes data
	let clientes: Cliente[] = [];
	let loadingClientes = true;

	// UI state
	let loading = false;
	let error: string | null = null;
	let selectedClienteId: number | null = null;

	// Form sections state
	let sections = {
		cliente: { open: true },
		tipoBien: { open: true },
		datos: { open: true },
		valores: { open: false }
	};

	// Formularios por tipo de bien
	let hogarForm: CreateHogarDto = {
		id_usuario: 0,
		tipo_inmueble: '',
		ciudad_inmueble: '',
		direccion_inmueble: '',
		numero_pisos: undefined,
		ano_construccion: undefined,
		valor_inmueble_avaluo: undefined,
		valor_contenidos_normales_avaluo: undefined,
		valor_contenidos_especiales_avaluo: undefined,
		valor_equipo_electronico_avaluo: undefined,
		valor_maquinaria_equipo_avaluo: undefined
	};

	let vehiculoForm: CreateVehiculoDto = {
		id_usuario: 0,
		tipo_vehiculo: '',
		placa: '',
		marca: '',
		serie_referencia: '',
		ano_modelo: undefined,
		ano_nacimiento_conductor: undefined,
		codigo_fasecolda: '',
		valor_vehiculo: undefined,
		valor_accesorios_avaluo: undefined
	};

	let copropiedadForm: CreateCopropiedadDto = {
		id_usuario: 0,
		tipo_copropiedad: '',
		ciudad: '',
		direccion: '',
		estrato: undefined,
		ano_construccion: undefined,
		numero_torres: undefined,
		numero_maximo_pisos: undefined,
		numero_maximo_sotanos: undefined,
		cantidad_unidades_casa: undefined,
		cantidad_unidades_apartamentos: undefined,
		cantidad_unidades_locales: undefined,
		cantidad_unidades_oficinas: undefined,
		cantidad_unidades_otros: undefined,
		valor_edificio_area_comun_avaluo: undefined,
		valor_edificio_area_privada_avaluo: undefined,
		valor_maquinaria_equipo_avaluo: undefined,
		valor_equipo_electrico_electronico_avaluo: undefined,
		valor_muebles_avaluo: undefined
	};

	let otroBienForm: CreateOtroBienDto = {
		id_usuario: 0,
		tipo_seguro: '',
		bien_asegurado: '',
		valor_bien_asegurar: undefined,
		detalles_bien_asegurado: ''
	};

	// Select options
	const tipoBienOptions = TIPOS_BIEN.map(t => ({ value: t.value, label: t.label }));
	const tipoInmuebleOptions = TIPOS_INMUEBLE.map(t => ({ value: t.value, label: t.label }));
	const tipoVehiculoOptions = TIPOS_VEHICULO.map(t => ({ value: t.value, label: t.label }));
	const tipoCopropiedadOptions = TIPOS_COPROPIEDAD.map(t => ({ value: t.value, label: t.label }));
	const estratoOptions = [1, 2, 3, 4, 5, 6].map(e => ({ value: String(e), label: `Estrato ${e}` }));

	// Cargar clientes
	onMount(async () => {
		try {
			clientes = await clienteService.getAll();
		} catch (err) {
			console.error('Error loading clientes:', err);
			error = 'Error al cargar los clientes';
		} finally {
			loadingClientes = false;
		}
	});

	// Opciones de clientes
	$: clienteOptions = clientes.map(c => ({
		value: String(c.id),
		label: c.tipo_persona === 'PERSONA' 
			? `${c.nombre || 'Sin nombre'} (${c.numero_documento || 'Sin doc.'})`
			: `${c.razon_social || 'Sin razón social'} (${c.nit || 'Sin NIT'})`
	}));

	// Handle submit
	async function handleSubmit() {
		if (!selectedClienteId) {
			error = 'Debe seleccionar un cliente';
			return;
		}

		loading = true;
		error = null;

		try {
			let result;
			
			switch (tipoBien) {
				case 'HOGAR':
					hogarForm.id_usuario = selectedClienteId;
					result = await bienService.hogares.create(hogarForm);
					break;
				case 'VEHICULO':
					vehiculoForm.id_usuario = selectedClienteId;
					result = await bienService.vehiculos.create(vehiculoForm);
					break;
				case 'COPROPIEDAD':
					copropiedadForm.id_usuario = selectedClienteId;
					result = await bienService.copropiedades.create(copropiedadForm);
					break;
				case 'OTRO':
					otroBienForm.id_usuario = selectedClienteId;
					result = await bienService.otros.create(otroBienForm);
					break;
			}

			console.log('✅ Bien creado:', result);
			addNotification({
				type: 'success',
				message: `Bien de tipo ${tipoBien.charAt(0) + tipoBien.slice(1).toLowerCase()} creado exitosamente`
			});
			goto('/bienes');
		} catch (err: unknown) {
			console.error('❌ Error al crear bien:', err);
			if (err && typeof err === 'object' && 'error' in err) {
				error = (err as { error: string }).error;
			} else if (err instanceof Error) {
				error = err.message;
			} else {
				error = 'Error al crear el bien';
			}
		} finally {
			loading = false;
		}
	}

	function handleCancel() {
		goto('/bienes');
	}

	// Abrir sección de valores cuando se complete datos básicos
	$: if (selectedClienteId) {
		sections.valores.open = true;
	}
</script>

<svelte:head>
	<title>Nuevo Bien | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
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

<!-- Content -->
<div class="page-content">
	<div class="max-w-4xl mx-auto">
		<form class="form-container" on:submit|preventDefault={handleSubmit}>
			<!-- Form Title -->
			<h1 class="form-title">Registrar Nuevo Bien</h1>

			<!-- Error Message -->
			{#if error}
				<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
					<div class="flex items-center gap-2">
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
						<span>{error}</span>
					</div>
				</div>
			{/if}

			<!-- Section: Selección de Cliente -->
			<FormSection 
				title="Seleccionar Cliente" 
				bind:open={sections.cliente.open}
			>
				{#if loadingClientes}
					<div class="flex items-center gap-2 text-secondary-500">
						<svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
						</svg>
						<span>Cargando clientes...</span>
					</div>
				{:else if clientes.length === 0}
					<div class="bg-amber-50 border border-amber-200 text-amber-700 px-4 py-3 rounded-lg">
						<p class="font-medium">No hay clientes registrados</p>
						<p class="text-sm mt-1">Debe crear un cliente antes de poder registrar bienes.</p>
						<a href="/clientes/nuevo" class="btn btn-primary mt-3 inline-block">
							Crear Cliente
						</a>
					</div>
				{:else}
					<FormField 
						label="Cliente"
						helper="Seleccione el cliente propietario del bien."
						required
					>
						<Select 
							bind:value={selectedClienteId}
							options={clienteOptions}
							placeholder="Seleccionar cliente..."
							required
							disabled={loading}
						/>
					</FormField>
				{/if}
			</FormSection>

			<!-- Section: Tipo de Bien -->
			{#if selectedClienteId}
				<FormSection 
					title="Tipo de Bien" 
					bind:open={sections.tipoBien.open}
				>
					<FormField 
						label="Tipo de Bien"
						helper="Seleccione la categoría del bien a registrar."
						required
					>
						<Select 
							bind:value={tipoBien}
							options={tipoBienOptions}
							required
							disabled={loading}
						/>
					</FormField>
				</FormSection>

				<!-- Section: Datos del Bien -->
				<FormSection 
					title={tipoBien === 'HOGAR' ? 'Datos del Hogar' 
						: tipoBien === 'VEHICULO' ? 'Datos del Vehículo'
						: tipoBien === 'COPROPIEDAD' ? 'Datos de la Copropiedad'
						: 'Datos del Bien'}
					bind:open={sections.datos.open}
				>
					<!-- HOGAR FORM -->
					{#if tipoBien === 'HOGAR'}
						<div class="space-y-4">
							<FormField label={HogarFields.tipo_inmueble.label} required>
								<Select 
									bind:value={hogarForm.tipo_inmueble}
									options={tipoInmuebleOptions}
									placeholder="Seleccionar..."
									required
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.ciudad_inmueble.label}>
								<Input 
									bind:value={hogarForm.ciudad_inmueble}
									placeholder="Ej: Bogotá"
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.direccion_inmueble.label}>
								<Input 
									bind:value={hogarForm.direccion_inmueble}
									placeholder="Ej: Calle 123 #45-67"
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.numero_pisos.label}>
								<Input 
									type="number"
									bind:value={hogarForm.numero_pisos}
									placeholder="Ej: 2"
									min="1"
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.ano_construccion.label}>
								<Input 
									type="number"
									bind:value={hogarForm.ano_construccion}
									placeholder="Ej: 2010"
									min="1900"
									max={new Date().getFullYear()}
									disabled={loading}
								/>
							</FormField>
						</div>

					<!-- VEHICULO FORM -->
					{:else if tipoBien === 'VEHICULO'}
						<div class="space-y-4">
							<FormField label={VehiculoFields.tipo_vehiculo.label} required>
								<Select 
									bind:value={vehiculoForm.tipo_vehiculo}
									options={tipoVehiculoOptions}
									placeholder="Seleccionar..."
									required
									disabled={loading}
								/>
							</FormField>
							<FormField label={VehiculoFields.placa.label}>
								<Input 
									bind:value={vehiculoForm.placa}
									placeholder="Ej: ABC123"
									maxlength="10"
									disabled={loading}
								/>
							</FormField>
							<FormField label={VehiculoFields.marca.label}>
								<Input 
									bind:value={vehiculoForm.marca}
									placeholder="Ej: Chevrolet"
									disabled={loading}
								/>
							</FormField>
							<FormField label={VehiculoFields.serie_referencia.label}>
								<Input 
									bind:value={vehiculoForm.serie_referencia}
									placeholder="Ej: Spark GT"
									disabled={loading}
								/>
							</FormField>
							<FormField label={VehiculoFields.ano_modelo.label}>
								<Input 
									type="number"
									bind:value={vehiculoForm.ano_modelo}
									placeholder="Ej: 2020"
									min="1950"
									max={new Date().getFullYear() + 1}
									disabled={loading}
								/>
							</FormField>
							<FormField label={VehiculoFields.codigo_fasecolda.label}>
								<Input 
									bind:value={vehiculoForm.codigo_fasecolda}
									placeholder="Ej: 12345678"
									disabled={loading}
								/>
							</FormField>
							<FormField label={VehiculoFields.ano_nacimiento_conductor.label} helper="Año de nacimiento del conductor principal.">
								<Input 
									type="number"
									bind:value={vehiculoForm.ano_nacimiento_conductor}
									placeholder="Ej: 1985"
									min="1920"
									max={new Date().getFullYear() - 16}
									disabled={loading}
								/>
							</FormField>
						</div>

					<!-- COPROPIEDAD FORM -->
					{:else if tipoBien === 'COPROPIEDAD'}
						<div class="space-y-4">
							<FormField label={CopropiedadFields.tipo_copropiedad.label} required>
								<Select 
									bind:value={copropiedadForm.tipo_copropiedad}
									options={tipoCopropiedadOptions}
									placeholder="Seleccionar..."
									required
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.estrato.label}>
								<Select 
									bind:value={copropiedadForm.estrato}
									options={estratoOptions}
									placeholder="Seleccionar..."
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.ciudad.label}>
								<Input 
									bind:value={copropiedadForm.ciudad}
									placeholder="Ej: Bogotá"
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.direccion.label}>
								<Input 
									bind:value={copropiedadForm.direccion}
									placeholder="Ej: Carrera 10 #20-30"
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.ano_construccion.label}>
								<Input 
									type="number"
									bind:value={copropiedadForm.ano_construccion}
									placeholder="Ej: 2015"
									min="1900"
									max={new Date().getFullYear()}
									disabled={loading}
								/>
							</FormField>
						</div>
						<div class="border-t pt-4 mt-4">
							<h4 class="text-sm font-semibold text-secondary-700 mb-4">Estructura del Edificio</h4>
							<div class="space-y-4">
								<FormField label={CopropiedadFields.numero_torres.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.numero_torres}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
								<FormField label={CopropiedadFields.numero_maximo_pisos.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.numero_maximo_pisos}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
								<FormField label={CopropiedadFields.numero_maximo_sotanos.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.numero_maximo_sotanos}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
							</div>
						</div>
						<div class="border-t pt-4 mt-4">
							<h4 class="text-sm font-semibold text-secondary-700 mb-4">Cantidad de Unidades</h4>
							<div class="space-y-4">
								<FormField label={CopropiedadFields.cantidad_unidades_casa.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.cantidad_unidades_casa}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
								<FormField label={CopropiedadFields.cantidad_unidades_apartamentos.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.cantidad_unidades_apartamentos}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
								<FormField label={CopropiedadFields.cantidad_unidades_locales.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.cantidad_unidades_locales}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
								<FormField label={CopropiedadFields.cantidad_unidades_oficinas.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.cantidad_unidades_oficinas}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
								<FormField label={CopropiedadFields.cantidad_unidades_otros.label}>
									<Input 
										type="number"
										bind:value={copropiedadForm.cantidad_unidades_otros}
										placeholder="0"
										min="0"
										disabled={loading}
									/>
								</FormField>
							</div>
						</div>

					<!-- OTRO BIEN FORM -->
					{:else if tipoBien === 'OTRO'}
						<div class="space-y-4">
							<FormField label={OtroBienFields.tipo_seguro.label} required>
								<Input 
									bind:value={otroBienForm.tipo_seguro}
									placeholder="Ej: Seguro de Responsabilidad Civil"
									required
									disabled={loading}
								/>
							</FormField>
							<FormField label={OtroBienFields.bien_asegurado.label} required>
								<Input 
									bind:value={otroBienForm.bien_asegurado}
									placeholder="Ej: Equipo de Fotografía Profesional"
									required
									disabled={loading}
								/>
							</FormField>
							<FormField label={OtroBienFields.detalles_bien_asegurado.label} helper="Información adicional sobre el bien.">
								<textarea
									bind:value={otroBienForm.detalles_bien_asegurado}
									placeholder="Describa los detalles del bien a asegurar..."
									class="input min-h-[100px]"
									disabled={loading}
								></textarea>
							</FormField>
						</div>
					{/if}
				</FormSection>

				<!-- Section: Valores de Avalúo -->
				<FormSection 
					title="Valores de Avalúo"
					bind:open={sections.valores.open}
				>
					{#if tipoBien === 'HOGAR'}
						<div class="space-y-4">
							<FormField label={HogarFields.valor_inmueble_avaluo.label} helper="Valor comercial del inmueble.">
								<CurrencyInput 
									bind:value={hogarForm.valor_inmueble_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.valor_contenidos_normales_avaluo.label}>
								<CurrencyInput 
									bind:value={hogarForm.valor_contenidos_normales_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.valor_contenidos_especiales_avaluo.label}>
								<CurrencyInput 
									bind:value={hogarForm.valor_contenidos_especiales_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.valor_equipo_electronico_avaluo.label}>
								<CurrencyInput 
									bind:value={hogarForm.valor_equipo_electronico_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={HogarFields.valor_maquinaria_equipo_avaluo.label}>
								<CurrencyInput 
									bind:value={hogarForm.valor_maquinaria_equipo_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
						</div>
					{:else if tipoBien === 'VEHICULO'}
						<div class="space-y-4">
							<FormField label={VehiculoFields.valor_vehiculo.label} helper="Valor comercial del vehículo.">
								<CurrencyInput 
									bind:value={vehiculoForm.valor_vehiculo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={VehiculoFields.valor_accesorios_avaluo.label}>
								<CurrencyInput 
									bind:value={vehiculoForm.valor_accesorios_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
						</div>
					{:else if tipoBien === 'COPROPIEDAD'}
						<div class="space-y-4">
							<FormField label={CopropiedadFields.valor_edificio_area_comun_avaluo.label}>
								<CurrencyInput 
									bind:value={copropiedadForm.valor_edificio_area_comun_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.valor_edificio_area_privada_avaluo.label}>
								<CurrencyInput 
									bind:value={copropiedadForm.valor_edificio_area_privada_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.valor_maquinaria_equipo_avaluo.label}>
								<CurrencyInput 
									bind:value={copropiedadForm.valor_maquinaria_equipo_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.valor_equipo_electrico_electronico_avaluo.label}>
								<CurrencyInput 
									bind:value={copropiedadForm.valor_equipo_electrico_electronico_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
							<FormField label={CopropiedadFields.valor_muebles_avaluo.label}>
								<CurrencyInput 
									bind:value={copropiedadForm.valor_muebles_avaluo}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
						</div>
					{:else if tipoBien === 'OTRO'}
						<div class="space-y-4">
							<FormField label={OtroBienFields.valor_bien_asegurar.label} helper="Valor comercial del bien.">
								<CurrencyInput 
									bind:value={otroBienForm.valor_bien_asegurar}
									placeholder="0"
									disabled={loading}
								/>
							</FormField>
						</div>
					{/if}
				</FormSection>
			{/if}

			<!-- Form Actions -->
			<div class="form-actions">
				<button 
					type="button" 
					class="btn btn-secondary" 
					on:click={handleCancel}
					disabled={loading}
				>
					Cancelar
				</button>
				<button 
					type="submit" 
					class="btn btn-primary"
					disabled={loading || !selectedClienteId || loadingClientes}
				>
					{#if loading}
						<svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
						</svg>
						Guardando...
					{:else}
						Guardar Bien
					{/if}
				</button>
			</div>
		</form>
	</div>
</div>
