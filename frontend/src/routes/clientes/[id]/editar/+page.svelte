<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select } from '$components';
	import { clienteService } from '$services';
	import { ClienteFields } from '$constants';
	import type { UpdateClienteDto, TipoPersona } from '$lib/types/cliente';
	import { TIPOS_PERSONA, TIPOS_DOCUMENTO } from '$lib/types/cliente';

	// Alias para mayor legibilidad
	const F = ClienteFields;

	// ID del cliente desde la URL
	$: clienteId = parseInt($page.params.id || '0');

	// Form state
	let formData: UpdateClienteDto = {
		tipo_persona: 'PERSONA',
		usuario: '',
		
		// Campos comunes
		ciudad: '',
		direccion: '',
		telefono_movil: '',
		correo: '',
		
		// Campos persona natural
		nombre: '',
		tipo_documento: '',
		numero_documento: '',
		edad: undefined,
		
		// Campos empresa
		nit: '',
		razon_social: '',
		nombre_rep_legal: '',
		documento_rep_legal: '',
		telefono_rep_legal: '',
		correo_rep_legal: '',
		contacto_alternativo: ''
	};

	// UI state
	let loading = false;
	let loadingData = true;
	let error: string | null = null;
	let clienteNombre = '';

	// Section states
	let sections = {
		tipo: { open: true, status: 'active' as const },
		credenciales: { open: false, status: 'pending' as const },
		datosPersona: { open: false, status: 'pending' as const },
		datosEmpresa: { open: false, status: 'pending' as const },
		contacto: { open: false, status: 'pending' as const }
	};

	// Opciones para selects
	const tiposPersonaOptions = TIPOS_PERSONA.map(t => ({ value: t.value, label: t.label }));
	const tiposDocumentoOptions = TIPOS_DOCUMENTO.map(t => ({ value: t.value, label: t.label }));

	// Cargar datos del cliente
	onMount(async () => {
		try {
			const cliente = await clienteService.getById(clienteId);
			
			if (!cliente) {
				error = 'Cliente no encontrado';
				loadingData = false;
				return;
			}

			clienteNombre = cliente.tipo_persona === 'PERSONA' 
				? cliente.nombre || '' 
				: cliente.razon_social || '';

			// Mapear datos al formulario
			formData = {
				tipo_persona: cliente.tipo_persona,
				usuario: cliente.usuario || '',
				ciudad: cliente.ciudad || '',
				direccion: cliente.direccion || '',
				telefono_movil: cliente.telefono_movil || '',
				correo: cliente.correo || '',
				nombre: cliente.nombre || '',
				tipo_documento: cliente.tipo_documento || '',
				numero_documento: cliente.numero_documento || '',
				edad: cliente.edad,
				nit: cliente.nit || '',
				razon_social: cliente.razon_social || '',
				nombre_rep_legal: cliente.nombre_rep_legal || '',
				documento_rep_legal: cliente.documento_rep_legal || '',
				telefono_rep_legal: cliente.telefono_rep_legal || '',
				correo_rep_legal: cliente.correo_rep_legal || '',
				contacto_alternativo: cliente.contacto_alternativo || ''
			};

			// Abrir sección correspondiente
			if (cliente.tipo_persona === 'PERSONA') {
				sections.datosPersona.open = true;
			} else {
				sections.datosEmpresa.open = true;
			}

			console.log('✅ Datos cargados:', cliente);
		} catch (err) {
			console.error('❌ Error al cargar cliente:', err);
			error = err instanceof Error ? err.message : 'Error al cargar el cliente';
		} finally {
			loadingData = false;
		}
	});

	// Reactive: abrir sección correspondiente al tipo de persona
	$: if (!loadingData) {
		if (formData.tipo_persona === 'PERSONA') {
			sections.datosPersona.open = true;
			sections.datosEmpresa.open = false;
		} else {
			sections.datosPersona.open = false;
			sections.datosEmpresa.open = true;
		}
	}

	async function handleSubmit() {
		loading = true;
		error = null;

		try {
			// Construir payload con campos relevantes
			const payload: UpdateClienteDto = {
				tipo_persona: formData.tipo_persona,
				usuario: formData.usuario
			};

			// Agregar campos comunes si tienen valor
			if (formData.ciudad) payload.ciudad = formData.ciudad;
			if (formData.direccion) payload.direccion = formData.direccion;
			if (formData.telefono_movil) payload.telefono_movil = formData.telefono_movil;
			if (formData.correo) payload.correo = formData.correo;

			// Agregar campos según tipo de persona
			if (formData.tipo_persona === 'PERSONA') {
				if (formData.nombre) payload.nombre = formData.nombre;
				if (formData.tipo_documento) payload.tipo_documento = formData.tipo_documento;
				if (formData.numero_documento) payload.numero_documento = formData.numero_documento;
				if (formData.edad) payload.edad = formData.edad;
			} else {
				if (formData.razon_social) payload.razon_social = formData.razon_social;
				if (formData.nit) payload.nit = formData.nit;
				if (formData.nombre_rep_legal) payload.nombre_rep_legal = formData.nombre_rep_legal;
				if (formData.documento_rep_legal) payload.documento_rep_legal = formData.documento_rep_legal;
				if (formData.telefono_rep_legal) payload.telefono_rep_legal = formData.telefono_rep_legal;
				if (formData.correo_rep_legal) payload.correo_rep_legal = formData.correo_rep_legal;
				if (formData.contacto_alternativo) payload.contacto_alternativo = formData.contacto_alternativo;
			}

			console.log('📤 Actualizando cliente:', payload);
			
			const result = await clienteService.update(clienteId, payload);
			
			console.log('✅ Cliente actualizado:', result);
			
			goto('/clientes');
		} catch (err: unknown) {
			console.error('❌ Error al actualizar cliente:', err);
			if (err && typeof err === 'object' && 'error' in err) {
				error = (err as { error: string }).error;
			} else if (err instanceof Error) {
				error = err.message;
			} else {
				error = 'Error al actualizar el cliente';
			}
		} finally {
			loading = false;
		}
	}

	function handleCancel() {
		goto('/clientes');
	}
</script>

<svelte:head>
	<title>Editar {clienteNombre || 'Cliente'} | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<a href="/clientes" class="page-back-link">
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
		{:else if error && !formData.usuario}
			<!-- Error State -->
			<div class="form-container">
				<div class="flex items-center justify-center py-12">
					<div class="flex flex-col items-center gap-4 text-center">
						<svg class="w-12 h-12 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
						</svg>
						<p class="text-red-600 font-medium">{error}</p>
						<a href="/clientes" class="btn btn-secondary">Volver a la lista</a>
					</div>
				</div>
			</div>
		{:else}
			<form class="form-container" on:submit|preventDefault={handleSubmit}>
				<!-- Form Title -->
				<div class="form-title-section">
					<h1 class="form-title">Editar Cliente</h1>
					<p class="form-subtitle">Modifica los datos de <strong>{clienteNombre}</strong></p>
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

				<!-- Section: Tipo de Cliente -->
				<FormSection 
					title="Tipo de Cliente" 
					status={sections.tipo.status}
					bind:open={sections.tipo.open}
				>
					<FormField 
						label={F.tipo_persona.label}
						helper="Tipo de persona (no se recomienda cambiar después de crear)."
						required
					>
						<Select 
							bind:value={formData.tipo_persona}
							options={tiposPersonaOptions}
							required
							disabled={loading}
						/>
					</FormField>

					<FormField 
						label={F.usuario.label}
						helper="Nombre de usuario único para iniciar sesión."
						required
					>
						<Input 
							bind:value={formData.usuario}
							placeholder="Ej: jperez"
							required
							disabled={loading}
						/>
					</FormField>
				</FormSection>

				<!-- Section: Datos Persona Natural (solo si tipo_persona = PERSONA) -->
				{#if formData.tipo_persona === 'PERSONA'}
					<FormSection 
						title="Datos Personales" 
						status={sections.datosPersona.status}
						bind:open={sections.datosPersona.open}
					>
						<FormField 
							label={F.nombre.label}
							helper="Nombre completo como aparece en el documento de identidad."
							required
						>
							<Input 
								bind:value={formData.nombre}
								placeholder="Ej: Juan Carlos Pérez García"
								required
								disabled={loading}
							/>
						</FormField>

						<div class="grid grid-cols-2 gap-4">
							<FormField 
								label={F.tipo_documento.label}
								helper="Tipo de documento de identidad."
							>
								<Select 
									bind:value={formData.tipo_documento}
									options={tiposDocumentoOptions}
									placeholder="Seleccionar..."
									disabled={loading}
								/>
							</FormField>

							<FormField 
								label={F.numero_documento.label}
								helper="Número sin puntos ni espacios."
							>
								<Input 
									bind:value={formData.numero_documento}
									placeholder="Ej: 1234567890"
									disabled={loading}
								/>
							</FormField>
						</div>

						<FormField 
							label={F.edad.label}
							helper="Edad actual del cliente."
						>
							<Input 
								type="number"
								bind:value={formData.edad}
								placeholder="Ej: 35"
								min="18"
								max="120"
								disabled={loading}
							/>
						</FormField>
					</FormSection>
				{/if}

				<!-- Section: Datos Empresa (solo si tipo_persona = EMPRESA) -->
				{#if formData.tipo_persona === 'EMPRESA'}
					<FormSection 
						title="Datos de la Empresa" 
						status={sections.datosEmpresa.status}
						bind:open={sections.datosEmpresa.open}
					>
						<FormField 
							label={F.razon_social.label}
							helper="Nombre legal de la empresa."
							required
						>
							<Input 
								bind:value={formData.razon_social}
								placeholder="Ej: Empresa ABC S.A.S"
								required
								disabled={loading}
							/>
						</FormField>

						<FormField 
							label={F.nit.label}
							helper="Número de Identificación Tributaria."
						>
							<Input 
								bind:value={formData.nit}
								placeholder="Ej: 900123456-1"
								disabled={loading}
							/>
						</FormField>

						<div class="border-t border-secondary-200 pt-4 mt-4">
							<h4 class="text-sm font-semibold text-secondary-700 mb-4">Representante Legal</h4>
							
							<div class="grid grid-cols-2 gap-4">
								<FormField 
									label={F.nombre_rep_legal.label}
									helper="Nombre completo."
								>
									<Input 
										bind:value={formData.nombre_rep_legal}
										placeholder="Ej: María García López"
										disabled={loading}
									/>
								</FormField>

								<FormField 
									label={F.documento_rep_legal.label}
									helper="Documento de identidad."
								>
									<Input 
										bind:value={formData.documento_rep_legal}
										placeholder="Ej: 9876543210"
										disabled={loading}
									/>
								</FormField>

								<FormField 
									label={F.telefono_rep_legal.label}
									helper="Teléfono de contacto."
								>
									<Input 
										type="tel"
										bind:value={formData.telefono_rep_legal}
										placeholder="Ej: 3109876543"
										disabled={loading}
									/>
								</FormField>

								<FormField 
									label={F.correo_rep_legal.label}
									helper="Correo electrónico."
								>
									<Input 
										type="email"
										bind:value={formData.correo_rep_legal}
										placeholder="Ej: rep.legal@empresa.com"
										disabled={loading}
									/>
								</FormField>
							</div>
						</div>

						<FormField 
							label={F.contacto_alternativo.label}
							helper="Información de contacto alternativo."
						>
							<Input 
								bind:value={formData.contacto_alternativo}
								placeholder="Ej: Secretaría - 6012345678"
								disabled={loading}
							/>
						</FormField>
					</FormSection>
				{/if}

				<!-- Section: Información de Contacto -->
				<FormSection 
					title="Información de Contacto" 
					status={sections.contacto.status}
					bind:open={sections.contacto.open}
				>
					<FormField 
						label={F.correo.label}
						helper="Correo electrónico principal de contacto."
					>
						<Input 
							type="email"
							bind:value={formData.correo}
							placeholder="Ej: cliente@correo.com"
							disabled={loading}
						/>
					</FormField>

					<FormField 
						label={F.telefono_movil.label}
						helper="Número de celular con indicativo."
					>
						<Input 
							type="tel"
							bind:value={formData.telefono_movil}
							placeholder="Ej: 3001234567"
							disabled={loading}
						/>
					</FormField>

					<FormField 
						label={F.ciudad.label}
						helper="Ciudad de residencia o sede principal."
					>
						<Input 
							bind:value={formData.ciudad}
							placeholder="Ej: Bogotá"
							disabled={loading}
						/>
					</FormField>

					<FormField 
						label={F.direccion.label}
						helper="Dirección completa."
					>
						<Input 
							bind:value={formData.direccion}
							placeholder="Ej: Calle 123 #45-67, Barrio Centro"
							disabled={loading}
						/>
					</FormField>
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
						disabled={loading}
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
