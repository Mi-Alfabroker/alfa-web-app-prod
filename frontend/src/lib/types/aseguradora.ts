import type { BaseEntity } from './index';

/**
 * Aseguradora entity type - matches backend model
 */
export interface Aseguradora extends BaseEntity {
	// Campos base
	nombre: string;
	numeral_asistencia?: string;
	correo_comercial?: string;
	correo_reclamaciones?: string;
	direccion_oficina?: string;
	contacto_asignado?: string;
	ruta_logo?: string;
	ruta_pais_logo?: string;
	respaldo_aseguradora?: string;

	// Copropiedad - Asistencia
	cop_asistencia_area_comun?: string;
	cop_asistencia_area_privada?: string;

	// Copropiedad - Daños Materiales
	cop_dm_deducible_terremoto?: string;
	cop_dm_deducible_inundacion?: string;
	cop_dm_deducible_incendio?: string;
	cop_dm_deducible_amit?: string;
	cop_dm_deducible_tuberia_vidrio?: string;

	// Copropiedad - Daños Internos
	cop_di_deducible_maq_equipo?: string;
	cop_di_deducible_equipo_electronico?: string;

	// Copropiedad - Sustracción con Violencia
	cop_scv_deducible_maq_equipo?: string;
	cop_scv_deducible_equipo_electronico?: string;
	cop_scv_deducible_dineros?: string;
	cop_scv_deducible_muebles?: string;

	// Copropiedad - Directores & Administradores
	cop_da_deducible_amparo_basico?: string;

	// Copropiedad - RCE Deducibles
	cop_rce_deducible_contratistas?: string;
	cop_rce_deducible_cruzada?: string;
	cop_rce_deducible_patronal?: string;
	cop_rce_deducible_parqueaderos?: string;
	cop_rce_deducible_gastos_medicos?: string;

	// Copropiedad - RCE Sublimites
	cop_rce_sublimite_contratistas?: string;
	cop_rce_sublimite_cruzada?: string;
	cop_rce_sublimite_patronal?: string;
	cop_rce_sublimite_parqueaderos?: string;
	cop_rce_sublimite_gastos_medicos?: string;

	// Copropiedad - Manejo
	cop_manejo_deducible_amparo_basico?: string;

	// Copropiedad - Transporte de Valores
	cop_tv_deducible_amparo_basico?: string;

	// Hogar - Deducibles Daños
	hog_deducible_terremoto?: string;
	hog_deducible_amit?: string;
	hog_deducible_demas_eventos?: string;

	// Hogar - Hurto Contenidos Normales
	hog_hurto_cn_terremoto?: string;
	hog_hurto_cn_demas_eventos?: string;
	hog_hurto_cn_hurto?: string;

	// Hogar - Hurto Contenidos Especiales
	hog_hurto_ce_hurto?: string;

	// Hogar - Hurto Equipo Electrónico
	hog_hurto_ee_hurto?: string;

	// Hogar - Valores Asegurados
	hog_valor_asegurado_inmueble?: string;
	hog_valor_asegurado_contenidos_normales?: string;
	hog_valor_asegurado_contenidos_especiales?: string;
	hog_valor_asegurado_equipo_electronico?: string;

	// Hogar - Coberturas Adicionales
	hog_cobertura_adicional_1?: string;
	hog_cobertura_adicional_2?: string;
	hog_cobertura_adicional_3?: string;

	// Vehículos - Valores Asegurados
	veh_valor_asegurado_vehiculo?: string;
	veh_valor_asegurado_accesorios?: string;
	veh_valor_asegurado_rc?: string;

	// Vehículos - Deducibles Pérdida
	veh_deducible_perdida_parcial?: string;
	veh_deducible_perdida_total?: string;
	veh_deducible_terremoto?: string;

	// Vehículos - Deducibles Hurto
	veh_hurto_perdida_parcial?: string;
	veh_hurto_perdida_total?: string;

	// Vehículos - Deducible RC
	veh_deducible_rc?: string;

	// Vehículos - Sublímites RC
	veh_rc_sublimite_bienes_terceros?: string;
	veh_rc_sublimite_amparo_patrimonial?: string;
	veh_rc_sublimite_muerte_lesion_una?: string;
	veh_rc_sublimite_muerte_lesion_dos_mas?: string;

	// Vehículos - Coberturas Adicionales
	veh_cobertura_adicional_1?: string;
	veh_cobertura_adicional_2?: string;
	veh_cobertura_adicional_3?: string;
	veh_cobertura_adicional_4?: string;
	veh_cobertura_adicional_5?: string;
	veh_cobertura_adicional_6?: string;
	veh_cobertura_adicional_7?: string;

	// Otros - Valores Asegurados
	otr_valor_asegurado_inmueble?: string;
	otr_valor_asegurado_contenidos_normales?: string;
	otr_valor_asegurado_contenidos_especiales?: string;
	otr_valor_asegurado_equipo_electronico?: string;

	// Otros - Deducibles Daños
	otr_deducible_terremoto?: string;
	otr_deducible_amit?: string;
	otr_deducible_demas_eventos?: string;

	// Otros - Deducibles Hurto
	otr_hurto_cn_deducible?: string;
	otr_hurto_ce_deducible?: string;
	otr_hurto_ee_deducible?: string;

	// Otros - Coberturas Adicionales
	otr_cobertura_adicional_1?: string;
	otr_cobertura_adicional_2?: string;
	otr_cobertura_adicional_3?: string;
}

/**
 * DTO for creating a new aseguradora
 * All fields optional except nombre
 */
export type CreateAseguradoraDto = Omit<Aseguradora, 'id' | 'created_at' | 'updated_at'>;

/**
 * DTO for updating an aseguradora
 * All fields optional
 */
export type UpdateAseguradoraDto = Partial<CreateAseguradoraDto>;
