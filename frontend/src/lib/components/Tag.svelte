<script lang="ts">
	/**
	 * Tag - pill label in the design system's four-state vocabulary.
	 *
	 * @prop variant - accent (active/positive) | accent-2 (pending/info)
	 *                 | neutral (inert) | outline (terminal/negative)
	 */
	type TagVariant = 'accent' | 'accent-2' | 'neutral' | 'outline';

	export let variant: TagVariant = 'neutral';
</script>

<span class="tag tag-{variant}">
	<slot />
</span>
