<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { PolizaDetalle } from '$components';
	import { aseguradoraService, bienService, clienteService, polizaService } from '$services';
	import { clienteNombre } from '$utils';
	import type { PolizaOtroBien } from '$lib/types/poliza';

	$: polizaId = Number($page.params.id);

	// The backend column is `valor_asegurado`; this page previously read
	// `valor_bien_asegurado`, which does not exist and so always rendered "—".
	const valores = [{ key: 'valor_asegurado', label: 'Valor asegurado' }];

	async function loadBien(poliza: PolizaOtroBien) {
		const otro = await bienService.otros.getById(poliza.id_otro_bien);
		return {
			clienteId: otro?.id_usuario ?? null,
			fields: [
				{ label: 'Bien asegurado', value: otro?.bien_asegurado || '—' },
				{ label: 'Tipo de seguro', value: otro?.tipo_seguro || '—' },
				{ label: 'Detalles', value: otro?.detalles_bien_asegurado || '—' }
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
	<title>Póliza Otro bien | {APP_NAME}</title>
</svelte:head>

<PolizaDetalle
	{polizaId}
	rubroLabel="Otros ramos"
	rubroSlug="otro"
	service={polizaService.otroBien}
	{valores}
	{loadBien}
	{loadClienteNombre}
	loadAseguradoras={() => aseguradoraService.getAll()}
	showEntrega={(poliza) => poliza.estado === 'VIGENTE' && !!poliza.numero_poliza}
/>
