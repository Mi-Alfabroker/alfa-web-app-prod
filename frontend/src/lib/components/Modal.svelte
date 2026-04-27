<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { fade, scale } from 'svelte/transition';

	export let open: boolean = false;
	export let title: string = '';
	export let size: 'sm' | 'md' | 'lg' | 'xl' | 'full' = 'md';

	const dispatch = createEventDispatcher();

	function close() {
		open = false;
		dispatch('close');
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape' && open) {
			close();
		}
	}

	function handleBackdropClick(e: MouseEvent) {
		if (e.target === e.currentTarget) {
			close();
		}
	}

	const sizeClasses = {
		sm: 'max-w-md',
		md: 'max-w-lg',
		lg: 'max-w-2xl',
		xl: 'max-w-4xl',
		full: 'max-w-6xl'
	};
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
	<!-- Backdrop -->
	<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
	<div 
		class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
		transition:fade={{ duration: 150 }}
		on:click={handleBackdropClick}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
	>
		<!-- Modal Content -->
		<div 
			class="bg-white rounded-lg shadow-xl w-full {sizeClasses[size]} max-h-[90vh] flex flex-col"
			transition:scale={{ duration: 150, start: 0.95 }}
		>
			<!-- Header -->
			<div class="flex items-center justify-between px-6 py-4 border-b border-secondary-200">
				<h2 id="modal-title" class="text-lg font-semibold text-secondary-900">{title}</h2>
				<button 
					type="button"
					class="p-1.5 text-secondary-400 hover:text-secondary-600 hover:bg-secondary-100 rounded-lg transition-colors"
					on:click={close}
					aria-label="Cerrar"
				>
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>

			<!-- Body -->
			<div class="flex-1 overflow-y-auto px-6 py-4">
				<slot />
			</div>

			<!-- Footer (optional) -->
			{#if $$slots.footer}
				<div class="px-6 py-4 border-t border-secondary-200 bg-secondary-50">
					<slot name="footer" />
				</div>
			{/if}
		</div>
	</div>
{/if}
