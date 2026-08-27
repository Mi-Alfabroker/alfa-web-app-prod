<script lang="ts">
	/**
	 * FlujoPoliza - barra de pasos datos → cotizaciones → propuesta → entrega.
	 *
	 * No decide nada: pinta lo que `flujoPoliza()` deriva, para que el detalle,
	 * generar, entregar y el menú de la lista muestren exactamente el mismo
	 * estado y no puedan contradecirse.
	 *
	 * @prop pasoActual - marca el paso en curso cuando la pantalla ES ese paso;
	 *                    si se omite, se marca el que la póliza tenga pendiente.
	 */
	import { ESTADO_LABELS, flujoPoliza } from '$utils';
	import type { PasoId } from '$utils';
	import type { Poliza } from '$lib/types/poliza';

	export let poliza: Poliza;
	export let rubroSlug: string;
	export let pasoActual: PasoId | null = null;

	$: flujo = flujoPoliza(poliza, rubroSlug);
</script>

<nav class="flujo" aria-label="Progreso de la póliza">
	{#each flujo.pasos as paso, i}
		{#if i > 0}
			<span class="flujo-sep" aria-hidden="true"></span>
		{/if}

		{@const marcado = (pasoActual ? paso.id === pasoActual : paso.current) && !flujo.terminal}
		{@const clases = [
			'flujo-paso',
			paso.done ? 'flujo-paso-done' : '',
			marcado ? 'flujo-paso-current' : '',
			!paso.enabled ? 'flujo-paso-blocked' : ''
		]
			.filter(Boolean)
			.join(' ')}

		{#if paso.enabled && paso.href && !flujo.terminal}
			<a href={paso.href} class={clases} aria-current={marcado ? 'step' : undefined}>
				<span class="flujo-marca" aria-hidden="true">{paso.done ? '✓' : i + 1}</span>
				{paso.label}
			</a>
		{:else}
			<span class={clases} title={paso.blockedReason ?? ''}>
				<span class="flujo-marca" aria-hidden="true">{paso.done ? '✓' : i + 1}</span>
				{paso.label}
			</span>
		{/if}
	{/each}

	{#if flujo.terminal}
		<span class="flujo-terminal">
			Póliza {ESTADO_LABELS[poliza.estado].toLowerCase()}
		</span>
	{/if}
</nav>
