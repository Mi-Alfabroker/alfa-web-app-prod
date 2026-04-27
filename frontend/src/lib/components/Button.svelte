<script lang="ts">
	type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost';
	type ButtonSize = 'sm' | 'md' | 'lg';

	export let variant: ButtonVariant = 'primary';
	export let size: ButtonSize = 'md';
	export let disabled: boolean = false;
	export let loading: boolean = false;
	export let type: 'button' | 'submit' | 'reset' = 'button';

	const variantClasses: Record<ButtonVariant, string> = {
		primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
		secondary: 'bg-secondary-200 text-secondary-900 hover:bg-secondary-300 focus:ring-secondary-500',
		danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
		ghost: 'bg-transparent text-secondary-700 hover:bg-secondary-100 focus:ring-secondary-500'
	};

	const sizeClasses: Record<ButtonSize, string> = {
		sm: 'px-3 py-1.5 text-sm',
		md: 'px-4 py-2 text-base',
		lg: 'px-6 py-3 text-lg'
	};
</script>

<button
	{type}
	disabled={disabled || loading}
	class="inline-flex items-center justify-center font-medium rounded-lg transition-colors duration-200 
		focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed
		{variantClasses[variant]} {sizeClasses[size]}"
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
