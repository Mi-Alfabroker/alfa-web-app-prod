<script lang="ts">
	/**
	 * FormField - etiqueta, control y, si hace falta, una ayuda debajo.
	 *
	 * La ayuda va DEBAJO del control, no entre la etiqueta y él. Colocada en
	 * medio, cada campo se leía como tres líneas de texto antes de llegar al
	 * input y el formulario se sentía interminable aunque tuviera pocos campos.
	 * Debajo cumple su papel —se lee al dudar— sin estorbar el recorrido normal.
	 *
	 * @prop label - texto de la etiqueta
	 * @prop helper - ayuda bajo el control (opcional)
	 * @prop required - muestra el indicador de obligatorio
	 * @prop horizontal - layout antiguo de etiqueta a la izquierda
	 * @prop wide - ocupa la fila completa de la rejilla de la sección
	 */

	export let label: string;
	export let helper: string = '';
	export let required: boolean = false;
	export let horizontal: boolean = false;
	export let wide: boolean = false;
</script>

{#if horizontal}
	<div class="form-field {wide ? 'form-field-wide' : ''}">
		<div class="form-label-group">
			<label class="form-label">
				{label}
				{#if required}<span class="form-required">*</span>{/if}
			</label>
			{#if helper}
				<span class="form-label-helper">{helper}</span>
			{/if}
		</div>
		<div class="form-input-group">
			<slot />
		</div>
	</div>
{:else}
	<div class="form-field-vertical {wide ? 'form-field-wide' : ''}">
		<label class="form-label">
			{label}
			{#if required}<span class="form-required">*</span>{/if}
		</label>
		<div class="form-input-group">
			<slot />
		</div>
		{#if helper}
			<span class="form-field-hint">{helper}</span>
		{/if}
	</div>
{/if}
