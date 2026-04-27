<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { FormularioEntrega, Button, Loading } from '$components';
	import { polizaService, aseguradoraService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import type { PolizaVehiculo } from '$lib/types/poliza';
	import type { Aseguradora } from '$lib/types/aseguradora';

	// Route params
	$: polizaId = Number($page.params.id);

	// Data state
	let poliza: PolizaVehiculo | null = null;
	let aseguradoras: Aseguradora[] = [];

	// UI state
	let loading = true;
	let submitting = false;
	let error: string | null = null;

	// Form data
	let formData: Record<string, any> = {
		aseguradora_numero: null,
		nombre_aseguradora: '',
		numeral_asistencia: '',
		valor_total_prima: 0,
		numero_poliza: '',
		fecha_inicio_vigencia: '',
		fecha_fin_vigencia: '',
		medio_pago: 'contado',
		estado_cartera: 'pendiente',
		valor_comision: 0,
		financiacion_entidad: '',
		financiacion_periodicidad: 'mensual',
		financiacion_num_cuotas: 3,
		financiacion_fecha_primera: '',
		financiacion_cuota_actual: 1
	};

	onMount(async () => {
		await loadData();
	});

	async function loadData() {
		loading = true;
		error = null;
		try {
			const [polizaData, aseguradorasData] = await Promise.all([
				polizaService.vehiculo.getById(polizaId),
				aseguradoraService.getAll()
			]);

			poliza = polizaData;
			aseguradoras = aseguradorasData;

			if (poliza.estado !== 'PROSPECTO') {
				addNotification({
					type: 'error',
					title: 'Error',
					message: 'Solo se pueden entregar pólizas en estado PROSPECTO'
				});
				goto(`/propuestas/vehiculo/${polizaId}`);
				return;
			}

			if (poliza.inicio_vigencia) {
				formData.fecha_inicio_vigencia = poliza.inicio_vigencia.split('T')[0];
			}
			if (poliza.fin_vigencia) {
				formData.fecha_fin_vigencia = poliza.fin_vigencia.split('T')[0];
			}

		} catch (err) {
			console.error('Error loading data:', err);
			error = err instanceof Error ? err.message : 'Error al cargar datos';
		} finally {
			loading = false;
		}
	}

	async function handleAseguradoraChange(aseguradoraNumero: number) {
		const idAseguradoraKey = `id_aseguradora_${aseguradoraNumero}` as keyof PolizaVehiculo;
		const idAseguradora = poliza?.[idAseguradoraKey] as number | null;

		if (!idAseguradora) {
			addNotification({
				type: 'warning',
				title: 'Advertencia',
				message: `No hay aseguradora ${aseguradoraNumero} asignada en esta póliza`
			});
			return;
		}

		try {
			const datos = await aseguradoraService.getDatosEntrega(idAseguradora);
			formData.nombre_aseguradora = datos.nombre;
			formData.numeral_asistencia = datos.numeral_asistencia || '';

			const valorPrimaKey = `valor_prima_aseg_${aseguradoraNumero}` as keyof PolizaVehiculo;
			const valorPrima = poliza?.[valorPrimaKey] as number | null;
			if (valorPrima) {
				formData.valor_total_prima = valorPrima;
			}
		} catch (err) {
			console.error('Error loading aseguradora datos:', err);
			addNotification({
				type: 'error',
				title: 'Error',
				message: 'No se pudo cargar la información de la aseguradora'
			});
		}
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();
		
		if (!poliza) return;

		submitting = true;
		error = null;

		try {
			if (!formData.aseguradora_numero) {
				throw new Error('Debe seleccionar un número de aseguradora');
			}
			if (!formData.nombre_aseguradora || !formData.numeral_asistencia) {
				throw new Error('Complete los datos de la aseguradora');
			}
			if (!formData.numero_poliza || !formData.fecha_inicio_vigencia || !formData.fecha_fin_vigencia) {
				throw new Error('Complete los datos de la póliza');
			}
			if (formData.medio_pago === 'financiera') {
				if (!formData.financiacion_entidad || !formData.financiacion_fecha_primera) {
					throw new Error('Complete los datos de financiación');
				}
			}

			const payload = {
				aseguradora_seleccionada: formData.aseguradora_numero,
				nombre_aseguradora: formData.nombre_aseguradora,
				numeral_asistencia: formData.numeral_asistencia,
				valor_total_prima: formData.valor_total_prima,
				numero_poliza_aseguradora: formData.numero_poliza,
				inicio_vigencia: formData.fecha_inicio_vigencia,
				fin_vigencia: formData.fecha_fin_vigencia,
				medio_pago: formData.medio_pago,
				estado_cartera: formData.estado_cartera,
				valor_comision: formData.valor_comision || 0,
				...(formData.medio_pago === 'financiera' && {
					financiacion_entidad: formData.financiacion_entidad,
					financiacion_periodicidad: formData.financiacion_periodicidad,
					financiacion_num_cuotas: formData.financiacion_num_cuotas,
					financiacion_fecha_primera_cuota: formData.financiacion_fecha_primera,
					financiacion_cuota_actual: formData.financiacion_cuota_actual
				})
			};

			const result = await polizaService.vehiculo.entregar(polizaId, payload);

			addNotification({
				type: 'success',
				title: 'Póliza Entregada',
				message: `Póliza ${result.consecutivo} entregada exitosamente`
			});

			goto(`/propuestas/vehiculo/${polizaId}`);

		} catch (err) {
			console.error('❌ Error entregando póliza:', err);
			error = err instanceof Error ? err.message : 'Error al entregar la póliza';
			addNotification({
				type: 'error',
				title: 'Error',
				message: error
			});
		} finally {
			submitting = false;
		}
	}

	function handleCancel() {
		goto(`/propuestas/vehiculo/${polizaId}`);
	}

	$: valorPrimaSeleccionada = poliza && formData.aseguradora_numero 
		? (poliza as any)[`valor_prima_aseg_${formData.aseguradora_numero}`] || 0
		: 0;
</script>

<svelte:head>
	<title>Entregar Póliza {poliza?.consecutivo || ''} | {APP_NAME}</title>
</svelte:head>

<header class="page-header">
	<div class="flex items-center gap-4">
		<button 
			type="button" 
			class="p-2 hover:bg-secondary-100 rounded-lg transition-colors"
			on:click={handleCancel}
		>
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
			</svg>
		</button>

		<div>
			<h1 class="page-title">Entregar Póliza</h1>
			<p class="text-sm text-secondary-600">
				{#if poliza}
					{poliza.consecutivo} - Vehículo
				{/if}
			</p>
		</div>
	</div>
</header>

<main class="page-content">
	{#if loading}
		<Loading />
	{:else if error && !poliza}
		<div class="error-message">
			<p>{error}</p>
			<Button on:click={handleCancel}>Volver</Button>
		</div>
	{:else if poliza}
		<form on:submit={handleSubmit} class="max-w-5xl mx-auto">
			<div class="bg-white rounded-xl shadow-lg overflow-hidden p-6">
				<!-- Información de la Propuesta -->
				<div class="bg-gradient-to-r from-primary-50 to-primary-100 border-b border-primary-200 px-8 py-6">
					<h2 class="text-lg font-semibold text-primary-900 mb-2">Información de la Propuesta</h2>
					<div class="grid grid-cols-2 gap-4 text-sm">
						<div>
							<span class="text-secondary-600">Consecutivo:</span>
							<span class="font-medium text-secondary-900 ml-2">{poliza.consecutivo}</span>
						</div>
						<div>
							<span class="text-secondary-600">Estado Actual:</span>
							<span class="font-medium text-secondary-900 ml-2">{poliza.estado}</span>
						</div>
					</div>
				</div>

				<FormularioEntrega
					bind:formData
					{aseguradoras}
					valorTotalPrima={valorPrimaSeleccionada}
					onAseguradoraChange={handleAseguradoraChange}
				/>

				{#if error}
					<div class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
						<p class="text-sm text-red-700">{error}</p>
					</div>
				{/if}

				<div class="mt-6 flex gap-3 justify-end">
					<Button variant="secondary" on:click={handleCancel} disabled={submitting}>
						Cancelar
					</Button>
					<Button type="submit" variant="primary" disabled={submitting}>
						{#if submitting}
							Entregando...
						{:else}
							Entregar Póliza
						{/if}
					</Button>
				</div>
			</div>
		</form>
	{/if}
</main>
