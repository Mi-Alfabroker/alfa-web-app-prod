<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { FormField, CurrencyInput, Select, Modal, Input } from '$components';
	import { polizaService, bienService, clienteService, aseguradoraService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import type { PolizaCopropiedad, EstadoPoliza, CambiarEstadoDto } from '$lib/types/poliza';
	import type { Copropiedad } from '$lib/types/bien';
	import type { Cliente } from '$lib/types/cliente';
	import type { Aseguradora } from '$lib/types/aseguradora';

	// Route params
	$: polizaId = Number($page.params.id);

	// Data state
	let poliza: PolizaCopropiedad | null = null;
	let copropiedad: Copropiedad | null = null;
	let cliente: Cliente | null = null;
	let aseguradoras: Aseguradora[] = [];

	// UI state
	let loading = true;
	let saving = false;
	let error: string | null = null;
	let editMode = false;

	// Form data
	let formData: Record<string, unknown> = {};

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
			poliza = await polizaService.copropiedad.getById(polizaId);
			
			// Load related data
			const [copropiedadData, aseguradorasData] = await Promise.all([
				bienService.copropiedades.getById(poliza.id_copropiedad),
				aseguradoraService.getAll()
			]);
			
			copropiedad = copropiedadData;
			aseguradoras = aseguradorasData;
			
			// Load cliente
			if (copropiedad) {
				const clientes = await clienteService.getAll();
				cliente = clientes.find(c => c.id === copropiedad!.id_usuario) || null;
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
			valor_area_comun_asegurado: poliza.valor_area_comun_asegurado || undefined,
			valor_area_privada_asegurado: poliza.valor_area_privada_asegurado || undefined,
			valor_maquinaria_equipo_asegurado: poliza.valor_maquinaria_equipo_asegurado || undefined,
			valor_equipo_electronico_asegurado: poliza.valor_equipo_electronico_asegurado || undefined,
			valor_muebles_asegurado: poliza.valor_muebles_asegurado || undefined,
			valor_directores_asegurado: poliza.valor_directores_asegurado ?? 0,
			valor_rce_asegurado: poliza.valor_rce_asegurado ?? 0,
			valor_manejo_asegurado: poliza.valor_manejo_asegurado ?? 0,
			valor_transporte_valores_vigencia_asegurado: poliza.valor_transporte_valores_vigencia_asegurado ?? 0,
			valor_transporte_valores_despacho_asegurado: poliza.valor_transporte_valores_despacho_asegurado ?? 0,
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
			await polizaService.copropiedad.update(polizaId, dataToSend);
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
			await polizaService.copropiedad.cambiarEstado(polizaId, data);
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

	function formatCurrency(value: number | null | undefined): string {
		if (value === null || value === undefined) return '—';
		return new Intl.NumberFormat('es-CO', {
			style: 'currency',
			currency: 'COP',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(value);
	}

	function formatDate(dateStr: string | null | undefined): string {
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

	function getAseguradoraNombre(id: number | null | undefined): string {
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

	// Helpers para acceder propiedades dinámicas sin casting en template
	function getAseguradoraId(num: number): number | null {
		if (!poliza) return null;
		const key = `id_aseguradora_${num}`;
		return (poliza as Record<string, unknown>)[key] as number | null;
	}

	function getPrimaAseg(num: number): number | null {
		if (!poliza) return null;
		const key = `valor_prima_aseg_${num}`;
		return (poliza as Record<string, unknown>)[key] as number | null;
	}

	function tieneAseguradora(num: number): boolean {
		return !!(getAseguradoraId(num) || getPrimaAseg(num));
	}

	function getModalAsegOptions() {
		return [1, 2, 3, 4, 5]
			.filter(n => getAseguradoraId(n))
			.map(n => ({ value: n, label: `${n} - ${getAseguradoraNombre(getAseguradoraId(n))}` }));
	}

	// Helper para Select de aseguradoras
	$: aseguradorasOptions = aseguradoras.map(a => ({ value: a.id, label: a.nombre }));
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
				{poliza?.estado === 'PROSPECTO' ? 'Propuesta' : 'Póliza'} Copropiedad
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
					on:click={() => goto(`/propuestas/copropiedad/${polizaId}/generar`)}
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
					on:click={() => goto(`/propuestas/copropiedad/${polizaId}/entregar`)}
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
					on:click={() => goto(`/propuestas/copropiedad/${polizaId}/generar`)}
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
				<svg class="animate-spin h-8 w-8 text-primary-500" fill="none" viewBox="0 0 24 24">
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
					{#if copropiedad}
						<div class="grid grid-cols-2 gap-4">
							<div>
								<p class="text-xs text-secondary-500 mb-1">Tipo de Copropiedad</p>
								<p class="text-sm font-medium">{copropiedad.tipo_copropiedad || '—'}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Ciudad</p>
								<p class="text-sm">{copropiedad.ciudad || '—'}</p>
							</div>
							<div class="col-span-2">
								<p class="text-xs text-secondary-500 mb-1">Dirección</p>
								<p class="text-sm">{copropiedad.direccion || '—'}</p>
							</div>
							<div>
								<p class="text-xs text-secondary-500 mb-1">Estrato</p>
								<p class="text-sm">{copropiedad.estrato || '—'}</p>
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
						<div class="space-y-4">
							<FormField label="Valor Área Común">
								<CurrencyInput bind:value={formData.valor_area_comun_asegurado} />
							</FormField>
							<FormField label="Valor Área Privada">
								<CurrencyInput bind:value={formData.valor_area_privada_asegurado} />
							</FormField>
							<FormField label="Maquinaria y Equipo">
								<CurrencyInput bind:value={formData.valor_maquinaria_equipo_asegurado} />
							</FormField>
							<FormField label="Equipo Electrónico">
								<CurrencyInput bind:value={formData.valor_equipo_electronico_asegurado} />
							</FormField>
							<FormField label="Muebles y Enseres">
								<CurrencyInput bind:value={formData.valor_muebles_asegurado} />
							</FormField>
							<!-- Nota explicativa para valores en millones -->
							<div class="mt-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl">
								<div class="flex items-start gap-3">
									<div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
										<svg class="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
									</div>
									<div>
										<h4 class="font-semibold text-blue-800 text-sm">Valores expresados en Millones</h4>
										<p class="text-blue-700 text-xs mt-1">
											Ingrese el valor en <strong>millones de pesos</strong>. 
											Ejemplo: <span class="bg-blue-100 px-1.5 py-0.5 rounded font-mono">20</span> = $20.000.000
										</p>
									</div>
								</div>
							</div>
							
							<div class="mt-3 space-y-3 pl-3 border-l-4 border-blue-300">
								<FormField label="Directores y Administradores">
									<div class="relative">
										<Input type="number" bind:value={formData.valor_directores_asegurado} placeholder="0" />
										<span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-blue-500 font-medium">millones</span>
									</div>
								</FormField>
								<FormField label="RCE">
									<div class="relative">
										<Input type="number" bind:value={formData.valor_rce_asegurado} placeholder="0" />
										<span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-blue-500 font-medium">millones</span>
									</div>
								</FormField>
								<FormField label="Manejo">
									<div class="relative">
										<Input type="number" bind:value={formData.valor_manejo_asegurado} placeholder="0" />
										<span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-blue-500 font-medium">millones</span>
									</div>
								</FormField>
								<FormField label="Transporte Valores (Vigencia)">
									<div class="relative">
										<Input type="number" bind:value={formData.valor_transporte_valores_vigencia_asegurado} placeholder="0" />
										<span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-blue-500 font-medium">millones</span>
									</div>
								</FormField>
								<FormField label="Transporte Valores (Despacho)">
									<div class="relative">
										<Input type="number" bind:value={formData.valor_transporte_valores_despacho_asegurado} placeholder="0" />
										<span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-blue-500 font-medium">millones</span>
									</div>
								</FormField>
							</div>
						</div>
					{:else}
						<div class="space-y-3">
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Valor Área Común</span>
								<span class="font-medium">{formatCurrency(poliza.valor_area_comun_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Valor Área Privada</span>
								<span class="font-medium">{formatCurrency(poliza.valor_area_privada_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Maquinaria y Equipo</span>
								<span class="font-medium">{formatCurrency(poliza.valor_maquinaria_equipo_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Equipo Electrónico</span>
								<span class="font-medium">{formatCurrency(poliza.valor_equipo_electronico_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Muebles y Enseres</span>
								<span class="font-medium">{formatCurrency(poliza.valor_muebles_asegurado)}</span>
							</div>
							<!-- Nota explicativa para valores en millones -->
							<div class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
								<div class="flex items-center gap-2">
									<svg class="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
									<p class="text-blue-700 text-xs">
										<strong>Valores en millones:</strong> 20 = $20.000.000
									</p>
								</div>
							</div>
							
							<div class="mt-3 space-y-2 pl-2 border-l-4 border-blue-300">
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Directores y Administradores</span>
									<span class="font-semibold text-blue-700">{poliza.valor_directores_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">RCE</span>
									<span class="font-semibold text-blue-700">{poliza.valor_rce_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Manejo</span>
									<span class="font-semibold text-blue-700">{poliza.valor_manejo_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Transporte Valores (Vigencia)</span>
									<span class="font-semibold text-blue-700">{poliza.valor_transporte_valores_vigencia_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Transporte Valores (Despacho)</span>
									<span class="font-semibold text-blue-700">{poliza.valor_transporte_valores_despacho_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
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
								<div class="p-4 bg-secondary-50 rounded-lg space-y-4">
									<p class="text-sm font-medium text-secondary-700">Opción {num}</p>
									<FormField label="Aseguradora">
										<Select 
											options={aseguradorasOptions} 
											bind:value={formData[`id_aseguradora_${num}`]}
											placeholder="Seleccionar..."
										/>
									</FormField>
									<FormField label="Valor Prima">
										<CurrencyInput bind:value={formData[`valor_prima_aseg_${num}`]} />
									</FormField>
								</div>
							{/each}
						</div>
					{:else}
						<div class="space-y-3">
							{#each [1, 2, 3, 4, 5] as num}
								{#if tieneAseguradora(num)}
									<div class="flex items-center justify-between p-3 bg-secondary-50 rounded-lg
										{poliza.aseguradora_seleccionada === num ? 'ring-2 ring-green-500' : ''}">
										<div class="flex items-center gap-3">
											<span class="w-6 h-6 flex items-center justify-center bg-secondary-200 rounded-full text-xs font-medium">
												{num}
											</span>
											<span class="font-medium">{getAseguradoraNombre(getAseguradoraId(num))}</span>
											{#if poliza.aseguradora_seleccionada === num}
												<span class="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full">Seleccionada</span>
											{/if}
										</div>
										<span class="font-medium text-primary-600">{formatCurrency(getPrimaAseg(num))}</span>
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
						<div class="space-y-4">
							<FormField label="Prima Neta">
								<CurrencyInput bind:value={formData.valor_prima_neta} />
							</FormField>
							<FormField label="Otros Costos">
								<CurrencyInput bind:value={formData.valor_otros_costos} />
							</FormField>
							<FormField label="IVA">
								<Input type="number" bind:value={formData.valor_iva} placeholder="0" />
							</FormField>
							<FormField label="Comisión Percibida">
								<CurrencyInput bind:value={formData.ingreso_comision_percibido} />
							</FormField>
						</div>
					{:else}
						<div class="space-y-3">
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Prima Neta</span>
								<span class="font-medium">{formatCurrency(poliza.valor_prima_neta)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Otros Costos</span>
								<span class="font-medium">{formatCurrency(poliza.valor_otros_costos)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">IVA</span>
								<span class="font-medium">{formatCurrency(poliza.valor_iva)}</span>
							</div>
							<div class="flex justify-between py-2">
								<span class="text-secondary-600">Comisión Percibida</span>
								<span class="font-medium text-green-600">{formatCurrency(poliza.ingreso_comision_percibido)}</span>
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
							<FormField label="Inicio">
								<input type="date" class="input" bind:value={formData.inicio_vigencia} />
							</FormField>
							<FormField label="Fin">
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
							<FormField label="Número de Póliza">
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
		<FormField label="Nuevo Estado">
			<Select 
				options={estadosOptions.filter(e => e.value !== poliza?.estado)}
				bind:value={nuevoEstado}
			/>
		</FormField>
		
		{#if nuevoEstado === 'VIGENTE'}
			<FormField label="Aseguradora Seleccionada">
				<Select 
					options={getModalAsegOptions()}
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
