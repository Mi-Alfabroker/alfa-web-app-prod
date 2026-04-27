<script lang="ts">
	import { APP_NAME } from '$lib/config';
	import { FormSection, FormField, Input, Select } from '$components';

	// Form state
	let formData = {
		// Información de la Propuesta
		titulo: '',
		cliente: '',
		aseguradora: '',
		tipoSeguro: '',
		fechaInicio: '',
		fechaFin: '',
		
		// Detalles
		primaTotal: '',
		comision: '',
		
		// Observaciones
		descripcion: '',
		observaciones: ''
	};

	// Section states
	let sections = {
		propuesta: { open: true, status: 'active' as const },
		detalles: { open: false, status: 'pending' as const },
		observaciones: { open: false, status: 'pending' as const },
		documentos: { open: false, status: 'pending' as const }
	};

	const tiposSeguro = [
		{ value: 'vida', label: 'Vida' },
		{ value: 'auto', label: 'Automóvil' },
		{ value: 'hogar', label: 'Hogar' },
		{ value: 'salud', label: 'Salud' },
		{ value: 'empresarial', label: 'Empresarial' }
	];

	function handleSubmit() {
		console.log('Form submitted:', formData);
	}

	function handleCancel() {
		window.history.back();
	}
</script>

<svelte:head>
	<title>Nueva Propuesta | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<a href="/propuestas" class="page-back-link">
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
			<h1 class="form-title">Nueva Propuesta de Seguro</h1>

			<!-- Section: Información de la Propuesta -->
			<FormSection 
				title="Información de la Propuesta" 
				status={sections.propuesta.status}
				bind:open={sections.propuesta.open}
			>
				<FormField 
					label="Título de la propuesta"
					helper="Nombre descriptivo para identificar la propuesta."
					required
				>
					<Input 
						bind:value={formData.titulo}
						placeholder="Ej: Seguro de vida para Juan Pérez"
						required
					/>
				</FormField>

				<FormField 
					label="Cliente"
					helper="Seleccione el cliente asociado."
					required
				>
					<Select 
						bind:value={formData.cliente}
						options={[]}
						placeholder="Buscar cliente..."
					/>
				</FormField>

				<FormField 
					label="Aseguradora"
					helper="Compañía de seguros."
					required
				>
					<Select 
						bind:value={formData.aseguradora}
						options={[]}
						placeholder="Seleccionar aseguradora..."
					/>
				</FormField>

				<FormField 
					label="Tipo de Seguro"
					helper="Categoría del producto."
				>
					<Select 
						bind:value={formData.tipoSeguro}
						options={tiposSeguro}
						placeholder="Seleccionar tipo..."
					/>
				</FormField>

				<FormField 
					label="Vigencia"
					helper="Período de cobertura del seguro."
				>
					<div class="form-input-row">
						<Input 
							type="date"
							bind:value={formData.fechaInicio}
						/>
						<Input 
							type="date"
							bind:value={formData.fechaFin}
						/>
					</div>
				</FormField>
			</FormSection>

			<!-- Section: Detalles Financieros -->
			<FormSection 
				title="Detalles Financieros" 
				status={sections.detalles.status}
				bind:open={sections.detalles.open}
			>
				<FormField 
					label="Prima Total"
					helper="Monto total de la prima."
				>
					<Input 
						type="number"
						bind:value={formData.primaTotal}
						placeholder="0.00"
					/>
				</FormField>

				<FormField 
					label="Comisión"
					helper="Porcentaje o monto de comisión."
				>
					<Input 
						type="number"
						bind:value={formData.comision}
						placeholder="0.00"
					/>
				</FormField>
			</FormSection>

			<!-- Section: Observaciones -->
			<FormSection 
				title="Observaciones" 
				status={sections.observaciones.status}
				bind:open={sections.observaciones.open}
			>
				<FormField 
					label="Descripción"
					helper="Detalles de la propuesta."
				>
					<Input 
						type="textarea"
						bind:value={formData.descripcion}
						placeholder="Describa los detalles de la propuesta..."
					/>
				</FormField>

				<FormField 
					label="Observaciones"
					helper="Notas internas."
				>
					<Input 
						type="textarea"
						bind:value={formData.observaciones}
						placeholder="Notas adicionales..."
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
					helper="Cotizaciones, pólizas, etc."
				>
					<div class="border-2 border-dashed border-secondary-300 rounded-lg p-8 text-center">
						<div class="text-secondary-400 mb-2">
							<svg class="w-10 h-10 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" 
									d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
							</svg>
						</div>
						<p class="text-sm text-secondary-500 mb-2">
							Arrastra archivos aquí o
						</p>
						<button type="button" class="link-button">
							selecciona desde tu computadora
						</button>
					</div>
				</FormField>
			</FormSection>

			<!-- Form Actions -->
			<div class="form-actions">
				<button type="button" class="btn btn-secondary" on:click={handleCancel}>
					Cancelar
				</button>
				<button type="submit" class="btn btn-primary">
					Guardar Propuesta
				</button>
			</div>
		</form>
	</div>
</div>
