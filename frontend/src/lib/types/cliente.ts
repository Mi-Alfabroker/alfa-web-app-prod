import type { BaseEntity } from './index';

/**
 * Tipos de persona disponibles
 */
export type TipoPersona = 'PERSONA' | 'EMPRESA';

/**
 * Tipos de usuario disponibles
 */
export type TipoUsuario = 'CLIENTE' | 'AGENTE' | 'ADMINISTRADOR' | 'SUPERADMIN';

/**
 * Cliente entity type - matches backend Usuario model
 * En el contexto del frontend de clientes, usamos "Cliente" 
 * que se mapea a "Usuario" con tipo_usuario = 'CLIENTE' en el backend
 */
export interface Cliente extends BaseEntity {
	tipo_persona: TipoPersona;
	
	// Campos comunes
	ciudad?: string;
	direccion?: string;
	telefono_movil?: string;
	correo?: string;
	usuario: string;
	tipo_usuario: TipoUsuario;
	
	// Campos para PERSONA natural
	tipo_documento?: string;
	numero_documento?: string;
	nombre?: string;
	edad?: number;
	
	// Campos para EMPRESA
	nit?: string;
	razon_social?: string;
	nombre_rep_legal?: string;
	documento_rep_legal?: string;
	telefono_rep_legal?: string;
	correo_rep_legal?: string;
	contacto_alternativo?: string;
}

/**
 * DTO for creating a new cliente
 */
export interface CreateClienteDto {
	tipo_persona: TipoPersona;
	usuario: string;
	clave: string;
	tipo_usuario?: TipoUsuario; // Default: CLIENTE
	
	// Campos comunes
	ciudad?: string;
	direccion?: string;
	telefono_movil?: string;
	correo?: string;
	
	// Campos para PERSONA
	tipo_documento?: string;
	numero_documento?: string;
	nombre?: string;
	edad?: number;
	
	// Campos para EMPRESA
	nit?: string;
	razon_social?: string;
	nombre_rep_legal?: string;
	documento_rep_legal?: string;
	telefono_rep_legal?: string;
	correo_rep_legal?: string;
	contacto_alternativo?: string;
}

/**
 * DTO for updating a cliente
 */
export type UpdateClienteDto = Partial<Omit<CreateClienteDto, 'clave'>> & {
	clave?: string; // Password is optional on update
};

/**
 * Opciones para tipo de documento
 */
export const TIPOS_DOCUMENTO = [
	{ value: 'CC', label: 'Cédula de Ciudadanía' },
	{ value: 'CE', label: 'Cédula de Extranjería' },
	{ value: 'TI', label: 'Tarjeta de Identidad' },
	{ value: 'PP', label: 'Pasaporte' },
	{ value: 'NIT', label: 'NIT' }
] as const;

/**
 * Opciones para tipo de persona
 */
export const TIPOS_PERSONA = [
	{ value: 'PERSONA', label: 'Persona Natural' },
	{ value: 'EMPRESA', label: 'Empresa' }
] as const;
