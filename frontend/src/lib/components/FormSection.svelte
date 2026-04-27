<script lang="ts">
	/**
	 * FormSection - Collapsible form section with status indicator
	 * 
	 * @prop title - Section title
	 * @prop status - 'pending' | 'active' | 'complete'
	 * @prop open - Whether section is expanded (bindable)
	 */

	export let title: string;
	export let status: 'pending' | 'active' | 'complete' = 'pending';
	export let open: boolean = false;

	function toggle() {
		open = !open;
	}

	function getIndicatorClass(status: string): string {
		switch (status) {
			case 'active':
				return 'form-section-indicator-active';
			case 'complete':
				return 'form-section-indicator-complete';
			default:
				return '';
		}
	}
</script>

<div class="form-section">
	<!-- Header (clickable) -->
	<button
		type="button"
		class="form-section-header w-full"
		on:click={toggle}
		aria-expanded={open}
	>
		<div class="form-section-title">
			<span class="form-section-indicator {getIndicatorClass(status)}"></span>
			<span class="form-section-title-text">{title}</span>
		</div>
		
		<svg
			class="form-section-chevron {open ? 'form-section-chevron-open' : ''}"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			stroke-width="2"
		>
			<path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
		</svg>
	</button>

	<!-- Content (collapsible) -->
	<div class="collapse-content {open ? 'open' : ''}">
		<div>
			<div class="form-section-content">
				<slot />
			</div>
		</div>
	</div>
</div>
