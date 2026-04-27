<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select, Modal, CurrencyInput } from '$components';
	import { polizaService, clienteService, bienService, aseguradoraService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import type { Cliente } from '$lib/types/cliente';
	import type { Aseguradora } from '$lib/types/aseguradora';
	import type { Hogar, Vehiculo, Copropiedad, OtroBien, TipoBien } from '$lib/types/bien';

	// Tipo de bien desde la URL
	$: tipoBien = ($page.params.tipo?.toUpperCase() || 'HOGAR') as TipoBien;
	$: bienIdFromQuery = $page.url.searchParams.get('bien_id');

	// Data state
	let clientes: Cliente[] = [];
	let aseguradoras: Aseguradora[] = [];
	let bienes: (Hogar | Vehiculo | Copropiedad | OtroBien)[] = [];
	
	// UI state
	let loading = true;
	let saving = false;
	let selectedBienId: number | null = null;
	let selectedBien: Hogar | Vehiculo | Copropiedad | OtroBien | null = null;

	// Form data
	let formData = {
		// Vigencia
		inicio_vigencia: '',
		fin_vigencia: '',
		
		// Aseguradora 1
		id_aseguradora_1: null as number | null,
		valor_prima_aseg_1: null as number | null,
		
		// Aseguradora 2
		id_aseguradora_2: null as number | null,
		valor_prima_aseg_2: null as number | null,
		
		// Aseguradora 3
		id_aseguradora_3: null as number | null,
		valor_prima_aseg_3: null as number | null,
		
		// Aseguradora 4
		id_aseguradora_4: null as number | null,
		valor_prima_aseg_4: null as number | null,
		
		// Aseguradora 5
		id_aseguradora_5: null as number | null,
		valor_prima_aseg_5: null as number | null,
		
		// Valores financieros
		valor_prima_neta: null as number | null,
		valor_otros_costos: null as number | null,
		valor_iva: null as number | null,
		ingreso_comision_percibido: null as number | null,
		
		// Valores específicos del bien (hogar)
		valor_inmueble_asegurado: null as number | null,
		valor_contenidos_normales_asegurado: null as number | null,
		valor_contenidos_especiales_asegurado: null as number | null,
		valor_equipo_electronico_asegurado: null as number | null,
		valor_maquinaria_equipo_asegurado: null as number | null,
		
		// Valores específicos (vehículo)
		valor_vehiculo_asegurado: null as number | null,
		valor_accesorios_asegurado: null as number | null,
		
		// Valores específicos (copropiedad)
		valor_area_comun_asegurado: null as number | null,
		valor_area_privada_asegurado: null as number | null,
		valor_muebles_asegurado: null as number | null,
		
		// Valores específicos (otro bien)
		valor_bien_asegurado: null as number | null
	};

	// Section states
	let sections = {
		bien: { open: true },
		vigencia: { open: true },
		aseguradoras: { open: true },
		valores: { open: false },
		financiero: { open: false }
	};

	// Cargar datos
	onMount(async () => {
		await Promise.all([
			loadClientes(),
			loadAseguradoras(),
			loadBienes()
		]);
		
		// Si viene un bien_id en la URL, seleccionarlo
		if (bienIdFromQuery) {
			selectedBienId = parseInt(bienIdFromQuery);
			updateSelectedBien();
		}
		
		loading = false;
	});

	async function loadClientes() {
		try {
			clientes = await clienteService.getAll();
		} catch (err) {
			console.error('Error loading clientes:', err);
		}
	}

	async function loadAseguradoras() {
		try {
			aseguradoras = await aseguradoraService.getAll();
		} catch (err) {
			console.error('Error loading aseguradoras:', err);
		}
	}

	async function loadBienes() {
		try {
			if (tipoBien === 'HOGAR') {
				bienes = await bienService.hogares.getAll();
			} else if (tipoBien === 'VEHICULO') {
				bienes = await bienService.vehiculos.getAll();
			} else if (tipoBien === 'COPROPIEDAD') {
				bienes = await bienService.copropiedades.getAll();
			} else {
				bienes = await bienService.otros.getAll();
			}
		} catch (err) {
			console.error('Error loading bienes:', err);
		}
	}

	// Actualizar bien seleccionado
	function updateSelectedBien() {
		selectedBien = bienes.find(b => b.id === selectedBienId) || null;
		
		// Pre-llenar valores del bien si existe
		if (selectedBien) {
			if ('valor_inmueble_avaluo' in selectedBien) {
				formData.valor_inmueble_asegurado = selectedBien.valor_inmueble_avaluo;
				formData.valor_contenidos_normales_asegurado = selectedBien.valor_contenidos_normales_avaluo;
				formData.valor_contenidos_especiales_asegurado = selectedBien.valor_contenidos_especiales_avaluo;
				formData.valor_equipo_electronico_asegurado = selectedBien.valor_equipo_electronico_avaluo;
				formData.valor_maquinaria_equipo_asegurado = selectedBien.valor_maquinaria_equipo_avaluo;
			} else if ('valor_vehiculo' in selectedBien) {
				formData.valor_vehiculo_asegurado = selectedBien.valor_vehiculo;
				formData.valor_accesorios_asegurado = selectedBien.valor_accesorios_avaluo;
			} else if ('valor_edificio_area_comun_avaluo' in selectedBien) {
				const cop = selectedBien as Copropiedad;
				formData.valor_area_comun_asegurado = cop.valor_edificio_area_comun_avaluo;
				formData.valor_area_privada_asegurado = cop.valor_edificio_area_privada_avaluo;
				formData.valor_muebles_asegurado = cop.valor_muebles_avaluo;
				formData.valor_maquinaria_equipo_asegurado = cop.valor_maquinaria_equipo_avaluo;
			} else if ('valor_bien_asegurar' in selectedBien) {
				formData.valor_bien_asegurado = selectedBien.valor_bien_asegurar;
			}
		}
	}

	$: if (selectedBienId && bienes.length > 0) {
		updateSelectedBien();
	}

	// Helpers
	function getClienteName(idUsuario: number): string {
		const cliente = clientes.find(c => c.id === idUsuario);
		if (!cliente) return `#${idUsuario}`;
		return cliente.tipo_persona === 'PERSONA' 
			? cliente.nombre || `#${idUsuario}`
			: cliente.razon_social || `#${idUsuario}`;
	}

	function getBienDescripcion(bien: Hogar | Vehiculo | Copropiedad | OtroBien): string {
		if ('tipo_inmueble' in bien) {
			return `${bien.tipo_inmueble || 'Hogar'} - ${bien.direccion_inmueble || ''}, ${bien.ciudad_inmueble || ''}`;
		} else if ('placa' in bien) {
			return `${bien.marca || ''} ${bien.placa || ''} (${bien.ano_modelo || ''})`.trim();
		} else if ('tipo_copropiedad' in bien) {
			return `${bien.tipo_copropiedad || 'Copropiedad'} - ${bien.direccion || ''}, ${bien.ciudad || ''}`;
		} else if ('bien_asegurado' in bien) {
			return bien.bien_asegurado || 'Otro bien';
		}
		return `Bien #${(bien as { id: number }).id}`;
	}

	function formatCurrency(value: number | null): string {
		if (value === null || value === undefined) return '';
		return new Intl.NumberFormat('es-CO', {
			style: 'currency',
			currency: 'COP',
			minimumFractionDigits: 0
		}).format(value);
	}

	// Opciones de aseguradoras para Select
	$: aseguradoraOptions = aseguradoras.map(a => ({
		value: a.id,
		label: a.nombre
	}));

	// Opciones de bienes para Select
	$: bienOptions = bienes.map(b => ({
		value: b.id,
		label: `#${b.id} - ${getBienDescripcion(b)} (${getClienteName(b.id_usuario)})`
	}));

	// Título según tipo
	$: tipoLabel = tipoBien === 'HOGAR' ? 'Hogar' 
		: tipoBien === 'VEHICULO' ? 'Vehículo'
		: tipoBien === 'COPROPIEDAD' ? 'Copropiedad'
		: 'Otro Bien';

	// Guardar propuesta
	async function handleSubmit() {
		if (!selectedBienId) {
			addNotification({
				type: 'error',
				message: 'Debes seleccionar un bien'
			});
			return;
		}

		saving = true;
		try {
			// Construir datos según el tipo
			let createData: Record<string, unknown> = {
				inicio_vigencia: formData.inicio_vigencia || null,
				fin_vigencia: formData.fin_vigencia || null,
				id_aseguradora_1: formData.id_aseguradora_1,
				valor_prima_aseg_1: formData.valor_prima_aseg_1,
				id_aseguradora_2: formData.id_aseguradora_2,
				valor_prima_aseg_2: formData.valor_prima_aseg_2,
				id_aseguradora_3: formData.id_aseguradora_3,
				valor_prima_aseg_3: formData.valor_prima_aseg_3,
				id_aseguradora_4: formData.id_aseguradora_4,
				valor_prima_aseg_4: formData.valor_prima_aseg_4,
				id_aseguradora_5: formData.id_aseguradora_5,
				valor_prima_aseg_5: formData.valor_prima_aseg_5,
				valor_prima_neta: formData.valor_prima_neta,
				valor_otros_costos: formData.valor_otros_costos,
				valor_iva: formData.valor_iva,
				ingreso_comision_percibido: formData.ingreso_comision_percibido
			};

			let resultado;
			if (tipoBien === 'HOGAR') {
				createData = {
					...createData,
					id_hogar: selectedBienId,
					valor_inmueble_asegurado: formData.valor_inmueble_asegurado,
					valor_contenidos_normales_asegurado: formData.valor_contenidos_normales_asegurado,
					valor_contenidos_especiales_asegurado: formData.valor_contenidos_especiales_asegurado,
					valor_equipo_electronico_asegurado: formData.valor_equipo_electronico_asegurado,
					valor_maquinaria_equipo_asegurado: formData.valor_maquinaria_equipo_asegurado
				};
				resultado = await polizaService.hogar.create(createData);
			} else if (tipoBien === 'VEHICULO') {
				createData = {
					...createData,
					id_vehiculo: selectedBienId,
					valor_vehiculo_asegurado: formData.valor_vehiculo_asegurado,
					valor_accesorios_asegurado: formData.valor_accesorios_asegurado
				};
				resultado = await polizaService.vehiculo.create(createData);
			} else if (tipoBien === 'COPROPIEDAD') {
				createData = {
					...createData,
					id_copropiedad: selectedBienId,
					valor_area_comun_asegurado: formData.valor_area_comun_asegurado,
					valor_area_privada_asegurado: formData.valor_area_privada_asegurado,
					valor_muebles_asegurado: formData.valor_muebles_asegurado,
					valor_maquinaria_equipo_asegurado: formData.valor_maquinaria_equipo_asegurado
				};
				resultado = await polizaService.copropiedad.create(createData);
			} else {
				createData = {
					...createData,
					id_otro_bien: selectedBienId,
					valor_bien_asegurado: formData.valor_bien_asegurado
				};
				resultado = await polizaService.otroBien.create(createData);
			}

			addNotification({
				type: 'success',
				title: 'Propuesta creada',
				message: `Se creó la propuesta ${resultado.consecutivo} exitosamente.`
			});

			// Redirigir al detalle de la propuesta
			goto(`/propuestas/${tipoBien.toLowerCase()}/${resultado.id}`);
			
		} catch (err) {
			console.error('Error creating propuesta:', err);
			addNotification({
				type: 'error',
				title: 'Error',
				message: err instanceof Error ? err.message : 'No se pudo crear la propuesta'
			});
		} finally {
			saving = false;
		}
	}

	function handleCancel() {
		goto('/propuestas');
	}
</script>

<svelte:head>
	<title>Nueva Propuesta de {tipoLabel} | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<a href="/propuestas" class="page-back-link">
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
			</svg>
			<span>Volver a Pólizas</span>
		</a>
	</div>
</header>

<!-- Content -->
<div class="page-content">
	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="flex flex-col items-center gap-4">
				<svg class="animate-spin h-8 w-8 text-primary-500" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
				</svg>
				<p class="text-secondary-600">Cargando...</p>
			</div>
		</div>
	{:else}
		<div class="max-w-4xl mx-auto">
			<form class="form-container" on:submit|preventDefault={handleSubmit}>
				<div class="flex items-center gap-3 mb-6">
					<span class="text-3xl">
						{tipoBien === 'HOGAR' ? '🏠' : tipoBien === 'VEHICULO' ? '🚗' : tipoBien === 'COPROPIEDAD' ? '🏢' : '📦'}
					</span>
					<h1 class="form-title mb-0">Nueva Propuesta de {tipoLabel}</h1>
				</div>

				<!-- Section: Selección de Bien -->
				<FormSection 
					title="Bien a Asegurar" 
					bind:open={sections.bien}
				>
					<FormField 
						label="Seleccionar {tipoLabel}"
						helper="Elige el bien para el cual crearás la propuesta."
						required
					>
						<Select 
							bind:value={selectedBienId}
							options={bienOptions}
							placeholder="Buscar bien..."
						/>
					</FormField>

					{#if selectedBien}
						<div class="bg-primary-50 border border-primary-200 rounded-lg p-4 mt-4">
							<h4 class="font-medium text-primary-900 mb-2">Bien seleccionado</h4>
							<div class="grid grid-cols-2 gap-4 text-sm">
								<div>
									<span class="text-primary-600">Cliente:</span>
									<span class="font-medium ml-1">{getClienteName(selectedBien.id_usuario)}</span>
								</div>
								<div>
									<span class="text-primary-600">ID:</span>
									<span class="font-mono ml-1">#{selectedBien.id}</span>
								</div>
								{#if 'ciudad_inmueble' in selectedBien}
									<div>
										<span class="text-primary-600">Ciudad:</span>
										<span class="ml-1">{selectedBien.ciudad_inmueble}</span>
									</div>
									<div>
										<span class="text-primary-600">Tipo:</span>
										<span class="ml-1">{selectedBien.tipo_inmueble}</span>
									</div>
								{:else if 'placa' in selectedBien}
									<div>
										<span class="text-primary-600">Placa:</span>
										<span class="font-mono ml-1">{selectedBien.placa}</span>
									</div>
									<div>
										<span class="text-primary-600">Marca:</span>
										<span class="ml-1">{selectedBien.marca}</span>
									</div>
								{:else if 'tipo_copropiedad' in selectedBien}
									<div>
										<span class="text-primary-600">Ciudad:</span>
										<span class="ml-1">{selectedBien.ciudad}</span>
									</div>
									<div>
										<span class="text-primary-600">Tipo:</span>
										<span class="ml-1">{selectedBien.tipo_copropiedad}</span>
									</div>
								{:else if 'tipo_seguro' in selectedBien}
									<div class="col-span-2">
										<span class="text-primary-600">Tipo de seguro:</span>
										<span class="ml-1">{selectedBien.tipo_seguro}</span>
									</div>
								{/if}
							</div>
						</div>
					{/if}
				</FormSection>

				<!-- Section: Vigencia -->
				<FormSection 
					title="Vigencia del Seguro" 
					bind:open={sections.vigencia}
				>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<div>
							<label class="block text-sm font-medium text-secondary-700 mb-1">
								Fecha de inicio
							</label>
							<Input 
								type="date"
								bind:value={formData.inicio_vigencia}
							/>
							<p class="mt-1 text-xs text-secondary-500">Inicio de la vigencia del seguro.</p>
						</div>

						<div>
							<label class="block text-sm font-medium text-secondary-700 mb-1">
								Fecha de fin
							</label>
							<Input 
								type="date"
								bind:value={formData.fin_vigencia}
							/>
							<p class="mt-1 text-xs text-secondary-500">Fin de la vigencia del seguro.</p>
						</div>
					</div>
				</FormSection>

				<!-- Section: Opciones de Aseguradoras -->
				<FormSection 
					title="Opciones de Aseguradoras" 
					bind:open={sections.aseguradoras}
				>
					<p class="text-sm text-secondary-500 mb-4">
						Puedes agregar hasta 5 opciones de aseguradoras con sus respectivos valores de prima.
					</p>

					<!-- Opción 1 -->
					<div class="p-4 bg-secondary-50 rounded-lg mb-3 space-y-4">
						<p class="text-sm font-medium text-secondary-700">Opción 1</p>
						<FormField label="Aseguradora">
							<Select 
								bind:value={formData.id_aseguradora_1}
								options={aseguradoraOptions}
								placeholder="Seleccionar..."
							/>
						</FormField>
						<FormField label="Valor Prima">
							<CurrencyInput 
								bind:value={formData.valor_prima_aseg_1}
								placeholder="0"
							/>
						</FormField>
					</div>

					<!-- Opción 2 -->
					<div class="p-4 bg-secondary-50 rounded-lg mb-3 space-y-4">
						<p class="text-sm font-medium text-secondary-700">Opción 2</p>
						<FormField label="Aseguradora">
							<Select 
								bind:value={formData.id_aseguradora_2}
								options={aseguradoraOptions}
								placeholder="Seleccionar..."
							/>
						</FormField>
						<FormField label="Valor Prima">
							<CurrencyInput 
								bind:value={formData.valor_prima_aseg_2}
								placeholder="0"
							/>
						</FormField>
					</div>

					<!-- Opción 3 -->
					<div class="p-4 bg-secondary-50 rounded-lg mb-3 space-y-4">
						<p class="text-sm font-medium text-secondary-700">Opción 3</p>
						<FormField label="Aseguradora">
							<Select 
								bind:value={formData.id_aseguradora_3}
								options={aseguradoraOptions}
								placeholder="Seleccionar..."
							/>
						</FormField>
						<FormField label="Valor Prima">
							<CurrencyInput 
								bind:value={formData.valor_prima_aseg_3}
								placeholder="0"
							/>
						</FormField>
					</div>

					<!-- Opción 4 -->
					<div class="p-4 bg-secondary-50 rounded-lg mb-3 space-y-4">
						<p class="text-sm font-medium text-secondary-700">Opción 4</p>
						<FormField label="Aseguradora">
							<Select 
								bind:value={formData.id_aseguradora_4}
								options={aseguradoraOptions}
								placeholder="Seleccionar..."
							/>
						</FormField>
						<FormField label="Valor Prima">
							<CurrencyInput 
								bind:value={formData.valor_prima_aseg_4}
								placeholder="0"
							/>
						</FormField>
					</div>

					<!-- Opción 5 -->
					<div class="p-4 bg-secondary-50 rounded-lg space-y-4">
						<p class="text-sm font-medium text-secondary-700">Opción 5</p>
						<FormField label="Aseguradora">
							<Select 
								bind:value={formData.id_aseguradora_5}
								options={aseguradoraOptions}
								placeholder="Seleccionar..."
							/>
						</FormField>
						<FormField label="Valor Prima">
							<CurrencyInput 
								bind:value={formData.valor_prima_aseg_5}
								placeholder="0"
							/>
						</FormField>
					</div>
				</FormSection>

				<!-- Section: Valores Asegurados -->
				<FormSection 
					title="Valores Asegurados" 
					bind:open={sections.valores}
				>
					{#if tipoBien === 'HOGAR'}
						<div class="space-y-4">
							<FormField label="Valor Inmueble Asegurado">
								<CurrencyInput 
									bind:value={formData.valor_inmueble_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Contenidos Normales">
								<CurrencyInput 
									bind:value={formData.valor_contenidos_normales_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Contenidos Especiales">
								<CurrencyInput 
									bind:value={formData.valor_contenidos_especiales_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Equipo Electrónico">
								<CurrencyInput 
									bind:value={formData.valor_equipo_electronico_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Maquinaria y Equipo">
								<CurrencyInput 
									bind:value={formData.valor_maquinaria_equipo_asegurado}
									placeholder="0"
								/>
							</FormField>
						</div>
					{:else if tipoBien === 'VEHICULO'}
						<div class="space-y-4">
							<FormField label="Valor Vehículo Asegurado">
								<CurrencyInput 
									bind:value={formData.valor_vehiculo_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Accesorios Asegurado">
								<CurrencyInput 
									bind:value={formData.valor_accesorios_asegurado}
									placeholder="0"
								/>
							</FormField>
						</div>
					{:else if tipoBien === 'COPROPIEDAD'}
						<div class="space-y-4">
							<FormField label="Valor Área Común Asegurado">
								<CurrencyInput 
									bind:value={formData.valor_area_comun_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Área Privada Asegurado">
								<CurrencyInput 
									bind:value={formData.valor_area_privada_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Muebles y Enseres">
								<CurrencyInput 
									bind:value={formData.valor_muebles_asegurado}
									placeholder="0"
								/>
							</FormField>
							<FormField label="Valor Maquinaria y Equipo">
								<CurrencyInput 
									bind:value={formData.valor_maquinaria_equipo_asegurado}
									placeholder="0"
								/>
							</FormField>
						</div>
					{:else}
						<FormField label="Valor del Bien Asegurado">
							<CurrencyInput 
								bind:value={formData.valor_bien_asegurado}
								placeholder="0"
							/>
						</FormField>
					{/if}
				</FormSection>

				<!-- Section: Valores Financieros -->
				<FormSection 
					title="Valores Financieros (Opcional)" 
					bind:open={sections.financiero}
				>
					<p class="text-sm text-secondary-500 mb-4">
						Estos valores se llenan cuando la propuesta cambie a estado VIGENTE.
					</p>
					<div class="space-y-4">
						<FormField label="Prima Neta">
							<CurrencyInput 
								bind:value={formData.valor_prima_neta}
								placeholder="0"
							/>
						</FormField>
						<FormField label="Otros Costos">
							<CurrencyInput 
								bind:value={formData.valor_otros_costos}
								placeholder="0"
							/>
						</FormField>
						<FormField label="IVA">
							<Input 
								type="number"
								bind:value={formData.valor_iva}
								placeholder="0"
							/>
						</FormField>
						<FormField label="Ingreso Comisión Percibido">
							<CurrencyInput 
								bind:value={formData.ingreso_comision_percibido}
								placeholder="0"
							/>
						</FormField>
					</div>
				</FormSection>

				<!-- Form Actions -->
				<div class="form-actions">
					<button type="button" class="btn btn-secondary" on:click={handleCancel} disabled={saving}>
						Cancelar
					</button>
					<button type="submit" class="btn btn-primary flex items-center gap-2" disabled={saving || !selectedBienId}>
						{#if saving}
							<svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
							</svg>
							Guardando...
						{:else}
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
							</svg>
							Crear Propuesta
						{/if}
					</button>
				</div>
			</form>
		</div>
	{/if}
</div>
