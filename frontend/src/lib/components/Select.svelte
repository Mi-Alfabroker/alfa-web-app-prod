<script lang="ts">
	/**
	 * Select - Styled select component
	 * 
	 * @prop value - Selected value (bindable)
	 * @prop options - Array of options { value, label }
	 * @prop placeholder - Placeholder option text
	 * @prop name - Select name attribute
	 * @prop id - Select id attribute
	 * @prop required - Required field
	 * @prop disabled - Disabled state
	 * @prop error - Show error state
	 */

	type Option = {
		value: string | number;
		label: string;
	};

	export let value: string | number = '';
	export let options: Option[] = [];
	export let placeholder: string = 'Seleccionar...';
	export let name: string = '';
	export let id: string = '';
	export let required: boolean = false;
	export let disabled: boolean = false;
	export let error: boolean = false;

	$: selectClass = `select ${error ? 'input-error' : ''}`;
</script>

<select
	class={selectClass}
	{name}
	{id}
	{required}
	{disabled}
	bind:value
	on:change
	on:blur
>
	{#if placeholder}
		<option value="" disabled selected>{placeholder}</option>
	{/if}
	{#each options as option}
		<option value={option.value}>{option.label}</option>
	{/each}
</select>
