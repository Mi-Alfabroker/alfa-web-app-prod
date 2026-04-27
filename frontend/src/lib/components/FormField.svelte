<script lang="ts">
	/**
	 * FormField - Form field with horizontal label layout
	 * 
	 * @prop label - Field label text
	 * @prop helper - Helper text below label (optional)
	 * @prop required - Show required indicator
	 * @prop vertical - Use vertical layout instead of horizontal
	 */

	export let label: string;
	export let helper: string = '';
	export let required: boolean = false;
	export let vertical: boolean = false;
</script>

<div class={vertical ? 'form-field-vertical' : 'form-field'}>
	<!-- Label group -->
	<div class="form-label-group">
		<label class="form-label">
			{label}
			{#if required}
				<span class="text-red-500">*</span>
			{/if}
		</label>
		{#if helper}
			<span class="form-label-helper">{helper}</span>
		{/if}
	</div>

	<!-- Input group (slot) -->
	<div class="form-input-group">
		<slot />
	</div>
</div>
