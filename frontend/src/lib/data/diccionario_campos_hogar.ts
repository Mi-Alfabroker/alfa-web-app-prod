/**
 * DICCIONARIO DE CAMPOS PARA PROPUESTAS DE HOGAR
 * 
 * Mapea códigos cortos [N] a nombres descriptivos de variables.
 * Esto permite usar códigos compactos en el Excel mientras se mantiene
 * la referencia a qué representa cada campo.
 * 
 * Estructura:
 * - [1]-[2]: Encabez ado general
 * - [3]-[14]: Datos del cliente y generales (12 campos)
 * - [15]-[19]: Avalúos (5 campos)
 * - [20]-[25]: Valores asegurados (6 campos)
 * - [26]-[30]: Infraseguro (5 campos)
 * - [31]-[47]: Aseguradora 1 (17 campos)
 * - [48]-[64]: Aseguradora 2 (17 campos)
 * - [65]-[81]: Aseguradora 3 (17 campos)
 * - [82]-[98]: Aseguradora 4 (17 campos)
 * - [99]-[115]: Aseguradora 5 (17 campos)
 */

export const DICCIONARIO_CAMPOS_HOGAR: Record<string, string> = {
	// =========================================================================
	// SECCIÓN 1: ENCABEZADO
	// =========================================================================
	"[1]": "fecha_expedicion",
	"[2]": "año_vigencia",

	// =========================================================================
	// SECCIÓN 2: DATOS DEL CLIENTE / INMUEBLE
	// =========================================================================
	"[3]": "nombre_cliente",
	"[4]": "nit",
	"[5]": "tipo_inmueble",
	"[6]": "ciudad_inmueble",
	"[7]": "direccion_inmueble",
	"[8]": "numero_pisos",
	"[9]": "ano_construccion",
	"[10]": "asesor",
	"[11]": "poliza_actual",
	"[12]": "aseguradora_actual",
	"[13]": "tasa_interes",
	"[14]": "comentarios",

	// =========================================================================
	// SECCIÓN 3: VALORES DEL BIEN (AVALÚO)
	// =========================================================================
	"[15]": "valor_inmueble_avaluo",
	"[16]": "valor_contenidos_normales_avaluo",
	"[17]": "valor_contenidos_especiales_avaluo",
	"[18]": "valor_equipo_electronico_avaluo",
	"[19]": "valor_maquinaria_equipo_avaluo",

	// =========================================================================
	// SECCIÓN 4: VALORES ASEGURADOS
	// =========================================================================
	"[20]": "valor_inmueble_asegurado",
	"[21]": "valor_contenidos_normales_asegurado",
	"[22]": "valor_contenidos_especiales_asegurado",
	"[23]": "valor_equipo_electronico_asegurado",
	"[24]": "valor_maquinaria_equipo_asegurado",
	"[25]": "valor_rc_asegurado",

	// =========================================================================
	// SECCIÓN 5: INFRASEGURO
	// =========================================================================
	"[26]": "infraseg_inmueble",
	"[27]": "infraseg_contenidos_normales",
	"[28]": "infraseg_contenidos_especiales",
	"[29]": "infraseg_equipo_electronico",
	"[30]": "infraseg_maquinaria",

	// =========================================================================
	// ASEGURADORA 1 - [31] a [47]
	// =========================================================================
	"[31]": "nombre_aseg_1",
	"[32]": "pais_origen_aseg_1",
	"[33]": "respaldo_aseg_1",
	"[34]": "valor_prima_aseg_1",
	"[35]": "valor_total_anual_aseg_1",
	// Deducibles Daños
	"[36]": "hog_deducible_terremoto_aseg_1",
	"[37]": "hog_deducible_amit_aseg_1",
	"[38]": "hog_deducible_demas_eventos_aseg_1",
	// Deducibles Hurto Contenidos Normales
	"[39]": "hog_hurto_cn_terremoto_aseg_1",
	"[40]": "hog_hurto_cn_demas_eventos_aseg_1",
	"[41]": "hog_hurto_cn_hurto_aseg_1",
	// Deducibles Hurto Contenidos Especiales
	"[42]": "hog_hurto_ce_hurto_aseg_1",
	// Deducibles Hurto Equipo Electrónico
	"[43]": "hog_hurto_ee_hurto_aseg_1",
	// Coberturas Adicionales
	"[44]": "hog_cobertura_adicional_1_aseg_1",
	"[45]": "hog_cobertura_adicional_2_aseg_1",
	"[46]": "hog_cobertura_adicional_3_aseg_1",
	"[47]": "hog_observaciones_aseg_1",

	// =========================================================================
	// ASEGURADORA 2 - [48] a [64]
	// =========================================================================
	"[48]": "nombre_aseg_2",
	"[49]": "pais_origen_aseg_2",
	"[50]": "respaldo_aseg_2",
	"[51]": "valor_prima_aseg_2",
	"[52]": "valor_total_anual_aseg_2",
	// Deducibles Daños
	"[53]": "hog_deducible_terremoto_aseg_2",
	"[54]": "hog_deducible_amit_aseg_2",
	"[55]": "hog_deducible_demas_eventos_aseg_2",
	// Deducibles Hurto Contenidos Normales
	"[56]": "hog_hurto_cn_terremoto_aseg_2",
	"[57]": "hog_hurto_cn_demas_eventos_aseg_2",
	"[58]": "hog_hurto_cn_hurto_aseg_2",
	// Deducibles Hurto Contenidos Especiales
	"[59]": "hog_hurto_ce_hurto_aseg_2",
	// Deducibles Hurto Equipo Electrónico
	"[60]": "hog_hurto_ee_hurto_aseg_2",
	// Coberturas Adicionales
	"[61]": "hog_cobertura_adicional_1_aseg_2",
	"[62]": "hog_cobertura_adicional_2_aseg_2",
	"[63]": "hog_cobertura_adicional_3_aseg_2",
	"[64]": "hog_observaciones_aseg_2",

	// =========================================================================
	// ASEGURADORA 3 - [65] a [81]
	// =========================================================================
	"[65]": "nombre_aseg_3",
	"[66]": "pais_origen_aseg_3",
	"[67]": "respaldo_aseg_3",
	"[68]": "valor_prima_aseg_3",
	"[69]": "valor_total_anual_aseg_3",
	// Deducibles Daños
	"[70]": "hog_deducible_terremoto_aseg_3",
	"[71]": "hog_deducible_amit_aseg_3",
	"[72]": "hog_deducible_demas_eventos_aseg_3",
	// Deducibles Hurto Contenidos Normales
	"[73]": "hog_hurto_cn_terremoto_aseg_3",
	"[74]": "hog_hurto_cn_demas_eventos_aseg_3",
	"[75]": "hog_hurto_cn_hurto_aseg_3",
	// Deducibles Hurto Contenidos Especiales
	"[76]": "hog_hurto_ce_hurto_aseg_3",
	// Deducibles Hurto Equipo Electrónico
	"[77]": "hog_hurto_ee_hurto_aseg_3",
	// Coberturas Adicionales
	"[78]": "hog_cobertura_adicional_1_aseg_3",
	"[79]": "hog_cobertura_adicional_2_aseg_3",
	"[80]": "hog_cobertura_adicional_3_aseg_3",
	"[81]": "hog_observaciones_aseg_3",

	// =========================================================================
	// ASEGURADORA 4 - [82] a [98]
	// =========================================================================
	"[82]": "nombre_aseg_4",
	"[83]": "pais_origen_aseg_4",
	"[84]": "respaldo_aseg_4",
	"[85]": "valor_prima_aseg_4",
	"[86]": "valor_total_anual_aseg_4",
	// Deducibles Daños
	"[87]": "hog_deducible_terremoto_aseg_4",
	"[88]": "hog_deducible_amit_aseg_4",
	"[89]": "hog_deducible_demas_eventos_aseg_4",
	// Deducibles Hurto Contenidos Normales
	"[90]": "hog_hurto_cn_terremoto_aseg_4",
	"[91]": "hog_hurto_cn_demas_eventos_aseg_4",
	"[92]": "hog_hurto_cn_hurto_aseg_4",
	// Deducibles Hurto Contenidos Especiales
	"[93]": "hog_hurto_ce_hurto_aseg_4",
	// Deducibles Hurto Equipo Electrónico
	"[94]": "hog_hurto_ee_hurto_aseg_4",
	// Coberturas Adicionales
	"[95]": "hog_cobertura_adicional_1_aseg_4",
	"[96]": "hog_cobertura_adicional_2_aseg_4",
	"[97]": "hog_cobertura_adicional_3_aseg_4",
	"[98]": "hog_observaciones_aseg_4",

	// =========================================================================
	// ASEGURADORA 5 - [99] a [115]
	// =========================================================================
	"[99]": "nombre_aseg_5",
	"[100]": "pais_origen_aseg_5",
	"[101]": "respaldo_aseg_5",
	"[102]": "valor_prima_aseg_5",
	"[103]": "valor_total_anual_aseg_5",
	// Deducibles Daños
	"[104]": "hog_deducible_terremoto_aseg_5",
	"[105]": "hog_deducible_amit_aseg_5",
	"[106]": "hog_deducible_demas_eventos_aseg_5",
	// Deducibles Hurto Contenidos Normales
	"[107]": "hog_hurto_cn_terremoto_aseg_5",
	"[108]": "hog_hurto_cn_demas_eventos_aseg_5",
	"[109]": "hog_hurto_cn_hurto_aseg_5",
	// Deducibles Hurto Contenidos Especiales
	"[110]": "hog_hurto_ce_hurto_aseg_5",
	// Deducibles Hurto Equipo Electrónico
	"[111]": "hog_hurto_ee_hurto_aseg_5",
	// Coberturas Adicionales
	"[112]": "hog_cobertura_adicional_1_aseg_5",
	"[113]": "hog_cobertura_adicional_2_aseg_5",
	"[114]": "hog_cobertura_adicional_3_aseg_5",
	"[115]": "hog_observaciones_aseg_5",

	// =========================================================================
	// ENTREGA [517]-[528]
	// =========================================================================
	"[517]": "nombre_aseguradora",
	"[518]": "numero_poliza",
	"[519]": "fecha_inicio_vigencia",
	"[520]": "fecha_fin_vigencia",
	"[521]": "valor_total_prima",
	"[522]": "medio_pago",
	"[523]": "numeral_asistencia",
	"[524]": "financiacion_num_cuotas",
	"[525]": "financiacion_valor_cuota",
	"[526]": "financiacion_fecha_primera",
	"[527]": "financiacion_periodicidad",
	"[528]": "financiacion_cuota_actual"
};

// Diccionario inverso: nombre descriptivo -> código
export const DICCIONARIO_INVERSO_HOGAR: Record<string, string> = Object.fromEntries(
	Object.entries(DICCIONARIO_CAMPOS_HOGAR).map(([k, v]) => [v, k])
);

// Función helper para obtener el offset de índice para cada aseguradora
export function getAseguradoraOffset(asegNum: number): number {
	// Aseg 1: 31, Aseg 2: 48, Aseg 3: 65, Aseg 4: 82, Aseg 5: 99
	const offsets = [31, 48, 65, 82, 99];
	return offsets[asegNum - 1] || 31;
}
