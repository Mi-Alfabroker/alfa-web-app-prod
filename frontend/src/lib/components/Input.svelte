<script lang="ts">
	/**
	 * Input - Styled input component
	 * 
	 * @prop type - Input type (text, email, tel, date, number, url, password, textarea)
	 * @prop value - Input value (bindable)
	 * @prop placeholder - Placeholder text
	 * @prop name - Input name attribute
	 * @prop id - Input id attribute
	 * @prop required - Required field
	 * @prop disabled - Disabled state
	 * @prop error - Show error state
	 * @prop helperText - Helper text below input
	 * @prop errorText - Error message to display
	 */

	export let type: 'text' | 'email' | 'tel' | 'date' | 'number' | 'url' | 'password' | 'textarea' = 'text';
	export let value: string = '';
	export let placeholder: string = '';
	export let name: string = '';
	export let id: string = '';
	export let required: boolean = false;
	export let disabled: boolean = false;
	export let error: boolean = false;
	export let helperText: string = '';
	export let errorText: string = '';

	$: inputClass = `input ${error ? 'input-error' : ''}`;
</script>

<div class="w-full">
	{#if type === 'textarea'}
		<textarea
			class="textarea {error ? 'input-error' : ''}"
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		></textarea>
	{:else if type === 'email'}
		<input
			type="email"
			class={inputClass}
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		/>
	{:else if type === 'tel'}
		<input
			type="tel"
			class={inputClass}
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		/>
	{:else if type === 'date'}
		<input
			type="date"
			class={inputClass}
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		/>
	{:else if type === 'number'}
		<input
			type="number"
			class={inputClass}
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		/>
	{:else if type === 'url'}
		<input
			type="url"
			class={inputClass}
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		/>
	{:else if type === 'password'}
		<input
			type="password"
			class={inputClass}
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		/>
	{:else}
		<input
			type="text"
			class={inputClass}
			{name}
			{id}
			{placeholder}
			{required}
			{disabled}
			bind:value
			on:input
			on:change
			on:blur
			on:focus
		/>
	{/if}

	{#if errorText && error}
		<p class="input-error-text mt-1">{errorText}</p>
	{:else if helperText}
		<p class="input-helper mt-1">{helperText}</p>
	{/if}
</div>
