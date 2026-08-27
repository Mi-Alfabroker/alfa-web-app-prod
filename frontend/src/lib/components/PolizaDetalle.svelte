<script lang="ts">
	/**
	 * PolizaDetalle - the detail/edit screen shared by all four rubros.
	 *
	 * The four rubro pages differ only in which insured-value columns they carry,
	 * how the bien is described, and which service performs the CRUD; everything
	 * else (quote slots, financials, vigencia, state changes, edit mode) is
	 * identical. They used to be four near-copies of ~600 lines each, so the
	 * layout lives here once and each route supplies its own configuration.
	 *
	 * Layout follows the design: a 1.7fr / 1fr split, with the insured values as
	 * cards and the prima as a large metric in the right rail.
	 */
	import { goto } from '$app/navigation';
	import {
		CurrencyInput,
		FormField,
		Modal,
		PageHeader,
		SeccionEntrega,
		Select,
		StatusBadge,
		Tag
	} from '$components';
	import FlujoPoliza from './FlujoPoliza.svelte';
	import { addNotification } from '$lib/stores/notifications';
	import { invalidateCatalog } from '$lib/stores/catalog';
	import { ESTADO_LABELS, flujoPoliza, formatDateShort, money } from '$utils';
	import { auth } from '$lib/stores/auth';
	import type { Aseguradora } from '$lib/types/aseguradora';
	import type { CambiarEstadoDto, EstadoPoliza, Poliza } from '$lib/types/poliza';

	/**
	 * A CRUD surface shaped like the per-rubro entries of `polizaService`.
	 * Not exported: in a Svelte component script `export` declares a prop.
	 */
	interface PolizaCrudService {
		getById: (id: number) => Promise<any>;
		update: (id: number, data: Record<string, unknown>) => Promise<any>;
		cambiarEstado: (id: number, data: CambiarEstadoDto) => Promise<any>;
	}

	export let polizaId: number;
	export let rubroLabel: string;
	export let rubroSlug: string;
	export let service: PolizaCrudService;
	/** Insured-value columns for this rubro, in display order. */
	export let valores: { key: string; label: string }[] = [];
	/** Loads the bien and returns its display fields plus the owning cliente id. */
	export let loadBien: (poliza: any) => Promise<{
		fields: { label: string; value: string }[];
		clienteId: number | null;
	}>;
	export let loadAseguradoras: () => Promise<Aseguradora[]>;
	export let loadClienteNombre: (clienteId: number | null) => Promise<string>;
	/** Renders the delivery summary once the póliza has been handed over. */
	export let showEntrega: (poliza: any) => boolean = () => false;

	const FINANCIEROS = [
		{ key: 'valor_prima_neta', label: 'Prima neta' },
		{ key: 'valor_otros_costos', label: 'Otros costos' },
		{ key: 'valor_iva', label: 'IVA' },
		{ key: 'ingreso_comision_percibido', label: 'Comisión percibida' }
	];

	const SLOTS = [1, 2, 3, 4, 5];

	const estadosOptions: { value: EstadoPoliza; label: string }[] = [
		{ value: 'PROSPECTO', label: 'Propuesta' },
		{ value: 'VIGENTE', label: 'Vigente' },
		{ value: 'VENCIDA', label: 'Vencida' },
		{ value: 'CANCELADA', label: 'Cancelada' }
	];

	let poliza: (Poliza & Record<string, any>) | null = null;
	let bienFields: { label: string; value: string }[] = [];
	let clienteNombreValue = '—';
	let aseguradoras: Aseguradora[] = [];

	let loading = true;
	let saving = false;
	let error: string | null = null;
	let editMode = false;

	let formData: Record<string, any> = {};

	let showEstadoModal = false;
	let nuevoEstado: EstadoPoliza = 'VIGENTE';
	let aseguradoraSeleccionada: number = 1;

	// Reload whenever the route id changes, so navigating between two pólizas of
	// the same rubro refetches instead of showing the previous one.
	$: if (polizaId) void loadData(polizaId);

	async function loadData(id: number) {
		loading = true;
		error = null;
		try {
			poliza = await service.getById(id);
			const [bien, asegs] = await Promise.all([loadBien(poliza), loadAseguradoras()]);
			bienFields = bien.fields;
			aseguradoras = asegs;
			clienteNombreValue = await loadClienteNombre(bien.clienteId);
			initFormData();
		} catch (err) {
			console.error('Error loading poliza:', err);
			error = err instanceof Error ? err.message : 'Error al cargar la póliza';
		} finally {
			loading = false;
		}
	}

	function initFormData() {
		if (!poliza) return;
		const next: Record<string, any> = {
			inicio_vigencia: poliza.inicio_vigencia ?? undefined,
			fin_vigencia: poliza.fin_vigencia ?? undefined,
			numero_poliza_aseguradora: poliza.numero_poliza_aseguradora ?? undefined
		};
		for (const slot of SLOTS) {
			next[`id_aseguradora_${slot}`] = poliza[`id_aseguradora_${slot}`] ?? undefined;
			next[`valor_prima_aseg_${slot}`] = poliza[`valor_prima_aseg_${slot}`] ?? undefined;
		}
		for (const { key } of [...valores, ...FINANCIEROS]) {
			next[key] = poliza[key] ?? undefined;
		}
		formData = next;
	}

	/** The backend needs explicit nulls to clear a column; undefined is ignored. */
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
			await service.update(polizaId, prepareDataForSave(formData));
			addNotification({
				type: 'success',
				title: 'Guardado',
				message: 'Los cambios se han guardado correctamente'
			});
			editMode = false;
			invalidateCatalog();
			await loadData(polizaId);
		} catch (err) {
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
		nuevoEstado = poliza?.estado === 'PROSPECTO' ? 'VIGENTE' : (poliza?.estado ?? 'VIGENTE');
		aseguradoraSeleccionada = poliza?.aseguradora_seleccionada ?? 1;
		showEstadoModal = true;
	}

	async function handleCambiarEstado() {
		if (!poliza) return;
		saving = true;
		try {
			const data: CambiarEstadoDto = { estado: nuevoEstado };
			if (nuevoEstado === 'VIGENTE') {
				data.aseguradora_seleccionada = Number(aseguradoraSeleccionada);
			}
			await service.cambiarEstado(polizaId, data);
			addNotification({
				type: 'success',
				title: 'Estado actualizado',
				message: `La póliza ahora está en estado ${nuevoEstado}`
			});
			showEstadoModal = false;
			invalidateCatalog();
			await loadData(polizaId);
		} catch (err) {
			addNotification({
				type: 'error',
				title: 'Error',
				message: err instanceof Error ? err.message : 'No se pudo cambiar el estado'
			});
		} finally {
			saving = false;
		}
	}

	function aseguradoraNombre(id: number | null | undefined): string {
		if (!id) return '—';
		return aseguradoras.find((a) => a.id === id)?.nombre ?? `#${id}`;
	}

	$: flujo = poliza ? flujoPoliza(poliza, rubroSlug) : null;
	// Escape para corregir pólizas mal cargadas; el resto sigue el flujo.
	$: puedeForzarEstado =
		$auth.user?.tipo_usuario === 'ADMINISTRADOR' || $auth.user?.tipo_usuario === 'SUPERADMIN';

	$: aseguradorasOptions = aseguradoras.map((a) => ({ value: String(a.id), label: a.nombre }));
	$: esPropuesta = poliza?.estado === 'PROSPECTO';
	$: estadoLabel = poliza ? (ESTADO_LABELS[poliza.estado] ?? poliza.estado) : '';
	$: tieneCotizacion = SLOTS.some((slot) => poliza?.[`valor_prima_aseg_${slot}`]);
	/** Quote slot that was bound, or the cheapest quote while still a proposal. */
	$: primaVigenteValor = (() => {
		if (!poliza) return null;
		const slot = poliza.aseguradora_seleccionada;
		if (slot) return poliza[`valor_prima_aseg_${slot}`] ?? poliza.valor_prima_neta ?? null;
		const quotes = SLOTS.map((s) => poliza?.[`valor_prima_aseg_${s}`]).filter(
			(v): v is number => typeof v === 'number'
		);
		return quotes.length ? Math.min(...quotes) : (poliza.valor_prima_neta ?? null);
	})();
	$: slotsConDatos = poliza
		? SLOTS.filter((slot) => poliza?.[`id_aseguradora_${slot}`] || poliza?.[`valor_prima_aseg_${slot}`])
		: [];
</script>

<div class="page-shell">
	<PageHeader
		title={poliza?.consecutivo ?? `${esPropuesta ? 'Propuesta' : 'Póliza'} ${rubroLabel}`}
		crumb="Inicio / Operación / Pólizas"
		subtitle="{clienteNombreValue} · {rubroLabel}"
		backHref="/propuestas"
		backLabel="Volver a pólizas"
	>
		<svelte:fragment slot="actions">
			{#if poliza && flujo}
				<!--
					Una sola acción primaria: la que toca ahora. Antes había tres botones
					hermanos sin indicar cuál iba primero, que era la raíz de la confusión.
				-->
				{#if flujo.siguiente}
					{#if flujo.siguiente.enabled && flujo.siguiente.href}
						<a class="btn-primary !min-h-[38px]" href={flujo.siguiente.href}>
							Continuar: {flujo.siguiente.label}
						</a>
					{:else}
						<button
							type="button"
							class="btn-primary !min-h-[38px]"
							disabled
							title={flujo.siguiente.blockedReason}
						>
							{flujo.siguiente.blockedReason}
						</button>
					{/if}
				{/if}
				{#if !editMode}
					<button type="button" class="btn-secondary !min-h-[38px]" on:click={() => (editMode = true)}>
						Editar
					</button>
				{/if}
			{/if}
		</svelte:fragment>
	</PageHeader>

	{#if poliza}
		<FlujoPoliza {poliza} {rubroSlug} />
	{/if}

	{#if loading}
		<div class="card flex items-center gap-3">
			<span
				class="block h-4 w-4 rounded-full"
				style="border: 2px solid var(--color-accent-200); border-top-color: var(--color-accent-600); animation: spin .7s linear infinite"
			></span>
			<span style="color: var(--color-text-60)">Cargando póliza…</span>
		</div>
	{:else if error}
		<div
			class="card"
			style="border-color: var(--color-accent-400); background: var(--color-accent-100)"
		>
			<p class="font-medium" style="color: var(--color-accent-900)">No fue posible cargar la póliza</p>
			<p class="text-sm" style="color: var(--color-accent-900)">{error}</p>
		</div>
	{:else if poliza}
		{#if showEntrega(poliza)}
			<div class="mb-3.5">
				<SeccionEntrega {poliza} />
			</div>
		{/if}

		<div class="detail-grid">
			<!-- Main column -->
			<div class="flex flex-col gap-3.5 min-w-0">
				<div class="card">
					<div class="row-card-head !mb-3.5">
						<StatusBadge status={poliza.estado} label={estadoLabel} />
						<Tag variant="neutral">{rubroLabel}</Tag>
						{#if poliza.inicio_vigencia}
							<span class="text-xs" style="color: var(--color-text-55)">
								Vigente desde {formatDateShort(poliza.inicio_vigencia)}
							</span>
						{/if}
					</div>

					<div class="field-grid">
						<div>
							<div class="field-label">Cliente</div>
							<div class="field-value">{clienteNombreValue}</div>
						</div>
						{#each bienFields as field}
							<div>
								<div class="field-label">{field.label}</div>
								<div class="field-value">{field.value}</div>
							</div>
						{/each}
						<div>
							<div class="field-label">Aseguradora</div>
							<div class="field-value">
								{aseguradoraNombre(
									poliza.aseguradora_seleccionada
										? poliza[`id_aseguradora_${poliza.aseguradora_seleccionada}`]
										: null
								)}
							</div>
						</div>
						<div>
							<div class="field-label">N° de póliza</div>
							<div class="field-value">{poliza.numero_poliza_aseguradora || '—'}</div>
						</div>
					</div>
				</div>

				<!-- Insured values -->
				<div class="card">
					<h3 class="card-heading">Valores asegurados</h3>
					{#if editMode}
						<div class="grid gap-3.5 sm:grid-cols-2">
							{#each valores as valor}
								<FormField label={valor.label}>
									<CurrencyInput bind:value={formData[valor.key]} />
								</FormField>
							{/each}
						</div>
					{:else}
						<div class="grid gap-2.5" style="grid-template-columns: repeat(auto-fit, minmax(230px, 1fr))">
							{#each valores as valor}
								<div class="rounded-xl px-3 py-2.5" style="border: 1px solid var(--color-divider)">
									<div class="field-label">{valor.label}</div>
									<div class="text-[15px] font-semibold">{money(poliza[valor.key])}</div>
								</div>
							{/each}
						</div>
					{/if}
				</div>

				<!-- Quote slots -->
				<div class="card">
					<h3 class="card-heading">Opciones de aseguradoras</h3>
					<p class="text-xs mb-3" style="color: var(--color-text-55)">
						Hasta cinco cotizaciones por póliza; al emitirla se marca la elegida.
					</p>

					{#if editMode}
						<div class="flex flex-col gap-2.5">
							{#each SLOTS as slot}
								<div
									class="grid gap-3.5 rounded-xl p-3 sm:grid-cols-2"
									style="border: 1px solid var(--color-divider)"
								>
									<FormField label="Aseguradora {slot}">
										<Select
											options={aseguradorasOptions}
											bind:value={formData[`id_aseguradora_${slot}`]}
											placeholder="Seleccionar…"
										/>
									</FormField>
									<FormField label="Prima {slot}">
										<CurrencyInput bind:value={formData[`valor_prima_aseg_${slot}`]} />
									</FormField>
								</div>
							{/each}
						</div>
					{:else if slotsConDatos.length}
						<div class="flex flex-col gap-2">
							{#each slotsConDatos as slot}
								<div
									class="flex flex-wrap items-center gap-2.5 rounded-xl px-3 py-2.5"
									style="border: 1px solid {poliza.aseguradora_seleccionada === slot
										? 'var(--color-accent)'
										: 'var(--color-divider)'}; background: {poliza.aseguradora_seleccionada === slot
										? 'var(--color-accent-100)'
										: 'transparent'}"
								>
									<span
										class="grid h-6 w-6 flex-none place-items-center rounded-full text-xs font-medium"
										style="background: var(--color-surface)">{slot}</span
									>
									<span class="font-medium">{aseguradoraNombre(poliza[`id_aseguradora_${slot}`])}</span>
									{#if poliza.aseguradora_seleccionada === slot}
										<Tag variant="accent">Seleccionada</Tag>
									{/if}
									<span class="ml-auto font-semibold">
										{money(poliza[`valor_prima_aseg_${slot}`])}
									</span>
								</div>
							{/each}
						</div>
					{:else}
						<p class="text-sm" style="color: var(--color-text-60)">
							Todavía no se han registrado cotizaciones para esta póliza.
						</p>
					{/if}
				</div>

				{#if editMode}
					<div class="flex justify-end gap-2">
						<button
							type="button"
							class="btn-secondary"
							disabled={saving}
							on:click={() => {
								editMode = false;
								initFormData();
							}}
						>
							Cancelar
						</button>
						<button type="button" class="btn-primary" disabled={saving} on:click={handleSave}>
							{saving ? 'Guardando…' : 'Guardar cambios'}
						</button>
					</div>
				{/if}
			</div>

			<!-- Right rail -->
			<div class="flex flex-col gap-3.5 min-w-0">
				<div class="card">
					<div class="field-label">
						{poliza.aseguradora_seleccionada ? 'Prima anual' : 'Mejor cotización'}
					</div>
					<div class="detail-metric">{money(primaVigenteValor)}</div>

					<div class="my-3.5 h-px" style="background: var(--color-divider)"></div>

					{#if editMode}
						<div class="flex flex-col gap-3.5">
							{#each FINANCIEROS as item}
								<FormField label={item.label}>
									<CurrencyInput bind:value={formData[item.key]} />
								</FormField>
							{/each}
						</div>
					{:else}
						<div class="flex flex-col gap-2.5 text-sm">
							{#each FINANCIEROS as item}
								<div class="flex justify-between gap-2.5">
									<span style="color: var(--color-text-60)">{item.label}</span>
									<span class="font-medium">{money(poliza[item.key])}</span>
								</div>
							{/each}
						</div>
					{/if}
				</div>

				<div class="card">
					<h3 class="card-heading">Vigencia</h3>
					{#if editMode}
						<div class="flex flex-col gap-3.5">
							<FormField label="Inicio">
								<input type="date" class="input" bind:value={formData.inicio_vigencia} />
							</FormField>
							<FormField label="Fin">
								<input type="date" class="input" bind:value={formData.fin_vigencia} />
							</FormField>
							<FormField label="N° de póliza aseguradora">
								<input type="text" class="input" bind:value={formData.numero_poliza_aseguradora} />
							</FormField>
						</div>
					{:else}
						<div class="flex flex-col gap-2.5 text-sm">
							<div class="flex justify-between gap-2.5">
								<span style="color: var(--color-text-60)">Inicio</span>
								<span class="font-medium">{formatDateShort(poliza.inicio_vigencia)}</span>
							</div>
							<div class="flex justify-between gap-2.5">
								<span style="color: var(--color-text-60)">Fin</span>
								<span class="font-medium">{formatDateShort(poliza.fin_vigencia)}</span>
							</div>
							<div class="flex justify-between gap-2.5">
								<span style="color: var(--color-text-60)">Creada</span>
								<span class="font-medium">{formatDateShort(poliza.created_at)}</span>
							</div>
							<div class="flex justify-between gap-2.5">
								<span style="color: var(--color-text-60)">Actualizada</span>
								<span class="font-medium">{formatDateShort(poliza.updated_at)}</span>
							</div>
						</div>
					{/if}
				</div>

				<div class="card">
					<h3 class="card-heading">Acciones</h3>
					<!--
						Los pasos del recorrido viven en la barra y en el botón primario.
						Aquí sólo queda lo que NO es un paso: el documento de entrega
						(posterior al recorrido) y las salidas.
					-->
					<div class="flex flex-col gap-2">
						{#if poliza.estado === 'VIGENTE'}
							<a
								class="btn-secondary !justify-start !min-h-[38px]"
								href="/propuestas/{rubroSlug}/{polizaId}/generar?doc=entrega"
							>
								Generar documento de entrega
							</a>
							{#if poliza.entrega_generada_at}
								<span class="text-xs -mt-1 px-1" style="color: var(--color-text-55)">
									Último documento: {formatDateShort(poliza.entrega_generada_at)}
								</span>
							{/if}
						{/if}
						{#if puedeForzarEstado && poliza.estado !== 'CANCELADA'}
							<button
								type="button"
								class="btn-secondary !justify-start !min-h-[38px]"
								on:click={openCambiarEstadoModal}
							>
								Cambiar estado
							</button>
						{/if}
						<button
							type="button"
							class="btn-secondary !justify-start !min-h-[38px]"
							on:click={() => goto('/propuestas')}
						>
							Volver al listado
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>

<Modal bind:open={showEstadoModal} title="Cambiar estado" size="sm">
	<div class="space-y-3.5">
		<FormField label="Nuevo estado">
			<Select
				options={estadosOptions.filter((e) => e.value !== poliza?.estado)}
				bind:value={nuevoEstado}
			/>
		</FormField>

		{#if nuevoEstado === 'VIGENTE'}
			<FormField label="Aseguradora seleccionada">
				<Select
					options={SLOTS.filter((slot) => poliza?.[`id_aseguradora_${slot}`]).map((slot) => ({
						value: String(slot),
						label: `${slot} — ${aseguradoraNombre(poliza?.[`id_aseguradora_${slot}`])}`
					}))}
					bind:value={aseguradoraSeleccionada}
				/>
			</FormField>
			<p class="text-sm" style="color: var(--color-text-60)">
				Al pasar a vigente debes indicar cuál de las aseguradoras cotizadas fue la elegida.
			</p>
		{/if}
	</div>

	<svelte:fragment slot="footer">
		<div class="flex justify-end gap-2">
			<button
				type="button"
				class="btn-secondary"
				disabled={saving}
				on:click={() => (showEstadoModal = false)}
			>
				Cancelar
			</button>
			<button type="button" class="btn-primary" disabled={saving} on:click={handleCambiarEstado}>
				{saving ? 'Guardando…' : 'Cambiar estado'}
			</button>
		</div>
	</svelte:fragment>
</Modal>
