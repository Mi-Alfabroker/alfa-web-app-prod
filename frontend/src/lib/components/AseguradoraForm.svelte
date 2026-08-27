<script lang="ts">
	/**
	 * AseguradoraForm - the design's pill-tabbed aseguradora editor, shared by
	 * the create and edit routes.
	 *
	 * Replaces two ~1000-line accordion pages that each laid out the same ~80
	 * condition columns by hand. The structure now comes from
	 * ASEGURADORA_RUBROS, so the two routes cannot drift apart.
	 *
	 * Each condition renders as a card carrying its section, a
	 * "Sin definir / Definido / Editado" state, and an accent border once the
	 * value differs from what was loaded.
	 */
	import { goto } from '$app/navigation';
	import { PageHeader, PillTabs, Tag } from '$components';
	import { ASEGURADORA_GENERALES, ASEGURADORA_RUBROS } from '$constants';
	import { aseguradoraService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import { invalidateCatalog } from '$lib/stores/catalog';
	import type { Aseguradora } from '$lib/types/aseguradora';

	/** Omit for the create form; pass an id to load and update. */
	export let aseguradoraId: number | null = null;

	let formData: Record<string, string> = {};
	/** Values as loaded, so "Editado" reflects a real change by the user. */
	let original: Record<string, string> = {};

	let activeTab = 'generales';
	let loading = aseguradoraId !== null;
	let saving = false;
	let error: string | null = null;

	const tabs = [
		{ id: 'generales', label: 'Generales' },
		...ASEGURADORA_RUBROS.map((r) => ({
			id: r.id,
			label: r.label,
			count: r.sections.reduce((n, s) => n + s.fields.length, 0)
		}))
	];

	const RUBRO_KEYS = ASEGURADORA_RUBROS.flatMap((r) =>
		r.sections.flatMap((s) => s.fields.map((f) => f.key))
	);
	const ALL_KEYS = [...ASEGURADORA_GENERALES.map((f) => f.key), ...RUBRO_KEYS];

	function blank(): Record<string, string> {
		return Object.fromEntries(ALL_KEYS.map((k) => [k, '']));
	}

	async function load(id: number | null) {
		if (id === null) {
			formData = blank();
			original = blank();
			loading = false;
			return;
		}
		loading = true;
		error = null;
		try {
			const record = (await aseguradoraService.getById(id)) as unknown as Record<string, unknown>;
			const next = blank();
			for (const key of ALL_KEYS) {
				const value = record[key];
				next[key] = value === null || value === undefined ? '' : String(value);
			}
			formData = next;
			original = { ...next };
		} catch (err) {
			error = err instanceof Error ? err.message : 'Error al cargar la aseguradora';
		} finally {
			loading = false;
		}
	}

	// Reload whenever the route id changes.
	$: void load(aseguradoraId);

	$: activeRubro = ASEGURADORA_RUBROS.find((r) => r.id === activeTab) ?? null;

	// Counts the per-rubro conditions only; the contact fields are not conditions.
	$: definidos = RUBRO_KEYS.filter((k) => formData[k]?.trim()).length;
	$: editados = ALL_KEYS.filter((k) => (formData[k] ?? '') !== (original[k] ?? '')).length;

	interface FieldState {
		label: string;
		variant: 'accent' | 'neutral';
		edited: boolean;
	}

	/**
	 * `current` and `loaded` are passed in rather than read from the closure on
	 * purpose. Svelte derives a reactive statement's dependencies from the names
	 * that appear in its own expression, so a helper that reached for `formData`
	 * internally would never re-run as the user types — the state tags and the
	 * accent border would stay frozen at their initial values.
	 */
	function buildStates(
		current: Record<string, string>,
		loaded: Record<string, string>
	): Record<string, FieldState> {
		const out: Record<string, FieldState> = {};
		for (const key of RUBRO_KEYS) {
			const value = current[key] ?? '';
			if (value !== (loaded[key] ?? '')) {
				out[key] = { label: 'Editado', variant: 'accent', edited: true };
			} else if (value.trim()) {
				out[key] = { label: 'Definido', variant: 'neutral', edited: false };
			} else {
				out[key] = { label: 'Sin definir', variant: 'neutral', edited: false };
			}
		}
		return out;
	}

	$: fieldStates = buildStates(formData, original);

	/** Restore the loaded values for the visible rubro only. */
	function restoreRubro() {
		if (!activeRubro) return;
		const keys = activeRubro.sections.flatMap((s) => s.fields.map((f) => f.key));
		const next = { ...formData };
		for (const key of keys) next[key] = original[key] ?? '';
		formData = next;
	}

	/** Empty strings become null so the backend clears the column. */
	function payload(): Record<string, unknown> {
		const out: Record<string, unknown> = {};
		for (const key of ALL_KEYS) {
			const value = formData[key]?.trim();
			out[key] = value ? value : null;
		}
		return out;
	}

	async function handleSave() {
		if (!formData.nombre?.trim()) {
			addNotification({
				type: 'error',
				title: 'Falta el nombre',
				message: 'El nombre de la aseguradora es obligatorio.'
			});
			activeTab = 'generales';
			return;
		}

		saving = true;
		try {
			if (aseguradoraId === null) {
				const created = (await aseguradoraService.create(payload() as any)) as Aseguradora;
				addNotification({
					type: 'success',
					title: 'Aseguradora registrada',
					message: `${created.nombre} quedó disponible para cotizar.`
				});
				invalidateCatalog();
				await goto(`/aseguradoras/${created.id}`);
			} else {
				await aseguradoraService.update(aseguradoraId, payload() as any);
				addNotification({
					type: 'success',
					title: 'Cambios guardados',
					message: 'Las condiciones de la aseguradora se actualizaron.'
				});
				invalidateCatalog();
				await goto(`/aseguradoras/${aseguradoraId}`);
			}
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
</script>

<div class="page-shell">
	<PageHeader
		title={aseguradoraId === null ? 'Registrar aseguradora' : formData.nombre || 'Editar aseguradora'}
		crumb="Inicio / Operación / Aseguradoras"
		subtitle="Datos de contacto y condiciones negociadas por rubro"
		backHref={aseguradoraId === null ? '/aseguradoras' : `/aseguradoras/${aseguradoraId}`}
		backLabel="Volver a aseguradoras"
	/>

	{#if loading}
		<div class="card flex items-center gap-3">
			<span
				class="block h-4 w-4 rounded-full"
				style="border: 2px solid var(--color-accent-200); border-top-color: var(--color-accent-600); animation: spin .7s linear infinite"
			></span>
			<span style="color: var(--color-text-60)">Cargando aseguradora…</span>
		</div>
	{:else if error}
		<div class="card" style="border-color: var(--color-accent-400); background: var(--color-accent-100)">
			<p class="font-medium" style="color: var(--color-accent-900)">
				No fue posible cargar la aseguradora
			</p>
			<p class="text-sm" style="color: var(--color-accent-900)">{error}</p>
		</div>
	{:else}
		<div class="flex flex-col gap-3.5">
			<PillTabs {tabs} bind:active={activeTab} />

			{#if activeTab === 'generales'}
				<div class="card">
					<h3 class="card-heading">Datos de la aseguradora</h3>
					<div class="grid gap-3.5 sm:grid-cols-2">
						{#each ASEGURADORA_GENERALES as field}
							<div>
								<label class="mb-1.5 block text-[13px] font-medium" for={field.key}>
									{field.label}
									{#if field.key === 'nombre'}<span style="color: var(--color-accent-800)">*</span>{/if}
								</label>
								<input
									id={field.key}
									class="input"
									bind:value={formData[field.key]}
									placeholder={field.placeholder ?? ''}
								/>
							</div>
						{/each}
					</div>
				</div>
			{:else if activeRubro}
				<div
					class="flex flex-wrap items-center gap-3 rounded-xl px-3.5 py-2.5"
					style="background: var(--color-accent-100); border: 1px solid var(--color-accent-300)"
				>
					<div class="flex-1 min-w-[220px] text-[13px]" style="color: var(--color-accent-900)">
						Condiciones negociadas para <strong>{activeRubro.label}</strong>. Se usan al construir la
						propuesta; deja en blanco lo que no aplique.
					</div>
					<button
						type="button"
						class="btn-secondary !h-8 !py-0 !px-3 !text-xs"
						style="background: var(--color-bg)"
						on:click={restoreRubro}
					>
						Descartar cambios del rubro
					</button>
				</div>

				{#each activeRubro.sections as section}
					<div class="card">
						<h3 class="card-heading">{section.title}</h3>
						<div
							class="grid gap-2.5"
							style="grid-template-columns: repeat(auto-fit, minmax(268px, 1fr))"
						>
							{#each section.fields as field}
								{@const state = fieldStates[field.key]}
								<div
									class="rounded-xl px-3 py-3 shadow-sm"
									style="background: var(--color-bg); border: 1px solid {state.edited
										? 'var(--color-accent)'
										: 'var(--color-divider)'}"
								>
									<div class="mb-1.5 flex items-center gap-2">
										<span
											class="text-[10.5px] uppercase"
											style="letter-spacing: .05em; color: var(--color-accent-800)"
										>
											{section.title}
										</span>
										<span class="ml-auto">
											<Tag variant={state.variant}>{state.label}</Tag>
										</span>
									</div>
									<label class="mb-1.5 block text-[13px] font-medium" for={field.key}>
										{field.label}
									</label>
									<input
										id={field.key}
										class="input !min-h-[38px] !text-[13px]"
										bind:value={formData[field.key]}
										placeholder="Sin definir"
									/>
								</div>
							{/each}
						</div>
					</div>
				{/each}
			{/if}

			<div class="flex flex-wrap items-center gap-2.5 card">
				<span class="text-xs" style="color: var(--color-text-55)">
					{definidos} condiciones definidas · {editados} sin guardar
				</span>
				<div class="ml-auto flex gap-2">
					<a
						class="btn-secondary !min-h-[38px]"
						href={aseguradoraId === null ? '/aseguradoras' : `/aseguradoras/${aseguradoraId}`}
					>
						Cancelar
					</a>
					<button
						type="button"
						class="btn-primary !min-h-[38px]"
						disabled={saving}
						on:click={handleSave}
					>
						{#if saving}
							Guardando…
						{:else}
							{aseguradoraId === null ? 'Registrar aseguradora' : 'Guardar cambios'}
						{/if}
					</button>
				</div>
			</div>
		</div>
	{/if}
</div>
