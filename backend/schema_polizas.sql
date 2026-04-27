-- ============================================================================
-- SCHEMA: POLIZAS (Insurance Policies)
-- Fecha: 2026-01-31
-- Descripción: Tablas para manejar pólizas de seguros por tipo de bien
-- Relación: 1 Bien puede tener N Pólizas
-- ============================================================================

-- ============================================================================
-- TABLA: polizas_hogar
-- Pólizas de seguros para bienes tipo Hogar
-- ============================================================================
CREATE TABLE IF NOT EXISTS polizas_hogar (
    id SERIAL PRIMARY KEY,
    
    -- Relación con el bien (Hogar)
    id_hogar INTEGER NOT NULL REFERENCES hogares(id) ON DELETE CASCADE,
    
    -- Consecutivo único: B{bien_id}C{cliente_id}F{YYYYMMDD}
    consecutivo VARCHAR(50) NOT NULL UNIQUE,
    
    -- Estado de la póliza
    estado VARCHAR(20) NOT NULL DEFAULT 'PROSPECTO' 
        CHECK (estado IN ('PROSPECTO', 'VIGENTE', 'VENCIDA', 'CANCELADA')),
    
    -- Fechas de vigencia
    inicio_vigencia DATE,
    fin_vigencia DATE,
    
    -- Primas de aseguradoras (hasta 5 opciones) - BigInt para operaciones matemáticas
    valor_prima_aseg_1 BIGINT,
    valor_prima_aseg_2 BIGINT,
    valor_prima_aseg_3 BIGINT,
    valor_prima_aseg_4 BIGINT,
    valor_prima_aseg_5 BIGINT,
    
    -- Llaves foráneas a aseguradoras (hasta 5 opciones)
    id_aseguradora_1 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_2 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_3 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_4 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_5 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    
    -- Aseguradora seleccionada (1-5) cuando la póliza está vigente
    aseguradora_seleccionada SMALLINT CHECK (aseguradora_seleccionada BETWEEN 1 AND 5),
    
    -- Número de póliza asignado por la aseguradora
    numero_poliza_aseguradora VARCHAR(100),
    
    -- Valores financieros (BigInt para operaciones matemáticas)
    valor_prima_neta BIGINT,
    valor_otros_costos BIGINT,
    valor_iva BIGINT,
    ingreso_comision_percibido BIGINT,
    
    -- Valores asegurados específicos de Hogar
    valor_inmueble_asegurado NUMERIC(15, 2),
    valor_contenidos_normales_asegurado NUMERIC(15, 2),
    valor_contenidos_especiales_asegurado NUMERIC(15, 2),
    valor_equipo_electronico_asegurado NUMERIC(15, 2),
    valor_maquinaria_equipo_asegurado NUMERIC(15, 2),
    valor_rc_asegurado NUMERIC(15, 2),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para polizas_hogar
CREATE INDEX IF NOT EXISTS idx_polizas_hogar_id_hogar ON polizas_hogar(id_hogar);
CREATE INDEX IF NOT EXISTS idx_polizas_hogar_consecutivo ON polizas_hogar(consecutivo);
CREATE INDEX IF NOT EXISTS idx_polizas_hogar_estado ON polizas_hogar(estado);


-- ============================================================================
-- TABLA: polizas_vehiculo
-- Pólizas de seguros para bienes tipo Vehículo
-- ============================================================================
CREATE TABLE IF NOT EXISTS polizas_vehiculo (
    id SERIAL PRIMARY KEY,
    
    -- Relación con el bien (Vehiculo)
    id_vehiculo INTEGER NOT NULL REFERENCES vehiculos(id) ON DELETE CASCADE,
    
    -- Consecutivo único
    consecutivo VARCHAR(50) NOT NULL UNIQUE,
    
    -- Estado de la póliza
    estado VARCHAR(20) NOT NULL DEFAULT 'PROSPECTO' 
        CHECK (estado IN ('PROSPECTO', 'VIGENTE', 'VENCIDA', 'CANCELADA')),
    
    -- Fechas de vigencia
    inicio_vigencia DATE,
    fin_vigencia DATE,
    
    -- Primas de aseguradoras (hasta 5 opciones)
    valor_prima_aseg_1 BIGINT,
    valor_prima_aseg_2 BIGINT,
    valor_prima_aseg_3 BIGINT,
    valor_prima_aseg_4 BIGINT,
    valor_prima_aseg_5 BIGINT,
    
    -- Llaves foráneas a aseguradoras
    id_aseguradora_1 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_2 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_3 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_4 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_5 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    
    -- Aseguradora seleccionada
    aseguradora_seleccionada SMALLINT CHECK (aseguradora_seleccionada BETWEEN 1 AND 5),
    
    -- Número de póliza asignado por la aseguradora
    numero_poliza_aseguradora VARCHAR(100),
    
    -- Valores financieros
    valor_prima_neta BIGINT,
    valor_otros_costos BIGINT,
    valor_iva BIGINT,
    ingreso_comision_percibido BIGINT,
    
    -- Valores asegurados específicos de Vehículo
    valor_vehiculo_asegurado NUMERIC(15, 2),
    valor_accesorios_asegurado NUMERIC(15, 2),
    valor_rc_asegurado NUMERIC(15, 2),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para polizas_vehiculo
CREATE INDEX IF NOT EXISTS idx_polizas_vehiculo_id_vehiculo ON polizas_vehiculo(id_vehiculo);
CREATE INDEX IF NOT EXISTS idx_polizas_vehiculo_consecutivo ON polizas_vehiculo(consecutivo);
CREATE INDEX IF NOT EXISTS idx_polizas_vehiculo_estado ON polizas_vehiculo(estado);


-- ============================================================================
-- TABLA: polizas_copropiedad
-- Pólizas de seguros para bienes tipo Copropiedad
-- ============================================================================
CREATE TABLE IF NOT EXISTS polizas_copropiedad (
    id SERIAL PRIMARY KEY,
    
    -- Relación con el bien (Copropiedad)
    id_copropiedad INTEGER NOT NULL REFERENCES copropiedades(id) ON DELETE CASCADE,
    
    -- Consecutivo único
    consecutivo VARCHAR(50) NOT NULL UNIQUE,
    
    -- Estado de la póliza
    estado VARCHAR(20) NOT NULL DEFAULT 'PROSPECTO' 
        CHECK (estado IN ('PROSPECTO', 'VIGENTE', 'VENCIDA', 'CANCELADA')),
    
    -- Fechas de vigencia
    inicio_vigencia DATE,
    fin_vigencia DATE,
    
    -- Primas de aseguradoras (hasta 5 opciones)
    valor_prima_aseg_1 BIGINT,
    valor_prima_aseg_2 BIGINT,
    valor_prima_aseg_3 BIGINT,
    valor_prima_aseg_4 BIGINT,
    valor_prima_aseg_5 BIGINT,
    
    -- Llaves foráneas a aseguradoras
    id_aseguradora_1 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_2 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_3 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_4 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_5 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    
    -- Aseguradora seleccionada
    aseguradora_seleccionada SMALLINT CHECK (aseguradora_seleccionada BETWEEN 1 AND 5),
    
    -- Número de póliza asignado por la aseguradora
    numero_poliza_aseguradora VARCHAR(100),
    
    -- Valores financieros
    valor_prima_neta BIGINT,
    valor_otros_costos BIGINT,
    valor_iva BIGINT,
    ingreso_comision_percibido BIGINT,
    
    -- Valores asegurados específicos de Copropiedad
    valor_area_comun_asegurado NUMERIC(15, 2),
    valor_area_privada_asegurado NUMERIC(15, 2),
    valor_maquinaria_equipo_asegurado NUMERIC(15, 2),
    valor_equipo_electronico_asegurado NUMERIC(15, 2),
    valor_muebles_asegurado NUMERIC(15, 2),
    valor_directores_asegurado NUMERIC(15, 2),
    valor_rce_asegurado NUMERIC(15, 2),
    valor_manejo_asegurado NUMERIC(15, 2),
    valor_transporte_valores_vigencia_asegurado NUMERIC(15, 2),
    valor_transporte_valores_despacho_asegurado NUMERIC(15, 2),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para polizas_copropiedad
CREATE INDEX IF NOT EXISTS idx_polizas_copropiedad_id_copropiedad ON polizas_copropiedad(id_copropiedad);
CREATE INDEX IF NOT EXISTS idx_polizas_copropiedad_consecutivo ON polizas_copropiedad(consecutivo);
CREATE INDEX IF NOT EXISTS idx_polizas_copropiedad_estado ON polizas_copropiedad(estado);


-- ============================================================================
-- TABLA: polizas_otro_bien
-- Pólizas de seguros para otros tipos de bienes
-- ============================================================================
CREATE TABLE IF NOT EXISTS polizas_otro_bien (
    id SERIAL PRIMARY KEY,
    
    -- Relación con el bien (OtroBien)
    id_otro_bien INTEGER NOT NULL REFERENCES otros_bienes(id) ON DELETE CASCADE,
    
    -- Consecutivo único
    consecutivo VARCHAR(50) NOT NULL UNIQUE,
    
    -- Estado de la póliza
    estado VARCHAR(20) NOT NULL DEFAULT 'PROSPECTO' 
        CHECK (estado IN ('PROSPECTO', 'VIGENTE', 'VENCIDA', 'CANCELADA')),
    
    -- Fechas de vigencia
    inicio_vigencia DATE,
    fin_vigencia DATE,
    
    -- Primas de aseguradoras (hasta 5 opciones)
    valor_prima_aseg_1 BIGINT,
    valor_prima_aseg_2 BIGINT,
    valor_prima_aseg_3 BIGINT,
    valor_prima_aseg_4 BIGINT,
    valor_prima_aseg_5 BIGINT,
    
    -- Llaves foráneas a aseguradoras
    id_aseguradora_1 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_2 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_3 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_4 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    id_aseguradora_5 INTEGER REFERENCES aseguradoras(id) ON DELETE SET NULL,
    
    -- Aseguradora seleccionada
    aseguradora_seleccionada SMALLINT CHECK (aseguradora_seleccionada BETWEEN 1 AND 5),
    
    -- Número de póliza asignado por la aseguradora
    numero_poliza_aseguradora VARCHAR(100),
    
    -- Valores financieros
    valor_prima_neta BIGINT,
    valor_otros_costos BIGINT,
    valor_iva BIGINT,
    ingreso_comision_percibido BIGINT,
    
    -- Valores asegurados específicos de Otro Bien
    valor_asegurado NUMERIC(15, 2),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para polizas_otro_bien
CREATE INDEX IF NOT EXISTS idx_polizas_otro_bien_id_otro_bien ON polizas_otro_bien(id_otro_bien);
CREATE INDEX IF NOT EXISTS idx_polizas_otro_bien_consecutivo ON polizas_otro_bien(consecutivo);
CREATE INDEX IF NOT EXISTS idx_polizas_otro_bien_estado ON polizas_otro_bien(estado);


-- ============================================================================
-- TRIGGERS: Actualizar updated_at automáticamente
-- ============================================================================

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para polizas_hogar
DROP TRIGGER IF EXISTS update_polizas_hogar_updated_at ON polizas_hogar;
CREATE TRIGGER update_polizas_hogar_updated_at
    BEFORE UPDATE ON polizas_hogar
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para polizas_vehiculo
DROP TRIGGER IF EXISTS update_polizas_vehiculo_updated_at ON polizas_vehiculo;
CREATE TRIGGER update_polizas_vehiculo_updated_at
    BEFORE UPDATE ON polizas_vehiculo
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para polizas_copropiedad
DROP TRIGGER IF EXISTS update_polizas_copropiedad_updated_at ON polizas_copropiedad;
CREATE TRIGGER update_polizas_copropiedad_updated_at
    BEFORE UPDATE ON polizas_copropiedad
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para polizas_otro_bien
DROP TRIGGER IF EXISTS update_polizas_otro_bien_updated_at ON polizas_otro_bien;
CREATE TRIGGER update_polizas_otro_bien_updated_at
    BEFORE UPDATE ON polizas_otro_bien
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- COMENTARIOS DE TABLAS Y COLUMNAS
-- ============================================================================

COMMENT ON TABLE polizas_hogar IS 'Pólizas de seguros para bienes tipo Hogar';
COMMENT ON TABLE polizas_vehiculo IS 'Pólizas de seguros para bienes tipo Vehículo';
COMMENT ON TABLE polizas_copropiedad IS 'Pólizas de seguros para bienes tipo Copropiedad';
COMMENT ON TABLE polizas_otro_bien IS 'Pólizas de seguros para otros tipos de bienes';

COMMENT ON COLUMN polizas_hogar.consecutivo IS 'Identificador único formato B{bien_id}C{cliente_id}F{YYYYMMDD}';
COMMENT ON COLUMN polizas_hogar.estado IS 'PROSPECTO=Propuesta, VIGENTE=Activa, VENCIDA=Expirada, CANCELADA=Anulada';
COMMENT ON COLUMN polizas_hogar.aseguradora_seleccionada IS 'Número 1-5 indicando cuál de las 5 aseguradoras cotizadas fue seleccionada';


-- ============================================================================
-- CONSULTAS ÚTILES (Ejemplos)
-- ============================================================================

-- Ver todas las propuestas (estado PROSPECTO)
-- SELECT * FROM polizas_hogar WHERE estado = 'PROSPECTO';

-- Ver pólizas vigentes que vencen en los próximos 30 días
-- SELECT * FROM polizas_hogar 
-- WHERE estado = 'VIGENTE' 
--   AND fin_vigencia BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days';

-- Ver todas las pólizas de un usuario (a través del bien)
-- SELECT p.* FROM polizas_hogar p
-- JOIN hogares h ON p.id_hogar = h.id
-- WHERE h.id_usuario = 1;
