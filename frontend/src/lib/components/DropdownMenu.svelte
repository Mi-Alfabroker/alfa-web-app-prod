<script lang="ts">
	/**
	 * DropdownMenu - popover anchored to its own trigger button, clamped to the
	 * viewport so a row menu near the bottom or right edge stays fully visible.
	 *
	 * @prop width - popover width in px, also used for the horizontal clamp
	 * @prop height - expected popover height in px, used for the vertical clamp
	 * @prop align - anchor the popover's right edge to the trigger's right edge
	 *               (default) or its left to the trigger's left
	 * @prop label - accessible label for the trigger
	 * @slot trigger - trigger content; defaults to a vertical "kebab" icon
	 * @slot default - menu items (use .menu-item / .menu-divider)
	 */
	export let width: number = 226;
	export let height: number = 210;
	export let align: 'left' | 'right' = 'right';
	export let label: string = 'Acciones';
	export let open: boolean = false;

	let pos = { top: '0px', left: '0px' };

	function place(event: MouseEvent) {
		const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
		const anchorLeft = align === 'right' ? rect.right - width : rect.left;
		pos = {
			top: Math.max(8, Math.min(rect.bottom + 6, window.innerHeight - height)) + 'px',
			left: Math.max(8, Math.min(anchorLeft, window.innerWidth - width - 8)) + 'px'
		};
	}

	function toggle(event: MouseEvent) {
		if (!open) place(event);
		open = !open;
	}

	export function close() {
		open = false;
	}
</script>

<button
	type="button"
	class="btn-secondary btn-icon !w-8 !h-8 !border-transparent"
	title={label}
	aria-label={label}
	aria-expanded={open}
	on:click|stopPropagation={toggle}
>
	<slot name="trigger">
		<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
			<circle cx="12" cy="5.5" r="1.2" />
			<circle cx="12" cy="12" r="1.2" />
			<circle cx="12" cy="18.5" r="1.2" />
		</svg>
	</slot>
</button>

{#if open}
	<!-- Full-viewport catcher below the popover: one click anywhere closes it. -->
	<div
		class="fixed inset-0 z-[69]"
		role="presentation"
		on:click={close}
	></div>
	<div
		class="menu-popover"
		style="top: {pos.top}; left: {pos.left}; width: {width}px"
		role="menu"
		tabindex="-1"
		on:click={close}
		on:keydown={(e) => e.key === 'Escape' && close()}
	>
		<slot />
	</div>
{/if}
