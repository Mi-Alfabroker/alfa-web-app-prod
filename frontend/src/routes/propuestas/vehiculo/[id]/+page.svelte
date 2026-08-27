<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { PolizaDetalle } from '$components';
	import { aseguradoraService, bienService, clienteService, polizaService } from '$services';
	import { clienteNombre } from '$utils';
	import type { PolizaVehiculo } from '$lib/types/poliza';

	$: polizaId = Number($page.params.id);

	const valores = [
		{ key: 'valor_vehiculo_asegurado', label: 'Valor vehículo' },
		{ key: 'valor_accesorios_asegurado', label: 'Accesorios' },
		{ key: 'valor_rc_asegurado', label: 'Responsabilidad civil' }
	];

	async function loadBien(poliza: PolizaVehiculo) {
		const vehiculo = await bienService.vehiculos.getById(poliza.id_vehiculo);
		return {
			clienteId: vehiculo?.id_usuario ?? null,
			fields: [
				{ label: 'Placa', value: vehiculo?.placa || '—' },
				{ label: 'Marca', value: vehiculo?.marca || '—' },
				{ label: 'Tipo', value: vehiculo?.tipo_vehiculo || '—' },
				{ label: 'Modelo/Año', value: vehiculo?.ano_modelo ? String(vehiculo.ano_modelo) : '—' },
				{ label: 'Serie/Referencia', value: vehiculo?.serie_referencia || '—' }
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
	<title>Póliza Vehículo | {APP_NAME}</title>
</svelte:head>

<PolizaDetalle
	{polizaId}
	rubroLabel="Vehículos"
	rubroSlug="vehiculo"
	service={polizaService.vehiculo}
	{valores}
	{loadBien}
	{loadClienteNombre}
	loadAseguradoras={() => aseguradoraService.getAll()}
	showEntrega={(poliza) => poliza.estado === 'VIGENTE' && !!poliza.numero_poliza}
/>
