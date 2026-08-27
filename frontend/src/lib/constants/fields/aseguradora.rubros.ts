/**
 * Aseguradora conditions grouped by rubro and section.
 *
 * The per-rubro condition columns (`cop_*`, `hog_*`, `veh_*`, `otr_*`) were
 * previously laid out by hand inside the two aseguradora form pages, with the
 * hogar / vehículo / otros labels written inline. That meant the create form
 * and the edit form could disagree about which fields exist. This module is the
 * single description of that structure; both forms and the read-only ficha
 * render from it.
 *
 * Copropiedad labels come from `AseguradoraFields`, which already declares
 * them; the other three rubros are declared here.
 */

import { AseguradoraFields } from './aseguradora.fields';

export interface RubroSection {
	title: string;
	fields: { key: string; label: string }[];
}

export interface RubroConfig {
	/** Tab id, matching the column prefix without the underscore. */
	id: 'cop' | 'hog' | 'veh' | 'otr';
	label: string;
	sections: RubroSection[];
}

/** Label for a copropiedad column, read from the shared field definitions. */
function cop(key: keyof typeof AseguradoraFields): { key: string; label: string } {
	const def = AseguradoraFields[key];
	return { key: def.db, label: def.label };
}

export const ASEGURADORA_RUBROS: RubroConfig[] = [
	{
		id: 'cop',
		label: 'Copropiedades',
		sections: [
			{
				title: 'Asistencia',
				fields: [cop('cop_asistencia_area_comun'), cop('cop_asistencia_area_privada')]
			},
			{
				title: 'Daños materiales',
				fields: [
					cop('cop_dm_deducible_terremoto'),
					cop('cop_dm_deducible_inundacion'),
					cop('cop_dm_deducible_incendio'),
					cop('cop_dm_deducible_amit'),
					cop('cop_dm_deducible_tuberia_vidrio')
				]
			},
			{
				title: 'Daños internos',
				fields: [
					cop('cop_di_deducible_maq_equipo'),
					cop('cop_di_deducible_equipo_electronico')
				]
			},
			{
				title: 'Sustracción con violencia',
				fields: [
					cop('cop_scv_deducible_maq_equipo'),
					cop('cop_scv_deducible_equipo_electronico'),
					cop('cop_scv_deducible_dineros'),
					cop('cop_scv_deducible_muebles')
				]
			},
			{
				title: 'Directores y administradores',
				fields: [cop('cop_da_deducible_amparo_basico')]
			},
			{
				title: 'RCE · deducibles',
				fields: [
					cop('cop_rce_deducible_contratistas'),
					cop('cop_rce_deducible_cruzada'),
					cop('cop_rce_deducible_patronal'),
					cop('cop_rce_deducible_parqueaderos'),
					cop('cop_rce_deducible_gastos_medicos')
				]
			},
			{
				title: 'RCE · sublímites',
				fields: [
					cop('cop_rce_sublimite_contratistas'),
					cop('cop_rce_sublimite_cruzada'),
					cop('cop_rce_sublimite_patronal'),
					cop('cop_rce_sublimite_parqueaderos'),
					cop('cop_rce_sublimite_gastos_medicos')
				]
			},
			{ title: 'Manejo', fields: [cop('cop_manejo_deducible_amparo_basico')] },
			{ title: 'Transporte de valores', fields: [cop('cop_tv_deducible_amparo_basico')] }
		]
	},
	{
		id: 'hog',
		label: 'Hogar',
		sections: [
			{
				title: 'Deducibles daños',
				fields: [
					{ key: 'hog_deducible_terremoto', label: 'Deducible terremoto' },
					{ key: 'hog_deducible_amit', label: 'Deducible AMIT' },
					{ key: 'hog_deducible_demas_eventos', label: 'Deducible demás eventos' }
				]
			},
			{
				title: 'Hurto contenidos normales',
				fields: [
					{ key: 'hog_hurto_cn_terremoto', label: 'Terremoto' },
					{ key: 'hog_hurto_cn_demas_eventos', label: 'Demás eventos' },
					{ key: 'hog_hurto_cn_hurto', label: 'Hurto' }
				]
			},
			{
				title: 'Hurto contenidos especiales',
				fields: [{ key: 'hog_hurto_ce_hurto', label: 'Hurto' }]
			},
			{
				title: 'Hurto equipo electrónico',
				fields: [{ key: 'hog_hurto_ee_hurto', label: 'Hurto' }]
			},
			{
				title: 'Coberturas adicionales',
				fields: [
					{ key: 'hog_cobertura_adicional_1', label: 'Cobertura adicional 1' },
					{ key: 'hog_cobertura_adicional_2', label: 'Cobertura adicional 2' },
					{ key: 'hog_cobertura_adicional_3', label: 'Cobertura adicional 3' }
				]
			}
		]
	},
	{
		id: 'veh',
		label: 'Vehículos',
		sections: [
			{
				title: 'Deducibles pérdida',
				fields: [
					{ key: 'veh_deducible_perdida_parcial', label: 'Pérdida parcial' },
					{ key: 'veh_deducible_perdida_total', label: 'Pérdida total' },
					{ key: 'veh_deducible_terremoto', label: 'Terremoto' }
				]
			},
			{
				title: 'Deducibles hurto',
				fields: [
					{ key: 'veh_hurto_perdida_parcial', label: 'Hurto pérdida parcial' },
					{ key: 'veh_hurto_perdida_total', label: 'Hurto pérdida total' }
				]
			},
			{
				title: 'Responsabilidad civil',
				fields: [{ key: 'veh_deducible_rc', label: 'Deducible RC' }]
			},
			{
				title: 'RC · sublímites',
				fields: [
					{ key: 'veh_rc_sublimite_bienes_terceros', label: 'Bienes a terceros' },
					{ key: 'veh_rc_sublimite_amparo_patrimonial', label: 'Amparo patrimonial' },
					{ key: 'veh_rc_sublimite_muerte_lesion_una', label: 'Muerte o lesión (1 persona)' },
					{
						key: 'veh_rc_sublimite_muerte_lesion_dos_mas',
						label: 'Muerte o lesión (2+ personas)'
					}
				]
			},
			{
				title: 'Coberturas adicionales',
				fields: [
					{ key: 'veh_cobertura_adicional_1', label: 'Adicional 1 · RC voluntaria' },
					{ key: 'veh_cobertura_adicional_2', label: 'Adicional 2 · Daños a ocupantes' },
					{ key: 'veh_cobertura_adicional_3', label: 'Adicional 3 · Asistencia en viaje' },
					{ key: 'veh_cobertura_adicional_4', label: 'Adicional 4 · Vehículo de reemplazo' },
					{ key: 'veh_cobertura_adicional_5', label: 'Adicional 5 · Exención de deducible' },
					{ key: 'veh_cobertura_adicional_6', label: 'Adicional 6 · Accidentes del conductor' },
					{ key: 'veh_cobertura_adicional_7', label: 'Adicional 7 · Eventos de la naturaleza' }
				]
			}
		]
	},
	{
		id: 'otr',
		label: 'Otros ramos',
		sections: [
			{
				title: 'Deducibles daños',
				fields: [
					{ key: 'otr_deducible_terremoto', label: 'Deducible terremoto' },
					{ key: 'otr_deducible_amit', label: 'Deducible AMIT' },
					{ key: 'otr_deducible_demas_eventos', label: 'Deducible demás eventos' }
				]
			},
			{
				title: 'Deducibles hurto',
				fields: [
					{ key: 'otr_hurto_cn_deducible', label: 'Contenidos normales' },
					{ key: 'otr_hurto_ce_deducible', label: 'Contenidos especiales' },
					{ key: 'otr_hurto_ee_deducible', label: 'Equipo electrónico' }
				]
			},
			{
				title: 'Coberturas adicionales',
				fields: [
					{ key: 'otr_cobertura_adicional_1', label: 'Cobertura adicional 1' },
					{ key: 'otr_cobertura_adicional_2', label: 'Cobertura adicional 2' },
					{ key: 'otr_cobertura_adicional_3', label: 'Cobertura adicional 3' }
				]
			}
		]
	}
];

/** Every condition column, flattened. */
export const ASEGURADORA_RUBRO_FIELDS = ASEGURADORA_RUBROS.flatMap((r) =>
	r.sections.flatMap((s) => s.fields.map((f) => ({ ...f, rubro: r.id, section: s.title })))
);

export function rubroConfig(id: string): RubroConfig | undefined {
	return ASEGURADORA_RUBROS.find((r) => r.id === id);
}

/** The aseguradora's own identity and contact columns. */
export const ASEGURADORA_GENERALES: { key: string; label: string; placeholder?: string }[] = [
	{ key: 'nombre', label: 'Nombre', placeholder: 'Razón social de la aseguradora' },
	{ key: 'numeral_asistencia', label: 'Numeral de asistencia', placeholder: '#322 · 018000…' },
	{ key: 'correo_comercial', label: 'Correo comercial', placeholder: 'comercial@aseguradora.co' },
	{
		key: 'correo_reclamaciones',
		label: 'Correo de reclamaciones',
		placeholder: 'siniestros@aseguradora.co'
	},
	{ key: 'direccion_oficina', label: 'Dirección de oficina', placeholder: 'Ciudad · dirección' },
	{ key: 'contacto_asignado', label: 'Contacto asignado', placeholder: 'Nombre · teléfono' },
	{
		key: 'respaldo_aseguradora',
		label: 'Respaldo internacional',
		placeholder: 'Reasegurador o grupo'
	}
];
