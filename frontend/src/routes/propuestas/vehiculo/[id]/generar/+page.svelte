<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { FormField, FormSection, Input, Select, CurrencyInput, Modal } from '$components';
	import { polizaService, bienService, clienteService, aseguradoraService, propuestaService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import { getAuthUser } from '$lib/stores/auth';
	import type { PolizaVehiculo } from '$lib/types/poliza';
	import type { Vehiculo } from '$lib/types/bien';
	import type { Cliente } from '$lib/types/cliente';
	import type { Aseguradora } from '$lib/types/aseguradora';
	import { DICCIONARIO_CAMPOS_VEHICULOS, getAseguradoraOffset } from '$lib/data/diccionario_campos_vehiculos';

	// Route params
	$: polizaId = Number($page.params.id);

	// Data state
	let poliza: PolizaVehiculo | null = null;
	let vehiculo: Vehiculo | null = null;
	let cliente: Cliente | null = null;
	let aseguradoras: Aseguradora[] = [];
	let aseguradorasSeleccionadas: (Aseguradora | null)[] = [null, null, null, null, null];

	// UI state
	let loading = true;
	let generating = false;
	let generatingEntrega = false;
	let error: string | null = null;
	
	// Success modal state
	let showSuccessModal = false;
	let generatedFilename = '';
	let generatedSavedPath = '';

	// Secciones expandidas
	let expandedSections: Record<string, boolean> = {
		encabezado: true,
		cliente: true,
		avaluo: true,
		asegurados: true,
		aseguradoras: true
	};

	// =========================================================================
	// CAMPOS MANUALES DEL FORMULARIO
	// =========================================================================
	let camposManuales = {
		asesor: '',
		polizaActual: '',
		aseguradoraActual: '',
		tasaInteres: 2.5,  // Tasa de interés mensual por defecto (2.5%)
		comentarios: '',
		valor_asegurado_vehiculo: 0,
		valor_asegurado_accesorios: 0,
		valor_asegurado_rc: 0,
		// Datos de entrega [517]-[528] — se llenan manualmente al generar entrega
		nombre_aseguradora: '',
		numero_poliza: '',
		fecha_inicio_vigencia: '',
		fecha_fin_vigencia: '',
		valor_total_prima: '',
		medio_pago: '',
		numeral_asistencia: '',
		financiacion_num_cuotas: '',
		financiacion_valor_cuota: '',
		financiacion_fecha_primera: '',
		financiacion_periodicidad: '',
		financiacion_cuota_actual: ''
	};

	// =========================================================================
	// INTERFACE PARA DEDUCIBLE
	// =========================================================================
	interface Deducible {
		porcentaje: string;
		tipo: string;
		minimo: string;
	}

	interface CoberturasAseguradora {
		[key: string]: Deducible | string | boolean;
		// Deducibles Pérdida
		veh_deducible_perdida_parcial: Deducible;
		veh_deducible_perdida_total: Deducible;
		veh_deducible_terremoto: Deducible;
		// Deducibles Hurto
		veh_hurto_perdida_parcial: Deducible;
		veh_hurto_perdida_total: Deducible;
		// Deducible RC
		veh_deducible_rc: Deducible;
		// Sublímites RC (4 campos)
		veh_rc_sublimite_bienes_terceros: string;
		veh_rc_sublimite_amparo_patrimonial: string;
		veh_rc_sublimite_muerte_lesion_una: string;
		veh_rc_sublimite_muerte_lesion_dos_mas: string;
		// Coberturas Adicionales (7 checks)
		veh_cobertura_adicional_1: boolean;
		veh_cobertura_adicional_2: boolean;
		veh_cobertura_adicional_3: boolean;
		veh_cobertura_adicional_4: boolean;
		veh_cobertura_adicional_5: boolean;
		veh_cobertura_adicional_6: boolean;
		veh_cobertura_adicional_7: boolean;
		// Campos adicionales
		veh_observaciones: string;
		veh_asistencia_tipo: string;
		veh_conductor_elegido: string;
		veh_beneficiario_adicional: string;
	}

	// Estado editable de coberturas por aseguradora (1-5)
	let coberturasEditables: CoberturasAseguradora[] = [];

	// Acordeones de coberturas expandidos por aseguradora
	let expandedCoberturas: Record<string, boolean>[] = [{}, {}, {}, {}, {}];

	// Nombres de las 7 coberturas adicionales
	const nombresCoberturas = [
		'Responsabilidad Civil Voluntaria',
		'Daños a Ocupantes',
		'Asistencia en Viaje',
		'Vehículo de Reemplazo',
		'Exención Deducible',
		'Accidentes Personales Conductor',
		'Eventos de la Naturaleza'
	];

	onMount(async () => {
		const authUser = getAuthUser();
		if (authUser) {
			camposManuales.asesor = authUser.nombre || authUser.razon_social || authUser.usuario || '';
		}
		await loadData();
	});

	// Crear coberturas vacías por defecto
	function crearCoberturasVacias(): CoberturasAseguradora {
		const deducibleVacio = (): Deducible => ({ porcentaje: '', tipo: '', minimo: '' });
		return {
			veh_deducible_perdida_parcial: deducibleVacio(),
			veh_deducible_perdida_total: deducibleVacio(),
			veh_deducible_terremoto: deducibleVacio(),
			veh_hurto_perdida_parcial: deducibleVacio(),
			veh_hurto_perdida_total: deducibleVacio(),
			veh_deducible_rc: deducibleVacio(),
			veh_rc_sublimite_bienes_terceros: '',
			veh_rc_sublimite_amparo_patrimonial: '',
			veh_rc_sublimite_muerte_lesion_una: '',
			veh_rc_sublimite_muerte_lesion_dos_mas: '',
			veh_cobertura_adicional_1: false,
			veh_cobertura_adicional_2: false,
			veh_cobertura_adicional_3: false,
			veh_cobertura_adicional_4: false,
			veh_cobertura_adicional_5: false,
			veh_cobertura_adicional_6: false,
			veh_cobertura_adicional_7: false,
			veh_observaciones: '',
			veh_asistencia_tipo: '',
			veh_conductor_elegido: '',
			veh_beneficiario_adicional: ''
		};
	}

	// Inicializar coberturas desde aseguradora de la BD
	function inicializarCoberturasDesdeAseguradora(aseg: Aseguradora | null): CoberturasAseguradora {
		const coberturas = crearCoberturasVacias();
		if (!aseg) return coberturas;

		// Separar y asignar cada campo deducible
		const sep = (valor: string | undefined) => {
			if (!valor) return { porcentaje: '', tipo: '', minimo: '' };
			const p = valor.split(',');
			return { porcentaje: p[0] || '', tipo: p[1] || '', minimo: p[2] || '' };
		};

		// Deducibles Pérdida
		coberturas.veh_deducible_perdida_parcial = sep(aseg.veh_deducible_perdida_parcial);
		coberturas.veh_deducible_perdida_total = sep(aseg.veh_deducible_perdida_total);
		coberturas.veh_deducible_terremoto = sep(aseg.veh_deducible_terremoto);
		
		// Deducibles Hurto
		coberturas.veh_hurto_perdida_parcial = sep(aseg.veh_hurto_perdida_parcial);
		coberturas.veh_hurto_perdida_total = sep(aseg.veh_hurto_perdida_total);
		
		// Deducible RC
		coberturas.veh_deducible_rc = sep(aseg.veh_deducible_rc);
		
		// Sublímites RC (valores monetarios simples)
		coberturas.veh_rc_sublimite_bienes_terceros = aseg.veh_rc_sublimite_bienes_terceros || '';
		coberturas.veh_rc_sublimite_amparo_patrimonial = aseg.veh_rc_sublimite_amparo_patrimonial || '';
		coberturas.veh_rc_sublimite_muerte_lesion_una = aseg.veh_rc_sublimite_muerte_lesion_una || '';
		coberturas.veh_rc_sublimite_muerte_lesion_dos_mas = aseg.veh_rc_sublimite_muerte_lesion_dos_mas || '';
		
		// Coberturas adicionales (checks - siempre inician false, se marcan manualmente)
		coberturas.veh_cobertura_adicional_1 = aseg.veh_cobertura_adicional_1 === 'SI' || aseg.veh_cobertura_adicional_1 === 'true';
		coberturas.veh_cobertura_adicional_2 = aseg.veh_cobertura_adicional_2 === 'SI' || aseg.veh_cobertura_adicional_2 === 'true';
		coberturas.veh_cobertura_adicional_3 = aseg.veh_cobertura_adicional_3 === 'SI' || aseg.veh_cobertura_adicional_3 === 'true';
		coberturas.veh_cobertura_adicional_4 = aseg.veh_cobertura_adicional_4 === 'SI' || aseg.veh_cobertura_adicional_4 === 'true';
		coberturas.veh_cobertura_adicional_5 = aseg.veh_cobertura_adicional_5 === 'SI' || aseg.veh_cobertura_adicional_5 === 'true';
		coberturas.veh_cobertura_adicional_6 = aseg.veh_cobertura_adicional_6 === 'SI' || aseg.veh_cobertura_adicional_6 === 'true';
		coberturas.veh_cobertura_adicional_7 = aseg.veh_cobertura_adicional_7 === 'SI' || aseg.veh_cobertura_adicional_7 === 'true';

		return coberturas;
	}

	async function loadData() {
		loading = true;
		error = null;
		try {
			// Load poliza
			poliza = await polizaService.vehiculo.getById(polizaId);
			
			if (!poliza) {
				throw new Error('No se encontró la póliza');
			}
			
			// Load related data
			const [vehiculoData, aseguradorasData] = await Promise.all([
				bienService.vehiculos.getById(poliza.id_vehiculo),
				aseguradoraService.getAll()
			]);
			
			vehiculo = vehiculoData;
			aseguradoras = aseguradorasData;
			
			// Cargar aseguradoras seleccionadas en la póliza e inicializar coberturas
			coberturasEditables = [];
			for (let i = 0; i < 5; i++) {
				const idAseg = (poliza as any)[`id_aseguradora_${i + 1}`];
				if (idAseg) {
					const aseg = aseguradoras.find((a: Aseguradora) => a.id === idAseg) || null;
					aseguradorasSeleccionadas[i] = aseg;
					coberturasEditables[i] = inicializarCoberturasDesdeAseguradora(aseg);
				} else {
					aseguradorasSeleccionadas[i] = null;
					coberturasEditables[i] = crearCoberturasVacias();
				}
			}
			
			// Inicializar valores asegurados editables
			camposManuales.valor_asegurado_vehiculo = poliza.valor_asegurado_vehiculo || 0;
			camposManuales.valor_asegurado_accesorios = poliza.valor_asegurado_accesorios || 0;
			camposManuales.valor_asegurado_rc = poliza.valor_asegurado_rc || 0;

			// Load cliente
			if (vehiculo) {
				const clientes = await clienteService.getAll();
				cliente = clientes.find((c: Cliente) => c.id === vehiculo!.id_usuario) || null;
			}

			// Pre-poblar campos de entrega desde la póliza (si ya fue entregada)
			if (poliza.estado === 'VIGENTE') {
				camposManuales.nombre_aseguradora = poliza.nombre_aseguradora || '';
				camposManuales.numero_poliza = poliza.numero_poliza_aseguradora || '';
				camposManuales.fecha_inicio_vigencia = poliza.inicio_vigencia ? poliza.inicio_vigencia.split('T')[0] : '';
				camposManuales.fecha_fin_vigencia = poliza.fin_vigencia ? poliza.fin_vigencia.split('T')[0] : '';
				camposManuales.valor_total_prima = poliza.valor_total_prima ? String(poliza.valor_total_prima) : '';
				camposManuales.medio_pago = poliza.medio_pago || '';
				camposManuales.numeral_asistencia = poliza.numeral_asistencia || '';
				camposManuales.financiacion_num_cuotas = poliza.financiacion_num_cuotas ? String(poliza.financiacion_num_cuotas) : '';
				camposManuales.financiacion_valor_cuota = poliza.financiacion_valor_cuota ? String(poliza.financiacion_valor_cuota) : '';
				camposManuales.financiacion_fecha_primera = poliza.financiacion_fecha_primera_cuota ? poliza.financiacion_fecha_primera_cuota.split('T')[0] : '';
				camposManuales.financiacion_periodicidad = poliza.financiacion_periodicidad || '';
				camposManuales.financiacion_cuota_actual = poliza.financiacion_cuota_actual ? String(poliza.financiacion_cuota_actual) : '';
			}
		} catch (err) {
			console.error('Error loading data:', err);
			error = err instanceof Error ? err.message : 'Error al cargar los datos';
		} finally {
			loading = false;
		}
	}

	// =========================================================================
	// HELPER: Formatear fecha de expedición (fecha actual al generar)
	// =========================================================================
	function formatearFecha(): string {
		const fecha = new Date();
		const dia = fecha.getDate();
		const meses = [
			'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
			'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
		];
		const mes = meses[fecha.getMonth()];
		const anio = fecha.getFullYear();
		return `${dia} de ${mes} ${anio}`;
	}

	// =========================================================================
	// HELPER: Calcular año de vigencia
	// =========================================================================
	function calcularVigencia(): string {
		const ahora = new Date();
		return `${ahora.getFullYear()}-${ahora.getFullYear() + 1}`;
	}

	// =========================================================================
	// HELPER: Calcular cuota con interés (fórmula de amortización)
	// =========================================================================
	function calcularCuotaConInteres(prima: number, tasaPorcentaje: number, numCuotas: number): number {
		if (!prima || prima <= 0 || numCuotas <= 0) return 0;
		const tasa = tasaPorcentaje / 100;
		if (tasa <= 0) return Math.round(prima / numCuotas);
		const factor = Math.pow(1 + tasa, numCuotas);
		const cuota = prima * ((tasa * factor) / (factor - 1));
		return Math.round(cuota);
	}

	// =========================================================================
	// HELPER: Obtener nombre del cliente
	// =========================================================================
	function getNombreCliente(): string {
		if (!cliente) return '';
		return cliente.tipo_persona === 'PERSONA' 
			? cliente.nombre || ''
			: cliente.razon_social || '';
	}

	// =========================================================================
	// CONSTRUIR JSON con CÓDIGOS [N] para Excel
	// =========================================================================
	function buildVariablesJson(): Record<string, string> {
		if (!poliza || !vehiculo || !cliente) {
			return {};
		}

		// Helper: Formatear valor monetario con separadores de miles
		const formatMoney = (value: number | null | undefined): string => {
			if (value === null || value === undefined || value === 0) return '0';
			return new Intl.NumberFormat('es-CO', {
				minimumFractionDigits: 0,
				maximumFractionDigits: 0
			}).format(value);
		};

		// Helper: Convertir cualquier valor a string
		const str = (value: any): string => {
			if (value === null || value === undefined) return '';
			return String(value);
		};

		// JSON con CÓDIGOS [N]
		const campos_reemplazo_vehiculos: Record<string, string> = {
			// SECCIÓN 1: ENCABEZADO [1]-[2]
			"[1]": formatearFecha(),
			"[2]": calcularVigencia(),

			// SECCIÓN 2: DATOS DEL CLIENTE / VEHÍCULO [3]-[16]
			"[3]": getNombreCliente(),
			"[4]": cliente.tipo_persona === 'EMPRESA' ? str(cliente.nit) : str(cliente.numero_documento),
			"[5]": str(vehiculo.tipo_vehiculo),
			"[6]": str(vehiculo.marca),
			"[7]": str(vehiculo.ano_modelo),
			"[8]": str(vehiculo.placa),
			"[9]": str(vehiculo.codigo_fasecolda),
			"[10]": str(cliente.ciudad_residencia),
			"[11]": str(poliza.uso_vehiculo) || 'Particular', // Puede venir de la póliza o del vehículo
			"[12]": camposManuales.asesor,
			"[13]": camposManuales.polizaActual,
			"[14]": camposManuales.aseguradoraActual,
			"[15]": str(camposManuales.tasaInteres),
			"[16]": camposManuales.comentarios,

			// SECCIÓN 3: VALORES DEL BIEN (AVALÚO COMERCIAL) [17]-[21]
			"[17]": formatMoney(vehiculo.valor_vehiculo),
			"[18]": formatMoney(vehiculo.valor_accesorios_avaluo),
			"[19]": formatMoney(poliza.valor_rc_avaluo),
			"[20]": formatMoney((vehiculo.valor_vehiculo || 0) + (vehiculo.valor_accesorios_avaluo || 0)),
			"[21]": str(vehiculo.ano_modelo),

			// SECCIÓN 4: VALORES ASEGURADOS [22]-[25]
				"[22]": formatMoney(camposManuales.valor_asegurado_vehiculo),
				"[23]": formatMoney(camposManuales.valor_asegurado_accesorios),
				"[24]": formatMoney(camposManuales.valor_asegurado_rc),
				"[25]": formatMoney((camposManuales.valor_asegurado_vehiculo || 0) + (camposManuales.valor_asegurado_accesorios || 0))
		};

		// =====================================================================
		// ASEGURADORAS 1-5: [26]-[155]
		// Cada aseguradora tiene 26 campos
		// =====================================================================
		const asegOffsets = [26, 52, 78, 104, 130]; // Inicio de cada aseguradora

		for (let i = 0; i < 5; i++) {
			const base = asegOffsets[i];
			const aseg = aseguradorasSeleccionadas[i];
			const prima = (poliza as any)[`valor_prima_aseg_${i + 1}`];
			const cob = coberturasEditables[i];

			// Datos base [+0 a +4]
			campos_reemplazo_vehiculos[`[${base}]`] = str(aseg?.nombre);
			campos_reemplazo_vehiculos[`[${base + 1}]`] = str(aseg?.ruta_pais_logo);
			campos_reemplazo_vehiculos[`[${base + 2}]`] = str(aseg?.respaldo_aseguradora);
			campos_reemplazo_vehiculos[`[${base + 3}]`] = formatMoney(prima);
			campos_reemplazo_vehiculos[`[${base + 4}]`] = formatMoney(prima);

			// Deducibles Pérdida [+5 a +7]
			const ded_pp = cob.veh_deducible_perdida_parcial as Deducible;
			campos_reemplazo_vehiculos[`[${base + 5}]`] = `${ded_pp.porcentaje}% ${ded_pp.tipo} Mín $${formatMoney(Number(ded_pp.minimo))}`;
			
			const ded_pt = cob.veh_deducible_perdida_total as Deducible;
			campos_reemplazo_vehiculos[`[${base + 6}]`] = `${ded_pt.porcentaje}% ${ded_pt.tipo} Mín $${formatMoney(Number(ded_pt.minimo))}`;
			
			const ded_terr = cob.veh_deducible_terremoto as Deducible;
			campos_reemplazo_vehiculos[`[${base + 7}]`] = `${ded_terr.porcentaje}% ${ded_terr.tipo} Mín $${formatMoney(Number(ded_terr.minimo))}`;

			// Deducibles Hurto [+8 a +9]
			const hur_pp = cob.veh_hurto_perdida_parcial as Deducible;
			campos_reemplazo_vehiculos[`[${base + 8}]`] = `${hur_pp.porcentaje}% ${hur_pp.tipo} Mín $${formatMoney(Number(hur_pp.minimo))}`;
			
			const hur_pt = cob.veh_hurto_perdida_total as Deducible;
			campos_reemplazo_vehiculos[`[${base + 9}]`] = `${hur_pt.porcentaje}% ${hur_pt.tipo} Mín $${formatMoney(Number(hur_pt.minimo))}`;

			// Deducible RC [+10]
			const ded_rc = cob.veh_deducible_rc as Deducible;
			campos_reemplazo_vehiculos[`[${base + 10}]`] = `${ded_rc.porcentaje}% ${ded_rc.tipo} Mín $${formatMoney(Number(ded_rc.minimo))}`;

			// Sublímites RC [+11 a +14]
			campos_reemplazo_vehiculos[`[${base + 11}]`] = formatMoney(Number(cob.veh_rc_sublimite_bienes_terceros));
			campos_reemplazo_vehiculos[`[${base + 12}]`] = formatMoney(Number(cob.veh_rc_sublimite_amparo_patrimonial));
			campos_reemplazo_vehiculos[`[${base + 13}]`] = formatMoney(Number(cob.veh_rc_sublimite_muerte_lesion_una));
			campos_reemplazo_vehiculos[`[${base + 14}]`] = formatMoney(Number(cob.veh_rc_sublimite_muerte_lesion_dos_mas));

			// Coberturas Adicionales [+15 a +21] - checkboxes
			campos_reemplazo_vehiculos[`[${base + 15}]`] = cob.veh_cobertura_adicional_1 ? 'SI' : 'NO';
			campos_reemplazo_vehiculos[`[${base + 16}]`] = cob.veh_cobertura_adicional_2 ? 'SI' : 'NO';
			campos_reemplazo_vehiculos[`[${base + 17}]`] = cob.veh_cobertura_adicional_3 ? 'SI' : 'NO';
			campos_reemplazo_vehiculos[`[${base + 18}]`] = cob.veh_cobertura_adicional_4 ? 'SI' : 'NO';
			campos_reemplazo_vehiculos[`[${base + 19}]`] = cob.veh_cobertura_adicional_5 ? 'SI' : 'NO';
			campos_reemplazo_vehiculos[`[${base + 20}]`] = cob.veh_cobertura_adicional_6 ? 'SI' : 'NO';
			campos_reemplazo_vehiculos[`[${base + 21}]`] = cob.veh_cobertura_adicional_7 ? 'SI' : 'NO';

			// Campos adicionales [+22 a +25]
			campos_reemplazo_vehiculos[`[${base + 22}]`] = str(cob.veh_observaciones);
			campos_reemplazo_vehiculos[`[${base + 23}]`] = str(cob.veh_asistencia_tipo);
			campos_reemplazo_vehiculos[`[${base + 24}]`] = str(cob.veh_conductor_elegido);
			campos_reemplazo_vehiculos[`[${base + 25}]`] = str(cob.veh_beneficiario_adicional);
		}

		// =====================================================================
		// SECCIÓN ENTREGA [517]-[528]
		// Campos llenados manualmente en la sección "Datos de Entrega"
		// =====================================================================
		const formatFechaManual = (fechaISO: string): string => {
			if (!fechaISO) return '';
			const d = new Date(fechaISO + 'T00:00:00');
			const meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
			return `${d.getDate()} de ${meses[d.getMonth()]} ${d.getFullYear()}`;
		};

		campos_reemplazo_vehiculos['[517]'] = str(camposManuales.nombre_aseguradora);
		campos_reemplazo_vehiculos['[518]'] = str(camposManuales.numero_poliza);
		campos_reemplazo_vehiculos['[519]'] = formatFechaManual(camposManuales.fecha_inicio_vigencia);
		campos_reemplazo_vehiculos['[520]'] = formatFechaManual(camposManuales.fecha_fin_vigencia);
		campos_reemplazo_vehiculos['[521]'] = formatMoney(Number(camposManuales.valor_total_prima) || 0);
		campos_reemplazo_vehiculos['[522]'] = str(camposManuales.medio_pago);
		campos_reemplazo_vehiculos['[523]'] = str(camposManuales.numeral_asistencia);
		campos_reemplazo_vehiculos['[524]'] = str(camposManuales.financiacion_num_cuotas);
		campos_reemplazo_vehiculos['[525]'] = formatMoney(Number(camposManuales.financiacion_valor_cuota) || 0);
		campos_reemplazo_vehiculos['[526]'] = formatFechaManual(camposManuales.financiacion_fecha_primera);
		campos_reemplazo_vehiculos['[527]'] = str(camposManuales.financiacion_periodicidad);
		campos_reemplazo_vehiculos['[528]'] = str(camposManuales.financiacion_cuota_actual);

		return campos_reemplazo_vehiculos;
	}

	// =========================================================================
	// CONSTRUIR JSON de imágenes
	// =========================================================================
	function buildImagenesJson(): Record<string, string> {
		const imagenes: Record<string, string> = {};
		
		for (let i = 0; i < 5; i++) {
			const aseg = aseguradorasSeleccionadas[i];
			if (aseg) {
				if (aseg.ruta_logo) {
					imagenes[`logo_aseg_${i + 1}`] = aseg.ruta_logo;
				}
				if (aseg.ruta_pais_logo) {
					imagenes[`bandera_aseg_${i + 1}`] = aseg.ruta_pais_logo;
				}
			}
		}
		
		return imagenes;
	}

	// =========================================================================
	// GENERAR PROPUESTA
	// =========================================================================
	async function generarPropuesta() {
		if (!poliza || !vehiculo || !cliente) {
			addNotification({
				type: 'error',
				title: 'Error',
				message: 'Faltan datos necesarios para generar la propuesta'
			});
			return;
		}

		generating = true;

		try {
			const variables = buildVariablesJson();
			const imagenes = buildImagenesJson();

			console.log('📤 JSON enviado al API:', JSON.stringify({ template_name: 'vehiculos', variables, imagenes }, null, 2));

			const result = await propuestaService.generateAndDownload({
				template_name: 'vehiculos',
				variables,
				imagenes
			});

			generatedFilename = result.filename;
			generatedSavedPath = result.savedPath;
			
			// Guardar valores de cuotas calculadas en la póliza
			await guardarValoresCuotas();
			
			showSuccessModal = true;

		} catch (err) {
			console.error('Error generando propuesta:', err);
			addNotification({
				type: 'error',
				title: 'Error al Generar',
				message: err instanceof Error ? err.message : 'No se pudo generar la propuesta'
			});
		} finally {
			generating = false;
		}
	}

	// =========================================================================
	// GENERAR ENTREGA
	// =========================================================================
	async function generarEntrega() {
		if (!poliza || !vehiculo || !cliente) {
			addNotification({
				type: 'error',
				title: 'Error',
				message: 'Faltan datos necesarios para generar la entrega'
			});
			return;
		}

		generatingEntrega = true;

		try {
			const variables = buildVariablesJson();
			const imagenes = buildImagenesJson();

			console.log('📤 JSON entrega enviado al API:', JSON.stringify({ template_name: 'entrega_vehiculos', variables, imagenes }, null, 2));

			const result = await propuestaService.generateAndDownload({
				template_name: 'entrega_vehiculos',
				variables,
				imagenes
			});

			generatedFilename = result.filename;
			generatedSavedPath = result.savedPath;
			showSuccessModal = true;

		} catch (err) {
			console.error('Error generando entrega:', err);
			addNotification({
				type: 'error',
				title: 'Error al Generar Entrega',
				message: err instanceof Error ? err.message : 'No se pudo generar la entrega'
			});
		} finally {
			generatingEntrega = false;
		}
	}

	// =========================================================================
	// GUARDAR VALORES DE CUOTAS CALCULADAS
	// =========================================================================
	async function guardarValoresCuotas() {
		if (!poliza) return;

		// Calcular valores de cuotas para cada plan usando la tasa de interés configurada
		const valoresCuotas: any = {};
		
		for (let i = 0; i < 5; i++) {
			const prima = getPrimaByIndex(i);
			if (prima && prima > 0) {
				valoresCuotas.valor_cuota_3 = Math.round(prima / 3);
				valoresCuotas.valor_cuota_5 = calcularCuotaConInteres(prima, camposManuales.tasaInteres, 5);
				valoresCuotas.valor_cuota_8 = calcularCuotaConInteres(prima, camposManuales.tasaInteres, 8);
				valoresCuotas.valor_cuota_11 = calcularCuotaConInteres(prima, camposManuales.tasaInteres, 11);
				break;
			}
		}

		try {
			await polizaService.vehiculo.update(polizaId, valoresCuotas);
			console.log('✅ Valores de cuotas guardados:', valoresCuotas);
		} catch (err) {
			console.error('⚠️ Error guardando valores de cuotas:', err);
		}
	}

	function toggleSection(section: string) {
		expandedSections[section] = !expandedSections[section];
	}

	function formatCurrency(value: number | null | undefined): string {
		if (value === null || value === undefined) return '—';
		return new Intl.NumberFormat('es-CO', {
			style: 'currency',
			currency: 'COP',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(value);
	}

	function getPrimaByIndex(index: number): number | null {
		if (!poliza) return null;
		const key = `valor_prima_aseg_${index + 1}` as keyof PolizaVehiculo;
		return poliza[key] as number | null;
	}

	function toggleCoberturaSection(asegIndex: number, section: string) {
		expandedCoberturas[asegIndex][section] = !expandedCoberturas[asegIndex][section];
		expandedCoberturas = [...expandedCoberturas];
	}
</script>

<svelte:head>
	<title>Generar Propuesta Vehículos | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<button 
			type="button" 
			class="p-2 hover:bg-secondary-100 rounded-lg transition-colors"
			on:click={() => goto(`/propuestas/vehiculo/${polizaId}`)}
		>
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
			</svg>
		</button>
		<div>
			<h1 class="page-title">Generar Propuesta Vehículos</h1>
			{#if poliza}
				<p class="text-secondary-500 text-sm mt-1 font-mono">{poliza.consecutivo}</p>
			{/if}
		</div>
	</div>
	
	<div class="flex items-center gap-3">
		<button
			type="button"
			class="btn btn-primary flex items-center gap-2"
			on:click={generarPropuesta}
			disabled={loading || generating || generatingEntrega || !poliza}
		>
			{#if generating}
				<svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
				</svg>
				Generando...
			{:else}
				<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
				</svg>
				Generar Propuesta
			{/if}
		</button>
		{#if poliza?.estado === 'VIGENTE'}
			<button
				type="button"
				class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
				on:click={generarEntrega}
				disabled={loading || generating || generatingEntrega || !poliza}
			>
				{#if generatingEntrega}
					<svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
					</svg>
					Generando Entrega...
				{:else}
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
					Generar Entrega
				{/if}
			</button>
		{/if}
	</div>
</header>

<!-- Content -->
<div class="page-content">
	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="flex flex-col items-center gap-4">
				<svg class="animate-spin h-8 w-8 text-primary-500" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
				</svg>
				<p class="text-secondary-600">Cargando datos...</p>
			</div>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
			<p class="font-medium">Error</p>
			<p class="text-sm">{error}</p>
		</div>
	{:else if poliza && vehiculo}
		<div class="space-y-4">
			<!-- SECCIÓN 1: ENCABEZADO -->
			<FormSection title="1. Encabezado del Documento" collapsible defaultExpanded={expandedSections.encabezado}>
				<div class="space-y-4">
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div class="p-3 bg-secondary-50 rounded-lg">
							<p class="text-xs text-secondary-500 mb-1">Fecha de Expedición</p>
							<p class="text-sm font-medium">{formatearFecha()}</p>
							<span class="text-xs text-blue-600">[CALCULADO]</span>
						</div>
						<div class="p-3 bg-secondary-50 rounded-lg">
							<p class="text-xs text-secondary-500 mb-1">Año de Vigencia</p>
							<p class="text-sm font-medium">{calcularVigencia()}</p>
							<span class="text-xs text-blue-600">[CALCULADO]</span>
						</div>
					</div>
					
					<!-- Campos Manuales -->
					<div class="border-t border-secondary-200 pt-4">
						<p class="text-sm font-medium text-orange-600 mb-3">Campos Manuales</p>
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<FormField label="Asesor" required>
								<Input bind:value={camposManuales.asesor} placeholder="Nombre del asesor" />
							</FormField>
							<FormField label="Póliza Actual">
								<Input bind:value={camposManuales.polizaActual} placeholder="Número póliza actual" />
							</FormField>
							<FormField label="Aseguradora Actual">
								<Input bind:value={camposManuales.aseguradoraActual} placeholder="Aseguradora actual" />
							</FormField>
							<FormField label="Tasa de Interés Mensual (%)" required>
								<Input type="number" bind:value={camposManuales.tasaInteres} placeholder="2.5" step="0.1" />
							</FormField>
						</div>
						<div class="mt-4">
							<FormField label="Comentarios">
								<textarea 
									bind:value={camposManuales.comentarios}
									class="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
									rows="3"
									placeholder="Comentarios adicionales..."
								></textarea>
							</FormField>
						</div>
					</div>

					<!-- Datos de Entrega (solo visible en estado VIGENTE) -->
					{#if poliza?.estado === 'VIGENTE'}
					<div class="border-t border-green-200 pt-4 mt-4">
						<p class="text-sm font-medium text-green-700 mb-3">📋 Datos de Entrega <span class="text-xs text-green-500 ml-1">[517]-[528]</span></p>
						<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
							<FormField label="Aseguradora Elegida [517]">
								<Input bind:value={camposManuales.nombre_aseguradora} placeholder="Nombre de la aseguradora" />
							</FormField>
							<FormField label="Número de Póliza [518]">
								<Input bind:value={camposManuales.numero_poliza} placeholder="Ej: POL-2026-001" />
							</FormField>
							<FormField label="Numeral de Asistencia [523]">
								<Input bind:value={camposManuales.numeral_asistencia} placeholder="Ej: 3A" />
							</FormField>
							<FormField label="Fecha Inicio Vigencia [519]">
								<Input type="date" bind:value={camposManuales.fecha_inicio_vigencia} />
							</FormField>
							<FormField label="Fecha Fin Vigencia [520]">
								<Input type="date" bind:value={camposManuales.fecha_fin_vigencia} />
							</FormField>
							<FormField label="Valor Total Prima [521]">
								<Input type="number" bind:value={camposManuales.valor_total_prima} placeholder="0" />
							</FormField>
							<FormField label="Medio de Pago [522]">
								<Select bind:value={camposManuales.medio_pago}>
									<option value="">Seleccionar...</option>
									<option value="contado">Contado</option>
									<option value="financiera">Financiera</option>
								</Select>
							</FormField>
						</div>
						{#if camposManuales.medio_pago === 'financiera'}
						<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-4 p-3 bg-green-50 rounded-lg">
							<p class="col-span-full text-xs font-medium text-green-600 mb-1">Datos de Financiación</p>
							<FormField label="Núm. Cuotas [524]">
								<Select bind:value={camposManuales.financiacion_num_cuotas}>
									<option value="">...</option>
									<option value="3">3 cuotas</option>
									<option value="5">5 cuotas</option>
									<option value="8">8 cuotas</option>
									<option value="11">11 cuotas</option>
								</Select>
							</FormField>
							<FormField label="Valor Cuota [525]">
								<Input type="number" bind:value={camposManuales.financiacion_valor_cuota} placeholder="0" />
							</FormField>
							<FormField label="Fecha Primera Cuota [526]">
								<Input type="date" bind:value={camposManuales.financiacion_fecha_primera} />
							</FormField>
							<FormField label="Periodicidad [527]">
								<Select bind:value={camposManuales.financiacion_periodicidad}>
									<option value="">...</option>
									<option value="mensual">Mensual</option>
									<option value="bimestral">Bimestral</option>
									<option value="trimestral">Trimestral</option>
								</Select>
							</FormField>
							<FormField label="Cuota Actual [528]">
								<Input type="number" bind:value={camposManuales.financiacion_cuota_actual} placeholder="1" />
							</FormField>
						</div>
						{/if}
					</div>
					{/if}
				</div>
			</FormSection>

			<!-- SECCIÓN 2: DATOS DEL CLIENTE / VEHÍCULO -->
			<FormSection title="2. Datos del Cliente / Vehículo" collapsible defaultExpanded={expandedSections.cliente}>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Nombre Cliente</p>
						<p class="text-sm font-medium">{getNombreCliente() || '—'}</p>
						<span class="text-xs text-green-600">[BD:usuarios]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">NIT / Documento</p>
						<p class="text-sm font-medium">{cliente?.tipo_persona === 'EMPRESA' ? (cliente?.nit || '—') : (cliente?.numero_documento || '—')}</p>
						<span class="text-xs text-green-600">[BD:usuarios]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Tipo de Vehículo</p>
						<p class="text-sm font-medium">{vehiculo.tipo_vehiculo || '—'}</p>
						<span class="text-xs text-green-600">[BD:vehiculos]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Marca</p>
						<p class="text-sm font-medium">{vehiculo.marca || '—'}</p>
						<span class="text-xs text-green-600">[BD:vehiculos]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Modelo (Año)</p>
						<p class="text-sm font-medium">{vehiculo.ano_modelo || '—'}</p>
						<span class="text-xs text-green-600">[BD:vehiculos]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Placa</p>
						<p class="text-sm font-medium font-mono text-lg">{vehiculo.placa || '—'}</p>
						<span class="text-xs text-green-600">[BD:vehiculos]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Código Fasecolda</p>
						<p class="text-sm font-medium font-mono">{vehiculo.codigo_fasecolda || '—'}</p>
						<span class="text-xs text-green-600">[BD:vehiculos]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Ciudad de Circulación</p>
						<p class="text-sm font-medium">{cliente?.ciudad_residencia || '—'}</p>
						<span class="text-xs text-green-600">[BD:usuarios]</span>
					</div>
				</div>
			</FormSection>

			<!-- SECCIÓN 3: VALORES DE AVALÚO -->
			<FormSection title="3. Valores de Avalúo Comercial" collapsible defaultExpanded={expandedSections.avaluo}>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Vehículo (Fasecolda)</p>
						<p class="text-sm font-medium">{formatCurrency(vehiculo.valor_vehiculo)}</p>
						<span class="text-xs text-green-600">[BD:vehiculos]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Accesorios</p>
						<p class="text-sm font-medium">{formatCurrency(vehiculo.valor_accesorios_avaluo)}</p>
						<span class="text-xs text-green-600">[BD:vehiculos]</span>
					</div>
					<div class="p-3 bg-secondary-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">RC (Avalúo)</p>
						<p class="text-sm font-medium">{formatCurrency(poliza.valor_rc_avaluo)}</p>
						<span class="text-xs text-green-600">[BD:polizas]</span>
					</div>
					<div class="p-3 bg-blue-50 rounded-lg">
						<p class="text-xs text-secondary-500 mb-1">Valor Total</p>
						<p class="text-sm font-medium font-semibold">{formatCurrency((vehiculo.valor_vehiculo || 0) + (vehiculo.valor_accesorios_avaluo || 0))}</p>
						<span class="text-xs text-blue-600">[CALCULADO]</span>
					</div>
				</div>
			</FormSection>

			<!-- SECCIÓN 4: VALORES ASEGURADOS -->
			<FormSection title="4. Valores Asegurados" collapsible defaultExpanded={expandedSections.asegurados}>
				<div class="space-y-4">
					<div class="border-t border-secondary-200 pt-4">
						<p class="text-sm font-medium text-orange-600 mb-3">Campos Editables</p>
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<FormField label="Vehículo">
								<CurrencyInput bind:value={camposManuales.valor_asegurado_vehiculo} />
							</FormField>
							<FormField label="Accesorios">
								<CurrencyInput bind:value={camposManuales.valor_asegurado_accesorios} />
							</FormField>
							<FormField label="RC">
								<CurrencyInput bind:value={camposManuales.valor_asegurado_rc} />
							</FormField>
							<div class="p-3 bg-blue-50 rounded-lg">
								<p class="text-xs text-secondary-500 mb-1">Valor Total Asegurado</p>
								<p class="text-sm font-medium font-semibold">{formatCurrency((camposManuales.valor_asegurado_vehiculo || 0) + (camposManuales.valor_asegurado_accesorios || 0))}</p>
								<span class="text-xs text-blue-600">[CALCULADO]</span>
							</div>
						</div>
					</div>
				</div>
			</FormSection>

			<!-- SECCIÓN 5: ASEGURADORAS (1-5) -->
			<FormSection title="5. Coberturas por Aseguradora" collapsible defaultExpanded={expandedSections.aseguradoras}>
				<div class="space-y-6">
					{#each [0, 1, 2, 3, 4] as i}
						{@const aseg = aseguradorasSeleccionadas[i]}
						{@const prima = getPrimaByIndex(i)}
						{@const cuota3 = Math.round((prima || 0) / 3)}
						{@const cuota5 = calcularCuotaConInteres(prima || 0, camposManuales.tasaInteres, 5)}
						{@const cuota8 = calcularCuotaConInteres(prima || 0, camposManuales.tasaInteres, 8)}
						{@const cuota11 = calcularCuotaConInteres(prima || 0, camposManuales.tasaInteres, 11)}
						{#if (aseg || prima) && coberturasEditables[i]}
							<div class="border-2 border-primary-200 rounded-xl overflow-hidden">
								<!-- Header de Aseguradora -->
								<div class="bg-gradient-to-r from-primary-500 to-primary-600 px-4 py-3">
									<div class="flex items-center justify-between">
										<div class="flex items-center gap-3">
											<span class="w-10 h-10 flex items-center justify-center bg-white text-primary-600 rounded-full font-bold text-lg">
												{i + 1}
											</span>
											<div>
												<span class="font-bold text-white text-lg">{aseg?.nombre || 'Sin aseguradora'}</span>
												<p class="text-primary-100 text-xs">{aseg?.respaldo_aseguradora || ''}</p>
											</div>
										</div>
										<div class="text-right">
											<p class="text-primary-200 text-xs">Prima Anual</p>
											<p class="font-bold text-white text-xl">{formatCurrency(prima)}</p>
										</div>
									</div>
									<!-- Opciones de Financiación -->
									<div class="mt-3 pt-3 border-t border-primary-400">
										<p class="text-primary-200 text-xs text-center mb-2">Opciones de Financiación</p>
										<div class="grid grid-cols-4 gap-2">
											<div class="text-center bg-green-600 rounded-lg py-2 px-1">
												<p class="text-green-100 text-xs font-medium">3 cuotas</p>
												<p class="text-white font-bold">{formatCurrency(cuota3)}</p>
												<p class="text-green-200 text-[10px]">sin interés</p>
											</div>
											<div class="text-center bg-white/10 rounded-lg py-2 px-1">
												<p class="text-primary-100 text-xs font-medium">5 cuotas</p>
												<p class="text-white font-bold">{formatCurrency(cuota5)}</p>
												<p class="text-primary-200 text-[10px]">{camposManuales.tasaInteres}% mes</p>
											</div>
											<div class="text-center bg-white/10 rounded-lg py-2 px-1">
												<p class="text-primary-100 text-xs font-medium">8 cuotas</p>
												<p class="text-white font-bold">{formatCurrency(cuota8)}</p>
												<p class="text-primary-200 text-[10px]">{camposManuales.tasaInteres}% mes</p>
											</div>
											<div class="text-center bg-white/10 rounded-lg py-2 px-1">
												<p class="text-primary-100 text-xs font-medium">11 cuotas</p>
												<p class="text-white font-bold">{formatCurrency(cuota11)}</p>
												<p class="text-primary-200 text-[10px]">{camposManuales.tasaInteres}% mes</p>
											</div>
										</div>
									</div>
								</div>

								<div class="p-4 space-y-3 bg-gray-50">
									<!-- DEDUCIBLES PÉRDIDA -->
									<div class="bg-white rounded-lg border border-blue-200 overflow-hidden">
										<button type="button" class="w-full px-4 py-3 bg-blue-50 flex items-center justify-between hover:bg-blue-100" on:click={() => toggleCoberturaSection(i, 'perdida')}>
											<h4 class="font-semibold text-blue-700">Deducibles Pérdida - 3 coberturas</h4>
											<svg class="w-5 h-5 text-blue-600 transition-transform {expandedCoberturas[i]?.perdida ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
										</button>
										{#if expandedCoberturas[i]?.perdida}
											<div class="p-4 space-y-3">
												{#each [
													{ key: 'veh_deducible_perdida_parcial', label: 'Pérdida Parcial' },
													{ key: 'veh_deducible_perdida_total', label: 'Pérdida Total' },
													{ key: 'veh_deducible_terremoto', label: 'Terremoto' }
												] as cob}
													<div class="grid grid-cols-4 gap-2 items-center p-2 bg-blue-50 rounded">
														<span class="font-medium text-sm text-blue-800">{cob.label}</span>
														<input type="text" bind:value={coberturasEditables[i][cob.key].porcentaje} class="input input-sm" placeholder="%" />
														<input type="text" bind:value={coberturasEditables[i][cob.key].tipo} class="input input-sm" placeholder="Tipo" />
														<input type="text" bind:value={coberturasEditables[i][cob.key].minimo} class="input input-sm" placeholder="Mín" />
													</div>
												{/each}
											</div>
										{/if}
									</div>

									<!-- DEDUCIBLES HURTO -->
									<div class="bg-white rounded-lg border border-red-200 overflow-hidden">
										<button type="button" class="w-full px-4 py-3 bg-red-50 flex items-center justify-between hover:bg-red-100" on:click={() => toggleCoberturaSection(i, 'hurto')}>
											<h4 class="font-semibold text-red-700">Deducibles Hurto - 2 coberturas</h4>
											<svg class="w-5 h-5 text-red-600 transition-transform {expandedCoberturas[i]?.hurto ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
										</button>
										{#if expandedCoberturas[i]?.hurto}
											<div class="p-4 space-y-3">
												{#each [
													{ key: 'veh_hurto_perdida_parcial', label: 'Pérdida Parcial' },
													{ key: 'veh_hurto_perdida_total', label: 'Pérdida Total' }
												] as cob}
													<div class="grid grid-cols-4 gap-2 items-center p-2 bg-red-50 rounded">
														<span class="font-medium text-sm text-red-800">{cob.label}</span>
														<input type="text" bind:value={coberturasEditables[i][cob.key].porcentaje} class="input input-sm" placeholder="%" />
														<input type="text" bind:value={coberturasEditables[i][cob.key].tipo} class="input input-sm" placeholder="Tipo" />
														<input type="text" bind:value={coberturasEditables[i][cob.key].minimo} class="input input-sm" placeholder="Mín" />
													</div>
												{/each}
											</div>
										{/if}
									</div>

									<!-- DEDUCIBLE RC -->
									<div class="bg-white rounded-lg border border-teal-200 overflow-hidden">
										<button type="button" class="w-full px-4 py-3 bg-teal-50 flex items-center justify-between hover:bg-teal-100" on:click={() => toggleCoberturaSection(i, 'rc_ded')}>
											<h4 class="font-semibold text-teal-700">Deducible RC - 1 cobertura</h4>
											<svg class="w-5 h-5 text-teal-600 transition-transform {expandedCoberturas[i]?.rc_ded ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
										</button>
										{#if expandedCoberturas[i]?.rc_ded}
											<div class="p-4">
												<div class="grid grid-cols-4 gap-2 items-center p-2 bg-teal-50 rounded">
													<span class="font-medium text-sm text-teal-800">Responsabilidad Civil</span>
													<input type="text" bind:value={coberturasEditables[i].veh_deducible_rc.porcentaje} class="input input-sm" placeholder="%" />
													<input type="text" bind:value={coberturasEditables[i].veh_deducible_rc.tipo} class="input input-sm" placeholder="Tipo" />
													<input type="text" bind:value={coberturasEditables[i].veh_deducible_rc.minimo} class="input input-sm" placeholder="Mín" />
												</div>
											</div>
										{/if}
									</div>

									<!-- SUBLÍMITES RC -->
									<div class="bg-white rounded-lg border border-amber-200 overflow-hidden">
										<button type="button" class="w-full px-4 py-3 bg-amber-50 flex items-center justify-between hover:bg-amber-100" on:click={() => toggleCoberturaSection(i, 'rc_sub')}>
											<h4 class="font-semibold text-amber-700">Sublímites RC - 4 coberturas</h4>
											<svg class="w-5 h-5 text-amber-600 transition-transform {expandedCoberturas[i]?.rc_sub ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
										</button>
										{#if expandedCoberturas[i]?.rc_sub}
											<div class="p-4 space-y-3">
												{#each [
													{ key: 'veh_rc_sublimite_bienes_terceros', label: 'Bienes a Terceros' },
													{ key: 'veh_rc_sublimite_amparo_patrimonial', label: 'Amparo Patrimonial' },
													{ key: 'veh_rc_sublimite_muerte_lesion_una', label: 'Muerte/Lesión (1 persona)' },
													{ key: 'veh_rc_sublimite_muerte_lesion_dos_mas', label: 'Muerte/Lesión (2+ personas)' }
												] as sub}
													<div class="grid grid-cols-2 gap-2 items-center p-2 bg-amber-50 rounded">
														<span class="font-medium text-sm text-amber-800">{sub.label}</span>
														<input type="number" bind:value={coberturasEditables[i][sub.key]} class="input input-sm" placeholder="Valor en COP" />
													</div>
												{/each}
											</div>
										{/if}
									</div>

									<!-- COBERTURAS ADICIONALES -->
									<div class="bg-white rounded-lg border border-orange-200 overflow-hidden">
										<button type="button" class="w-full px-4 py-3 bg-orange-50 flex items-center justify-between hover:bg-orange-100" on:click={() => toggleCoberturaSection(i, 'adicionales')}>
											<h4 class="font-semibold text-orange-700">Coberturas Adicionales - 7 coberturas</h4>
											<svg class="w-5 h-5 text-orange-600 transition-transform {expandedCoberturas[i]?.adicionales ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
										</button>
										{#if expandedCoberturas[i]?.adicionales}
											<div class="p-4">
												<div class="grid grid-cols-1 md:grid-cols-2 gap-2">
													{#each nombresCoberturas as nombre, idx}
														<label class="flex items-center gap-2 p-2 bg-orange-50 rounded cursor-pointer hover:bg-orange-100">
															<input 
																type="checkbox" 
																bind:checked={coberturasEditables[i][`veh_cobertura_adicional_${idx + 1}`]}
																class="w-4 h-4 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
															/>
															<span class="text-sm">{nombre}</span>
														</label>
													{/each}
												</div>
											</div>
										{/if}
									</div>

									<!-- INFORMACIÓN ADICIONAL -->
									<div class="bg-white rounded-lg border border-green-200 overflow-hidden">
										<button type="button" class="w-full px-4 py-3 bg-green-50 flex items-center justify-between hover:bg-green-100" on:click={() => toggleCoberturaSection(i, 'info')}>
											<h4 class="font-semibold text-green-700">Información Adicional</h4>
											<svg class="w-5 h-5 text-green-600 transition-transform {expandedCoberturas[i]?.info ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
										</button>
										{#if expandedCoberturas[i]?.info}
											<div class="p-4 space-y-3">
												<div>
													<p class="block text-xs text-secondary-500 mb-1">Tipo de Asistencia</p>
													<input type="text" bind:value={coberturasEditables[i].veh_asistencia_tipo} class="input text-sm" placeholder="Ej: Nacional 24/7" />
												</div>
												<div>
													<p class="block text-xs text-secondary-500 mb-1">Conductor Elegido</p>
													<input type="text" bind:value={coberturasEditables[i].veh_conductor_elegido} class="input text-sm" placeholder="Nombre del conductor" />
												</div>
												<div>
													<p class="block text-xs text-secondary-500 mb-1">Beneficiario Adicional</p>
													<input type="text" bind:value={coberturasEditables[i].veh_beneficiario_adicional} class="input text-sm" placeholder="Nombre del beneficiario" />
												</div>
												<div>
													<p class="block text-xs text-secondary-500 mb-1">Observaciones</p>
													<textarea 
														bind:value={coberturasEditables[i].veh_observaciones}
														class="w-full px-3 py-2 border border-secondary-300 rounded-lg text-sm"
														rows="2"
														placeholder="Observaciones generales..."
													></textarea>
												</div>
											</div>
										{/if}
									</div>
								</div>
							</div>
						{/if}
					{/each}
				</div>
			</FormSection>
		</div>
	{/if}
</div>

<!-- Modal de Éxito -->
<Modal bind:open={showSuccessModal} title="Propuesta Generada" size="sm">
	<div class="text-center space-y-4">
		<div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center">
			<svg class="w-10 h-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
			</svg>
		</div>
		<div>
			<h3 class="text-lg font-semibold text-secondary-900">Propuesta generada correctamente</h3>
			<p class="text-secondary-600 mt-2">El archivo se ha descargado automáticamente.</p>
		</div>
		<div class="bg-secondary-50 rounded-lg p-4 text-left">
			<p class="text-xs text-secondary-500 mb-1">Archivo generado:</p>
			<p class="text-sm font-mono font-medium text-secondary-800 break-all">{generatedFilename}</p>
			{#if generatedSavedPath}
				<p class="text-xs text-secondary-500 mt-3 mb-1">Guardado en servidor:</p>
				<p class="text-xs font-mono text-secondary-600 break-all">{generatedSavedPath}</p>
			{/if}
		</div>
	</div>
	<svelte:fragment slot="footer">
		<div class="flex justify-center gap-3">
			<button type="button" class="btn btn-secondary" on:click={() => showSuccessModal = false}>
				Cerrar
			</button>
			<button type="button" class="btn btn-primary" on:click={() => goto(`/propuestas/vehiculo/${polizaId}`)}>
				Volver a la Propuesta
			</button>
		</div>
	</svelte:fragment>
</Modal>

<style>
	.input-sm {
		@apply px-2 py-1 text-sm border border-secondary-300 rounded focus:outline-none focus:ring-1 focus:ring-primary-500;
	}
</style>
