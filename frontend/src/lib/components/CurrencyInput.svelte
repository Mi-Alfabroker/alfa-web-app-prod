<script lang="ts">
	/**
	 * CurrencyInput - Input para valores monetarios con formato de miles
	 * 
	 * Muestra los valores con separadores de miles (puntos) mientras se escribe
	 * y mantiene el valor numérico real para el binding.
	 * 
	 * @prop value - Valor numérico (bindable)
	 * @prop placeholder - Placeholder text
	 * @prop name - Input name attribute
	 * @prop id - Input id attribute
	 * @prop required - Required field
	 * @prop disabled - Disabled state
	 * @prop prefix - Prefijo a mostrar (ej: "$")
	 */

	export let value: number | undefined = undefined;
	export let placeholder: string = '0';
	export let name: string = '';
	export let id: string = '';
	export let required: boolean = false;
	export let disabled: boolean = false;
	export let prefix: string = '';

	// Valor formateado para mostrar
	let displayValue: string = '';

	// Formatear número con separadores de miles (usando punto)
	function formatNumber(num: number | undefined): string {
		if (num === undefined || num === null || isNaN(num)) return '';
		// Usar toLocaleString con configuración para puntos como separador de miles
		return num.toLocaleString('es-CO', { 
			maximumFractionDigits: 0,
			useGrouping: true 
		});
	}

	// Parsear string formateado a número
	function parseFormattedNumber(str: string): number | undefined {
		if (!str || str.trim() === '') return undefined;
		// Remover puntos (separadores de miles) y espacios
		const cleaned = str.replace(/\./g, '').replace(/\s/g, '');
		const num = parseInt(cleaned, 10);
		return isNaN(num) ? undefined : num;
	}

	// Inicializar displayValue cuando cambia value externamente
	$: {
		const formatted = formatNumber(value);
		if (formatted !== displayValue.replace(/\./g, '').replace(/\s/g, '') && 
		    formatNumber(parseFormattedNumber(displayValue)) !== formatted) {
			displayValue = formatted;
		}
	}

	// Manejar input del usuario
	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		let inputValue = target.value;
		
		// Solo permitir dígitos y puntos
		inputValue = inputValue.replace(/[^\d]/g, '');
		
		// Parsear a número
		const numValue = inputValue ? parseInt(inputValue, 10) : undefined;
		
		// Actualizar el valor real
		value = numValue;
		
		// Formatear para mostrar
		displayValue = formatNumber(numValue);
		
		// Actualizar el input con el valor formateado
		target.value = displayValue;
	}

	// Manejar cuando el campo pierde el foco
	function handleBlur() {
		displayValue = formatNumber(value);
	}

	// Manejar cuando el campo recibe el foco
	function handleFocus(event: Event) {
		const target = event.target as HTMLInputElement;
		// Seleccionar todo el texto al hacer foco
		setTimeout(() => target.select(), 0);
	}
</script>

<div class="relative w-full">
	{#if prefix}
		<span class="absolute left-3 top-1/2 -translate-y-1/2 text-secondary-500 pointer-events-none">
			{prefix}
		</span>
	{/if}
	<input
		type="text"
		inputmode="numeric"
		class="input {prefix ? 'pl-8' : ''}"
		{name}
		{id}
		placeholder={placeholder}
		{required}
		{disabled}
		value={displayValue}
		on:input={handleInput}
		on:blur={handleBlur}
		on:focus={handleFocus}
	/>
</div>
