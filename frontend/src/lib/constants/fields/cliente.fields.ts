/**
 * Cliente Field Definitions
 * Mapeo entre campos de BD/backend y labels de UI
 */

export type FieldDef = {
	db: string;     // Nombre en BD (lo que envía/recibe el backend)
	label: string;  // Label para UI (tablas, formularios)
};

// =============================================================================
// CAMPOS DE CLIENTE
// =============================================================================
export const ClienteFields = {
	// =========================================================================
	// IDENTIFICACIÓN
	// =========================================================================
	id: { db: 'id', label: 'ID' },
	tipo_persona: { db: 'tipo_persona', label: 'Tipo de Persona' },
	tipo_usuario: { db: 'tipo_usuario', label: 'Tipo de Usuario' },

	// =========================================================================
	// CAMPOS COMUNES Y LOGIN
	// =========================================================================
	usuario: { db: 'usuario', label: 'Usuario' },
	clave: { db: 'clave', label: 'Contraseña' },
	correo: { db: 'correo', label: 'Correo Electrónico' },
	telefono_movil: { db: 'telefono_movil', label: 'Teléfono Móvil' },
	ciudad: { db: 'ciudad', label: 'Ciudad' },
	direccion: { db: 'direccion', label: 'Dirección' },

	// =========================================================================
	// CAMPOS PERSONA NATURAL
	// =========================================================================
	nombre: { db: 'nombre', label: 'Nombre Completo' },
	tipo_documento: { db: 'tipo_documento', label: 'Tipo de Documento' },
	numero_documento: { db: 'numero_documento', label: 'Número de Documento' },
	edad: { db: 'edad', label: 'Edad' },

	// =========================================================================
	// CAMPOS EMPRESA
	// =========================================================================
	nit: { db: 'nit', label: 'NIT' },
	razon_social: { db: 'razon_social', label: 'Razón Social' },
	nombre_rep_legal: { db: 'nombre_rep_legal', label: 'Nombre Rep. Legal' },
	documento_rep_legal: { db: 'documento_rep_legal', label: 'Documento Rep. Legal' },
	telefono_rep_legal: { db: 'telefono_rep_legal', label: 'Teléfono Rep. Legal' },
	correo_rep_legal: { db: 'correo_rep_legal', label: 'Correo Rep. Legal' },
	contacto_alternativo: { db: 'contacto_alternativo', label: 'Contacto Alternativo' },

	// =========================================================================
	// TIMESTAMPS
	// =========================================================================
	created_at: { db: 'created_at', label: 'Fecha Creación' },
	updated_at: { db: 'updated_at', label: 'Última Actualización' },
} as const;

// Tipo inferido del objeto
export type ClienteFieldKey = keyof typeof ClienteFields;

// Helper: obtener el nombre de BD de un campo
export function getClienteDbField(key: ClienteFieldKey): string {
	return ClienteFields[key].db;
}

// Helper: obtener el label de un campo
export function getClienteLabel(key: ClienteFieldKey): string {
	return ClienteFields[key].label;
}
