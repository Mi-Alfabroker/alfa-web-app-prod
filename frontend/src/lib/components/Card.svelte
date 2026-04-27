<script lang="ts">
	export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';

	const paddingClasses = {
		none: '',
		sm: 'p-4',
		md: 'p-6',
		lg: 'p-8'
	};
</script>

<div class="bg-white rounded-xl shadow-sm border border-secondary-200 {paddingClasses[padding]}">
	<slot />
</div>
