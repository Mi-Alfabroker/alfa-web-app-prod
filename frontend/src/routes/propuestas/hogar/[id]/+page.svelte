<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { PolizaDetalle } from '$components';
	import { aseguradoraService, bienService, clienteService, polizaService } from '$services';
	import { clienteNombre } from '$utils';
	import type { PolizaHogar } from '$lib/types/poliza';

	$: polizaId = Number($page.params.id);

	const valores = [
		{ key: 'valor_inmueble_asegurado', label: 'Valor inmueble' },
		{ key: 'valor_contenidos_normales_asegurado', label: 'Contenidos normales' },
		{ key: 'valor_contenidos_especiales_asegurado', label: 'Contenidos especiales' },
		{ key: 'valor_equipo_electronico_asegurado', label: 'Equipo electrónico' },
		{ key: 'valor_maquinaria_equipo_asegurado', label: 'Maquinaria y equipo' },
		{ key: 'valor_rc_asegurado', label: 'Responsabilidad civil' }
	];

	async function loadBien(poliza: PolizaHogar) {
		const hogar = await bienService.hogares.getById(poliza.id_hogar);
		return {
			clienteId: hogar?.id_usuario ?? null,
			fields: [
				{ label: 'Tipo de inmueble', value: hogar?.tipo_inmueble || '—' },
				{ label: 'Ciudad', value: hogar?.ciudad_inmueble || '—' },
				{ label: 'Dirección', value: hogar?.direccion_inmueble || '—' }
			]
		};
	}

	async function loadClienteNombre(clienteId: number | null) {
		if (!clienteId) return '—';
		const clientes = await clienteService.getAll();
		return clienteNombre(
			clientes.find((c) => c.id === clienteId),
			clienteId
		);
	}
</script>

<svelte:head>
	<title>Póliza Hogar | {APP_NAME}</title>
</svelte:head>

<PolizaDetalle
	{polizaId}
	rubroLabel="Hogar"
	rubroSlug="hogar"
	service={polizaService.hogar}
	{valores}
	{loadBien}
	{loadClienteNombre}
	loadAseguradoras={() => aseguradoraService.getAll()}
	showEntrega={(poliza) => poliza.estado === 'VIGENTE' && !!poliza.numero_poliza}
/>
