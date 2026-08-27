<script lang="ts">
	/**
	 * Avatar - initials tile used as the lead element of a row card.
	 *
	 * @prop name - full name/label; initials are derived from it
	 * @prop text - explicit label, overrides the derived initials (e.g. "HOG")
	 * @prop shape - circle for people, square for entities and documents
	 * @prop strong - dark gold fill, for aseguradora tiles
	 */
	import { initials } from '$utils/formatters';

	export let name: string = '';
	export let text: string = '';
	export let shape: 'circle' | 'square' = 'circle';
	export let strong: boolean = false;

	$: label = text || initials(name);
</script>

<span class="avatar avatar-{shape} {strong ? 'avatar-strong' : ''}">{label}</span>
