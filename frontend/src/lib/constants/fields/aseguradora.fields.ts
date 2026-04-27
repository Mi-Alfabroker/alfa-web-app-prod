/**
 * Aseguradora Field Definitions
 * Mapeo entre campos de BD/backend y labels de UI
 * 
 * Uso:
 *   import { AseguradoraFields } from '$lib/constants/fields';
 *   
 *   // En columnas de tabla
 *   { key: AseguradoraFields.nombre.db, label: AseguradoraFields.nombre.label }
 *   
 *   // En formularios
 *   <FormField label={AseguradoraFields.correo_comercial.label}>
 */

export type FieldDef = {
	db: string;     // Nombre en BD (lo que envía/recibe el backend)
	label: string;  // Label para UI (tablas, formularios)
};

// =============================================================================
// CAMPOS DE ASEGURADORA
// =============================================================================
export const AseguradoraFields = {
	// =========================================================================
	// CAMPOS BASE
	// =========================================================================
	id: { db: 'id', label: 'ID' },
	nombre: { db: 'nombre', label: 'Nombre' },
	numeral_asistencia: { db: 'numeral_asistencia', label: 'Numeral Asistencia' },
	correo_comercial: { db: 'correo_comercial', label: 'Correo Comercial' },
	correo_reclamaciones: { db: 'correo_reclamaciones', label: 'Correo Reclamaciones' },
	direccion_oficina: { db: 'direccion_oficina', label: 'Dirección Oficina' },
	contacto_asignado: { db: 'contacto_asignado', label: 'Contacto Asignado' },
	ruta_logo: { db: 'ruta_logo', label: 'Logo' },
	ruta_pais_logo: { db: 'ruta_pais_logo', label: 'Bandera País' },
	respaldo_aseguradora: { db: 'respaldo_aseguradora', label: 'Respaldo Aseguradora' },
	created_at: { db: 'created_at', label: 'Fecha Creación' },
	updated_at: { db: 'updated_at', label: 'Última Actualización' },

	// =========================================================================
	// COPROPIEDAD - ASISTENCIA
	// =========================================================================
	cop_asistencia_area_comun: { db: 'cop_asistencia_area_comun', label: 'Asistencia Área Común' },
	cop_asistencia_area_privada: { db: 'cop_asistencia_area_privada', label: 'Asistencia Área Privada' },

	// =========================================================================
	// COPROPIEDAD - DAÑOS MATERIALES
	// =========================================================================
	cop_dm_deducible_terremoto: { db: 'cop_dm_deducible_terremoto', label: 'Deducible Terremoto' },
	cop_dm_deducible_inundacion: { db: 'cop_dm_deducible_inundacion', label: 'Deducible Inundación' },
	cop_dm_deducible_incendio: { db: 'cop_dm_deducible_incendio', label: 'Deducible Incendio' },
	cop_dm_deducible_amit: { db: 'cop_dm_deducible_amit', label: 'Deducible AMIT' },
	cop_dm_deducible_tuberia_vidrio: { db: 'cop_dm_deducible_tuberia_vidrio', label: 'Deducible Tubería/Vidrio' },

	// =========================================================================
	// COPROPIEDAD - DAÑOS INTERNOS
	// =========================================================================
	cop_di_deducible_maq_equipo: { db: 'cop_di_deducible_maq_equipo', label: 'Deducible Maq. y Equipo' },
	cop_di_deducible_equipo_electronico: { db: 'cop_di_deducible_equipo_electronico', label: 'Deducible Equipo Electrónico' },

	// =========================================================================
	// COPROPIEDAD - SUSTRACCIÓN CON VIOLENCIA
	// =========================================================================
	cop_scv_deducible_maq_equipo: { db: 'cop_scv_deducible_maq_equipo', label: 'Deducible Maq. y Equipo (SCV)' },
	cop_scv_deducible_equipo_electronico: { db: 'cop_scv_deducible_equipo_electronico', label: 'Deducible Equipo Electrónico (SCV)' },
	cop_scv_deducible_dineros: { db: 'cop_scv_deducible_dineros', label: 'Deducible Dineros' },
	cop_scv_deducible_muebles: { db: 'cop_scv_deducible_muebles', label: 'Deducible Muebles' },

	// =========================================================================
	// COPROPIEDAD - DIRECTORES & ADMINISTRADORES
	// =========================================================================
	cop_da_deducible_amparo_basico: { db: 'cop_da_deducible_amparo_basico', label: 'Deducible Amparo Básico (D&A)' },

	// =========================================================================
	// COPROPIEDAD - RCE DEDUCIBLES
	// =========================================================================
	cop_rce_deducible_contratistas: { db: 'cop_rce_deducible_contratistas', label: 'Deducible Contratistas' },
	cop_rce_deducible_cruzada: { db: 'cop_rce_deducible_cruzada', label: 'Deducible RC Cruzada' },
	cop_rce_deducible_patronal: { db: 'cop_rce_deducible_patronal', label: 'Deducible Patronal' },
	cop_rce_deducible_parqueaderos: { db: 'cop_rce_deducible_parqueaderos', label: 'Deducible Parqueaderos' },
	cop_rce_deducible_gastos_medicos: { db: 'cop_rce_deducible_gastos_medicos', label: 'Deducible Gastos Médicos' },

	// =========================================================================
	// COPROPIEDAD - RCE SUBLIMITES
	// =========================================================================
	cop_rce_sublimite_contratistas: { db: 'cop_rce_sublimite_contratistas', label: 'Sublímite Contratistas' },
	cop_rce_sublimite_cruzada: { db: 'cop_rce_sublimite_cruzada', label: 'Sublímite RC Cruzada' },
	cop_rce_sublimite_patronal: { db: 'cop_rce_sublimite_patronal', label: 'Sublímite Patronal' },
	cop_rce_sublimite_parqueaderos: { db: 'cop_rce_sublimite_parqueaderos', label: 'Sublímite Parqueaderos' },
	cop_rce_sublimite_gastos_medicos: { db: 'cop_rce_sublimite_gastos_medicos', label: 'Sublímite Gastos Médicos' },

	// =========================================================================
	// COPROPIEDAD - MANEJO
	// =========================================================================
	cop_manejo_deducible_amparo_basico: { db: 'cop_manejo_deducible_amparo_basico', label: 'Deducible Amparo Básico (Manejo)' },

	// =========================================================================
	// COPROPIEDAD - TRANSPORTE DE VALORES
	// =========================================================================
	cop_tv_deducible_amparo_basico: { db: 'cop_tv_deducible_amparo_basico', label: 'Deducible Amparo Básico (TV)' },
} as const;

// Tipo inferido del objeto
export type AseguradoraFieldKey = keyof typeof AseguradoraFields;

// Helper: obtener el nombre de BD de un campo
export function getDbField(key: AseguradoraFieldKey): string {
	return AseguradoraFields[key].db;
}

// Helper: obtener el label de un campo
export function getLabel(key: AseguradoraFieldKey): string {
	return AseguradoraFields[key].label;
}
