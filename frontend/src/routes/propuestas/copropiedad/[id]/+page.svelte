<script lang="ts">
	import { page } from '$app/stores';
	import { APP_NAME } from '$lib/config';
	import { PolizaDetalle } from '$components';
	import { aseguradoraService, bienService, clienteService, polizaService } from '$services';
	import { clienteNombre } from '$utils';
	import type { PolizaCopropiedad } from '$lib/types/poliza';

	$: polizaId = Number($page.params.id);

	const valores = [
		{ key: 'valor_area_comun_asegurado', label: 'Área común' },
		{ key: 'valor_area_privada_asegurado', label: 'Área privada' },
		{ key: 'valor_maquinaria_equipo_asegurado', label: 'Maquinaria y equipo' },
		{ key: 'valor_equipo_electronico_asegurado', label: 'Equipo electrónico' },
		{ key: 'valor_muebles_asegurado', label: 'Muebles y enseres' },
		{ key: 'valor_directores_asegurado', label: 'Directores y administradores' },
		{ key: 'valor_rce_asegurado', label: 'RCE' },
		{ key: 'valor_manejo_asegurado', label: 'Manejo' },
		{ key: 'valor_transporte_valores_vigencia_asegurado', label: 'Transporte de valores (vigencia)' },
		{ key: 'valor_transporte_valores_despacho_asegurado', label: 'Transporte de valores (despacho)' }
	];

	async function loadBien(poliza: PolizaCopropiedad) {
		const cop = await bienService.copropiedades.getById(poliza.id_copropiedad);
		return {
			clienteId: cop?.id_usuario ?? null,
			fields: [
				{ label: 'Tipo de copropiedad', value: cop?.tipo_copropiedad || '—' },
				{ label: 'Ciudad', value: cop?.ciudad || '—' },
				{ label: 'Dirección', value: cop?.direccion || '—' },
				{ label: 'Estrato', value: cop?.estrato != null ? String(cop.estrato) : '—' }
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
	<title>Póliza Copropiedad | {APP_NAME}</title>
</svelte:head>

<PolizaDetalle
	{polizaId}
	rubroLabel="Copropiedades"
	rubroSlug="copropiedad"
	service={polizaService.copropiedad}
	{valores}
	{loadBien}
	{loadClienteNombre}
	loadAseguradoras={() => aseguradoraService.getAll()}
	showEntrega={(poliza) => poliza.estado === 'VIGENTE' && !!poliza.numero_poliza}
/>
