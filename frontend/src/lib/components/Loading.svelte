<script lang="ts">
	export let size: 'sm' | 'md' | 'lg' = 'md';
	export let fullscreen: boolean = false;

	const sizeClasses = {
		sm: 'h-5 w-5',
		md: 'h-8 w-8',
		lg: 'h-12 w-12'
	};
</script>

{#if fullscreen}
	<div class="fixed inset-0 bg-secondary-900/50 flex items-center justify-center z-50">
		<svg
			class="animate-spin {sizeClasses[size]} text-white"
			fill="none"
			viewBox="0 0 24 24"
		>
			<circle
				class="opacity-25"
				cx="12"
				cy="12"
				r="10"
				stroke="currentColor"
				stroke-width="4"
			/>
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
			/>
		</svg>
	</div>
{:else}
	<div class="flex items-center justify-center">
		<svg
			class="animate-spin {sizeClasses[size]} text-primary-600"
			fill="none"
			viewBox="0 0 24 24"
		>
			<circle
				class="opacity-25"
				cx="12"
				cy="12"
				r="10"
				stroke="currentColor"
				stroke-width="4"
			/>
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
			/>
		</svg>
	</div>
{/if}
