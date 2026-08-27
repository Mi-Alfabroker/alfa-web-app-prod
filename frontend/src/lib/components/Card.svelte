<script lang="ts">
	/**
	 * Card - surface wrapper delegating to the .card class in app.css, so it
	 * cannot drift from the pages that use .card directly.
	 */
	export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';

	const paddingClasses = {
		none: 'p-0',
		sm: 'p-4',
		md: '',
		lg: 'p-8'
	};
</script>

<div class="card {paddingClasses[padding]}">
	<slot />
</div>
