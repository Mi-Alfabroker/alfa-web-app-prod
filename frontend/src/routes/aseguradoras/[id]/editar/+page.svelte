<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input } from '$components';
	import { aseguradoraService } from '$services';
	import { AseguradoraFields } from '$constants';
	import type { Aseguradora, UpdateAseguradoraDto } from '$types/aseguradora';

	// Alias para mayor legibilidad
	const F = AseguradoraFields;

	// ID de la aseguradora desde la URL
	$: aseguradoraId = parseInt($page.params.id || '0');

	// Form state - usando nombres de BD
	let formData: UpdateAseguradoraDto = {
		// Campos base
		nombre: '',
		numeral_asistencia: '',
		correo_comercial: '',
		correo_reclamaciones: '',
		direccion_oficina: '',
		contacto_asignado: '',
		respaldo_aseguradora: '',
		ruta_logo: '',
		ruta_pais_logo: '',
		
		// Copropiedad - Asistencia
		cop_asistencia_area_comun: '',
		cop_asistencia_area_privada: '',
		
		// Copropiedad - Daños Materiales
		cop_dm_deducible_terremoto: '',
		cop_dm_deducible_inundacion: '',
		cop_dm_deducible_incendio: '',
		cop_dm_deducible_amit: '',
		cop_dm_deducible_tuberia_vidrio: '',
		
		// Copropiedad - Daños Internos
		cop_di_deducible_maq_equipo: '',
		cop_di_deducible_equipo_electronico: '',
		
		// Copropiedad - Sustracción con Violencia
		cop_scv_deducible_maq_equipo: '',
		cop_scv_deducible_equipo_electronico: '',
		cop_scv_deducible_dineros: '',
		cop_scv_deducible_muebles: '',
		
		// Copropiedad - Directores & Administradores
		cop_da_deducible_amparo_basico: '',
		
		// Copropiedad - RCE Deducibles
		cop_rce_deducible_contratistas: '',
		cop_rce_deducible_cruzada: '',
		cop_rce_deducible_patronal: '',
		cop_rce_deducible_parqueaderos: '',
		cop_rce_deducible_gastos_medicos: '',
		
		// Copropiedad - RCE Sublimites
		cop_rce_sublimite_contratistas: '',
		cop_rce_sublimite_cruzada: '',
		cop_rce_sublimite_patronal: '',
		cop_rce_sublimite_parqueaderos: '',
		cop_rce_sublimite_gastos_medicos: '',
		
		// Copropiedad - Manejo
		cop_manejo_deducible_amparo_basico: '',
		
		// Copropiedad - Transporte de Valores
		cop_tv_deducible_amparo_basico: '',
		
		// Hogar - Deducibles Daños
		hog_deducible_terremoto: '',
		hog_deducible_amit: '',
		hog_deducible_demas_eventos: '',
		
		// Hogar - Hurto Contenidos Normales
		hog_hurto_cn_terremoto: '',
		hog_hurto_cn_demas_eventos: '',
		hog_hurto_cn_hurto: '',
		
		// Hogar - Hurto Contenidos Especiales
		hog_hurto_ce_hurto: '',
		
		// Hogar - Hurto Equipo Electrónico
		hog_hurto_ee_hurto: '',
		
		// Hogar - Coberturas Adicionales
		hog_cobertura_adicional_1: '',
		hog_cobertura_adicional_2: '',
		hog_cobertura_adicional_3: '',
		
		// Otros - Deducibles Daños
		otr_deducible_terremoto: '',
		otr_deducible_amit: '',
		otr_deducible_demas_eventos: '',
		
		// Otros - Deducibles Hurto
		otr_hurto_cn_deducible: '',
		otr_hurto_ce_deducible: '',
		otr_hurto_ee_deducible: '',
		
		// Otros - Coberturas Adicionales
		otr_cobertura_adicional_1: '',
		otr_cobertura_adicional_2: '',
		otr_cobertura_adicional_3: '',
		
		// Vehículos - Deducibles Pérdida
		veh_deducible_perdida_parcial: '',
		veh_deducible_perdida_total: '',
		veh_deducible_terremoto: '',
		
		// Vehículos - Deducibles Hurto
		veh_hurto_perdida_parcial: '',
		veh_hurto_perdida_total: '',
		
		// Vehículos - Deducible RC
		veh_deducible_rc: '',
		
		// Vehículos - Sublímites RC
		veh_rc_sublimite_bienes_terceros: '',
		veh_rc_sublimite_amparo_patrimonial: '',
		veh_rc_sublimite_muerte_lesion_una: '',
		veh_rc_sublimite_muerte_lesion_dos_mas: '',
		
		// Vehículos - Coberturas Adicionales
		veh_cobertura_adicional_1: '',
		veh_cobertura_adicional_2: '',
		veh_cobertura_adicional_3: '',
		veh_cobertura_adicional_4: '',
		veh_cobertura_adicional_5: '',
		veh_cobertura_adicional_6: '',
		veh_cobertura_adicional_7: ''
	};

	// UI state
	let loading = false;
	let loadingData = true;
	let error: string | null = null;
	let aseguradoraNombre = '';

	// Section states
	let sections = {
		general: { open: true, status: 'active' as const },
		contacto: { open: false, status: 'pending' as const },
		adicional: { open: false, status: 'pending' as const },
		copropiedad: { open: false, status: 'pending' as const },
		hogar: { open: false, status: 'pending' as const },
		otros: { open: false, status: 'pending' as const },
		vehiculos: { open: false, status: 'pending' as const }
	};

	// Sub-secciones de copropiedad (acordeón interno)
	let copSections = {
		asistencia: false,
		danosMateriales: false,
		danosInternos: false,
		sustraccion: false,
		directores: false,
		rceDeducibles: false,
		rceSublimites: false,
		manejo: false,
		transporte: false
	};

	// Sub-secciones de hogar (acordeón interno)
	let hogSections = {
		deduciblesDanos: false,
		hurtoContenidosNormales: false,
		hurtoContenidosEspeciales: false,
		hurtoEquipoElectronico: false,
		coberturasAdicionales: false
	};

	// Sub-secciones de otros (acordeón interno)
	let otrSections = {
		deduciblesDanos: false,
		hurtoDeducibles: false,
		coberturasAdicionales: false
	};

	// Sub-secciones de vehículos (acordeón interno)
	let vehSections = {
		deduciblesPerdida: false,
		deduciblesHurto: false,
		deducibleRc: false,
		sublimitesRc: false,
		coberturasAdicionales: false
	};

	function toggleCopSection(key: keyof typeof copSections) {
		copSections[key] = !copSections[key];
	}

	function toggleHogSection(key: keyof typeof hogSections) {
		hogSections[key] = !hogSections[key];
	}

	function toggleOtrSection(key: keyof typeof otrSections) {
		otrSections[key] = !otrSections[key];
	}

	function toggleVehSection(key: keyof typeof vehSections) {
		vehSections[key] = !vehSections[key];
	}

	// Cargar datos de la aseguradora
	onMount(async () => {
		try {
			const aseguradora = await aseguradoraService.getById(aseguradoraId);
			
			if (!aseguradora) {
				error = 'Aseguradora no encontrada';
				loadingData = false;
				return;
			}

			aseguradoraNombre = aseguradora.nombre;

			// Mapear datos al formulario (convertir null/undefined a string vacío)
			formData = {
				nombre: aseguradora.nombre || '',
				numeral_asistencia: aseguradora.numeral_asistencia || '',
				correo_comercial: aseguradora.correo_comercial || '',
				correo_reclamaciones: aseguradora.correo_reclamaciones || '',
				direccion_oficina: aseguradora.direccion_oficina || '',
				contacto_asignado: aseguradora.contacto_asignado || '',
				respaldo_aseguradora: aseguradora.respaldo_aseguradora || '',
				ruta_logo: aseguradora.ruta_logo || '',
				ruta_pais_logo: aseguradora.ruta_pais_logo || '',
				cop_asistencia_area_comun: aseguradora.cop_asistencia_area_comun || '',
				cop_asistencia_area_privada: aseguradora.cop_asistencia_area_privada || '',
				cop_dm_deducible_terremoto: aseguradora.cop_dm_deducible_terremoto || '',
				cop_dm_deducible_inundacion: aseguradora.cop_dm_deducible_inundacion || '',
				cop_dm_deducible_incendio: aseguradora.cop_dm_deducible_incendio || '',
				cop_dm_deducible_amit: aseguradora.cop_dm_deducible_amit || '',
				cop_dm_deducible_tuberia_vidrio: aseguradora.cop_dm_deducible_tuberia_vidrio || '',
				cop_di_deducible_maq_equipo: aseguradora.cop_di_deducible_maq_equipo || '',
				cop_di_deducible_equipo_electronico: aseguradora.cop_di_deducible_equipo_electronico || '',
				cop_scv_deducible_maq_equipo: aseguradora.cop_scv_deducible_maq_equipo || '',
				cop_scv_deducible_equipo_electronico: aseguradora.cop_scv_deducible_equipo_electronico || '',
				cop_scv_deducible_dineros: aseguradora.cop_scv_deducible_dineros || '',
				cop_scv_deducible_muebles: aseguradora.cop_scv_deducible_muebles || '',
				cop_da_deducible_amparo_basico: aseguradora.cop_da_deducible_amparo_basico || '',
				cop_rce_deducible_contratistas: aseguradora.cop_rce_deducible_contratistas || '',
				cop_rce_deducible_cruzada: aseguradora.cop_rce_deducible_cruzada || '',
				cop_rce_deducible_patronal: aseguradora.cop_rce_deducible_patronal || '',
				cop_rce_deducible_parqueaderos: aseguradora.cop_rce_deducible_parqueaderos || '',
				cop_rce_deducible_gastos_medicos: aseguradora.cop_rce_deducible_gastos_medicos || '',
				cop_rce_sublimite_contratistas: aseguradora.cop_rce_sublimite_contratistas || '',
				cop_rce_sublimite_cruzada: aseguradora.cop_rce_sublimite_cruzada || '',
				cop_rce_sublimite_patronal: aseguradora.cop_rce_sublimite_patronal || '',
				cop_rce_sublimite_parqueaderos: aseguradora.cop_rce_sublimite_parqueaderos || '',
				cop_rce_sublimite_gastos_medicos: aseguradora.cop_rce_sublimite_gastos_medicos || '',
				cop_manejo_deducible_amparo_basico: aseguradora.cop_manejo_deducible_amparo_basico || '',
				cop_tv_deducible_amparo_basico: aseguradora.cop_tv_deducible_amparo_basico || '',
				// Hogar
				hog_deducible_terremoto: aseguradora.hog_deducible_terremoto || '',
				hog_deducible_amit: aseguradora.hog_deducible_amit || '',
				hog_deducible_demas_eventos: aseguradora.hog_deducible_demas_eventos || '',
				hog_hurto_cn_terremoto: aseguradora.hog_hurto_cn_terremoto || '',
				hog_hurto_cn_demas_eventos: aseguradora.hog_hurto_cn_demas_eventos || '',
				hog_hurto_cn_hurto: aseguradora.hog_hurto_cn_hurto || '',
				hog_hurto_ce_hurto: aseguradora.hog_hurto_ce_hurto || '',
				hog_hurto_ee_hurto: aseguradora.hog_hurto_ee_hurto || '',
				hog_cobertura_adicional_1: aseguradora.hog_cobertura_adicional_1 || '',
				hog_cobertura_adicional_2: aseguradora.hog_cobertura_adicional_2 || '',
				hog_cobertura_adicional_3: aseguradora.hog_cobertura_adicional_3 || '',
				// Otros
				otr_deducible_terremoto: aseguradora.otr_deducible_terremoto || '',
				otr_deducible_amit: aseguradora.otr_deducible_amit || '',
				otr_deducible_demas_eventos: aseguradora.otr_deducible_demas_eventos || '',
				otr_hurto_cn_deducible: aseguradora.otr_hurto_cn_deducible || '',
				otr_hurto_ce_deducible: aseguradora.otr_hurto_ce_deducible || '',
				otr_hurto_ee_deducible: aseguradora.otr_hurto_ee_deducible || '',
				otr_cobertura_adicional_1: aseguradora.otr_cobertura_adicional_1 || '',
				otr_cobertura_adicional_2: aseguradora.otr_cobertura_adicional_2 || '',
			otr_cobertura_adicional_3: aseguradora.otr_cobertura_adicional_3 || '',
			// Vehículos
			veh_deducible_perdida_parcial: aseguradora.veh_deducible_perdida_parcial || '',
			veh_deducible_perdida_total: aseguradora.veh_deducible_perdida_total || '',
			veh_deducible_terremoto: aseguradora.veh_deducible_terremoto || '',
			veh_hurto_perdida_parcial: aseguradora.veh_hurto_perdida_parcial || '',
			veh_hurto_perdida_total: aseguradora.veh_hurto_perdida_total || '',
			veh_deducible_rc: aseguradora.veh_deducible_rc || '',
			veh_rc_sublimite_bienes_terceros: aseguradora.veh_rc_sublimite_bienes_terceros || '',
			veh_rc_sublimite_amparo_patrimonial: aseguradora.veh_rc_sublimite_amparo_patrimonial || '',
			veh_rc_sublimite_muerte_lesion_una: aseguradora.veh_rc_sublimite_muerte_lesion_una || '',
			veh_rc_sublimite_muerte_lesion_dos_mas: aseguradora.veh_rc_sublimite_muerte_lesion_dos_mas || '',
			veh_cobertura_adicional_1: aseguradora.veh_cobertura_adicional_1 || '',
			veh_cobertura_adicional_2: aseguradora.veh_cobertura_adicional_2 || '',
			veh_cobertura_adicional_3: aseguradora.veh_cobertura_adicional_3 || '',
			veh_cobertura_adicional_4: aseguradora.veh_cobertura_adicional_4 || '',
			veh_cobertura_adicional_5: aseguradora.veh_cobertura_adicional_5 || '',
			veh_cobertura_adicional_6: aseguradora.veh_cobertura_adicional_6 || '',
			veh_cobertura_adicional_7: aseguradora.veh_cobertura_adicional_7 || ''
			};

			console.log('✅ Datos cargados:', aseguradora);
		} catch (err) {
			console.error('❌ Error al cargar aseguradora:', err);
			error = err instanceof Error ? err.message : 'Error al cargar la aseguradora';
		} finally {
			loadingData = false;
		}
	});

	async function handleSubmit() {
		loading = true;
		error = null;

		try {
			// Filtrar campos vacíos antes de enviar
			const payload: UpdateAseguradoraDto = Object.fromEntries(
				Object.entries(formData).filter(([_, value]) => value !== '' && value !== null)
			) as UpdateAseguradoraDto;

			console.log('📤 Actualizando aseguradora:', payload);
			
			const result = await aseguradoraService.update(aseguradoraId, payload);
			
			console.log('✅ Aseguradora actualizada:', result);
			
			// Redirigir a la lista de aseguradoras
			goto('/aseguradoras');
		} catch (err) {
			console.error('❌ Error al actualizar aseguradora:', err);
			error = err instanceof Error ? err.message : 'Error al actualizar la aseguradora';
		} finally {
			loading = false;
		}
	}

	function handleCancel() {
		goto('/aseguradoras');
	}
</script>

<svelte:head>
	<title>Editar {aseguradoraNombre || 'Aseguradora'} | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<a href="/aseguradoras" class="page-back-link">
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
		{#if loadingData}
			<!-- Loading State -->
			<div class="form-container">
				<div class="flex items-center justify-center py-12">
					<div class="flex flex-col items-center gap-4">
						<svg class="animate-spin h-8 w-8 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
						</svg>
						<p class="text-secondary-600">Cargando datos...</p>
					</div>
				</div>
			</div>
		{:else if error && !formData.nombre}
			<!-- Error State -->
			<div class="form-container">
				<div class="flex items-center justify-center py-12">
					<div class="flex flex-col items-center gap-4 text-center">
						<svg class="w-12 h-12 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
						</svg>
						<p class="text-red-600 font-medium">{error}</p>
						<a href="/aseguradoras" class="btn btn-secondary">Volver a la lista</a>
					</div>
				</div>
			</div>
		{:else}
			<form class="form-container" on:submit|preventDefault={handleSubmit}>
				<!-- Form Title -->
				<div class="form-title-section">
					<h1 class="form-title">Editar Aseguradora</h1>
					<p class="form-subtitle">Modifica los datos de <strong>{aseguradoraNombre}</strong></p>
				</div>

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

				<!-- Section: Información General -->
				<FormSection 
					title="Información General" 
					status={sections.general.status}
					bind:open={sections.general.open}
				>
					<FormField label={F.nombre.label} helper="Nombre oficial de la compañía aseguradora." required>
						<Input bind:value={formData.nombre} placeholder="Ej: Seguros Alfa S.A." disabled={loading} />
					</FormField>
					
					<FormField label={F.respaldo_aseguradora.label} helper="Grupo financiero o entidad de respaldo.">
						<Input bind:value={formData.respaldo_aseguradora} placeholder="Ej: Grupo Financiero Alfa" disabled={loading} />
					</FormField>
				</FormSection>

				<!-- Section: Información de Contacto -->
				<FormSection 
					title="Información de Contacto" 
					status={sections.contacto.status}
					bind:open={sections.contacto.open}
				>
					<FormField label={F.numeral_asistencia.label} helper="Línea telefónica de asistencia 24/7.">
						<Input bind:value={formData.numeral_asistencia} placeholder="Ej: 800-123-4567" disabled={loading} />
					</FormField>
					
					<FormField label={F.correo_comercial.label} helper="Email para cotizaciones y consultas comerciales.">
						<Input type="email" bind:value={formData.correo_comercial} placeholder="Ej: comercial@aseguradora.com" disabled={loading} />
					</FormField>
					
					<FormField label={F.correo_reclamaciones.label} helper="Email para reportar siniestros y reclamaciones.">
						<Input type="email" bind:value={formData.correo_reclamaciones} placeholder="Ej: reclamaciones@aseguradora.com" disabled={loading} />
					</FormField>
					
					<FormField label={F.direccion_oficina.label} helper="Dirección de la oficina principal.">
						<Input bind:value={formData.direccion_oficina} placeholder="Ej: Av. Principal 123, Ciudad" disabled={loading} />
					</FormField>
					
					<FormField label={F.contacto_asignado.label} helper="Nombre del ejecutivo de cuenta asignado.">
						<Input bind:value={formData.contacto_asignado} placeholder="Ej: Juan Pérez" disabled={loading} />
					</FormField>
				</FormSection>

				<!-- Section: Información Adicional -->
				<FormSection 
					title="Información Adicional" 
					status={sections.adicional.status}
					bind:open={sections.adicional.open}
				>
					<FormField label={F.ruta_logo.label} helper="URL o ruta del logotipo de la aseguradora.">
						<Input bind:value={formData.ruta_logo} placeholder="Ej: /logos/aseguradora.png" disabled={loading} />
					</FormField>
					
					<FormField label={F.ruta_pais_logo.label} helper="URL o ruta de la bandera del país de origen.">
						<Input bind:value={formData.ruta_pais_logo} placeholder="Ej: /logos/flags/co.png" disabled={loading} />
					</FormField>
				</FormSection>

				<!-- Section: Configuración Copropiedad -->
				<FormSection 
					title="Configuración Copropiedad" 
					status={sections.copropiedad.status}
					bind:open={sections.copropiedad.open}
				>
					<!-- Explicación del formato -->
					<div class="bg-secondary-50 border border-secondary-200 rounded-lg p-4 mb-4">
						<p class="text-sm font-medium text-secondary-700 mb-2">Formato de los campos:</p>
						<div class="text-xs text-secondary-600 space-y-2">
							<p><strong>Asistencia:</strong> Lista de de la cantidad de servicios separados por coma <b>[totales,vidrieria,plomeria,cerrajeria,electricista]</b> (ej: 15,5,6,4,3)</p>
							<div>
								<p><strong>Deducibles/Sublímites:</strong> <code class="bg-white px-1.5 py-0.5 rounded font-mono">porcentaje,tipo,mínimo</code></p>
								<ul class="mt-1 ml-4 space-y-0.5">
									<li>• <strong>porcentaje:</strong> valor numérico (ej: 1, 3)</li>
									<li>• <strong>tipo:</strong> tipo de cálculo → <code class="bg-white px-1 rounded">Ej: Valor asegurable</code></li>
									<li>• <strong>mínimo:</strong> valor en SMMLV (ej: 2) o <code class="bg-white px-1 rounded">null</code></li>
								</ul>
							</div>
						</div>
					</div>

					<!-- Sub-section: Asistencia -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('asistencia')}
						>
							<span>Asistencia</span>
							<svg class="w-5 h-5 transition-transform {copSections.asistencia ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.asistencia}
							<div class="cop-subsection-content">
								<FormField label={F.cop_asistencia_area_comun.label} helper="Servicios incluidos para áreas comunes del edificio.">
									<Input bind:value={formData.cop_asistencia_area_comun} placeholder="totales,vidrieria,plomeria,cerrajeria,electricista" disabled={loading} />
								</FormField>
								<FormField label={F.cop_asistencia_area_privada.label} helper="Servicios incluidos para unidades privadas.">
									<Input bind:value={formData.cop_asistencia_area_privada} placeholder="totales,vidrieria,plomeria,cerrajeria,electricista" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Daños Materiales -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('danosMateriales')}
						>
							<span>Daños Materiales</span>
							<svg class="w-5 h-5 transition-transform {copSections.danosMateriales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.danosMateriales}
							<div class="cop-subsection-content">
								<FormField label={F.cop_dm_deducible_terremoto.label} helper="3,Valor asegurable,38 SMMLV">
									<Input bind:value={formData.cop_dm_deducible_terremoto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_dm_deducible_inundacion.label} helper="2,Valor asegurable,23 SMMLV">
									<Input bind:value={formData.cop_dm_deducible_inundacion} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_dm_deducible_incendio.label} helper="10,Valor asegurable,15 SMMLV">
									<Input bind:value={formData.cop_dm_deducible_incendio} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_dm_deducible_amit.label} helper="10,Valor asegurable,12 SMMLV">
									<Input bind:value={formData.cop_dm_deducible_amit} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_dm_deducible_tuberia_vidrio.label} helper="10,Valor asegurable,8 SMMLV">
									<Input bind:value={formData.cop_dm_deducible_tuberia_vidrio} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Daños Internos -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('danosInternos')}
						>
							<span>Daños Internos</span>
							<svg class="w-5 h-5 transition-transform {copSections.danosInternos ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.danosInternos}
							<div class="cop-subsection-content">
								<FormField label={F.cop_di_deducible_maq_equipo.label} helper="10,Valor asegurable,4 SMMLV">
									<Input bind:value={formData.cop_di_deducible_maq_equipo} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_di_deducible_equipo_electronico.label} helper="10,Valor asegurable,4 SMMLV">
									<Input bind:value={formData.cop_di_deducible_equipo_electronico} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Sustracción con Violencia -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('sustraccion')}
						>
							<span>Sustracción con Violencia</span>
							<svg class="w-5 h-5 transition-transform {copSections.sustraccion ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.sustraccion}
							<div class="cop-subsection-content">
								<FormField label={F.cop_scv_deducible_maq_equipo.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_scv_deducible_maq_equipo} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_scv_deducible_equipo_electronico.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_scv_deducible_equipo_electronico} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_scv_deducible_dineros.label} helper="10,Valor asegurable,1 SMMLV">
									<Input bind:value={formData.cop_scv_deducible_dineros} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_scv_deducible_muebles.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_scv_deducible_muebles} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Directores & Administradores -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('directores')}
						>
							<span>Directores y Administradores</span>
							<svg class="w-5 h-5 transition-transform {copSections.directores ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.directores}
							<div class="cop-subsection-content">
								<FormField label={F.cop_da_deducible_amparo_basico.label} helper="10,Valor asegurable,4 SMMLV">
									<Input bind:value={formData.cop_da_deducible_amparo_basico} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: RCE Deducibles -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('rceDeducibles')}
						>
							<span>RCE - Deducibles</span>
							<svg class="w-5 h-5 transition-transform {copSections.rceDeducibles ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.rceDeducibles}
							<div class="cop-subsection-content">
								<FormField label={F.cop_rce_deducible_contratistas.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_rce_deducible_contratistas} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_deducible_cruzada.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_rce_deducible_cruzada} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_deducible_patronal.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_rce_deducible_patronal} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_deducible_parqueaderos.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_rce_deducible_parqueaderos} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_deducible_gastos_medicos.label} helper="0,Valor asegurable,1 SMMLV">
									<Input bind:value={formData.cop_rce_deducible_gastos_medicos} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: RCE Sublimites -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('rceSublimites')}
						>
							<span>RCE - Sublímites</span>
							<svg class="w-5 h-5 transition-transform {copSections.rceSublimites ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.rceSublimites}
							<div class="cop-subsection-content">
								<FormField label={F.cop_rce_sublimite_contratistas.label} helper="30,Valor asegurable por evento,null">
									<Input bind:value={formData.cop_rce_sublimite_contratistas} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_sublimite_cruzada.label} helper="30,Valor asegurable por evento,null">
									<Input bind:value={formData.cop_rce_sublimite_cruzada} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_sublimite_patronal.label} helper="30,Valor asegurable por evento,null">
									<Input bind:value={formData.cop_rce_sublimite_patronal} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_sublimite_parqueaderos.label} helper="20,Valor asegurable por evento,null">
									<Input bind:value={formData.cop_rce_sublimite_parqueaderos} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label={F.cop_rce_sublimite_gastos_medicos.label} helper="10,Valor asegurable por evento,null">
									<Input bind:value={formData.cop_rce_sublimite_gastos_medicos} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Manejo -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('manejo')}
						>
							<span>Manejo</span>
							<svg class="w-5 h-5 transition-transform {copSections.manejo ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.manejo}
							<div class="cop-subsection-content">
								<FormField label={F.cop_manejo_deducible_amparo_basico.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_manejo_deducible_amparo_basico} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Transporte de Valores -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleCopSection('transporte')}
						>
							<span>Transporte de Valores</span>
							<svg class="w-5 h-5 transition-transform {copSections.transporte ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if copSections.transporte}
							<div class="cop-subsection-content">
								<FormField label={F.cop_tv_deducible_amparo_basico.label} helper="10,Valor asegurable,2 SMMLV">
									<Input bind:value={formData.cop_tv_deducible_amparo_basico} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>
				</FormSection>

				<!-- Section: Configuración Hogar -->
				<FormSection 
					title="Configuración Hogar" 
					status={sections.hogar.status}
					bind:open={sections.hogar.open}
				>
					<div class="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
						<h4 class="text-sm font-semibold text-blue-900 mb-2">📝 Formato de Campos</h4>
						<p class="text-xs text-blue-700">
							Todos los campos de deducibles usan el formato:
							<code class="bg-blue-100 px-2 py-1 rounded">porcentaje,tipo,minimo</code>
						</p>
						<p class="text-xs text-blue-600 mt-2">
							Ejemplo: <code class="bg-blue-100 px-2 py-1 rounded">10,Valor asegurable,500000</code>
						</p>
					</div>

					<!-- Sub-section: Deducibles Daños -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleHogSection('deduciblesDanos')}
						>
							<span>Deducibles Daños</span>
							<svg class="w-5 h-5 transition-transform {hogSections.deduciblesDanos ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if hogSections.deduciblesDanos}
							<div class="cop-subsection-content">
								<FormField label="Deducible Terremoto" helper="Ej: 3,Valor asegurable,500000">
									<Input bind:value={formData.hog_deducible_terremoto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Deducible AMIT" helper="Ej: 10,Valor asegurable,300000">
									<Input bind:value={formData.hog_deducible_amit} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Deducible Demás Eventos" helper="Ej: 10,Valor asegurable,200000">
									<Input bind:value={formData.hog_deducible_demas_eventos} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Hurto Contenidos Normales -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleHogSection('hurtoContenidosNormales')}
						>
							<span>Hurto Contenidos Normales</span>
							<svg class="w-5 h-5 transition-transform {hogSections.hurtoContenidosNormales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if hogSections.hurtoContenidosNormales}
							<div class="cop-subsection-content">
								<FormField label="Hurto CN - Terremoto" helper="Ej: 10,Valor asegurable,100000">
									<Input bind:value={formData.hog_hurto_cn_terremoto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Hurto CN - Demás Eventos" helper="Ej: 10,Valor asegurable,100000">
									<Input bind:value={formData.hog_hurto_cn_demas_eventos} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Hurto CN - Hurto" helper="Ej: 10,Valor asegurable,150000">
									<Input bind:value={formData.hog_hurto_cn_hurto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Hurto Contenidos Especiales -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleHogSection('hurtoContenidosEspeciales')}
						>
							<span>Hurto Contenidos Especiales</span>
							<svg class="w-5 h-5 transition-transform {hogSections.hurtoContenidosEspeciales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if hogSections.hurtoContenidosEspeciales}
							<div class="cop-subsection-content">
								<FormField label="Hurto CE - Hurto" helper="Ej: 10,Valor asegurable,200000">
									<Input bind:value={formData.hog_hurto_ce_hurto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Hurto Equipo Electrónico -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleHogSection('hurtoEquipoElectronico')}
						>
							<span>Hurto Equipo Electrónico</span>
							<svg class="w-5 h-5 transition-transform {hogSections.hurtoEquipoElectronico ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if hogSections.hurtoEquipoElectronico}
							<div class="cop-subsection-content">
								<FormField label="Hurto EE - Hurto" helper="Ej: 10,Valor asegurable,150000">
									<Input bind:value={formData.hog_hurto_ee_hurto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Coberturas Adicionales -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleHogSection('coberturasAdicionales')}
						>
							<span>Coberturas Adicionales</span>
							<svg class="w-5 h-5 transition-transform {hogSections.coberturasAdicionales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if hogSections.coberturasAdicionales}
							<div class="cop-subsection-content">
								<FormField label="Cobertura Adicional 1" helper="Descripción de cobertura adicional opcional">
									<Input bind:value={formData.hog_cobertura_adicional_1} placeholder="Ej: Responsabilidad Civil Familiar" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 2" helper="Descripción de cobertura adicional opcional">
									<Input bind:value={formData.hog_cobertura_adicional_2} placeholder="Ej: Servicio de cerrajería" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 3" helper="Descripción de cobertura adicional opcional">
									<Input bind:value={formData.hog_cobertura_adicional_3} placeholder="Ej: Daños estéticos" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>
				</FormSection>

				<!-- Sección: Configuración Otros -->
				<FormSection 
					title="Configuración Otros" 
					description="Deducibles y coberturas para otros tipos de seguros"
					bind:open={sections.otros.open}
					collapsible
				>
					<!-- Sub-section: Deducibles Daños -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleOtrSection('deduciblesDanos')}
						>
							<span>Deducibles Daños</span>
							<svg class="w-5 h-5 transition-transform {otrSections.deduciblesDanos ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if otrSections.deduciblesDanos}
							<div class="cop-subsection-content">
								<FormField label="Deducible Terremoto" helper="Ej: 10,Valor asegurable,500000">
									<Input bind:value={formData.otr_deducible_terremoto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Deducible AMIT" helper="Ej: 10,Valor asegurable,300000">
									<Input bind:value={formData.otr_deducible_amit} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Deducible Demás Eventos" helper="Ej: 10,Valor asegurable,200000">
									<Input bind:value={formData.otr_deducible_demas_eventos} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Deducibles Hurto -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleOtrSection('hurtoDeducibles')}
						>
							<span>Deducibles Hurto</span>
							<svg class="w-5 h-5 transition-transform {otrSections.hurtoDeducibles ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if otrSections.hurtoDeducibles}
							<div class="cop-subsection-content">
								<FormField label="Hurto CN - Deducible" helper="Ej: 10,Valor asegurable,100000">
									<Input bind:value={formData.otr_hurto_cn_deducible} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Hurto CE - Deducible" helper="Ej: 10,Valor asegurable,150000">
									<Input bind:value={formData.otr_hurto_ce_deducible} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Hurto EE - Deducible" helper="Ej: 10,Valor asegurable,150000">
									<Input bind:value={formData.otr_hurto_ee_deducible} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Coberturas Adicionales -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleOtrSection('coberturasAdicionales')}
						>
							<span>Coberturas Adicionales</span>
							<svg class="w-5 h-5 transition-transform {otrSections.coberturasAdicionales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if otrSections.coberturasAdicionales}
							<div class="cop-subsection-content">
								<FormField label="Cobertura Adicional 1" helper="Descripción de cobertura adicional opcional">
									<Input bind:value={formData.otr_cobertura_adicional_1} placeholder="Ej: Cobertura especial 1" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 2" helper="Descripción de cobertura adicional opcional">
									<Input bind:value={formData.otr_cobertura_adicional_2} placeholder="Ej: Cobertura especial 2" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 3" helper="Descripción de cobertura adicional opcional">
									<Input bind:value={formData.otr_cobertura_adicional_3} placeholder="Ej: Cobertura especial 3" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>
				</FormSection>

				<!-- Configuración Vehículos -->
				<FormSection 
					title="Configuración Vehículos" 
					description="Valores por defecto para pólizas de vehículos"
					collapsible 
					bind:open={sections.vehiculos.open}
					status={sections.vehiculos.status}
				>
					<!-- Sub-section: Deducibles Pérdida -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleVehSection('deduciblesPerdida')}
						>
							<span>Deducibles Pérdida</span>
							<svg class="w-5 h-5 transition-transform {vehSections.deduciblesPerdida ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if vehSections.deduciblesPerdida}
							<div class="cop-subsection-content">
								<FormField label="Pérdida Parcial" helper="Ej: 10,Valor asegurable,500000">
									<Input bind:value={formData.veh_deducible_perdida_parcial} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Pérdida Total" helper="Ej: 10,Valor asegurable,1000000">
									<Input bind:value={formData.veh_deducible_perdida_total} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Terremoto" helper="Ej: 10,Valor asegurable,1000000">
									<Input bind:value={formData.veh_deducible_terremoto} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Deducibles Hurto -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleVehSection('deduciblesHurto')}
						>
							<span>Deducibles Hurto</span>
							<svg class="w-5 h-5 transition-transform {vehSections.deduciblesHurto ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if vehSections.deduciblesHurto}
							<div class="cop-subsection-content">
								<FormField label="Hurto Pérdida Parcial" helper="Ej: 10,Valor asegurable,500000">
									<Input bind:value={formData.veh_hurto_perdida_parcial} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
								<FormField label="Hurto Pérdida Total" helper="Ej: 20,Valor asegurable,3000000">
									<Input bind:value={formData.veh_hurto_perdida_total} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Deducible RC -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleVehSection('deducibleRc')}
						>
							<span>Deducible RC</span>
							<svg class="w-5 h-5 transition-transform {vehSections.deducibleRc ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if vehSections.deducibleRc}
							<div class="cop-subsection-content">
								<FormField label="Deducible RC" helper="Ej: 10,Valor asegurado,500000">
									<Input bind:value={formData.veh_deducible_rc} placeholder="porcentaje,tipo,minimo" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Sublímites RC -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleVehSection('sublimitesRc')}
						>
							<span>Sublímites RC</span>
							<svg class="w-5 h-5 transition-transform {vehSections.sublimitesRc ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if vehSections.sublimitesRc}
							<div class="cop-subsection-content">
								<FormField label="Bienes a Terceros" helper="Valor en COP sin decimales">
									<Input bind:value={formData.veh_rc_sublimite_bienes_terceros} placeholder="Ej: 50000000" disabled={loading} />
								</FormField>
								<FormField label="Amparo Patrimonial" helper="Valor en COP sin decimales">
									<Input bind:value={formData.veh_rc_sublimite_amparo_patrimonial} placeholder="Ej: 100000000" disabled={loading} />
								</FormField>
								<FormField label="Muerte/Lesión (1 persona)" helper="Valor en COP sin decimales">
									<Input bind:value={formData.veh_rc_sublimite_muerte_lesion_una} placeholder="Ej: 200000000" disabled={loading} />
								</FormField>
								<FormField label="Muerte/Lesión (2+ personas)" helper="Valor en COP sin decimales">
									<Input bind:value={formData.veh_rc_sublimite_muerte_lesion_dos_mas} placeholder="Ej: 500000000" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>

					<!-- Sub-section: Coberturas Adicionales -->
					<div class="cop-subsection">
						<button 
							type="button"
							class="cop-subsection-header"
							on:click={() => toggleVehSection('coberturasAdicionales')}
						>
							<span>Coberturas Adicionales</span>
							<svg class="w-5 h-5 transition-transform {vehSections.coberturasAdicionales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</button>
						{#if vehSections.coberturasAdicionales}
							<div class="cop-subsection-content">
								<FormField label="Cobertura Adicional 1 (RC Voluntaria)" helper="SI / NO o descripción">
									<Input bind:value={formData.veh_cobertura_adicional_1} placeholder="Ej: SI" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 2 (Daños Ocupantes)" helper="SI / NO o descripción">
									<Input bind:value={formData.veh_cobertura_adicional_2} placeholder="Ej: SI" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 3 (Asistencia Viaje)" helper="SI / NO o descripción">
									<Input bind:value={formData.veh_cobertura_adicional_3} placeholder="Ej: SI" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 4 (Vehículo Reemplazo)" helper="SI / NO o descripción">
									<Input bind:value={formData.veh_cobertura_adicional_4} placeholder="Ej: NO" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 5 (Exención Deducible)" helper="SI / NO o descripción">
									<Input bind:value={formData.veh_cobertura_adicional_5} placeholder="Ej: NO" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 6 (Accidentes Conductor)" helper="SI / NO o descripción">
									<Input bind:value={formData.veh_cobertura_adicional_6} placeholder="Ej: SI" disabled={loading} />
								</FormField>
								<FormField label="Cobertura Adicional 7 (Eventos Naturaleza)" helper="SI / NO o descripción">
									<Input bind:value={formData.veh_cobertura_adicional_7} placeholder="Ej: NO" disabled={loading} />
								</FormField>
							</div>
						{/if}
					</div>
				</FormSection>

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
						disabled={loading || !formData.nombre}
					>
						{#if loading}
							<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							Guardando...
						{:else}
							Guardar Cambios
						{/if}
					</button>
				</div>
			</form>
		{/if}
	</div>
</div>
