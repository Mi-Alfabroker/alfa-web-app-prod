<script lang="ts">
	/**
	 * FormularioEntrega - Reusable form component for policy delivery
	 * Used to collect all required information when delivering a policy from PROSPECTO to VIGENTE state
	 */

	import { FormSection, FormField, Input, Select, CurrencyInput } from '$components';
	import type { Aseguradora } from '$lib/types/aseguradora';

	// Props
	export let formData: Record<string, any>;
	export let aseguradoras: Aseguradora[];
	export let valorTotalPrima: number = 0; // Prima seleccionada (valor_prima_aseg_1, 2, etc.)
	export let onAseguradoraChange: ((id: number) => void) | null = null;

	// Secciones expandibles
	let sections = {
		aseguradora: true,
		datos_poliza: true,
		forma_pago: true,
		financiacion: false,
		comision: true
	};

	// Opciones para selects
	const opcionesAseguradoras = [
		{ value: 1, label: 'Aseguradora 1' },
		{ value: 2, label: 'Aseguradora 2' },
		{ value: 3, label: 'Aseguradora 3' },
		{ value: 4, label: 'Aseguradora 4' },
		{ value: 5, label: 'Aseguradora 5' }
	];

	const mediosPago = [
		{ value: 'contado', label: 'Contado' },
		{ value: 'financiera', label: 'Financiera' }
	];

	const estadosCartera = [
		{ value: 'recaudado', label: 'Recaudado' },
		{ value: 'pendiente', label: 'Pendiente' },
		{ value: 'cancelado', label: 'Cancelado' },
		{ value: 'en_solicitud', label: 'En Solicitud' }
	];

	const periodicidades = [
		{ value: 'mensual', label: 'Mensual' },
		{ value: 'semestral', label: 'Semestral' },
		{ value: 'anual', label: 'Anual' }
	];

	const numeroCuotas = [
		{ value: 3, label: '3 cuotas (sin interés)' },
		{ value: 5, label: '5 cuotas' },
		{ value: 8, label: '8 cuotas' },
		{ value: 11, label: '11 cuotas' }
	];

	// Computed
	$: aseguradorasOptions = aseguradoras.map(a => ({ value: a.id, label: a.nombre }));
	$: mostrarFinanciacion = formData.medio_pago === 'financiera';

	// Handlers
	function handleAseguradoraNumeroChange() {
		if (onAseguradoraChange && formData.aseguradora_numero) {
			onAseguradoraChange(formData.aseguradora_numero);
		}
	}

	// Expandir sección financiación automáticamente si se selecciona financiera
	$: if (mostrarFinanciacion) {
		sections.financiacion = true;
	}
</script>

<div class="space-y-8 p-6">
	<!-- ============================================================ -->
	<!-- SECCIÓN: ASEGURADORA -->
	<!-- ============================================================ -->
	<FormSection title="Aseguradora" status="active" bind:open={sections.aseguradora}>
		<div class="space-y-6 px-6">
			<FormField label="Número de Aseguradora" required>
				<Select
					bind:value={formData.aseguradora_numero}
					options={opcionesAseguradoras}
					placeholder="Seleccionar aseguradora..."
					required
					on:change={handleAseguradoraNumeroChange}
				/>
				<p class="text-xs text-secondary-500 mt-1.5">
					Selecciona el número que corresponde a la aseguradora de esta propuesta
				</p>
			</FormField>

			<FormField label="Nombre Aseguradora" required>
				<Input
					bind:value={formData.nombre_aseguradora}
					placeholder="Ej: Seguros Bolívar"
					required
				/>
				<p class="text-xs text-secondary-500 mt-1.5">
					Se completa automáticamente al seleccionar el número
				</p>
			</FormField>

			<FormField label="Numeral de Asistencia" required>
				<Input
					bind:value={formData.numeral_asistencia}
					placeholder="Ej: 018000123456"
					required
				/>
			</FormField>

			<FormField label="Valor Total Prima" required>
				<CurrencyInput
					bind:value={formData.valor_total_prima}
					placeholder="Valor de la prima"
					required
				/>
				{#if valorTotalPrima > 0}
					<div class="mt-2 p-2 bg-primary-50 rounded border border-primary-200">
						<p class="text-xs text-primary-700 font-medium">
							Prima seleccionada: ${valorTotalPrima.toLocaleString('es-CO')}
						</p>
					</div>
				{/if}
			</FormField>
		</div>
	</FormSection>

	<!-- ============================================================ -->
	<!-- SECCIÓN: DATOS DE LA PÓLIZA -->
	<!-- ============================================================ -->
	<FormSection title="Datos de la Póliza" status="active" bind:open={sections.datos_poliza}>
		<div class="space-y-6 px-6">
			<FormField label="Número de Póliza" required>
				<Input
					bind:value={formData.numero_poliza}
					placeholder="Ej: POL-2026-001"
					required
				/>
				<p class="text-xs text-secondary-500 mt-1.5">
					Número de póliza asignado por la aseguradora
				</p>
			</FormField>

			<FormField label="Fecha Inicio Vigencia" required>
				<Input
					type="date"
					bind:value={formData.fecha_inicio_vigencia}
					required
				/>
			</FormField>

			<FormField label="Fecha Fin Vigencia" required>
				<Input
					type="date"
					bind:value={formData.fecha_fin_vigencia}
					required
				/>
			</FormField>
		</div>
	</FormSection>

	<!-- ============================================================ -->
	<!-- SECCIÓN: FORMA DE PAGO -->
	<!-- ============================================================ -->
	<FormSection title="Forma de Pago" status="active" bind:open={sections.forma_pago}>
		<div class="space-y-6 px-6">
			<FormField label="Medio de Pago" required>
				<Select
					bind:value={formData.medio_pago}
					options={mediosPago}
					placeholder="Seleccionar medio de pago..."
					required
				/>
				<p class="text-xs text-secondary-500 mt-1.5">
					Si selecciona "Financiera", se habilitarán los campos de financiación
				</p>
			</FormField>

			<FormField label="Estado Cartera" required>
				<Select
					bind:value={formData.estado_cartera}
					options={estadosCartera}
					placeholder="Seleccionar estado..."
					required
				/>
			</FormField>

			<FormField label="Valor Comisión">
				<CurrencyInput
					bind:value={formData.valor_comision}
					placeholder="Valor de la comisión (opcional)"
				/>
			</FormField>
		</div>
	</FormSection>

	<!-- ============================================================ -->
	<!-- SECCIÓN: FINANCIACIÓN (solo si medio_pago = 'financiera') -->
	<!-- ============================================================ -->
	{#if mostrarFinanciacion}
		<FormSection title="Financiación" status="active" bind:open={sections.financiacion}>
			<div class="space-y-6 px-6">
				<div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
					<div class="flex items-start gap-3">
						<svg class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
						<div>
							<p class="text-sm font-medium text-blue-900">Información de Financiación</p>
							<p class="text-xs text-blue-700 mt-1">
								Los valores de cuota se calcularon automáticamente al generar la propuesta. Asegúrese de que el número de cuotas seleccionado coincida con el plan mostrado al cliente.
							</p>
						</div>
					</div>
				</div>

				<FormField label="Entidad Financiera" required>
					<Input
						bind:value={formData.financiacion_entidad}
						placeholder="Ej: Bancolombia"
						required
					/>
				</FormField>

				<FormField label="Periodicidad" required>
					<Select
						bind:value={formData.financiacion_periodicidad}
						options={periodicidades}
						placeholder="Seleccionar periodicidad..."
						required
					/>
				</FormField>

				<FormField label="Número de Cuotas" required>
					<Select
						bind:value={formData.financiacion_num_cuotas}
						options={numeroCuotas}
						placeholder="Seleccionar plan de cuotas..."
						required
					/>
					<p class="text-xs text-secondary-500 mt-1.5">
						3 cuotas sin interés, 5/8/11 con tasa del 2.3% mensual
					</p>
				</FormField>

				<FormField label="Fecha Primera Cuota" required>
					<Input
						type="date"
						bind:value={formData.financiacion_fecha_primera}
						required
					/>
				</FormField>

				<FormField label="Cuota Actual" required>
					<Input
						type="number"
						bind:value={formData.financiacion_cuota_actual}
						placeholder="Ej: 1"
						required
					/>
					<p class="text-xs text-secondary-500 mt-1.5">
						Generalmente inicia en 1, indica la cuota que el cliente debe pagar
					</p>
				</FormField>
			</div>
		</FormSection>
	{/if}
</div>
