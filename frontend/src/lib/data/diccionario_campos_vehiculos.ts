/**
 * DICCIONARIO DE CAMPOS PARA PROPUESTAS DE VEHÍCULOS
 * 
 * Mapea códigos cortos [N] a nombres descriptivos de variables.
 * Esto permite usar códigos compactos en el Excel mientras se mantiene
 * la referencia a qué representa cada campo.
 * 
 * Estructura:
 * - [1]-[2]: Encabezado general
 * - [3]-[16]: Datos del cliente y vehículo (14 campos)
 * - [17]-[21]: Avalúos (5 campos, si aplica)
 * - [22]-[25]: Valores asegurados (4 campos)
 * - [26]-[51]: Aseguradora 1 (26 campos incluyendo 4 sublímites RC)
 * - [52]-[77]: Aseguradora 2 (26 campos)
 * - [78]-[103]: Aseguradora 3 (26 campos)
 * - [104]-[129]: Aseguradora 4 (26 campos)
 * - [130]-[155]: Aseguradora 5 (26 campos)
 */

export const DICCIONARIO_CAMPOS_VEHICULOS: Record<string, string> = {
	// =========================================================================
	// SECCIÓN 1: ENCABEZADO
	// =========================================================================
	"[1]": "fecha_expedicion",
	"[2]": "año_vigencia",

	// =========================================================================
	// SECCIÓN 2: DATOS DEL CLIENTE / VEHÍCULO
	// =========================================================================
	"[3]": "nombre_cliente",
	"[4]": "nit",
	"[5]": "tipo_vehiculo",
	"[6]": "marca",
	"[7]": "modelo_ano",
	"[8]": "placa",
	"[9]": "codigo_fasecolda",
	"[10]": "ciudad_circulacion",
	"[11]": "uso_vehiculo",
	"[12]": "asesor",
	"[13]": "poliza_actual",
	"[14]": "aseguradora_actual",
	"[15]": "tasa_interes",
	"[16]": "comentarios",

	// =========================================================================
	// SECCIÓN 3: VALORES DEL BIEN (AVALÚO COMERCIAL)
	// =========================================================================
	"[17]": "valor_comercial_fasecolda",
	"[18]": "valor_accesorios_avaluo",
	"[19]": "valor_rc_avaluo",
	"[20]": "valor_total_avaluo",
	"[21]": "año_modelo",

	// =========================================================================
	// SECCIÓN 4: VALORES ASEGURADOS
	// =========================================================================
	"[22]": "valor_asegurado_vehiculo",
	"[23]": "valor_asegurado_accesorios",
	"[24]": "valor_asegurado_rc",
	"[25]": "valor_total_asegurado",

	// =========================================================================
	// ASEGURADORA 1 - [26] a [51]
	// =========================================================================
	"[26]": "nombre_aseg_1",
	"[27]": "pais_origen_aseg_1",
	"[28]": "respaldo_aseg_1",
	"[29]": "valor_prima_aseg_1",
	"[30]": "valor_total_anual_aseg_1",
	// Deducibles Pérdida
	"[31]": "veh_deducible_perdida_parcial_aseg_1",
	"[32]": "veh_deducible_perdida_total_aseg_1",
	"[33]": "veh_deducible_terremoto_aseg_1",
	// Deducibles Hurto
	"[34]": "veh_hurto_perdida_parcial_aseg_1",
	"[35]": "veh_hurto_perdida_total_aseg_1",
	// Deducible RC
	"[36]": "veh_deducible_rc_aseg_1",
	// Sublímites RC (4 campos)
	"[37]": "veh_rc_sublimite_bienes_terceros_aseg_1",
	"[38]": "veh_rc_sublimite_amparo_patrimonial_aseg_1",
	"[39]": "veh_rc_sublimite_muerte_lesion_una_aseg_1",
	"[40]": "veh_rc_sublimite_muerte_lesion_dos_mas_aseg_1",
	// Coberturas Adicionales (7 checks)
	"[41]": "veh_cobertura_adicional_1_aseg_1",
	"[42]": "veh_cobertura_adicional_2_aseg_1",
	"[43]": "veh_cobertura_adicional_3_aseg_1",
	"[44]": "veh_cobertura_adicional_4_aseg_1",
	"[45]": "veh_cobertura_adicional_5_aseg_1",
	"[46]": "veh_cobertura_adicional_6_aseg_1",
	"[47]": "veh_cobertura_adicional_7_aseg_1",
	"[48]": "veh_observaciones_aseg_1",
	"[49]": "veh_asistencia_tipo_aseg_1",
	"[50]": "veh_conductor_elegido_aseg_1",
	"[51]": "veh_beneficiario_adicional_aseg_1",

	// =========================================================================
	// ASEGURADORA 2 - [52] a [77]
	// =========================================================================
	"[52]": "nombre_aseg_2",
	"[53]": "pais_origen_aseg_2",
	"[54]": "respaldo_aseg_2",
	"[55]": "valor_prima_aseg_2",
	"[56]": "valor_total_anual_aseg_2",
	// Deducibles Pérdida
	"[57]": "veh_deducible_perdida_parcial_aseg_2",
	"[58]": "veh_deducible_perdida_total_aseg_2",
	"[59]": "veh_deducible_terremoto_aseg_2",
	// Deducibles Hurto
	"[60]": "veh_hurto_perdida_parcial_aseg_2",
	"[61]": "veh_hurto_perdida_total_aseg_2",
	// Deducible RC
	"[62]": "veh_deducible_rc_aseg_2",
	// Sublímites RC (4 campos)
	"[63]": "veh_rc_sublimite_bienes_terceros_aseg_2",
	"[64]": "veh_rc_sublimite_amparo_patrimonial_aseg_2",
	"[65]": "veh_rc_sublimite_muerte_lesion_una_aseg_2",
	"[66]": "veh_rc_sublimite_muerte_lesion_dos_mas_aseg_2",
	// Coberturas Adicionales (7 checks)
	"[67]": "veh_cobertura_adicional_1_aseg_2",
	"[68]": "veh_cobertura_adicional_2_aseg_2",
	"[69]": "veh_cobertura_adicional_3_aseg_2",
	"[70]": "veh_cobertura_adicional_4_aseg_2",
	"[71]": "veh_cobertura_adicional_5_aseg_2",
	"[72]": "veh_cobertura_adicional_6_aseg_2",
	"[73]": "veh_cobertura_adicional_7_aseg_2",
	"[74]": "veh_observaciones_aseg_2",
	"[75]": "veh_asistencia_tipo_aseg_2",
	"[76]": "veh_conductor_elegido_aseg_2",
	"[77]": "veh_beneficiario_adicional_aseg_2",

	// =========================================================================
	// ASEGURADORA 3 - [78] a [103]
	// =========================================================================
	"[78]": "nombre_aseg_3",
	"[79]": "pais_origen_aseg_3",
	"[80]": "respaldo_aseg_3",
	"[81]": "valor_prima_aseg_3",
	"[82]": "valor_total_anual_aseg_3",
	// Deducibles Pérdida
	"[83]": "veh_deducible_perdida_parcial_aseg_3",
	"[84]": "veh_deducible_perdida_total_aseg_3",
	"[85]": "veh_deducible_terremoto_aseg_3",
	// Deducibles Hurto
	"[86]": "veh_hurto_perdida_parcial_aseg_3",
	"[87]": "veh_hurto_perdida_total_aseg_3",
	// Deducible RC
	"[88]": "veh_deducible_rc_aseg_3",
	// Sublímites RC (4 campos)
	"[89]": "veh_rc_sublimite_bienes_terceros_aseg_3",
	"[90]": "veh_rc_sublimite_amparo_patrimonial_aseg_3",
	"[91]": "veh_rc_sublimite_muerte_lesion_una_aseg_3",
	"[92]": "veh_rc_sublimite_muerte_lesion_dos_mas_aseg_3",
	// Coberturas Adicionales (7 checks)
	"[93]": "veh_cobertura_adicional_1_aseg_3",
	"[94]": "veh_cobertura_adicional_2_aseg_3",
	"[95]": "veh_cobertura_adicional_3_aseg_3",
	"[96]": "veh_cobertura_adicional_4_aseg_3",
	"[97]": "veh_cobertura_adicional_5_aseg_3",
	"[98]": "veh_cobertura_adicional_6_aseg_3",
	"[99]": "veh_cobertura_adicional_7_aseg_3",
	"[100]": "veh_observaciones_aseg_3",
	"[101]": "veh_asistencia_tipo_aseg_3",
	"[102]": "veh_conductor_elegido_aseg_3",
	"[103]": "veh_beneficiario_adicional_aseg_3",

	// =========================================================================
	// ASEGURADORA 4 - [104] a [129]
	// =========================================================================
	"[104]": "nombre_aseg_4",
	"[105]": "pais_origen_aseg_4",
	"[106]": "respaldo_aseg_4",
	"[107]": "valor_prima_aseg_4",
	"[108]": "valor_total_anual_aseg_4",
	// Deducibles Pérdida
	"[109]": "veh_deducible_perdida_parcial_aseg_4",
	"[110]": "veh_deducible_perdida_total_aseg_4",
	"[111]": "veh_deducible_terremoto_aseg_4",
	// Deducibles Hurto
	"[112]": "veh_hurto_perdida_parcial_aseg_4",
	"[113]": "veh_hurto_perdida_total_aseg_4",
	// Deducible RC
	"[114]": "veh_deducible_rc_aseg_4",
	// Sublímites RC (4 campos)
	"[115]": "veh_rc_sublimite_bienes_terceros_aseg_4",
	"[116]": "veh_rc_sublimite_amparo_patrimonial_aseg_4",
	"[117]": "veh_rc_sublimite_muerte_lesion_una_aseg_4",
	"[118]": "veh_rc_sublimite_muerte_lesion_dos_mas_aseg_4",
	// Coberturas Adicionales (7 checks)
	"[119]": "veh_cobertura_adicional_1_aseg_4",
	"[120]": "veh_cobertura_adicional_2_aseg_4",
	"[121]": "veh_cobertura_adicional_3_aseg_4",
	"[122]": "veh_cobertura_adicional_4_aseg_4",
	"[123]": "veh_cobertura_adicional_5_aseg_4",
	"[124]": "veh_cobertura_adicional_6_aseg_4",
	"[125]": "veh_cobertura_adicional_7_aseg_4",
	"[126]": "veh_observaciones_aseg_4",
	"[127]": "veh_asistencia_tipo_aseg_4",
	"[128]": "veh_conductor_elegido_aseg_4",
	"[129]": "veh_beneficiario_adicional_aseg_4",

	// =========================================================================
	// ASEGURADORA 5 - [130] a [155]
	// =========================================================================
	"[130]": "nombre_aseg_5",
	"[131]": "pais_origen_aseg_5",
	"[132]": "respaldo_aseg_5",
	"[133]": "valor_prima_aseg_5",
	"[134]": "valor_total_anual_aseg_5",
	// Deducibles Pérdida
	"[135]": "veh_deducible_perdida_parcial_aseg_5",
	"[136]": "veh_deducible_perdida_total_aseg_5",
	"[137]": "veh_deducible_terremoto_aseg_5",
	// Deducibles Hurto
	"[138]": "veh_hurto_perdida_parcial_aseg_5",
	"[139]": "veh_hurto_perdida_total_aseg_5",
	// Deducible RC
	"[140]": "veh_deducible_rc_aseg_5",
	// Sublímites RC (4 campos)
	"[141]": "veh_rc_sublimite_bienes_terceros_aseg_5",
	"[142]": "veh_rc_sublimite_amparo_patrimonial_aseg_5",
	"[143]": "veh_rc_sublimite_muerte_lesion_una_aseg_5",
	"[144]": "veh_rc_sublimite_muerte_lesion_dos_mas_aseg_5",
	// Coberturas Adicionales (7 checks)
	"[145]": "veh_cobertura_adicional_1_aseg_5",
	"[146]": "veh_cobertura_adicional_2_aseg_5",
	"[147]": "veh_cobertura_adicional_3_aseg_5",
	"[148]": "veh_cobertura_adicional_4_aseg_5",
	"[149]": "veh_cobertura_adicional_5_aseg_5",
	"[150]": "veh_cobertura_adicional_6_aseg_5",
	"[151]": "veh_cobertura_adicional_7_aseg_5",
	"[152]": "veh_observaciones_aseg_5",
	"[153]": "veh_asistencia_tipo_aseg_5",
	"[154]": "veh_conductor_elegido_aseg_5",
	"[155]": "veh_beneficiario_adicional_aseg_5",

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
export const DICCIONARIO_INVERSO_VEHICULOS: Record<string, string> = Object.fromEntries(
	Object.entries(DICCIONARIO_CAMPOS_VEHICULOS).map(([k, v]) => [v, k])
);

// Función helper para obtener el offset de índice para cada aseguradora
export function getAseguradoraOffset(asegNum: number): number {
	// Aseg 1: 26, Aseg 2: 52, Aseg 3: 78, Aseg 4: 104, Aseg 5: 130
	const offsets = [26, 52, 78, 104, 130];
	return offsets[asegNum - 1] || 26;
}
