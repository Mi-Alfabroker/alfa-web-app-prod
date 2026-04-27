<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { FormField, FormSection, CurrencyInput, Select, Modal, SeccionEntrega } from '$components';
	import { polizaService, bienService, clienteService, aseguradoraService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import type { PolizaHogar, UpdatePolizaHogarDto, EstadoPoliza, CambiarEstadoDto } from '$lib/types/poliza';
	import type { Hogar } from '$lib/types/bien';
	import type { Cliente } from '$lib/types/cliente';
	import type { Aseguradora } from '$lib/types/aseguradora';

	// Route params
	$: polizaId = Number($page.params.id);

	// Data state
	let poliza: (PolizaHogar & Record<string, any>) | null = null;
	let hogar: Hogar | null = null;
	let cliente: Cliente | null = null;
	let aseguradoras: Aseguradora[] = [];

	// UI state
	let loading = true;
	let saving = false;
	let error: string | null = null;
	let editMode = false;

	// Form data
	let formData: UpdatePolizaHogarDto & Record<string, any> = {};

	// Estado modal
	let showEstadoModal = false;
	let nuevoEstado: EstadoPoliza = 'VIGENTE';
	let aseguradoraSeleccionada: number = 1;

	// Opciones de estado
	const estadosOptions = [
		{ value: 'PROSPECTO', label: 'Prospecto' },
		{ value: 'VIGENTE', label: 'Vigente' },
		{ value: 'VENCIDA', label: 'Vencida' },
		{ value: 'CANCELADA', label: 'Cancelada' }
	];

	onMount(async () => {
		await loadData();
	});

	async function loadData() {
		loading = true;
		error = null;
		try {
			// Load poliza
			poliza = await polizaService.hogar.getById(polizaId);
			
			// Load related data
			const [hogarData, aseguradorasData] = await Promise.all([
				bienService.hogares.getById(poliza.id_hogar),
				aseguradoraService.getAll()
			]);
			
			hogar = hogarData;
			aseguradoras = aseguradorasData;
			
			// Load cliente
			if (hogar) {
				const clientes = await clienteService.getAll();
				cliente = clientes.find(c => c.id === hogar!.id_usuario) || null;
			}

			// Initialize form data
			initFormData();
		} catch (err) {
			console.error('Error loading data:', err);
			error = err instanceof Error ? err.message : 'Error al cargar la propuesta';
		} finally {
			loading = false;
		}
	}

	function initFormData() {
		if (!poliza) return;
		formData = {
			inicio_vigencia: poliza.inicio_vigencia || undefined,
			fin_vigencia: poliza.fin_vigencia || undefined,
			id_aseguradora_1: poliza.id_aseguradora_1 || undefined,
			id_aseguradora_2: poliza.id_aseguradora_2 || undefined,
			id_aseguradora_3: poliza.id_aseguradora_3 || undefined,
			id_aseguradora_4: poliza.id_aseguradora_4 || undefined,
			id_aseguradora_5: poliza.id_aseguradora_5 || undefined,
			valor_prima_aseg_1: poliza.valor_prima_aseg_1 || undefined,
			valor_prima_aseg_2: poliza.valor_prima_aseg_2 || undefined,
			valor_prima_aseg_3: poliza.valor_prima_aseg_3 || undefined,
			valor_prima_aseg_4: poliza.valor_prima_aseg_4 || undefined,
			valor_prima_aseg_5: poliza.valor_prima_aseg_5 || undefined,
			valor_inmueble_asegurado: poliza.valor_inmueble_asegurado || undefined,
			valor_contenidos_normales_asegurado: poliza.valor_contenidos_normales_asegurado || undefined,
			valor_contenidos_especiales_asegurado: poliza.valor_contenidos_especiales_asegurado || undefined,
			valor_equipo_electronico_asegurado: poliza.valor_equipo_electronico_asegurado || undefined,
			valor_maquinaria_equipo_asegurado: poliza.valor_maquinaria_equipo_asegurado || undefined,
			valor_rc_asegurado: poliza.valor_rc_asegurado || undefined,
			valor_prima_neta: poliza.valor_prima_neta || undefined,
			valor_otros_costos: poliza.valor_otros_costos || undefined,
			valor_iva: poliza.valor_iva || undefined,
			ingreso_comision_percibido: poliza.ingreso_comision_percibido || undefined,
			numero_poliza_aseguradora: poliza.numero_poliza_aseguradora || undefined
		};
	}

	// Convertir undefined a null para que el backend pueda actualizar los campos
	function prepareDataForSave(data: Record<string, unknown>): Record<string, unknown> {
		const result: Record<string, unknown> = {};
		for (const [key, value] of Object.entries(data)) {
			result[key] = value === undefined ? null : value;
		}
		return result;
	}

	async function handleSave() {
		saving = true;
		try {
			const dataToSend = prepareDataForSave(formData);
			await polizaService.hogar.update(polizaId, dataToSend);
			addNotification({
				type: 'success',
				title: 'Guardado',
				message: 'Los cambios se han guardado correctamente'
			});
			editMode = false;
			await loadData();
		} catch (err) {
			console.error('Error saving:', err);
			addNotification({
				type: 'error',
				title: 'Error',
				message: err instanceof Error ? err.message : 'No se pudieron guardar los cambios'
			});
		} finally {
			saving = false;
		}
	}

	function openCambiarEstadoModal() {
		nuevoEstado = poliza?.estado === 'PROSPECTO' ? 'VIGENTE' : poliza?.estado || 'VIGENTE';
		aseguradoraSeleccionada = poliza?.aseguradora_seleccionada || 1;
		showEstadoModal = true;
	}

	async function handleCambiarEstado() {
		if (!poliza) return;
		saving = true;
		try {
			const data: CambiarEstadoDto = { estado: nuevoEstado };
			if (nuevoEstado === 'VIGENTE') {
				data.aseguradora_seleccionada = aseguradoraSeleccionada;
			}
			await polizaService.hogar.cambiarEstado(polizaId, data);
			addNotification({
				type: 'success',
				title: 'Estado actualizado',
				message: `La póliza ahora está en estado ${nuevoEstado}`
			});
			showEstadoModal = false;
			await loadData();
		} catch (err) {
			console.error('Error changing status:', err);
			addNotification({
				type: 'error',
				title: 'Error',
				message: err instanceof Error ? err.message : 'No se pudo cambiar el estado'
			});
		} finally {
			saving = false;
		}
	}

	function formatCurrency(value: number | null): string {
		if (value === null || value === undefined) return '—';
		return new Intl.NumberFormat('es-CO', {
			style: 'currency',
			currency: 'COP',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(value);
	}

	function formatDate(dateStr: string | null): string {
		if (!dateStr) return '—';
		try {
			return new Date(dateStr).toLocaleDateString('es-CO', {
				day: '2-digit',
				month: 'long',
				year: 'numeric'
			});
		} catch {
			return dateStr;
		}
	}

	function getAseguradoraNombre(id: number | null): string {
		if (!id) return '—';
		const aseg = aseguradoras.find(a => a.id === id);
		return aseg?.nombre || `#${id}`;
	}

	function getClienteName(): string {
		if (!cliente) return '—';
		return cliente.tipo_persona === 'PERSONA' 
			? cliente.nombre || '—'
			: cliente.razon_social || '—';
	}

	// Helper para Select de aseguradoras
	$: aseguradorasOptions = aseguradoras.map(a => ({ value: String(a.id), label: a.nombre }));
</script>

<svelte:head>
	<title>Propuesta {poliza?.consecutivo || ''} | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<button 
			type="button" 
			class="p-2 hover:bg-secondary-100 rounded-lg transition-colors"
			on:click={() => goto('/propuestas')}
		>
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
			</svg>
		</button>
		<div>
			<h1 class="page-title">
				{poliza?.estado === 'PROSPECTO' ? 'Propuesta' : 'Póliza'} Hogar
			</h1>
			{#if poliza}
				<p class="text-secondary-500 text-sm mt-1 font-mono">{poliza.consecutivo}</p>
			{/if}
		</div>
	</div>
	
	{#if poliza}
		<div class="flex items-center gap-3">
			<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium
				{poliza.estado === 'PROSPECTO' ? 'bg-blue-100 text-blue-800' : ''}
				{poliza.estado === 'VIGENTE' ? 'bg-green-100 text-green-800' : ''}
				{poliza.estado === 'VENCIDA' ? 'bg-red-100 text-red-800' : ''}
				{poliza.estado === 'CANCELADA' ? 'bg-gray-100 text-gray-800' : ''}
			">
				{poliza.estado === 'PROSPECTO' ? 'Propuesta' : poliza.estado}
			</span>
			
			{#if poliza.estado !== 'CANCELADA'}
				<button
					type="button"
					class="btn btn-secondary"
					on:click={openCambiarEstadoModal}
				>
					Cambiar Estado
				</button>
			{/if}
			
			{#if poliza.estado === 'PROSPECTO'}
				<button
					type="button"
					class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
					on:click={() => goto(`/propuestas/hogar/${polizaId}/generar`)}
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
					Generar Propuesta
				</button>
			{/if}
			
			{#if poliza.estado === 'PROSPECTO' && (poliza.valor_prima_aseg_1 || poliza.valor_prima_aseg_2 || poliza.valor_prima_aseg_3 || poliza.valor_prima_aseg_4 || poliza.valor_prima_aseg_5)}
				<button
					type="button"
					class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
					on:click={() => goto(`/propuestas/hogar/${polizaId}/entregar`)}
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
					Entregar Póliza
				</button>
			{/if}

			{#if poliza.estado === 'VIGENTE'}
				<button
					type="button"
					class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
					on:click={() => goto(`/propuestas/hogar/${polizaId}/generar`)}
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
					Generar Entrega
				</button>
			{/if}
			
			{#if !editMode}
				<button
					type="button"
					class="btn btn-primary"
					on:click={() => editMode = true}
				>
					Editar
				</button>
			{/if}
		</div>
	{/if}
</header>

<!-- Content -->
<div class="page-content">
	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="flex flex-col items-center gap-4">
				<svg class="animate-spin h-8 w-8 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
				</svg>
				<p class="text-secondary-600">Cargando...</p>
			</div>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
			<p class="font-medium">Error</p>
			<p class="text-sm">{error}</p>
		</div>
	{:else if poliza}
		<!-- Sección de Entrega (solo para pólizas VIGENTES) -->
		{#if poliza.estado === 'VIGENTE' && poliza.numero_poliza}
			<div class="mb-6">
				<SeccionEntrega {poliza} />
			</div>
		{/if}

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Main Info -->
			<div class="lg:col-span-2 space-y-6">
				<!-- Información del Bien -->
				<div class="card">
					<h2 class="text-lg font-semibold text-secondary-900 mb-4">Información del Bien</h2>
					{#if hogar}
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">Tipo de Inmueble</p>
								<p class="text-sm font-medium">{hogar.tipo_inmueble || '—'}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Ciudad</p>
								<p class="text-sm">{hogar.ciudad_inmueble || '—'}</p>
							</div>
							<div class="col-span-2">
								<p class="text-xs text-secondary-500 mb-1">Dirección</p>
								<p class="text-sm">{hogar.direccion_inmueble || '—'}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Cliente</p>
								<p class="text-sm font-medium">{getClienteName()}</p>
							</div>
						</div>
					{/if}
				</div>

				<!-- Valores Asegurados -->
				<div class="card">
					<h2 class="text-lg font-semibold text-secondary-900 mb-4">Valores Asegurados</h2>
					{#if editMode}
						<div class="grid grid-cols-2 gap-4">
							<FormField label="Valor Inmueble" name="valor_inmueble_asegurado">
								<CurrencyInput bind:value={formData.valor_inmueble_asegurado} />
							</FormField>
							<FormField label="Contenidos Normales" name="valor_contenidos_normales_asegurado">
								<CurrencyInput bind:value={formData.valor_contenidos_normales_asegurado} />
							</FormField>
							<FormField label="Contenidos Especiales" name="valor_contenidos_especiales_asegurado">
								<CurrencyInput bind:value={formData.valor_contenidos_especiales_asegurado} />
							</FormField>
							<FormField label="Equipo Electrónico" name="valor_equipo_electronico_asegurado">
								<CurrencyInput bind:value={formData.valor_equipo_electronico_asegurado} />
							</FormField>
							<FormField label="Maquinaria/Equipo" name="valor_maquinaria_equipo_asegurado">
								<CurrencyInput bind:value={formData.valor_maquinaria_equipo_asegurado} />
							</FormField>
							<FormField label="RC" name="valor_rc_asegurado">
								<CurrencyInput bind:value={formData.valor_rc_asegurado} />
							</FormField>
						</div>
					{:else}
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">Valor Inmueble</p>
								<p class="text-sm font-medium text-primary-600">{formatCurrency(poliza.valor_inmueble_asegurado)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Contenidos Normales</p>
								<p class="text-sm">{formatCurrency(poliza.valor_contenidos_normales_asegurado)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Contenidos Especiales</p>
								<p class="text-sm">{formatCurrency(poliza.valor_contenidos_especiales_asegurado)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Equipo Electrónico</p>
								<p class="text-sm">{formatCurrency(poliza.valor_equipo_electronico_asegurado)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Maquinaria/Equipo</p>
								<p class="text-sm">{formatCurrency(poliza.valor_maquinaria_equipo_asegurado)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">RC</p>
								<p class="text-sm">{formatCurrency(poliza.valor_rc_asegurado)}</p>
							</div>
						</div>
					{/if}
				</div>

				<!-- Opciones de Aseguradoras -->
				<div class="card">
					<h2 class="text-lg font-semibold text-secondary-900 mb-4">Opciones de Aseguradoras</h2>
					{#if editMode}
						<div class="space-y-4">
							{#each [1, 2, 3, 4, 5] as num}
								<div class="grid grid-cols-2 gap-4 p-4 bg-secondary-50 rounded-lg">
									<FormField label={`Aseguradora ${num}`} name={`id_aseguradora_${num}`}>
										<Select 
											options={aseguradorasOptions} 
											bind:value={formData[`id_aseguradora_${num}`]}
											placeholder="Seleccionar..."
										/>
										/>
										/>
									</FormField>
									<FormField label={`Prima ${num}`} name={`valor_prima_aseg_${num}`}>
										<CurrencyInput bind:value={formData[`valor_prima_aseg_${num}`]} />
									</FormField>
								</div>
							{/each}
						</div>
					{:else}
						<div class="space-y-3">
							{#each [1, 2, 3, 4, 5] as num}
						{@const asegId = poliza[`id_aseguradora_${num}`]}
						{@const prima = poliza[`valor_prima_aseg_${num}`]}
								{#if asegId || prima}
									<div class="flex items-center justify-between p-3 bg-secondary-50 rounded-lg
										{poliza.aseguradora_seleccionada === num ? 'ring-2 ring-green-500' : ''}">
										<div class="flex items-center gap-3">
											<span class="w-6 h-6 flex items-center justify-center bg-secondary-200 rounded-full text-xs font-medium">
												{num}
											</span>
											<span class="font-medium">{getAseguradoraNombre(asegId)}</span>
											{#if poliza.aseguradora_seleccionada === num}
												<span class="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full">Seleccionada</span>
											{/if}
										</div>
										<span class="font-medium text-primary-600">{formatCurrency(prima)}</span>
									</div>
								{/if}
							{/each}
						</div>
					{/if}
				</div>

				<!-- Valores Financieros -->
				<div class="card">
					<h2 class="text-lg font-semibold text-secondary-900 mb-4">Valores Financieros</h2>
					{#if editMode}
						<div class="grid grid-cols-2 gap-4">
							<FormField label="Prima Neta" name="valor_prima_neta">
								<CurrencyInput bind:value={formData.valor_prima_neta} />
							</FormField>
							<FormField label="Otros Costos" name="valor_otros_costos">
								<CurrencyInput bind:value={formData.valor_otros_costos} />
							</FormField>
							<FormField label="IVA" name="valor_iva">
								<CurrencyInput bind:value={formData.valor_iva} />
							</FormField>
							<FormField label="Comisión Percibida" name="ingreso_comision_percibido">
								<CurrencyInput bind:value={formData.ingreso_comision_percibido} />
							</FormField>
						</div>
					{:else}
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">Prima Neta</p>
								<p class="text-sm font-medium">{formatCurrency(poliza.valor_prima_neta)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Otros Costos</p>
								<p class="text-sm">{formatCurrency(poliza.valor_otros_costos)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">IVA</p>
								<p class="text-sm">{formatCurrency(poliza.valor_iva)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Comisión Percibida</p>
								<p class="text-sm text-green-600 font-medium">{formatCurrency(poliza.ingreso_comision_percibido)}</p>
							</div>
						</div>
					{/if}
				</div>

				<!-- Actions -->
				{#if editMode}
					<div class="flex justify-end gap-3">
						<button
							type="button"
							class="btn btn-secondary"
							on:click={() => { editMode = false; initFormData(); }}
							disabled={saving}
						>
							Cancelar
						</button>
						<button
							type="button"
							class="btn btn-primary"
							on:click={handleSave}
							disabled={saving}
						>
							{#if saving}
								Guardando...
							{:else}
								Guardar Cambios
							{/if}
						</button>
					</div>
				{/if}
			</div>

			<!-- Sidebar -->
			<div class="space-y-6">
				<!-- Vigencia -->
				<div class="card">
					<h3 class="text-sm font-semibold text-secondary-900 mb-3">Vigencia</h3>
					{#if editMode}
						<div class="space-y-4">
							<FormField label="Inicio" name="inicio_vigencia">
								<input type="date" class="input" bind:value={formData.inicio_vigencia} />
							</FormField>
							<FormField label="Fin" name="fin_vigencia">
								<input type="date" class="input" bind:value={formData.fin_vigencia} />
							</FormField>
						</div>
					{:else}
						<div class="space-y-3">
							<div>
								<p class="text-xs text-secondary-500 mb-1">Inicio</p>
								<p class="text-sm">{formatDate(poliza.inicio_vigencia)}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Fin</p>
								<p class="text-sm">{formatDate(poliza.fin_vigencia)}</p>
							</div>
						</div>
					{/if}
				</div>

				<!-- Número de Póliza Aseguradora -->
				{#if poliza.estado === 'VIGENTE'}
					<div class="card">
						<h3 class="text-sm font-semibold text-secondary-900 mb-3">Póliza Aseguradora</h3>
						{#if editMode}
							<FormField label="Número de Póliza" name="numero_poliza_aseguradora">
								<input type="text" class="input" bind:value={formData.numero_poliza_aseguradora} />
							</FormField>
						{:else}
							<p class="font-mono text-sm">{poliza.numero_poliza_aseguradora || '—'}</p>
						{/if}
					</div>
				{/if}

				<!-- Metadata -->
				<div class="card">
					<h3 class="text-sm font-semibold text-secondary-900 mb-3">Información</h3>
					<div class="space-y-2 text-sm">
						<div class="flex justify-between">
							<span class="text-secondary-500">Creado</span>
							<span>{formatDate(poliza.created_at)}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-secondary-500">Actualizado</span>
							<span>{formatDate(poliza.updated_at)}</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>

<!-- Modal Cambiar Estado -->
<Modal bind:open={showEstadoModal} title="Cambiar Estado" size="sm">
	<div class="space-y-4">
		<FormField label="Nuevo Estado" name="nuevo_estado">
			<Select 
				options={estadosOptions.filter(e => e.value !== poliza?.estado)}
				bind:value={nuevoEstado}
			/>
		</FormField>
		
		{#if nuevoEstado === 'VIGENTE'}
			<FormField label="Aseguradora Seleccionada" name="aseguradora_seleccionada">
				<Select 
					options={[
						{ value: '1', label: `1 - ${getAseguradoraNombre(poliza?.id_aseguradora_1 || null)}` },
						{ value: '2', label: `2 - ${getAseguradoraNombre(poliza?.id_aseguradora_2 || null)}` },
						{ value: '3', label: `3 - ${getAseguradoraNombre(poliza?.id_aseguradora_3 || null)}` },
						{ value: '4', label: `4 - ${getAseguradoraNombre(poliza?.id_aseguradora_4 || null)}` },
						{ value: '5', label: `5 - ${getAseguradoraNombre(poliza?.id_aseguradora_5 || null)}` }
					].filter(o => poliza?.[`id_aseguradora_${o.value}`])}
					bind:value={aseguradoraSeleccionada}
				/>
			</FormField>
			<p class="text-sm text-secondary-500">
				Al cambiar a VIGENTE, debe seleccionar cuál de las aseguradoras cotizadas fue la elegida.
			</p>
		{/if}
	</div>

	<svelte:fragment slot="footer">
		<div class="flex justify-end gap-3">
			<button
				type="button"
				class="btn btn-secondary"
				on:click={() => showEstadoModal = false}
				disabled={saving}
			>
				Cancelar
			</button>
			<button
				type="button"
				class="btn btn-primary"
				on:click={handleCambiarEstado}
				disabled={saving}
			>
				{saving ? 'Guardando...' : 'Cambiar Estado'}
			</button>
		</div>
	</svelte:fragment>
</Modal>
