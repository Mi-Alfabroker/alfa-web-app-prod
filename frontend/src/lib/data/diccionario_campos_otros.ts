/**
 * DICCIONARIO DE CAMPOS PARA PROPUESTAS DE OTROS SEGUROS
 * 
 * Mapea códigos cortos [N] a nombres descriptivos de variables.
 * Esto permite usar códigos compactos en el Excel mientras se mantiene
 * la referencia a qué representa cada campo.
 * 
 * Estructura:
 * - [1]-[2]: Encabezado general
 * - [3]-[13]: Datos del cliente y bien (11 campos)
 * - [14]-[17]: Avalúos (4 campos)
 * - [18]-[22]: Valores asegurados (5 campos)
 * - [23]-[26]: Infraseguro (4 campos)
 * - [27]-[41]: Aseguradora 1 (15 campos)
 * - [42]-[56]: Aseguradora 2 (15 campos)
 * - [57]-[71]: Aseguradora 3 (15 campos)
 */

export const DICCIONARIO_CAMPOS_OTROS: Record<string, string> = {
	// =========================================================================
	// SECCIÓN 1: ENCABEZADO
	// =========================================================================
	"[1]": "fecha_expedicion",
	"[2]": "año_vigencia",

	// =========================================================================
	// SECCIÓN 2: DATOS DEL CLIENTE / BIEN ASEGURADO
	// =========================================================================
	"[3]": "nombre_cliente",
	"[4]": "nit",
	"[5]": "tipo_seguro",
	"[6]": "bien_asegurado",
	"[7]": "ciudad",
	"[8]": "direccion",
	"[9]": "asesor",
	"[10]": "poliza_actual",
	"[11]": "aseguradora_actual",
	"[12]": "tasa_interes",
	"[13]": "comentarios",

	// =========================================================================
	// SECCIÓN 3: VALORES DEL BIEN (AVALÚO)
	// =========================================================================
	"[14]": "valor_inmueble_avaluo",
	"[15]": "valor_contenidos_normales_avaluo",
	"[16]": "valor_contenidos_especiales_avaluo",
	"[17]": "valor_equipo_electronico_avaluo",

	// =========================================================================
	// SECCIÓN 4: VALORES ASEGURADOS
	// =========================================================================
	"[18]": "valor_inmueble_asegurado",
	"[19]": "valor_contenidos_normales_asegurado",
	"[20]": "valor_contenidos_especiales_asegurado",
	"[21]": "valor_equipo_electronico_asegurado",
	"[22]": "valor_rc_asegurado",

	// =========================================================================
	// SECCIÓN 5: INFRASEGURO
	// =========================================================================
	"[23]": "infraseg_inmueble",
	"[24]": "infraseg_contenidos_normales",
	"[25]": "infraseg_contenidos_especiales",
	"[26]": "infraseg_equipo_electronico",

	// =========================================================================
	// ASEGURADORA 1 - [27] a [41]
	// =========================================================================
	"[27]": "nombre_aseg_1",
	"[28]": "pais_origen_aseg_1",
	"[29]": "respaldo_aseg_1",
	"[30]": "valor_prima_aseg_1",
	"[31]": "valor_total_anual_aseg_1",
	// Deducibles Daños
	"[32]": "otr_deducible_terremoto_aseg_1",
	"[33]": "otr_deducible_amit_aseg_1",
	"[34]": "otr_deducible_demas_eventos_aseg_1",
	// Deducibles Hurto
	"[35]": "otr_hurto_cn_deducible_aseg_1",
	"[36]": "otr_hurto_ce_deducible_aseg_1",
	"[37]": "otr_hurto_ee_deducible_aseg_1",
	// Coberturas Adicionales
	"[38]": "otr_cobertura_adicional_1_aseg_1",
	"[39]": "otr_cobertura_adicional_2_aseg_1",
	"[40]": "otr_cobertura_adicional_3_aseg_1",
	"[41]": "otr_observaciones_aseg_1",

	// =========================================================================
	// ASEGURADORA 2 - [42] a [56]
	// =========================================================================
	"[42]": "nombre_aseg_2",
	"[43]": "pais_origen_aseg_2",
	"[44]": "respaldo_aseg_2",
	"[45]": "valor_prima_aseg_2",
	"[46]": "valor_total_anual_aseg_2",
	// Deducibles Daños
	"[47]": "otr_deducible_terremoto_aseg_2",
	"[48]": "otr_deducible_amit_aseg_2",
	"[49]": "otr_deducible_demas_eventos_aseg_2",
	// Deducibles Hurto
	"[50]": "otr_hurto_cn_deducible_aseg_2",
	"[51]": "otr_hurto_ce_deducible_aseg_2",
	"[52]": "otr_hurto_ee_deducible_aseg_2",
	// Coberturas Adicionales
	"[53]": "otr_cobertura_adicional_1_aseg_2",
	"[54]": "otr_cobertura_adicional_2_aseg_2",
	"[55]": "otr_cobertura_adicional_3_aseg_2",
	"[56]": "otr_observaciones_aseg_2",

	// =========================================================================
	// ASEGURADORA 3 - [57] a [71]
	// =========================================================================
	"[57]": "nombre_aseg_3",
	"[58]": "pais_origen_aseg_3",
	"[59]": "respaldo_aseg_3",
	"[60]": "valor_prima_aseg_3",
	"[61]": "valor_total_anual_aseg_3",
	// Deducibles Daños
	"[62]": "otr_deducible_terremoto_aseg_3",
	"[63]": "otr_deducible_amit_aseg_3",
	"[64]": "otr_deducible_demas_eventos_aseg_3",
	// Deducibles Hurto
	"[65]": "otr_hurto_cn_deducible_aseg_3",
	"[66]": "otr_hurto_ce_deducible_aseg_3",
	"[67]": "otr_hurto_ee_deducible_aseg_3",
	// Coberturas Adicionales
	"[68]": "otr_cobertura_adicional_1_aseg_3",
	"[69]": "otr_cobertura_adicional_2_aseg_3",
	"[70]": "otr_cobertura_adicional_3_aseg_3",
	"[71]": "otr_observaciones_aseg_3",

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
export const DICCIONARIO_INVERSO_OTROS: Record<string, string> = Object.fromEntries(
	Object.entries(DICCIONARIO_CAMPOS_OTROS).map(([k, v]) => [v, k])
);

// Función helper para obtener el offset de índice para cada aseguradora
export function getAseguradoraOffset(asegNum: number): number {
	// Aseg 1: 27, Aseg 2: 42, Aseg 3: 57
	const offsets = [27, 42, 57];
	return offsets[asegNum - 1] || 27;
}
