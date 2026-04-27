<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select } from '$components';

	$: id = $page.params.id;

	// Form state (would be loaded from API)
	let formData = {
		nombre: '',
		codigo: '',
		rfc: '',
		razonSocial: '',
		direccion: '',
		ciudad: '',
		codigoPostal: '',
		telefono: '',
		email: '',
		sitioWeb: '',
		tipoAseguradora: '',
		fechaConstitucion: '',
		observaciones: '',
		activo: true
	};

	// Section states
	let sections = {
		general: { open: true, status: 'complete' as const },
		contacto: { open: false, status: 'complete' as const },
		adicional: { open: false, status: 'pending' as const },
		documentos: { open: false, status: 'pending' as const }
	};

	const tiposAseguradora = [
		{ value: 'vida', label: 'Vida' },
		{ value: 'danos', label: 'Daños' },
		{ value: 'salud', label: 'Salud' },
		{ value: 'autos', label: 'Autos' },
		{ value: 'multiple', label: 'Múltiple' }
	];

	function handleSubmit() {
		console.log('Form updated:', formData);
	}

	function handleCancel() {
		window.history.back();
	}
</script>

<svelte:head>
	<title>Aseguradora #{id} | {APP_NAME}</title>
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
	<div class="flex items-center gap-3">
		<span class="badge badge-success">Activo</span>
	</div>
</header>

<!-- Content -->
<div class="page-content">
	<div class="max-w-4xl mx-auto">
		<form class="form-container" on:submit|preventDefault={handleSubmit}>
			<h1 class="form-title">Editar Aseguradora #{id}</h1>

			<!-- Section: Información General -->
			<FormSection 
				title="Información General" 
				status={sections.general.status}
				bind:open={sections.general.open}
			>
				<FormField 
					label="Nombre de la aseguradora"
					helper="Nombre comercial de la compañía."
					required
				>
					<Input 
						bind:value={formData.nombre}
						placeholder="Ej: Seguros Atlas"
						required
					/>
				</FormField>

				<FormField 
					label="Código"
					helper="Código interno único de identificación."
				>
					<Input 
						bind:value={formData.codigo}
						placeholder="Ej: SEG-001"
					/>
				</FormField>

				<FormField 
					label="RFC"
					helper="Registro Federal de Contribuyentes."
				>
					<Input 
						bind:value={formData.rfc}
						placeholder="Ej: SAT850101AAA"
					/>
				</FormField>

				<FormField 
					label="Razón Social"
					helper="Nombre legal registrado de la empresa."
				>
					<Input 
						bind:value={formData.razonSocial}
						placeholder="Ej: Seguros Atlas S.A. de C.V."
					/>
				</FormField>
			</FormSection>

			<!-- Section: Información de Contacto -->
			<FormSection 
				title="Información de Contacto" 
				status={sections.contacto.status}
				bind:open={sections.contacto.open}
			>
				<FormField 
					label="Dirección completa"
					helper="Calle, número y referencias."
				>
					<Input 
						bind:value={formData.direccion}
						placeholder="Calle, número, colonia"
					/>
				</FormField>

				<FormField 
					label="Ciudad y Código Postal"
					helper="Ubicación de las oficinas principales."
				>
					<div class="form-input-row">
						<Input 
							bind:value={formData.ciudad}
							placeholder="Ciudad"
						/>
						<Input 
							bind:value={formData.codigoPostal}
							placeholder="C.P."
						/>
					</div>
				</FormField>

				<FormField 
					label="Teléfono y Email"
					helper="Datos de contacto principal."
				>
					<div class="form-input-row">
						<Input 
							type="tel"
							bind:value={formData.telefono}
							placeholder="+52 000 000 0000"
						/>
						<Input 
							type="email"
							bind:value={formData.email}
							placeholder="contacto@ejemplo.com"
						/>
					</div>
				</FormField>

				<FormField 
					label="Sitio Web"
					helper="URL del sitio web oficial."
				>
					<Input 
						type="url"
						bind:value={formData.sitioWeb}
						placeholder="https://www.ejemplo.com"
					/>
				</FormField>
			</FormSection>

			<!-- Section: Información Adicional -->
			<FormSection 
				title="Información Adicional" 
				status={sections.adicional.status}
				bind:open={sections.adicional.open}
			>
				<FormField 
					label="Tipo de Aseguradora"
					helper="Categoría principal de productos."
				>
					<Select 
						bind:value={formData.tipoAseguradora}
						options={tiposAseguradora}
						placeholder="Seleccionar tipo..."
					/>
				</FormField>

				<FormField 
					label="Fecha de Constitución"
					helper="Fecha de creación de la empresa."
				>
					<Input 
						type="date"
						bind:value={formData.fechaConstitucion}
					/>
				</FormField>

				<FormField 
					label="Observaciones"
					helper="Notas adicionales o comentarios."
				>
					<Input 
						type="textarea"
						bind:value={formData.observaciones}
						placeholder="Escriba cualquier información adicional relevante..."
					/>
				</FormField>
			</FormSection>

			<!-- Section: Documentos -->
			<FormSection 
				title="Documentos" 
				status={sections.documentos.status}
				bind:open={sections.documentos.open}
			>
				<FormField 
					label="Documentos adjuntos"
					helper="Acta constitutiva, contratos, etc."
				>
					<div class="border-2 border-dashed border-secondary-300 rounded-lg p-8 text-center">
						<p class="text-sm text-secondary-500">
							No hay documentos adjuntos
						</p>
						<button type="button" class="link-button mt-2">
							+ Agregar documento
						</button>
					</div>
				</FormField>
			</FormSection>

			<!-- Form Actions -->
			<div class="form-actions">
				<button type="button" class="btn btn-danger btn-ghost">
					Eliminar
				</button>
				<div class="flex-1"></div>
				<button type="button" class="btn btn-secondary" on:click={handleCancel}>
					Cancelar
				</button>
				<button type="submit" class="btn btn-primary">
					Guardar Cambios
				</button>
			</div>
		</form>
	</div>
</div>
