-- Alfa-Broker Database Initialization Script
-- This script runs automatically when the PostgreSQL container starts
-- Database: alfabroker | User: admin | Password: admin

-- Create extension for UUID generation (optional, if needed in future)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================================
-- ASEGURADORAS (Insurance Providers) Table
-- =============================================================================
CREATE TABLE IF NOT EXISTS aseguradoras (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    numeral_asistencia VARCHAR(50),
    correo_comercial VARCHAR(255),
    correo_reclamaciones VARCHAR(255),
    direccion_oficina TEXT,
    contacto_asignado VARCHAR(255),
    ruta_logo VARCHAR(500),
    ruta_pais_logo VARCHAR(500),
    respaldo_aseguradora TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- =========================================================================
    -- CAMPOS PARA COPROPIEDAD
    -- =========================================================================
    
    -- Asistencia - Copropiedad
    cop_asistencia_area_comun VARCHAR(255),
    cop_asistencia_area_privada VARCHAR(255),
    
    -- Cobertura: DAÑOS MATERIALES - Deducibles
    cop_dm_deducible_terremoto VARCHAR(255),
    cop_dm_deducible_inundacion VARCHAR(255),
    cop_dm_deducible_incendio VARCHAR(255),
    cop_dm_deducible_amit VARCHAR(255),
    cop_dm_deducible_tuberia_vidrio VARCHAR(255),
    
    -- Cobertura: DAÑOS INTERNOS - Deducibles
    cop_di_deducible_maq_equipo VARCHAR(255),
    cop_di_deducible_equipo_electronico VARCHAR(255),
    
    -- Cobertura: SUSTRACCION CON VIOLENCIA - Deducibles
    cop_scv_deducible_maq_equipo VARCHAR(255),
    cop_scv_deducible_equipo_electronico VARCHAR(255),
    cop_scv_deducible_dineros VARCHAR(255),
    cop_scv_deducible_muebles VARCHAR(255),
    
    -- Cobertura: DIRECTORES & ADMINISTRADORES - Deducibles
    cop_da_deducible_amparo_basico VARCHAR(255),
    
    -- Cobertura: RCE - Deducibles
    cop_rce_deducible_contratistas VARCHAR(255),
    cop_rce_deducible_cruzada VARCHAR(255),
    cop_rce_deducible_patronal VARCHAR(255),
    cop_rce_deducible_parqueaderos VARCHAR(255),
    cop_rce_deducible_gastos_medicos VARCHAR(255),
    
    -- Cobertura: RCE - Sublimites
    cop_rce_sublimite_contratistas VARCHAR(255),
    cop_rce_sublimite_cruzada VARCHAR(255),
    cop_rce_sublimite_patronal VARCHAR(255),
    cop_rce_sublimite_parqueaderos VARCHAR(255),
    cop_rce_sublimite_gastos_medicos VARCHAR(255),
    
    -- Cobertura: MANEJO - Deducibles
    cop_manejo_deducible_amparo_basico VARCHAR(255),
    
    -- Cobertura: TRANSPORTE DE VALORES - Deducibles
    cop_tv_deducible_amparo_basico VARCHAR(255)
);

-- Index for faster searches by name
CREATE INDEX IF NOT EXISTS idx_aseguradoras_nombre ON aseguradoras(nombre);

-- =============================================================================
-- Trigger to auto-update 'updated_at' timestamp
-- =============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_aseguradoras_updated_at ON aseguradoras;
CREATE TRIGGER update_aseguradoras_updated_at
    BEFORE UPDATE ON aseguradoras
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- Initial seed data (sample insurers with copropiedad data)
-- =============================================================================
INSERT INTO aseguradoras (
    nombre, 
    numeral_asistencia, 
    correo_comercial, 
    correo_reclamaciones, 
    direccion_oficina, 
    contacto_asignado, 
    ruta_logo, 
    ruta_pais_logo, 
    respaldo_aseguradora,
    -- Copropiedad fields
    cop_asistencia_area_comun,
    cop_asistencia_area_privada,
    cop_dm_deducible_terremoto,
    cop_dm_deducible_inundacion,
    cop_dm_deducible_incendio,
    cop_dm_deducible_amit,
    cop_dm_deducible_tuberia_vidrio,
    cop_di_deducible_maq_equipo,
    cop_di_deducible_equipo_electronico,
    cop_scv_deducible_maq_equipo,
    cop_scv_deducible_equipo_electronico,
    cop_scv_deducible_dineros,
    cop_scv_deducible_muebles,
    cop_da_deducible_amparo_basico,
    cop_rce_deducible_contratistas,
    cop_rce_deducible_cruzada,
    cop_rce_deducible_patronal,
    cop_rce_deducible_parqueaderos,
    cop_rce_deducible_gastos_medicos,
    cop_rce_sublimite_contratistas,
    cop_rce_sublimite_cruzada,
    cop_rce_sublimite_patronal,
    cop_rce_sublimite_parqueaderos,
    cop_rce_sublimite_gastos_medicos,
    cop_manejo_deducible_amparo_basico,
    cop_tv_deducible_amparo_basico
)
VALUES 
    (
        'Seguros Alfa', 
        '800-123-4567', 
        'comercial@segurosalfa.com', 
        'reclamaciones@segurosalfa.com', 
        'Av. Principal 123, Ciudad', 
        'Juan Pérez', 
        '/logos/seguros_alfa.png', 
        '/logos/flags/co.png', 
        'Grupo Financiero Alfa',
        -- Copropiedad
        'vidrieria,plomeria,cerrajeria,electricista',
        'vidrieria,plomeria,cerrajeria',
        '3,porcentaje,50000000',
        '2,porcentaje,30000000',
        '10,porcentaje,20000000',
        '10,porcentaje,15000000',
        '10,porcentaje,10000000',
        '10,porcentaje,5000000',
        '10,porcentaje,5000000',
        '10,porcentaje,3000000',
        '10,porcentaje,3000000',
        '10,porcentaje,1000000',
        '10,porcentaje,2000000',
        '10,porcentaje,5000000',
        '10,porcentaje,3000000',
        '10,porcentaje,3000000',
        '10,porcentaje,3000000',
        '10,porcentaje,2000000',
        '0,porcentaje,500000',
        '30,porcentaje_evento,null',
        '30,porcentaje_evento,null',
        '30,porcentaje_evento,null',
        '20,porcentaje_evento,null',
        '10,porcentaje_evento,null',
        '10,porcentaje,3000000',
        '10,porcentaje,2000000'
    ),
    (
        'Protección Total S.A.', 
        '800-765-4321', 
        'ventas@protecciontotal.com', 
        'siniestros@protecciontotal.com', 
        'Calle 45 #12-34, Bogotá', 
        'María García', 
        '/logos/proteccion_total.png', 
        '/logos/flags/co.png', 
        'Holding Internacional PT',
        -- Copropiedad
        'vidrieria,plomeria,electricista',
        'plomeria,electricista',
        '2,porcentaje,40000000',
        '2,porcentaje,25000000',
        '10,porcentaje,15000000',
        '10,porcentaje,10000000',
        '10,porcentaje,8000000',
        '10,porcentaje,4000000',
        '10,porcentaje,4000000',
        '10,porcentaje,2500000',
        '10,porcentaje,2500000',
        '10,porcentaje,800000',
        '10,porcentaje,1500000',
        '10,porcentaje,4000000',
        '10,porcentaje,2500000',
        '10,porcentaje,2500000',
        '10,porcentaje,2500000',
        '10,porcentaje,1500000',
        '0,porcentaje,400000',
        '25,porcentaje_evento,null',
        '25,porcentaje_evento,null',
        '25,porcentaje_evento,null',
        '15,porcentaje_evento,null',
        '10,porcentaje_evento,null',
        '10,porcentaje,2500000',
        '10,porcentaje,1500000'
    )
ON CONFLICT DO NOTHING;

-- =============================================================================
-- USUARIOS (Users) Table
-- =============================================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    tipo_persona VARCHAR(10) NOT NULL,  -- 'PERSONA' o 'EMPRESA'
    
    -- =========================================================================
    -- CAMPOS COMUNES Y DE LOGIN
    -- =========================================================================
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    telefono_movil VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(15) NOT NULL,  -- 'CLIENTE', 'AGENTE', 'ADMINISTRADOR', 'SUPERADMIN'
    
    -- =========================================================================
    -- CAMPOS PARA PERSONA NATURAL (NULL si es empresa)
    -- =========================================================================
    tipo_documento VARCHAR(10),
    numero_documento VARCHAR(20),
    nombre VARCHAR(150),
    edad INTEGER,
    
    -- =========================================================================
    -- CAMPOS PARA EMPRESA (NULL si es persona)
    -- =========================================================================
    nit VARCHAR(20),
    razon_social VARCHAR(255),
    nombre_rep_legal VARCHAR(150),
    documento_rep_legal VARCHAR(20),
    telefono_rep_legal VARCHAR(20),
    correo_rep_legal VARCHAR(100),
    contacto_alternativo VARCHAR(255),
    
    -- =========================================================================
    -- TIMESTAMPS
    -- =========================================================================
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- =========================================================================
    -- CONSTRAINTS
    -- =========================================================================
    CONSTRAINT chk_tipo_persona CHECK (tipo_persona IN ('PERSONA', 'EMPRESA')),
    CONSTRAINT chk_tipo_usuario CHECK (tipo_usuario IN ('CLIENTE', 'AGENTE', 'ADMINISTRADOR', 'SUPERADMIN'))
);

-- Indexes para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_usuarios_usuario ON usuarios(usuario);
CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo);
CREATE INDEX IF NOT EXISTS idx_usuarios_tipo_usuario ON usuarios(tipo_usuario);
CREATE INDEX IF NOT EXISTS idx_usuarios_tipo_persona ON usuarios(tipo_persona);

-- Trigger para auto-actualizar 'updated_at'
DROP TRIGGER IF EXISTS update_usuarios_updated_at ON usuarios;
CREATE TRIGGER update_usuarios_updated_at
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- Seed data: Usuarios de ejemplo
-- =============================================================================
INSERT INTO usuarios (
    tipo_persona,
    usuario,
    clave,
    tipo_usuario,
    nombre,
    tipo_documento,
    numero_documento,
    edad,
    ciudad,
    direccion,
    telefono_movil,
    correo
)
VALUES 
    -- Usuario SUPERADMIN
    (
        'PERSONA',
        'superadmin',
        crypt('admin123', gen_salt('bf')),
        'SUPERADMIN',
        'Super Administrador',
        'CC',
        '0000000000',
        NULL,
        'Bogotá',
        'Oficina Principal',
        '3000000000',
        'superadmin@alfabroker.com'
    ),
    -- Usuario ADMINISTRADOR
    (
        'PERSONA',
        'admin',
        crypt('admin123', gen_salt('bf')),
        'ADMINISTRADOR',
        'Administrador Sistema',
        'CC',
        '1111111111',
        35,
        'Bogotá',
        'Calle 100 #10-20',
        '3001111111',
        'admin@alfabroker.com'
    ),
    -- Usuario AGENTE
    (
        'PERSONA',
        'agente01',
        crypt('agente123', gen_salt('bf')),
        'AGENTE',
        'Carlos Rodríguez',
        'CC',
        '2222222222',
        30,
        'Medellín',
        'Carrera 70 #30-40',
        '3002222222',
        'crodriguez@alfabroker.com'
    ),
    -- Usuario CLIENTE persona natural
    (
        'PERSONA',
        'jperez',
        crypt('cliente123', gen_salt('bf')),
        'CLIENTE',
        'Juan Pérez García',
        'CC',
        '1234567890',
        45,
        'Cali',
        'Av. 6 Norte #25-50',
        '3003333333',
        'jperez@email.com'
    )
ON CONFLICT (usuario) DO NOTHING;

-- Cliente empresa
INSERT INTO usuarios (
    tipo_persona,
    usuario,
    clave,
    tipo_usuario,
    razon_social,
    nit,
    nombre_rep_legal,
    documento_rep_legal,
    telefono_rep_legal,
    correo_rep_legal,
    contacto_alternativo,
    ciudad,
    direccion,
    telefono_movil,
    correo
)
VALUES 
    (
        'EMPRESA',
        'empresaabc',
        crypt('empresa123', gen_salt('bf')),
        'CLIENTE',
        'Empresa ABC S.A.S',
        '900123456-1',
        'María García López',
        '9876543210',
        '3109876543',
        'mgarcia@empresaabc.com',
        'Secretaría: 6012345678',
        'Bogotá',
        'Calle 72 #10-34, Of. 501',
        '3004444444',
        'info@empresaabc.com'
    )
ON CONFLICT (usuario) DO NOTHING;

-- =============================================================================
-- HOGARES (Homes) Table - Client assets
-- =============================================================================
CREATE TABLE IF NOT EXISTS hogares (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    
    -- Property information
    tipo_inmueble VARCHAR(100),           -- Casa, Apartamento, Finca, etc.
    ciudad_inmueble VARCHAR(100),
    direccion_inmueble VARCHAR(255),
    numero_pisos INTEGER,
    ano_construccion INTEGER,
    
    -- Asset values (avaluo)
    valor_inmueble_avaluo NUMERIC(15, 2),
    valor_contenidos_normales_avaluo NUMERIC(15, 2),
    valor_contenidos_especiales_avaluo NUMERIC(15, 2),
    valor_equipo_electronico_avaluo NUMERIC(15, 2),
    valor_maquinaria_equipo_avaluo NUMERIC(15, 2),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups by user
CREATE INDEX IF NOT EXISTS idx_hogares_usuario ON hogares(id_usuario);

-- Trigger for auto-update timestamp
DROP TRIGGER IF EXISTS update_hogares_updated_at ON hogares;
CREATE TRIGGER update_hogares_updated_at
    BEFORE UPDATE ON hogares
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- VEHICULOS (Vehicles) Table - Client assets
-- =============================================================================
CREATE TABLE IF NOT EXISTS vehiculos (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    
    -- Vehicle information
    tipo_vehiculo VARCHAR(100),           -- Automóvil, Motocicleta, Camión, etc.
    placa VARCHAR(10),
    marca VARCHAR(100),
    serie_referencia VARCHAR(100),
    ano_modelo INTEGER,
    ano_nacimiento_conductor INTEGER,
    codigo_fasecolda VARCHAR(50),
    
    -- Asset values
    valor_vehiculo NUMERIC(15, 2),
    valor_accesorios_avaluo NUMERIC(15, 2),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_vehiculos_usuario ON vehiculos(id_usuario);
CREATE INDEX IF NOT EXISTS idx_vehiculos_placa ON vehiculos(placa);

-- Trigger for auto-update timestamp
DROP TRIGGER IF EXISTS update_vehiculos_updated_at ON vehiculos;
CREATE TRIGGER update_vehiculos_updated_at
    BEFORE UPDATE ON vehiculos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- COPROPIEDADES (Co-ownerships/Condominiums) Table - Client assets
-- =============================================================================
CREATE TABLE IF NOT EXISTS copropiedades (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    
    -- Property information
    tipo_copropiedad VARCHAR(100),        -- Residencial, Comercial, Mixto
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    estrato INTEGER,
    ano_construccion INTEGER,
    
    -- Building structure
    numero_torres INTEGER,
    numero_maximo_pisos INTEGER,
    numero_maximo_sotanos INTEGER,
    
    -- Unit counts
    cantidad_unidades_casa INTEGER,
    cantidad_unidades_apartamentos INTEGER,
    cantidad_unidades_locales INTEGER,
    cantidad_unidades_oficinas INTEGER,
    cantidad_unidades_otros INTEGER,
    
    -- Asset values (avaluo)
    valor_edificio_area_comun_avaluo NUMERIC(15, 2),
    valor_edificio_area_privada_avaluo NUMERIC(15, 2),
    valor_maquinaria_equipo_avaluo NUMERIC(15, 2),
    valor_equipo_electrico_electronico_avaluo NUMERIC(15, 2),
    valor_muebles_avaluo NUMERIC(15, 2),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups by user
CREATE INDEX IF NOT EXISTS idx_copropiedades_usuario ON copropiedades(id_usuario);

-- Trigger for auto-update timestamp
DROP TRIGGER IF EXISTS update_copropiedades_updated_at ON copropiedades;
CREATE TRIGGER update_copropiedades_updated_at
    BEFORE UPDATE ON copropiedades
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- OTROS_BIENES (Other Assets) Table - Client assets
-- =============================================================================
CREATE TABLE IF NOT EXISTS otros_bienes (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    
    -- Asset information
    tipo_seguro VARCHAR(255),             -- Type of insurance applicable
    bien_asegurado VARCHAR(255),          -- Asset description
    valor_bien_asegurar NUMERIC(15, 2),
    detalles_bien_asegurado TEXT,         -- Additional information
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups by user
CREATE INDEX IF NOT EXISTS idx_otros_bienes_usuario ON otros_bienes(id_usuario);

-- Trigger for auto-update timestamp
DROP TRIGGER IF EXISTS update_otros_bienes_updated_at ON otros_bienes;
CREATE TRIGGER update_otros_bienes_updated_at
    BEFORE UPDATE ON otros_bienes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
