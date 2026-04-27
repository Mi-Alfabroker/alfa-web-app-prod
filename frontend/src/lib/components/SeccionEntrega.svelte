<script lang="ts">
	/**
	 * SeccionEntrega - Display component for policy delivery information
	 * Shows when policy status is VIGENTE
	 */

	import type { Poliza } from '$lib/types/poliza';

	export let poliza: Poliza;

	// Helper: formatear fecha
	function formatFecha(fecha: string | null | undefined): string {
		if (!fecha) return '—';
		const d = new Date(fecha);
		return d.toLocaleDateString('es-CO');
	}

	// Helper: formatear moneda
	function formatCurrency(value: number | null | undefined): string {
		if (value === null || value === undefined) return '—';
		return `$${value.toLocaleString('es-CO')}`;
	}

	// Helper: calcular próximo pago
	function calcularProximoPago(): { fecha: string; monto: number; cuota: number } | null {
		if (!poliza.medio_pago || poliza.medio_pago !== 'financiera') return null;
		if (!poliza.financiacion_fecha_primera || !poliza.financiacion_cuota_actual || !poliza.financiacion_num_cuotas) return null;

		const cuotaActual = poliza.financiacion_cuota_actual;
		const numCuotas = poliza.financiacion_num_cuotas;

		if (cuotaActual > numCuotas) return null; // Ya pagó todas

		// Calcular fecha: fecha_primera + (cuota_actual - 1) meses
		const fechaPrimera = new Date(poliza.financiacion_fecha_primera);
		const fechaProxima = new Date(fechaPrimera);
		fechaProxima.setMonth(fechaPrimera.getMonth() + (cuotaActual - 1));

		// Obtener valor de cuota según el plan
		const valorCuotaKey = `valor_cuota_${numCuotas}` as keyof typeof poliza;
		const montoValue = poliza[valorCuotaKey];
		const monto = typeof montoValue === 'number' ? montoValue : 0;

		return {
			fecha: formatFecha(fechaProxima.toISOString()),
			monto,
			cuota: cuotaActual
		};
	}

	// Computed
	$: tieneFinanciacion = poliza.medio_pago === 'financiera';
	$: proximoPago = calcularProximoPago();
	$: estadoCarteraColor = {
		'recaudado': 'bg-green-100 text-green-800',
		'pendiente': 'bg-yellow-100 text-yellow-800',
		'cancelado': 'bg-red-100 text-red-800',
		'en_solicitud': 'bg-blue-100 text-blue-800'
	}[poliza.estado_cartera || 'pendiente'] || 'bg-secondary-100 text-secondary-800';
</script>

<div class="bg-white rounded-lg shadow-sm">
	<div class="border-b border-secondary-200 p-4">
		<h2 class="text-lg font-semibold text-secondary-900">Información de Entrega</h2>
		<p class="text-sm text-secondary-600">Datos de la póliza vigente</p>
	</div>

	<div class="p-6 space-y-6">
		<!-- Aseguradora -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Aseguradora</div>
				<p class="text-secondary-900">{poliza.nombre_aseguradora || '—'}</p>
			</div>
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Numeral de Asistencia</div>
				<p class="text-secondary-900">{poliza.numeral_asistencia || '—'}</p>
			</div>
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Valor Total Prima</div>
				<p class="text-secondary-900 font-semibold">{formatCurrency(poliza.valor_total_prima)}</p>
			</div>
		</div>

		<div class="border-t border-secondary-200 pt-4"></div>

		<!-- Datos Póliza -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Número de Póliza</div>
				<p class="text-secondary-900 font-mono">{poliza.numero_poliza || '—'}</p>
			</div>
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Inicio Vigencia</div>
				<p class="text-secondary-900">{formatFecha(poliza.fecha_inicio_vigencia)}</p>
			</div>
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Fin Vigencia</div>
				<p class="text-secondary-900">{formatFecha(poliza.fecha_fin_vigencia)}</p>
			</div>
		</div>

		<div class="border-t border-secondary-200 pt-4"></div>

		<!-- Forma de Pago -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Medio de Pago</div>
				<p class="text-secondary-900 capitalize">{poliza.medio_pago || '—'}</p>
			</div>
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Estado Cartera</div>
				<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {estadoCarteraColor}">
					{poliza.estado_cartera?.replace('_', ' ') || 'Pendiente'}
				</span>
			</div>
			<div>
				<div class="text-sm font-medium text-secondary-700 mb-1">Valor Comisión</div>
				<p class="text-secondary-900">{formatCurrency(poliza.valor_comision)}</p>
			</div>
		</div>

		<!-- Financiación (condicional) -->
		{#if tieneFinanciacion}
			<div class="border-t border-secondary-200 pt-4"></div>
			
			<div class="bg-secondary-50 rounded-lg p-4">
				<h3 class="text-sm font-semibold text-secondary-900 mb-3">Financiación</h3>
				
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					<div>
						<div class="text-xs font-medium text-secondary-600 mb-1">Entidad Financiera</div>
						<p class="text-sm text-secondary-900">{poliza.financiacion_entidad || '—'}</p>
					</div>
					<div>
						<div class="text-xs font-medium text-secondary-600 mb-1">Periodicidad</div>
						<p class="text-sm text-secondary-900 capitalize">{poliza.financiacion_periodicidad || '—'}</p>
					</div>
					<div>
						<div class="text-xs font-medium text-secondary-600 mb-1">Plan de Cuotas</div>
						<p class="text-sm text-secondary-900">{poliza.financiacion_num_cuotas || 0} cuotas</p>
					</div>
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
					<div>
						<div class="text-xs font-medium text-secondary-600 mb-1">Fecha Primera Cuota</div>
						<p class="text-sm text-secondary-900">{formatFecha(poliza.financiacion_fecha_primera)}</p>
					</div>
					<div>
						<div class="text-xs font-medium text-secondary-600 mb-1">Cuota Actual</div>
						<p class="text-sm text-secondary-900">
							{poliza.financiacion_cuota_actual || 0} de {poliza.financiacion_num_cuotas || 0}
						</p>
					</div>
				</div>

				<!-- Próximo Pago -->
				{#if proximoPago}
					<div class="mt-4 p-3 bg-primary-50 border border-primary-200 rounded-lg">
						<div class="flex items-center justify-between">
							<div>
								<p class="text-xs font-medium text-primary-900">Próximo Pago</p>
								<p class="text-sm text-primary-700 mt-1">Cuota {proximoPago.cuota} - {proximoPago.fecha}</p>
							</div>
							<div class="text-right">
								<p class="text-lg font-bold text-primary-900">{formatCurrency(proximoPago.monto)}</p>
							</div>
						</div>
					</div>
				{:else}
					<div class="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
						<p class="text-sm text-green-700">✓ Todas las cuotas han sido pagadas</p>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
