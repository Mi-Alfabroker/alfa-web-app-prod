<script lang="ts">
	/**
	 * Button - thin wrapper over the .btn-* classes in app.css.
	 *
	 * It deliberately holds no colour or spacing of its own: when this
	 * component carried its own Tailwind maps it drifted from .btn-primary
	 * (white-on-gold here, ink-on-gold there), so the two rendered
	 * differently on the same page.
	 */
	type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost';
	type ButtonSize = 'sm' | 'md' | 'lg';

	export let variant: ButtonVariant = 'primary';
	export let size: ButtonSize = 'md';
	export let disabled: boolean = false;
	export let loading: boolean = false;
	export let type: 'button' | 'submit' | 'reset' = 'button';
	/** Extra classes, e.g. `btn-block` or `btn-icon`. */
	export let extraClass: string = '';

	const sizeClasses: Record<ButtonSize, string> = {
		sm: 'btn-sm',
		md: '',
		lg: 'btn-lg'
	};
</script>

<button
	{type}
	disabled={disabled || loading}
	class="btn-{variant} {sizeClasses[size]} {extraClass}"
	on:click
>
	{#if loading}
		<svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
			<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
			/>
		</svg>
	{/if}
	<slot />
</button>
