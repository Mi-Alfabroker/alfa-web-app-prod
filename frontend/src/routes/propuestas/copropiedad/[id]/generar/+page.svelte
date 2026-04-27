<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { APP_NAME } from '$lib/config';
	import { FormField, FormSection, Input, Select, CurrencyInput, Modal } from '$components';
	import { polizaService, bienService, clienteService, aseguradoraService, propuestaService } from '$services';
	import { addNotification } from '$lib/stores/notifications';
	import { getAuthUser } from '$lib/stores/auth';
	import type { PolizaCopropiedad } from '$lib/types/poliza';
	import type { Copropiedad } from '$lib/types/bien';
	import type { Cliente } from '$lib/types/cliente';
	import type { Aseguradora } from '$lib/types/aseguradora';
	import { DICCIONARIO_CAMPOS_COP, getAseguradoraOffset } from '$lib/data/diccionario_campos_copropiedad';

	// Route params
	$: polizaId = Number($page.params.id);

	// Data state
	let poliza: PolizaCopropiedad | null = null;
	let copropiedad: Copropiedad | null = null;
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
		detalles: true,
		avaluo: true,
		asegurados: true,
		infraseguro: true,
		aseguradoras: true,
		coberturas: false,
		asistencias: false,
		diferenciadoras: true
	};

	// =========================================================================
	// CAMPOS MANUALES DEL FORMULARIO
	// =========================================================================
	let camposManuales = {
		asesor: '',
		administrador: '',
		tasaInteres: 2.5,  // Tasa de interés mensual por defecto (2.5%)
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

	interface Asistencia {
		vidrieria: string;
		plomeria: string;
		cerrajeria: string;
		electricista: string;
	}

	interface CoberturasAseguradora {
		// Index signature para acceso dinámico
		[key: string]: Deducible | Asistencia | boolean | number;
		// Daños Materiales
		dm_terremoto: Deducible;
		dm_inundacion: Deducible;
		dm_incendio: Deducible;
		dm_amit: Deducible;
		dm_tuberia_vidrio: Deducible;
		// Daños Internos
		di_maq_equipo: Deducible;
		di_equipo_electronico: Deducible;
		// Sustracción con Violencia
		scv_maq_equipo: Deducible;
		scv_equipo_electronico: Deducible;
		scv_dineros: Deducible;
		scv_muebles: Deducible;
		// Directores & Administradores
		da_amparo_basico: Deducible;
		// RCE Deducibles
		rce_ded_contratistas: Deducible;
		rce_ded_cruzada: Deducible;
		rce_ded_patronal: Deducible;
		rce_ded_parqueaderos: Deducible;
		rce_ded_gastos_medicos: Deducible;
		// RCE Sublímites
		rce_sub_contratistas: Deducible;
		rce_sub_cruzada: Deducible;
		rce_sub_patronal: Deducible;
		rce_sub_parqueaderos: Deducible;
		rce_sub_gastos_medicos: Deducible;
		// Manejo
		manejo_amparo_basico: Deducible;
		// Transporte de Valores
		tv_amparo_basico: Deducible;
		// Asistencias
		asist_area_comun: Asistencia;
		asist_area_privada: Asistencia;
		// Diferenciadoras (campos de texto editables)
		cobertura_diferenciadora_1: string;
		cobertura_diferenciadora_2: string;
	}

	// Estado editable de coberturas por aseguradora (1-5)
	let coberturasEditables: CoberturasAseguradora[] = [];

	// Acordeones de coberturas expandidos por aseguradora
	let expandedCoberturas: Record<string, boolean>[] = [{}, {}, {}, {}, {}];

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
		const asistenciaVacia = (): Asistencia => ({ vidrieria: '', plomeria: '', cerrajeria: '', electricista: '' });
		return {
			dm_terremoto: deducibleVacio(),
			dm_inundacion: deducibleVacio(),
			dm_incendio: deducibleVacio(),
			dm_amit: deducibleVacio(),
			dm_tuberia_vidrio: deducibleVacio(),
			di_maq_equipo: deducibleVacio(),
			di_equipo_electronico: deducibleVacio(),
			scv_maq_equipo: deducibleVacio(),
			scv_equipo_electronico: deducibleVacio(),
			scv_dineros: deducibleVacio(),
			scv_muebles: deducibleVacio(),
			da_amparo_basico: deducibleVacio(),
			rce_ded_contratistas: deducibleVacio(),
			rce_ded_cruzada: deducibleVacio(),
			rce_ded_patronal: deducibleVacio(),
			rce_ded_parqueaderos: deducibleVacio(),
			rce_ded_gastos_medicos: deducibleVacio(),
			rce_sub_contratistas: deducibleVacio(),
			rce_sub_cruzada: deducibleVacio(),
			rce_sub_patronal: deducibleVacio(),
			rce_sub_parqueaderos: deducibleVacio(),
			rce_sub_gastos_medicos: deducibleVacio(),
			manejo_amparo_basico: deducibleVacio(),
			tv_amparo_basico: deducibleVacio(),
			asist_area_comun: asistenciaVacia(),
			asist_area_privada: asistenciaVacia(),
			cobertura_diferenciadora_1: 'No aplica demérito por uso',
			cobertura_diferenciadora_2: 'Accidentes personales consejo'
		};
	}

	// Inicializar coberturas desde aseguradora de la BD
	function inicializarCoberturasDesdeAseguradora(aseg: Aseguradora | null): CoberturasAseguradora {
		const coberturas = crearCoberturasVacias();
		if (!aseg) return coberturas;

		// Separar y asignar cada campo
		const sep = (valor: string | undefined) => {
			if (!valor) return { porcentaje: '', tipo: '', minimo: '' };
			const p = valor.split(',');
			return { porcentaje: p[0] || '', tipo: p[1] || '', minimo: p[2] || '' };
		};
		const sepAsist = (valor: string | undefined) => {
			if (!valor) return { vidrieria: '', plomeria: '', cerrajeria: '', electricista: '' };
			const p = valor.split(',');
			return { vidrieria: p[0] || '', plomeria: p[1] || '', cerrajeria: p[2] || '', electricista: p[3] || '' };
		};

		// Daños Materiales
		coberturas.dm_terremoto = sep(aseg.cop_dm_deducible_terremoto);
		coberturas.dm_inundacion = sep(aseg.cop_dm_deducible_inundacion);
		coberturas.dm_incendio = sep(aseg.cop_dm_deducible_incendio);
		coberturas.dm_amit = sep(aseg.cop_dm_deducible_amit);
		coberturas.dm_tuberia_vidrio = sep(aseg.cop_dm_deducible_tuberia_vidrio);
		// Daños Internos
		coberturas.di_maq_equipo = sep(aseg.cop_di_deducible_maq_equipo);
		coberturas.di_equipo_electronico = sep(aseg.cop_di_deducible_equipo_electronico);
		// Sustracción con Violencia
		coberturas.scv_maq_equipo = sep(aseg.cop_scv_deducible_maq_equipo);
		coberturas.scv_equipo_electronico = sep(aseg.cop_scv_deducible_equipo_electronico);
		coberturas.scv_dineros = sep(aseg.cop_scv_deducible_dineros);
		coberturas.scv_muebles = sep(aseg.cop_scv_deducible_muebles);
		// Directores & Administradores
		coberturas.da_amparo_basico = sep(aseg.cop_da_deducible_amparo_basico);
		// RCE Deducibles
		coberturas.rce_ded_contratistas = sep(aseg.cop_rce_deducible_contratistas);
		coberturas.rce_ded_cruzada = sep(aseg.cop_rce_deducible_cruzada);
		coberturas.rce_ded_patronal = sep(aseg.cop_rce_deducible_patronal);
		coberturas.rce_ded_parqueaderos = sep(aseg.cop_rce_deducible_parqueaderos);
		coberturas.rce_ded_gastos_medicos = sep(aseg.cop_rce_deducible_gastos_medicos);
		// RCE Sublímites
		coberturas.rce_sub_contratistas = sep(aseg.cop_rce_sublimite_contratistas);
		coberturas.rce_sub_cruzada = sep(aseg.cop_rce_sublimite_cruzada);
		coberturas.rce_sub_patronal = sep(aseg.cop_rce_sublimite_patronal);
		coberturas.rce_sub_parqueaderos = sep(aseg.cop_rce_sublimite_parqueaderos);
		coberturas.rce_sub_gastos_medicos = sep(aseg.cop_rce_sublimite_gastos_medicos);
		// Manejo
		coberturas.manejo_amparo_basico = sep(aseg.cop_manejo_deducible_amparo_basico);
		// Transporte de Valores
		coberturas.tv_amparo_basico = sep(aseg.cop_tv_deducible_amparo_basico);
		// Asistencias
		coberturas.asist_area_comun = sepAsist(aseg.cop_asistencia_area_comun);
		coberturas.asist_area_privada = sepAsist(aseg.cop_asistencia_area_privada);

		return coberturas;
	}

	async function loadData() {
		loading = true;
		error = null;
		try {
			// Load poliza
			poliza = await polizaService.copropiedad.getById(polizaId);
			
			if (!poliza) {
				throw new Error('No se encontró la póliza');
			}
			
			// Load related data
			const [copropiedadData, aseguradorasData] = await Promise.all([
				bienService.copropiedades.getById(poliza.id_copropiedad),
				aseguradoraService.getAll()
			]);
			
			copropiedad = copropiedadData;
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
			
			// Load cliente
			if (copropiedad) {
				const clientes = await clienteService.getAll();
				cliente = clientes.find((c: Cliente) => c.id === copropiedad!.id_usuario) || null;
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
	// HELPER: Separar campo concatenado (porcentaje,tipo,minimo)
	// =========================================================================
	function separarDeducible(valor: string | undefined | null): { porcentaje: string; tipo: string; minimo: string } {
		if (!valor) return { porcentaje: '', tipo: '', minimo: '' };
		const partes = valor.split(',');
		return {
			porcentaje: partes[0] || '',
			tipo: partes[1] || '',
			minimo: partes[2] || ''
		};
	}

	// =========================================================================
	// HELPER: Separar asistencias (vidrieria,plomeria,cerrajeria,electricista)
	// =========================================================================
	function separarAsistencias(valor: string | undefined | null): { vidrieria: string; plomeria: string; cerrajeria: string; electricista: string; total: number } {
		if (!valor) return { vidrieria: '', plomeria: '', cerrajeria: '', electricista: '', total: 0 };
		const partes = valor.split(',');
		const nums = partes.map(p => parseInt(p) || 0);
		return {
			vidrieria: partes[0] || '',
			plomeria: partes[1] || '',
			cerrajeria: partes[2] || '',
			electricista: partes[3] || '',
			total: nums.reduce((a, b) => a + b, 0)
		};
	}

	// =========================================================================
	// HELPER: Calcular infraseguro
	// =========================================================================
	function calcularInfraseguro(asegurado: number | null | undefined, avaluo: number | null | undefined): string {
		if (!asegurado || !avaluo || avaluo === 0) return '—';
		const infraseg = 1 - (asegurado / avaluo);
		if (infraseg <= 0) return '0%';
		return `${(infraseg * 100).toFixed(1)}%`;
	}

	// =========================================================================
	// HELPER: Formatear fecha de expedición (fecha actual al generar)
	// Formato: "8 de enero 2026"
	// =========================================================================
	function formatearFecha(): string {
		const fecha = new Date();
		const dia = fecha.getDate(); // Sin cero inicial
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
	// Fórmula: Prima * ((tasa * (1+tasa)^n) / ((1+tasa)^n - 1))
	// =========================================================================
	function calcularCuotaConInteres(prima: number, tasaPorcentaje: number, numCuotas: number): number {
		if (!prima || prima <= 0 || numCuotas <= 0) return 0;
		
		// Convertir tasa de porcentaje a decimal (ej: 2.5% -> 0.025)
		const tasa = tasaPorcentaje / 100;
		
		if (tasa <= 0) {
			// Si no hay interés, simplemente dividir
			return Math.round(prima / numCuotas);
		}
		
		// Fórmula de amortización
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
	// CONSTRUIR JSON campos_reemplazo_cop CON CÓDIGOS [N] para Excel
	// =========================================================================
	function buildVariablesJson(): Record<string, string> {
		if (!poliza || !copropiedad || !cliente) {
			return {};
		}

		// Helper: Formatear valor monetario con separadores de miles (sin símbolo $)
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

		// Helper: Sufijo % para campos de porcentaje (no duplica si ya termina en %)
		const pct = (value: any): string => {
			const s = str(value).trim();
			if (!s) return '';
			return s.endsWith('%') ? s : `${s}%`;
		};

		// JSON con CÓDIGOS [N] - Para reemplazo compacto en Excel
		const campos_reemplazo_cop: Record<string, string> = {
			// SECCIÓN 1: ENCABEZADO [1]-[2]
			"[1]": formatearFecha(),
			"[2]": calcularVigencia(),

			// SECCIÓN 2: DATOS DEL CLIENTE / COPROPIEDAD [3]-[9]
			"[3]": getNombreCliente(),
			"[4]": cliente.tipo_persona === 'EMPRESA' ? str(cliente.nit) : str(cliente.numero_documento),
			"[5]": camposManuales.administrador,
			"[6]": str(copropiedad.tipo_copropiedad),
			"[7]": str(copropiedad.ciudad),
			"[8]": str(copropiedad.direccion),
			"[9]": camposManuales.asesor,

			// SECCIÓN 3: DETALLES DE LA COPROPIEDAD [10]-[19]
			"[10]": str(copropiedad.ano_construccion),
			"[11]": str(copropiedad.estrato),
			"[12]": str(copropiedad.numero_torres),
			"[13]": str(copropiedad.numero_maximo_pisos),
			"[14]": str(copropiedad.numero_maximo_sotanos),
			"[15]": str(copropiedad.cantidad_unidades_casa),
			"[16]": str(copropiedad.cantidad_unidades_apartamentos),
			"[17]": str(copropiedad.cantidad_unidades_locales),
			"[18]": str(copropiedad.cantidad_unidades_oficinas),
			"[19]": str(copropiedad.cantidad_unidades_otros),

			// SECCIÓN 4: VALORES DEL BIEN (AVALÚO) [20]-[24]
			"[20]": formatMoney(copropiedad.valor_edificio_area_comun_avaluo),
			"[21]": formatMoney(copropiedad.valor_edificio_area_privada_avaluo),
			"[22]": formatMoney(copropiedad.valor_maquinaria_equipo_avaluo),
			"[23]": formatMoney(copropiedad.valor_equipo_electrico_electronico_avaluo),
			"[24]": formatMoney(copropiedad.valor_muebles_avaluo),

			// SECCIÓN 5: VALORES ASEGURADOS [25]-[34]
			"[25]": formatMoney(poliza.valor_area_comun_asegurado),
			"[26]": formatMoney(poliza.valor_area_privada_asegurado),
			"[27]": formatMoney(poliza.valor_maquinaria_equipo_asegurado),
			"[28]": formatMoney(poliza.valor_equipo_electronico_asegurado),
			"[29]": formatMoney(poliza.valor_muebles_asegurado),
			// Valores en MILLONES (se envía solo el número, el Excel lo formatea)
			"[30]": String(poliza.valor_directores_asegurado || 0),
			"[31]": String(poliza.valor_rce_asegurado || 0),
			"[32]": String(poliza.valor_manejo_asegurado || 0),
			"[33]": String(poliza.valor_transporte_valores_vigencia_asegurado || 0),
			"[34]": String(poliza.valor_transporte_valores_despacho_asegurado || 0),

			// SECCIÓN 6: INFRASEGURO [35]-[39]
			"[35]": calcularInfraseguro(poliza.valor_area_comun_asegurado, copropiedad.valor_edificio_area_comun_avaluo),
			"[36]": calcularInfraseguro(poliza.valor_area_privada_asegurado, copropiedad.valor_edificio_area_privada_avaluo),
			"[37]": calcularInfraseguro(poliza.valor_maquinaria_equipo_asegurado, copropiedad.valor_maquinaria_equipo_avaluo),
			"[38]": calcularInfraseguro(poliza.valor_equipo_electronico_asegurado, copropiedad.valor_equipo_electrico_electronico_avaluo),
			"[39]": calcularInfraseguro(poliza.valor_muebles_asegurado, copropiedad.valor_muebles_avaluo),

			// SECCIÓN 7: CAMPOS CALCULADOS [495]+
			"[495]": formatMoney(
				(poliza.valor_area_comun_asegurado || 0) +
				(poliza.valor_maquinaria_equipo_asegurado || 0) +
				(poliza.valor_equipo_electronico_asegurado || 0) +
				(poliza.valor_muebles_asegurado || 0)
			),
			"[496]": formatMoney(
				(poliza.valor_area_comun_asegurado || 0) +
				(poliza.valor_area_privada_asegurado || 0) +
				(poliza.valor_maquinaria_equipo_asegurado || 0) +
				(poliza.valor_equipo_electronico_asegurado || 0) +
				(poliza.valor_muebles_asegurado || 0)
			)
		};

		// SECCIÓN 8: FINANCIACIÓN [497]-[516]
		const tasa = camposManuales.tasaInteres;
		
		for (let i = 0; i < 5; i++) {
			const prima = (poliza as any)[`valor_prima_aseg_${i + 1}`] || 0;
			
			// 3 cuotas sin interés [497]-[501]
			campos_reemplazo_cop[`[${497 + i}]`] = formatMoney(Math.round(prima / 3));
			
			// 5 cuotas con interés [502]-[506]
			campos_reemplazo_cop[`[${502 + i}]`] = formatMoney(calcularCuotaConInteres(prima, tasa, 5));
			
			// 8 cuotas con interés [507]-[511]
			campos_reemplazo_cop[`[${507 + i}]`] = formatMoney(calcularCuotaConInteres(prima, tasa, 8));
			
			// 11 cuotas con interés [512]-[516]
			campos_reemplazo_cop[`[${512 + i}]`] = formatMoney(calcularCuotaConInteres(prima, tasa, 11));
		}

		// =====================================================================
		// ASEGURADORAS 1-5: [40]-[494]
		// Cada aseguradora tiene 91 campos (offset de 91 por aseguradora)
		// =====================================================================
		const asegOffsets = [40, 131, 222, 313, 404]; // Inicio de cada aseguradora

		for (let i = 0; i < 5; i++) {
			const base = asegOffsets[i];
			const aseg = aseguradorasSeleccionadas[i];
			const prima = (poliza as any)[`valor_prima_aseg_${i + 1}`];
			const cob = coberturasEditables[i];

			// Datos base [+0 a +8]
			campos_reemplazo_cop[`[${base}]`] = str(aseg?.nombre);
			campos_reemplazo_cop[`[${base + 1}]`] = str(aseg?.ruta_pais_logo);
			campos_reemplazo_cop[`[${base + 2}]`] = str(aseg?.respaldo_aseguradora);
			campos_reemplazo_cop[`[${base + 3}]`] = str(aseg?.numeral_asistencia);
			campos_reemplazo_cop[`[${base + 4}]`] = formatMoney(prima);
			campos_reemplazo_cop[`[${base + 5}]`] = formatMoney(prima);  // Valor total anual = Prima
			campos_reemplazo_cop[`[${base + 6}]`] = cob.cobertura_diferenciadora_1;
			campos_reemplazo_cop[`[${base + 7}]`] = cob.cobertura_diferenciadora_2;
			campos_reemplazo_cop[`[${base + 8}]`] = '';  // Campo reservado (antes: rotura_vidrios)

			// DM - Daños Materiales [+9 a +23]
			campos_reemplazo_cop[`[${base + 9}]`] = pct(cob.dm_terremoto.porcentaje);
			campos_reemplazo_cop[`[${base + 10}]`] = cob.dm_terremoto.tipo;
			campos_reemplazo_cop[`[${base + 11}]`] = cob.dm_terremoto.minimo;
			campos_reemplazo_cop[`[${base + 12}]`] = pct(cob.dm_inundacion.porcentaje);
			campos_reemplazo_cop[`[${base + 13}]`] = cob.dm_inundacion.tipo;
			campos_reemplazo_cop[`[${base + 14}]`] = cob.dm_inundacion.minimo;
			campos_reemplazo_cop[`[${base + 15}]`] = pct(cob.dm_incendio.porcentaje);
			campos_reemplazo_cop[`[${base + 16}]`] = cob.dm_incendio.tipo;
			campos_reemplazo_cop[`[${base + 17}]`] = cob.dm_incendio.minimo;
			campos_reemplazo_cop[`[${base + 18}]`] = pct(cob.dm_amit.porcentaje);
			campos_reemplazo_cop[`[${base + 19}]`] = cob.dm_amit.tipo;
			campos_reemplazo_cop[`[${base + 20}]`] = cob.dm_amit.minimo;
			campos_reemplazo_cop[`[${base + 21}]`] = pct(cob.dm_tuberia_vidrio.porcentaje);
			campos_reemplazo_cop[`[${base + 22}]`] = cob.dm_tuberia_vidrio.tipo;
			campos_reemplazo_cop[`[${base + 23}]`] = cob.dm_tuberia_vidrio.minimo;

			// DI - Daños Internos [+24 a +29]
			campos_reemplazo_cop[`[${base + 24}]`] = pct(cob.di_maq_equipo.porcentaje);
			campos_reemplazo_cop[`[${base + 25}]`] = cob.di_maq_equipo.tipo;
			campos_reemplazo_cop[`[${base + 26}]`] = cob.di_maq_equipo.minimo;
			campos_reemplazo_cop[`[${base + 27}]`] = pct(cob.di_equipo_electronico.porcentaje);
			campos_reemplazo_cop[`[${base + 28}]`] = cob.di_equipo_electronico.tipo;
			campos_reemplazo_cop[`[${base + 29}]`] = cob.di_equipo_electronico.minimo;

			// SCV - Sustracción con Violencia [+30 a +41]
			campos_reemplazo_cop[`[${base + 30}]`] = pct(cob.scv_maq_equipo.porcentaje);
			campos_reemplazo_cop[`[${base + 31}]`] = cob.scv_maq_equipo.tipo;
			campos_reemplazo_cop[`[${base + 32}]`] = cob.scv_maq_equipo.minimo;
			campos_reemplazo_cop[`[${base + 33}]`] = pct(cob.scv_equipo_electronico.porcentaje);
			campos_reemplazo_cop[`[${base + 34}]`] = cob.scv_equipo_electronico.tipo;
			campos_reemplazo_cop[`[${base + 35}]`] = cob.scv_equipo_electronico.minimo;
			campos_reemplazo_cop[`[${base + 36}]`] = pct(cob.scv_dineros.porcentaje);
			campos_reemplazo_cop[`[${base + 37}]`] = cob.scv_dineros.tipo;
			campos_reemplazo_cop[`[${base + 38}]`] = cob.scv_dineros.minimo;
			campos_reemplazo_cop[`[${base + 39}]`] = pct(cob.scv_muebles.porcentaje);
			campos_reemplazo_cop[`[${base + 40}]`] = cob.scv_muebles.tipo;
			campos_reemplazo_cop[`[${base + 41}]`] = cob.scv_muebles.minimo;

			// DA - Directores y Administradores [+42 a +44]
			campos_reemplazo_cop[`[${base + 42}]`] = pct(cob.da_amparo_basico.porcentaje);
			campos_reemplazo_cop[`[${base + 43}]`] = cob.da_amparo_basico.tipo;
			campos_reemplazo_cop[`[${base + 44}]`] = cob.da_amparo_basico.minimo;

			// RCE Deducibles [+45 a +59]
			campos_reemplazo_cop[`[${base + 45}]`] = pct(cob.rce_ded_contratistas.porcentaje);
			campos_reemplazo_cop[`[${base + 46}]`] = cob.rce_ded_contratistas.tipo;
			campos_reemplazo_cop[`[${base + 47}]`] = cob.rce_ded_contratistas.minimo;
			campos_reemplazo_cop[`[${base + 48}]`] = pct(cob.rce_ded_cruzada.porcentaje);
			campos_reemplazo_cop[`[${base + 49}]`] = cob.rce_ded_cruzada.tipo;
			campos_reemplazo_cop[`[${base + 50}]`] = cob.rce_ded_cruzada.minimo;
			campos_reemplazo_cop[`[${base + 51}]`] = pct(cob.rce_ded_patronal.porcentaje);
			campos_reemplazo_cop[`[${base + 52}]`] = cob.rce_ded_patronal.tipo;
			campos_reemplazo_cop[`[${base + 53}]`] = cob.rce_ded_patronal.minimo;
			campos_reemplazo_cop[`[${base + 54}]`] = pct(cob.rce_ded_parqueaderos.porcentaje);
			campos_reemplazo_cop[`[${base + 55}]`] = cob.rce_ded_parqueaderos.tipo;
			campos_reemplazo_cop[`[${base + 56}]`] = cob.rce_ded_parqueaderos.minimo;
			campos_reemplazo_cop[`[${base + 57}]`] = pct(cob.rce_ded_gastos_medicos.porcentaje);
			campos_reemplazo_cop[`[${base + 58}]`] = cob.rce_ded_gastos_medicos.tipo;
			campos_reemplazo_cop[`[${base + 59}]`] = cob.rce_ded_gastos_medicos.minimo;

			// RCE Sublímites [+60 a +74]
			campos_reemplazo_cop[`[${base + 60}]`] = pct(cob.rce_sub_contratistas.porcentaje);
			campos_reemplazo_cop[`[${base + 61}]`] = cob.rce_sub_contratistas.tipo;
			campos_reemplazo_cop[`[${base + 62}]`] = cob.rce_sub_contratistas.minimo;
			campos_reemplazo_cop[`[${base + 63}]`] = pct(cob.rce_sub_cruzada.porcentaje);
			campos_reemplazo_cop[`[${base + 64}]`] = cob.rce_sub_cruzada.tipo;
			campos_reemplazo_cop[`[${base + 65}]`] = cob.rce_sub_cruzada.minimo;
			campos_reemplazo_cop[`[${base + 66}]`] = pct(cob.rce_sub_patronal.porcentaje);
			campos_reemplazo_cop[`[${base + 67}]`] = cob.rce_sub_patronal.tipo;
			campos_reemplazo_cop[`[${base + 68}]`] = cob.rce_sub_patronal.minimo;
			campos_reemplazo_cop[`[${base + 69}]`] = pct(cob.rce_sub_parqueaderos.porcentaje);
			campos_reemplazo_cop[`[${base + 70}]`] = cob.rce_sub_parqueaderos.tipo;
			campos_reemplazo_cop[`[${base + 71}]`] = cob.rce_sub_parqueaderos.minimo;
			campos_reemplazo_cop[`[${base + 72}]`] = pct(cob.rce_sub_gastos_medicos.porcentaje);
			campos_reemplazo_cop[`[${base + 73}]`] = cob.rce_sub_gastos_medicos.tipo;
			campos_reemplazo_cop[`[${base + 74}]`] = cob.rce_sub_gastos_medicos.minimo;

			// Manejo [+75 a +77]
			campos_reemplazo_cop[`[${base + 75}]`] = pct(cob.manejo_amparo_basico.porcentaje);
			campos_reemplazo_cop[`[${base + 76}]`] = cob.manejo_amparo_basico.tipo;
			campos_reemplazo_cop[`[${base + 77}]`] = cob.manejo_amparo_basico.minimo;

			// Transporte de Valores [+78 a +80]
			campos_reemplazo_cop[`[${base + 78}]`] = pct(cob.tv_amparo_basico.porcentaje);
			campos_reemplazo_cop[`[${base + 79}]`] = cob.tv_amparo_basico.tipo;
			campos_reemplazo_cop[`[${base + 80}]`] = cob.tv_amparo_basico.minimo;

			// Asistencias Área Común [+81 a +85]
			campos_reemplazo_cop[`[${base + 81}]`] = str(cob.asist_area_comun.vidrieria);
			campos_reemplazo_cop[`[${base + 82}]`] = str(cob.asist_area_comun.plomeria);
			campos_reemplazo_cop[`[${base + 83}]`] = str(cob.asist_area_comun.cerrajeria);
			campos_reemplazo_cop[`[${base + 84}]`] = str(cob.asist_area_comun.electricista);
			campos_reemplazo_cop[`[${base + 85}]`] = str(calcularTotalAsistencias(cob.asist_area_comun));

			// Asistencias Área Privada [+86 a +90]
			campos_reemplazo_cop[`[${base + 86}]`] = str(cob.asist_area_privada.vidrieria);
			campos_reemplazo_cop[`[${base + 87}]`] = str(cob.asist_area_privada.plomeria);
			campos_reemplazo_cop[`[${base + 88}]`] = str(cob.asist_area_privada.cerrajeria);
			campos_reemplazo_cop[`[${base + 89}]`] = str(cob.asist_area_privada.electricista);
			campos_reemplazo_cop[`[${base + 90}]`] = str(calcularTotalAsistencias(cob.asist_area_privada));
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

		campos_reemplazo_cop['[517]'] = str(camposManuales.nombre_aseguradora);
		campos_reemplazo_cop['[518]'] = str(camposManuales.numero_poliza);
		campos_reemplazo_cop['[519]'] = formatFechaManual(camposManuales.fecha_inicio_vigencia);
		campos_reemplazo_cop['[520]'] = formatFechaManual(camposManuales.fecha_fin_vigencia);
		campos_reemplazo_cop['[521]'] = formatMoney(Number(camposManuales.valor_total_prima) || 0);
		campos_reemplazo_cop['[522]'] = str(camposManuales.medio_pago);
		campos_reemplazo_cop['[523]'] = str(camposManuales.numeral_asistencia);
		campos_reemplazo_cop['[524]'] = str(camposManuales.financiacion_num_cuotas);
		campos_reemplazo_cop['[525]'] = formatMoney(Number(camposManuales.financiacion_valor_cuota) || 0);
		campos_reemplazo_cop['[526]'] = formatFechaManual(camposManuales.financiacion_fecha_primera);
		campos_reemplazo_cop['[527]'] = str(camposManuales.financiacion_periodicidad);
		campos_reemplazo_cop['[528]'] = str(camposManuales.financiacion_cuota_actual);

		return campos_reemplazo_cop;
	}

	// =========================================================================
	// CONSTRUIR JSON de imágenes basado en aseguradoras seleccionadas
	// Usa los campos ruta_logo y ruta_pais_logo de la tabla aseguradoras
	// =========================================================================
	function buildImagenesJson(): Record<string, string> {
		const imagenes: Record<string, string> = {};
		
		for (let i = 0; i < 5; i++) {
			const aseg = aseguradorasSeleccionadas[i];
			if (aseg) {
				// Usar ruta_logo para el logo de la aseguradora
				if (aseg.ruta_logo) {
					imagenes[`logo_aseg_${i + 1}`] = aseg.ruta_logo;
				}
				
				// Usar ruta_pais_logo para la bandera del país
				if (aseg.ruta_pais_logo) {
					imagenes[`bandera_aseg_${i + 1}`] = aseg.ruta_pais_logo;
				}
			}
		}
		
		return imagenes;
	}

	// =========================================================================
	// GENERAR PROPUESTA - Llama al endpoint del backend
	// =========================================================================
	async function generarPropuesta() {
		if (!poliza || !copropiedad || !cliente) {
			addNotification({
				type: 'error',
				title: 'Error',
				message: 'Faltan datos necesarios para generar la propuesta'
			});
			return;
		}

		generating = true;

		try {
			// Construir el JSON de variables
			const variables = buildVariablesJson();
			
			// Construir el JSON de imágenes
			const imagenes = buildImagenesJson();

			// Log del JSON que se envía al API
			console.log('📤 JSON enviado al API:', JSON.stringify({ template_name: 'copropiedades', variables, imagenes }, null, 2));

			// Llamar al endpoint del backend
			const result = await propuestaService.generateAndDownload({
				template_name: 'copropiedades',
				variables,
				imagenes
			});

			// Guardar info para el modal
			generatedFilename = result.filename;
			generatedSavedPath = result.savedPath;

			// Guardar valores de cuotas calculadas en la póliza
			await guardarValoresCuotas();

			// Mostrar modal de éxito
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
		if (!poliza || !copropiedad || !cliente) {
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

			console.log('📤 JSON entrega enviado al API:', JSON.stringify({ template_name: 'entrega_copropiedades', variables, imagenes }, null, 2));

			const result = await propuestaService.generateAndDownload({
				template_name: 'entrega_copropiedades',
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
			await polizaService.copropiedad.update(polizaId, valoresCuotas);
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

	// Helper para obtener prima por índice
	function getPrimaByIndex(index: number): number | null {
		if (!poliza) return null;
		const key = `valor_prima_aseg_${index + 1}` as keyof PolizaCopropiedad;
		return poliza[key] as number | null;
	}

	// Helper para calcular total de asistencias
	function calcularTotalAsistencias(asist: Asistencia): number {
		return (parseInt(asist.vidrieria) || 0) + 
			   (parseInt(asist.plomeria) || 0) + 
			   (parseInt(asist.cerrajeria) || 0) + 
			   (parseInt(asist.electricista) || 0);
	}

	// Toggle para acordeones de coberturas por aseguradora
	function toggleCoberturaSection(asegIndex: number, section: string) {
		expandedCoberturas[asegIndex][section] = !expandedCoberturas[asegIndex][section];
		expandedCoberturas = [...expandedCoberturas];
	}

	// Helper para obtener un deducible tipado
	function getDeducible(cob: CoberturasAseguradora, key: string): Deducible {
		return cob[key] as Deducible;
	}
</script>

<svelte:head>
	<title>Generar Propuesta | {APP_NAME}</title>
</svelte:head>

<!-- Header -->
<header class="page-header">
	<div class="flex items-center gap-4">
		<button 
			type="button" 
			class="p-2 hover:bg-secondary-100 rounded-lg transition-colors"
			on:click={() => goto(`/propuestas/copropiedad/${polizaId}`)}
		>
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
			</svg>
		</button>
		<div>
			<h1 class="page-title">Generar Propuesta Copropiedad</h1>
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
	{:else if poliza && copropiedad}
		<div class="space-y-4">
			<!-- SECCIÓN 1: ENCABEZADO -->
			<div class="card">
				<button 
					type="button"
					class="w-full flex items-center justify-between text-left"
					on:click={() => toggleSection('encabezado')}
				>
					<h2 class="text-lg font-semibold text-secondary-900">1. Encabezado del Documento</h2>
					<svg class="w-5 h-5 transition-transform {expandedSections.encabezado ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if expandedSections.encabezado}
					<div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
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
				{/if}
			</div>

			<!-- SECCIÓN 2: DATOS DEL CLIENTE -->
			<div class="card">
				<button 
					type="button"
					class="w-full flex items-center justify-between text-left"
					on:click={() => toggleSection('cliente')}
				>
					<h2 class="text-lg font-semibold text-secondary-900">2. Datos del Cliente / Copropiedad</h2>
					<svg class="w-5 h-5 transition-transform {expandedSections.cliente ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if expandedSections.cliente}
					<div class="mt-4 space-y-4">
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
								<p class="text-xs text-secondary-500 mb-1">Ciudad</p>
								<p class="text-sm font-medium">{copropiedad.ciudad || '—'}</p>
								<span class="text-xs text-green-600">[BD:copropiedades]</span>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg">
								<p class="text-xs text-secondary-500 mb-1">Dirección</p>
								<p class="text-sm font-medium">{copropiedad.direccion || '—'}</p>
								<span class="text-xs text-green-600">[BD:copropiedades]</span>
							</div>
						</div>
						
						<!-- Campos Manuales -->
						<div class="border-t border-secondary-200 pt-4">
							<p class="text-sm font-medium text-orange-600 mb-3">Campos Manuales</p>
							<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
								<FormField label="Administrador">
									<Input bind:value={camposManuales.administrador} placeholder="Nombre del administrador" />
								</FormField>
								<FormField label="Asesor Comercial">
									<Input bind:value={camposManuales.asesor} placeholder="Nombre del asesor" />
								</FormField>
								<FormField label="Tasa de Interés Mensual (%)">
									<div class="relative">
										<Input type="number" step="0.1" bind:value={camposManuales.tasaInteres} placeholder="2.5" />
										<span class="absolute right-3 top-1/2 -translate-y-1/2 text-secondary-400 text-sm">%</span>
									</div>
									<p class="text-xs text-secondary-500 mt-1">Para financiación a 5, 8 y 11 cuotas</p>
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
				{/if}
			</div>

			<!-- SECCIÓN 3: DETALLES DE LA COPROPIEDAD -->
			<div class="card">
				<button 
					type="button"
					class="w-full flex items-center justify-between text-left"
					on:click={() => toggleSection('detalles')}
				>
					<h2 class="text-lg font-semibold text-secondary-900">3. Detalles de la Copropiedad</h2>
					<svg class="w-5 h-5 transition-transform {expandedSections.detalles ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if expandedSections.detalles}
					<div class="mt-4">
						<p class="text-xs text-green-600 mb-3">[BD:copropiedades]</p>
						<div class="grid grid-cols-2 md:grid-cols-4 gap-3">
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.ano_construccion || '—'}</p>
								<p class="text-xs text-secondary-500">Año Construcción</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.estrato || '—'}</p>
								<p class="text-xs text-secondary-500">Estrato</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.numero_torres || '—'}</p>
								<p class="text-xs text-secondary-500">Torres</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.numero_maximo_pisos || '—'}</p>
								<p class="text-xs text-secondary-500">Pisos Máx.</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.numero_maximo_sotanos || '—'}</p>
								<p class="text-xs text-secondary-500">Sótanos</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.cantidad_unidades_apartamentos || '—'}</p>
								<p class="text-xs text-secondary-500">Apartamentos</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.cantidad_unidades_casa || '—'}</p>
								<p class="text-xs text-secondary-500">Casas</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-2xl font-bold text-primary-600">{copropiedad.cantidad_unidades_locales || '—'}</p>
								<p class="text-xs text-secondary-500">Locales</p>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- SECCIÓN 4: VALORES DE AVALÚO -->
			<div class="card">
				<button 
					type="button"
					class="w-full flex items-center justify-between text-left"
					on:click={() => toggleSection('avaluo')}
				>
					<h2 class="text-lg font-semibold text-secondary-900">4. Valores de Avalúo (Valor Real del Bien)</h2>
					<svg class="w-5 h-5 transition-transform {expandedSections.avaluo ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if expandedSections.avaluo}
					<div class="mt-4">
						<p class="text-xs text-green-600 mb-3">[BD:copropiedades]</p>
						<div class="space-y-2">
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Edificio Área Común</span>
								<span class="font-medium">{formatCurrency(copropiedad.valor_edificio_area_comun_avaluo)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Edificio Área Privada</span>
								<span class="font-medium">{formatCurrency(copropiedad.valor_edificio_area_privada_avaluo)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Maquinaria y Equipo</span>
								<span class="font-medium">{formatCurrency(copropiedad.valor_maquinaria_equipo_avaluo)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Equipo Eléctrico/Electrónico</span>
								<span class="font-medium">{formatCurrency(copropiedad.valor_equipo_electrico_electronico_avaluo)}</span>
							</div>
							<div class="flex justify-between py-2">
								<span class="text-secondary-600">Muebles</span>
								<span class="font-medium">{formatCurrency(copropiedad.valor_muebles_avaluo)}</span>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- SECCIÓN 5: VALORES ASEGURADOS -->
			<div class="card">
				<button 
					type="button"
					class="w-full flex items-center justify-between text-left"
					on:click={() => toggleSection('asegurados')}
				>
					<h2 class="text-lg font-semibold text-secondary-900">5. Valores Asegurados</h2>
					<svg class="w-5 h-5 transition-transform {expandedSections.asegurados ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if expandedSections.asegurados}
					<div class="mt-4">
						<p class="text-xs text-green-600 mb-3">[BD:polizas_copropiedad]</p>
						<div class="space-y-2">
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Área Común</span>
								<span class="font-medium">{formatCurrency(poliza.valor_area_comun_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Área Privada</span>
								<span class="font-medium">{formatCurrency(poliza.valor_area_privada_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Maquinaria y Equipo</span>
								<span class="font-medium">{formatCurrency(poliza.valor_maquinaria_equipo_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Equipo Electrónico</span>
								<span class="font-medium">{formatCurrency(poliza.valor_equipo_electronico_asegurado)}</span>
							</div>
							<div class="flex justify-between py-2 border-b border-secondary-100">
								<span class="text-secondary-600">Muebles</span>
								<span class="font-medium">{formatCurrency(poliza.valor_muebles_asegurado)}</span>
							</div>
							<!-- Nota explicativa para valores en millones -->
							<div class="mt-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl">
								<div class="flex items-start gap-3">
									<div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
										<svg class="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
									</div>
									<div>
										<h4 class="font-semibold text-blue-800 text-sm">Valores expresados en Millones</h4>
										<p class="text-blue-700 text-xs mt-1">
											Los siguientes campos se ingresan en <strong>millones de pesos</strong>. 
											Por ejemplo: <span class="bg-blue-100 px-1.5 py-0.5 rounded font-mono">20</span> = $20.000.000
										</p>
									</div>
								</div>
							</div>
							
							<div class="mt-3 space-y-2 pl-2 border-l-4 border-blue-300">
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Directores y Administradores</span>
									<span class="font-semibold text-blue-700">{poliza.valor_directores_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">RCE</span>
									<span class="font-semibold text-blue-700">{poliza.valor_rce_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Manejo</span>
									<span class="font-semibold text-blue-700">{poliza.valor_manejo_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Transporte Valores (Vigencia)</span>
									<span class="font-semibold text-blue-700">{poliza.valor_transporte_valores_vigencia_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
								<div class="flex justify-between py-2">
									<span class="text-secondary-600">Transporte Valores (Despacho)</span>
									<span class="font-semibold text-blue-700">{poliza.valor_transporte_valores_despacho_asegurado ?? 0} <span class="text-xs text-blue-500">millones</span></span>
								</div>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- SECCIÓN 6: INFRASEGURO -->
			<div class="card">
				<button 
					type="button"
					class="w-full flex items-center justify-between text-left"
					on:click={() => toggleSection('infraseguro')}
				>
					<h2 class="text-lg font-semibold text-secondary-900">6. Infraseguro</h2>
					<svg class="w-5 h-5 transition-transform {expandedSections.infraseguro ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if expandedSections.infraseguro}
					<div class="mt-4">
						<p class="text-xs text-blue-600 mb-3">[CALCULADO] Fórmula: 1 - (valor_asegurado / valor_avaluo)</p>
						<div class="grid grid-cols-2 md:grid-cols-5 gap-3">
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-lg font-bold text-red-600">{calcularInfraseguro(poliza.valor_area_comun_asegurado, copropiedad.valor_edificio_area_comun_avaluo)}</p>
								<p class="text-xs text-secondary-500">Área Común</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-lg font-bold text-red-600">{calcularInfraseguro(poliza.valor_area_privada_asegurado, copropiedad.valor_edificio_area_privada_avaluo)}</p>
								<p class="text-xs text-secondary-500">Área Privada</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-lg font-bold text-red-600">{calcularInfraseguro(poliza.valor_maquinaria_equipo_asegurado, copropiedad.valor_maquinaria_equipo_avaluo)}</p>
								<p class="text-xs text-secondary-500">Maquinaria</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-lg font-bold text-red-600">{calcularInfraseguro(poliza.valor_equipo_electronico_asegurado, copropiedad.valor_equipo_electrico_electronico_avaluo)}</p>
								<p class="text-xs text-secondary-500">Eq. Electrónico</p>
							</div>
							<div class="p-3 bg-secondary-50 rounded-lg text-center">
								<p class="text-lg font-bold text-red-600">{calcularInfraseguro(poliza.valor_muebles_asegurado, copropiedad.valor_muebles_avaluo)}</p>
								<p class="text-xs text-secondary-500">Muebles</p>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- SECCIÓN 7-11: ASEGURADORAS CON TODAS LAS COBERTURAS EDITABLES -->
			<div class="card">
				<button 
					type="button"
					class="w-full flex items-center justify-between text-left"
					on:click={() => toggleSection('aseguradoras')}
				>
					<h2 class="text-lg font-semibold text-secondary-900">7-11. Aseguradoras y Coberturas (Editables)</h2>
					<svg class="w-5 h-5 transition-transform {expandedSections.aseguradoras ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
					</svg>
				</button>
				{#if expandedSections.aseguradoras}
					<div class="mt-4 space-y-6">
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
										<!-- COBERTURAS DIFERENCIADORAS Y EXTRAS -->
										<div class="bg-white rounded-lg p-4 border border-orange-200">
											<h4 class="font-semibold text-orange-700 mb-3 flex items-center gap-2">
												<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
												Coberturas Diferenciadoras
											</h4>
											<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
												<div>
													<label class="block text-xs text-secondary-500 mb-1">Cobertura Diferenciadora 1</label>
													<input 
														type="text" 
														bind:value={coberturasEditables[i].cobertura_diferenciadora_1} 
														class="input text-sm"
														placeholder="Ej: No aplica demérito por uso"
													/>
												</div>
												<div>
													<label class="block text-xs text-secondary-500 mb-1">Cobertura Diferenciadora 2</label>
													<input 
														type="text" 
														bind:value={coberturasEditables[i].cobertura_diferenciadora_2} 
														class="input text-sm"
														placeholder="Ej: Accidentes personales consejo"
													/>
												</div>
											</div>
										</div>

										<!-- DAÑOS MATERIALES (DM) -->
										<div class="bg-white rounded-lg border border-blue-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-blue-50 flex items-center justify-between hover:bg-blue-100" on:click={() => toggleCoberturaSection(i, 'dm')}>
												<h4 class="font-semibold text-blue-700">Daños Materiales (DM) - 5 coberturas</h4>
												<svg class="w-5 h-5 text-blue-600 transition-transform {expandedCoberturas[i]?.dm ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.dm}
												<div class="p-4 space-y-3">
													{#each [
														{ key: 'dm_terremoto', label: 'Terremoto' },
														{ key: 'dm_inundacion', label: 'Inundación' },
														{ key: 'dm_incendio', label: 'Incendio' },
														{ key: 'dm_amit', label: 'AMIT' },
														{ key: 'dm_tuberia_vidrio', label: 'Tubería/Vidrio' }
													] as cob}
														<div class="grid grid-cols-4 gap-2 items-center p-2 bg-blue-50 rounded">
															<span class="font-medium text-sm text-blue-800">{cob.label}</span>
															<input type="text" bind:value={coberturasEditables[i][cob.key].porcentaje} class="input input-sm" placeholder="%" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].tipo} class="input input-sm" placeholder="Tipo" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].minimo} class="input input-sm" placeholder="Mín SMMLV" />
														</div>
													{/each}
												</div>
											{/if}
										</div>

										<!-- DAÑOS INTERNOS (DI) -->
										<div class="bg-white rounded-lg border border-purple-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-purple-50 flex items-center justify-between hover:bg-purple-100" on:click={() => toggleCoberturaSection(i, 'di')}>
												<h4 class="font-semibold text-purple-700">Daños Internos (DI) - 2 coberturas</h4>
												<svg class="w-5 h-5 text-purple-600 transition-transform {expandedCoberturas[i]?.di ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.di}
												<div class="p-4 space-y-3">
													{#each [
														{ key: 'di_maq_equipo', label: 'Maquinaria y Equipo' },
														{ key: 'di_equipo_electronico', label: 'Equipo Electrónico' }
													] as cob}
														<div class="grid grid-cols-4 gap-2 items-center p-2 bg-purple-50 rounded">
															<span class="font-medium text-sm text-purple-800">{cob.label}</span>
															<input type="text" bind:value={coberturasEditables[i][cob.key].porcentaje} class="input input-sm" placeholder="%" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].tipo} class="input input-sm" placeholder="Tipo" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].minimo} class="input input-sm" placeholder="Mín SMMLV" />
														</div>
													{/each}
												</div>
											{/if}
										</div>

										<!-- SUSTRACCIÓN CON VIOLENCIA (SCV) -->
										<div class="bg-white rounded-lg border border-red-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-red-50 flex items-center justify-between hover:bg-red-100" on:click={() => toggleCoberturaSection(i, 'scv')}>
												<h4 class="font-semibold text-red-700">Sustracción con Violencia (SCV) - 4 coberturas</h4>
												<svg class="w-5 h-5 text-red-600 transition-transform {expandedCoberturas[i]?.scv ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.scv}
												<div class="p-4 space-y-3">
													{#each [
														{ key: 'scv_maq_equipo', label: 'Maquinaria y Equipo' },
														{ key: 'scv_equipo_electronico', label: 'Equipo Electrónico' },
														{ key: 'scv_dineros', label: 'Dineros' },
														{ key: 'scv_muebles', label: 'Muebles' }
													] as cob}
														<div class="grid grid-cols-4 gap-2 items-center p-2 bg-red-50 rounded">
															<span class="font-medium text-sm text-red-800">{cob.label}</span>
															<input type="text" bind:value={coberturasEditables[i][cob.key].porcentaje} class="input input-sm" placeholder="%" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].tipo} class="input input-sm" placeholder="Tipo" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].minimo} class="input input-sm" placeholder="Mín SMMLV" />
														</div>
													{/each}
												</div>
											{/if}
										</div>

										<!-- DIRECTORES & ADMINISTRADORES (DA) -->
										<div class="bg-white rounded-lg border border-amber-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-amber-50 flex items-center justify-between hover:bg-amber-100" on:click={() => toggleCoberturaSection(i, 'da')}>
												<h4 class="font-semibold text-amber-700">Directores & Administradores (DA) - 1 cobertura</h4>
												<svg class="w-5 h-5 text-amber-600 transition-transform {expandedCoberturas[i]?.da ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.da}
												<div class="p-4">
													<div class="grid grid-cols-4 gap-2 items-center p-2 bg-amber-50 rounded">
														<span class="font-medium text-sm text-amber-800">Amparo Básico</span>
														<input type="text" bind:value={coberturasEditables[i].da_amparo_basico.porcentaje} class="input input-sm" placeholder="%" />
														<input type="text" bind:value={coberturasEditables[i].da_amparo_basico.tipo} class="input input-sm" placeholder="Tipo" />
														<input type="text" bind:value={coberturasEditables[i].da_amparo_basico.minimo} class="input input-sm" placeholder="Mín SMMLV" />
													</div>
												</div>
											{/if}
										</div>

										<!-- RCE DEDUCIBLES -->
										<div class="bg-white rounded-lg border border-teal-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-teal-50 flex items-center justify-between hover:bg-teal-100" on:click={() => toggleCoberturaSection(i, 'rce_ded')}>
												<h4 class="font-semibold text-teal-700">RCE Deducibles - 5 coberturas</h4>
												<svg class="w-5 h-5 text-teal-600 transition-transform {expandedCoberturas[i]?.rce_ded ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.rce_ded}
												<div class="p-4 space-y-3">
													{#each [
														{ key: 'rce_ded_contratistas', label: 'Contratistas' },
														{ key: 'rce_ded_cruzada', label: 'Cruzada' },
														{ key: 'rce_ded_patronal', label: 'Patronal' },
														{ key: 'rce_ded_parqueaderos', label: 'Parqueaderos' },
														{ key: 'rce_ded_gastos_medicos', label: 'Gastos Médicos' }
													] as cob}
														<div class="grid grid-cols-4 gap-2 items-center p-2 bg-teal-50 rounded">
															<span class="font-medium text-sm text-teal-800">{cob.label}</span>
															<input type="text" bind:value={coberturasEditables[i][cob.key].porcentaje} class="input input-sm" placeholder="%" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].tipo} class="input input-sm" placeholder="Tipo" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].minimo} class="input input-sm" placeholder="Mín SMMLV" />
														</div>
													{/each}
												</div>
											{/if}
										</div>

										<!-- RCE SUBLÍMITES -->
										<div class="bg-white rounded-lg border border-cyan-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-cyan-50 flex items-center justify-between hover:bg-cyan-100" on:click={() => toggleCoberturaSection(i, 'rce_sub')}>
												<h4 class="font-semibold text-cyan-700">RCE Sublímites - 5 coberturas</h4>
												<svg class="w-5 h-5 text-cyan-600 transition-transform {expandedCoberturas[i]?.rce_sub ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.rce_sub}
												<div class="p-4 space-y-3">
													{#each [
														{ key: 'rce_sub_contratistas', label: 'Contratistas' },
														{ key: 'rce_sub_cruzada', label: 'Cruzada' },
														{ key: 'rce_sub_patronal', label: 'Patronal' },
														{ key: 'rce_sub_parqueaderos', label: 'Parqueaderos' },
														{ key: 'rce_sub_gastos_medicos', label: 'Gastos Médicos' }
													] as cob}
														<div class="grid grid-cols-4 gap-2 items-center p-2 bg-cyan-50 rounded">
															<span class="font-medium text-sm text-cyan-800">{cob.label}</span>
															<input type="text" bind:value={coberturasEditables[i][cob.key].porcentaje} class="input input-sm" placeholder="%" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].tipo} class="input input-sm" placeholder="Tipo" />
															<input type="text" bind:value={coberturasEditables[i][cob.key].minimo} class="input input-sm" placeholder="Mín SMMLV" />
														</div>
													{/each}
												</div>
											{/if}
										</div>

										<!-- MANEJO -->
										<div class="bg-white rounded-lg border border-indigo-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-indigo-50 flex items-center justify-between hover:bg-indigo-100" on:click={() => toggleCoberturaSection(i, 'manejo')}>
												<h4 class="font-semibold text-indigo-700">Manejo - 1 cobertura</h4>
												<svg class="w-5 h-5 text-indigo-600 transition-transform {expandedCoberturas[i]?.manejo ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.manejo}
												<div class="p-4">
													<div class="grid grid-cols-4 gap-2 items-center p-2 bg-indigo-50 rounded">
														<span class="font-medium text-sm text-indigo-800">Amparo Básico</span>
														<input type="text" bind:value={coberturasEditables[i].manejo_amparo_basico.porcentaje} class="input input-sm" placeholder="%" />
														<input type="text" bind:value={coberturasEditables[i].manejo_amparo_basico.tipo} class="input input-sm" placeholder="Tipo" />
														<input type="text" bind:value={coberturasEditables[i].manejo_amparo_basico.minimo} class="input input-sm" placeholder="Mín SMMLV" />
													</div>
												</div>
											{/if}
										</div>

										<!-- TRANSPORTE DE VALORES -->
										<div class="bg-white rounded-lg border border-pink-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-pink-50 flex items-center justify-between hover:bg-pink-100" on:click={() => toggleCoberturaSection(i, 'tv')}>
												<h4 class="font-semibold text-pink-700">Transporte de Valores - 1 cobertura</h4>
												<svg class="w-5 h-5 text-pink-600 transition-transform {expandedCoberturas[i]?.tv ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.tv}
												<div class="p-4">
													<div class="grid grid-cols-4 gap-2 items-center p-2 bg-pink-50 rounded">
														<span class="font-medium text-sm text-pink-800">Amparo Básico</span>
														<input type="text" bind:value={coberturasEditables[i].tv_amparo_basico.porcentaje} class="input input-sm" placeholder="%" />
														<input type="text" bind:value={coberturasEditables[i].tv_amparo_basico.tipo} class="input input-sm" placeholder="Tipo" />
														<input type="text" bind:value={coberturasEditables[i].tv_amparo_basico.minimo} class="input input-sm" placeholder="Mín SMMLV" />
													</div>
												</div>
											{/if}
										</div>

										<!-- ASISTENCIAS -->
										<div class="bg-white rounded-lg border border-green-200 overflow-hidden">
											<button type="button" class="w-full px-4 py-3 bg-green-50 flex items-center justify-between hover:bg-green-100" on:click={() => toggleCoberturaSection(i, 'asist')}>
												<h4 class="font-semibold text-green-700">Asistencias</h4>
												<svg class="w-5 h-5 text-green-600 transition-transform {expandedCoberturas[i]?.asist ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
											</button>
											{#if expandedCoberturas[i]?.asist}
												<div class="p-4 space-y-4">
													<!-- Área Común -->
													<div class="p-3 bg-blue-50 rounded-lg">
														<p class="font-semibold text-blue-800 mb-2">Área Común (Total: {calcularTotalAsistencias(coberturasEditables[i].asist_area_comun)})</p>
														<div class="grid grid-cols-4 gap-2">
															<div>
																<label class="text-xs text-blue-600">Vidriería</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_comun.vidrieria} class="input input-sm w-full" />
															</div>
															<div>
																<label class="text-xs text-blue-600">Plomería</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_comun.plomeria} class="input input-sm w-full" />
															</div>
															<div>
																<label class="text-xs text-blue-600">Cerrajería</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_comun.cerrajeria} class="input input-sm w-full" />
															</div>
															<div>
																<label class="text-xs text-blue-600">Electricista</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_comun.electricista} class="input input-sm w-full" />
															</div>
														</div>
													</div>
													<!-- Área Privada -->
													<div class="p-3 bg-green-50 rounded-lg">
														<p class="font-semibold text-green-800 mb-2">Área Privada (Total: {calcularTotalAsistencias(coberturasEditables[i].asist_area_privada)})</p>
														<div class="grid grid-cols-4 gap-2">
															<div>
																<label class="text-xs text-green-600">Vidriería</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_privada.vidrieria} class="input input-sm w-full" />
															</div>
															<div>
																<label class="text-xs text-green-600">Plomería</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_privada.plomeria} class="input input-sm w-full" />
															</div>
															<div>
																<label class="text-xs text-green-600">Cerrajería</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_privada.cerrajeria} class="input input-sm w-full" />
															</div>
															<div>
																<label class="text-xs text-green-600">Electricista</label>
																<input type="text" bind:value={coberturasEditables[i].asist_area_privada.electricista} class="input input-sm w-full" />
															</div>
														</div>
													</div>
												</div>
											{/if}
										</div>
									</div>
								</div>
							{/if}
						{/each}
					</div>
				{/if}
			</div>

			<!-- Botón final -->
			<div class="flex justify-center pt-4">
				<button
					type="button"
					class="btn btn-primary btn-lg flex items-center gap-3 px-8 py-4 text-lg"
					on:click={generarPropuesta}
					disabled={loading || generating || !poliza}
				>
					{#if generating}
						<svg class="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
						</svg>
						Generando Propuesta...
					{:else}
						<svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
						</svg>
						Generar Propuesta Excel
					{/if}
				</button>
			</div>
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
			<button
				type="button"
				class="btn btn-secondary"
				on:click={() => showSuccessModal = false}
			>
				Cerrar
			</button>
			<button
				type="button"
				class="btn btn-primary"
				on:click={() => goto(`/propuestas/copropiedad/${polizaId}`)}
			>
				Volver a la Propuesta
			</button>
		</div>
	</svelte:fragment>
</Modal>

<style>
	.btn-lg {
		font-size: 1.125rem;
		padding: 1rem 2rem;
	}
	
	.input-sm {
		padding: 0.375rem 0.5rem;
		font-size: 0.875rem;
		border-radius: 0.375rem;
		border: 1px solid #d1d5db;
		width: 100%;
	}
	
	.input-sm:focus {
		outline: none;
		border-color: #3b82f6;
		box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
	}
</style>
