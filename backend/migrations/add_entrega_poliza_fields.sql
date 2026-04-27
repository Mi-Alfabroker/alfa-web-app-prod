-- ============================================================================
-- MIGRACIÓN: Agregar campos de entrega de póliza
-- Fecha: 2026-03-18
-- Descripción: Agrega campos necesarios para el proceso de entrega de póliza
--              y gestión de financiación a todas las tablas de pólizas.
--              Estos campos se agregan a través de BasePolizaMixin que es
--              compartido por todas las tablas de pólizas.
-- ============================================================================

-- ============================================================================
-- PARTE 1: POLIZAS COPROPIEDAD - Campos de Entrega y Financiación
-- ============================================================================

ALTER TABLE polizas_copropiedad
-- Información de aseguradora seleccionada (desnormalizada)
ADD COLUMN nombre_aseguradora VARCHAR(255),
ADD COLUMN numeral_asistencia VARCHAR(100),

-- Valores de póliza
ADD COLUMN valor_total_prima BIGINT,

-- Forma de pago
ADD COLUMN medio_pago VARCHAR(20) CHECK (medio_pago IN ('contado', 'financiera')),
ADD COLUMN estado_cartera VARCHAR(20) CHECK (estado_cartera IN ('recaudado', 'pendiente', 'cancelado', 'en_solicitud')),

-- Financiación
ADD COLUMN financiacion_num_cuotas SMALLINT CHECK (financiacion_num_cuotas IN (3, 5, 8, 11)),
ADD COLUMN financiacion_cuota_actual SMALLINT,
ADD COLUMN financiacion_valor_cuota BIGINT,
ADD COLUMN financiacion_fecha_primera_cuota DATE,
ADD COLUMN financiacion_periodicidad VARCHAR(20) DEFAULT 'mensual' CHECK (financiacion_periodicidad IN ('mensual', 'bimestral', 'trimestral')),

-- Valores de cuotas precalculadas (guardadas al generar propuesta)
ADD COLUMN valor_cuota_3 BIGINT,
ADD COLUMN valor_cuota_5 BIGINT,
ADD COLUMN valor_cuota_8 BIGINT,
ADD COLUMN valor_cuota_11 BIGINT;

-- ============================================================================
-- PARTE 2: POLIZAS HOGAR - Campos de Entrega y Financiación
-- ============================================================================

ALTER TABLE polizas_hogar
-- Información de aseguradora seleccionada (desnormalizada)
ADD COLUMN nombre_aseguradora VARCHAR(255),
ADD COLUMN numeral_asistencia VARCHAR(100),

-- Valores de póliza
ADD COLUMN valor_total_prima BIGINT,

-- Forma de pago
ADD COLUMN medio_pago VARCHAR(20) CHECK (medio_pago IN ('contado', 'financiera')),
ADD COLUMN estado_cartera VARCHAR(20) CHECK (estado_cartera IN ('recaudado', 'pendiente', 'cancelado', 'en_solicitud')),

-- Financiación
ADD COLUMN financiacion_num_cuotas SMALLINT CHECK (financiacion_num_cuotas IN (3, 5, 8, 11)),
ADD COLUMN financiacion_cuota_actual SMALLINT,
ADD COLUMN financiacion_valor_cuota BIGINT,
ADD COLUMN financiacion_fecha_primera_cuota DATE,
ADD COLUMN financiacion_periodicidad VARCHAR(20) DEFAULT 'mensual' CHECK (financiacion_periodicidad IN ('mensual', 'bimestral', 'trimestral')),

-- Valores de cuotas precalculadas (guardadas al generar propuesta)
ADD COLUMN valor_cuota_3 BIGINT,
ADD COLUMN valor_cuota_5 BIGINT,
ADD COLUMN valor_cuota_8 BIGINT,
ADD COLUMN valor_cuota_11 BIGINT;

-- ============================================================================
-- PARTE 3: POLIZAS VEHICULO - Campos de Entrega y Financiación
-- ============================================================================

ALTER TABLE polizas_vehiculo
-- Información de aseguradora seleccionada (desnormalizada)
ADD COLUMN nombre_aseguradora VARCHAR(255),
ADD COLUMN numeral_asistencia VARCHAR(100),

-- Valores de póliza
ADD COLUMN valor_total_prima BIGINT,

-- Forma de pago
ADD COLUMN medio_pago VARCHAR(20) CHECK (medio_pago IN ('contado', 'financiera')),
ADD COLUMN estado_cartera VARCHAR(20) CHECK (estado_cartera IN ('recaudado', 'pendiente', 'cancelado', 'en_solicitud')),

-- Financiación
ADD COLUMN financiacion_num_cuotas SMALLINT CHECK (financiacion_num_cuotas IN (3, 5, 8, 11)),
ADD COLUMN financiacion_cuota_actual SMALLINT,
ADD COLUMN financiacion_valor_cuota BIGINT,
ADD COLUMN financiacion_fecha_primera_cuota DATE,
ADD COLUMN financiacion_periodicidad VARCHAR(20) DEFAULT 'mensual' CHECK (financiacion_periodicidad IN ('mensual', 'bimestral', 'trimestral')),

-- Valores de cuotas precalculadas (guardadas al generar propuesta)
ADD COLUMN valor_cuota_3 BIGINT,
ADD COLUMN valor_cuota_5 BIGINT,
ADD COLUMN valor_cuota_8 BIGINT,
ADD COLUMN valor_cuota_11 BIGINT;

-- ============================================================================
-- PARTE 4: POLIZAS OTRO BIEN - Campos de Entrega y Financiación
-- ============================================================================

ALTER TABLE polizas_otro_bien
-- Información de aseguradora seleccionada (desnormalizada)
ADD COLUMN nombre_aseguradora VARCHAR(255),
ADD COLUMN numeral_asistencia VARCHAR(100),

-- Valores de póliza
ADD COLUMN valor_total_prima BIGINT,

-- Forma de pago
ADD COLUMN medio_pago VARCHAR(20) CHECK (medio_pago IN ('contado', 'financiera')),
ADD COLUMN estado_cartera VARCHAR(20) CHECK (estado_cartera IN ('recaudado', 'pendiente', 'cancelado', 'en_solicitud')),

-- Financiación
ADD COLUMN financiacion_num_cuotas SMALLINT CHECK (financiacion_num_cuotas IN (3, 5, 8, 11)),
ADD COLUMN financiacion_cuota_actual SMALLINT,
ADD COLUMN financiacion_valor_cuota BIGINT,
ADD COLUMN financiacion_fecha_primera_cuota DATE,
ADD COLUMN financiacion_periodicidad VARCHAR(20) DEFAULT 'mensual' CHECK (financiacion_periodicidad IN ('mensual', 'bimestral', 'trimestral')),

-- Valores de cuotas precalculadas (guardadas al generar propuesta)
ADD COLUMN valor_cuota_3 BIGINT,
ADD COLUMN valor_cuota_5 BIGINT,
ADD COLUMN valor_cuota_8 BIGINT,
ADD COLUMN valor_cuota_11 BIGINT;

-- ============================================================================
-- NOTAS SOBRE LA MIGRACIÓN
-- ============================================================================
-- 
-- - Todos los campos son nullable por defecto (no afectan pólizas existentes)
-- - Los CHECK constraints se aplican solo cuando hay valor (NULL permitido)
-- - financiacion_periodicidad tiene default 'mensual'
-- - Los valores se guardan como BIGINT (sin decimales, en centavos si aplica)
-- - Esta migración es aditiva y reversible
--
-- ROLLBACK (si es necesario):
-- ALTER TABLE polizas_copropiedad DROP COLUMN nombre_aseguradora, DROP COLUMN numeral_asistencia, ...
-- ALTER TABLE polizas_hogar DROP COLUMN nombre_aseguradora, DROP COLUMN numeral_asistencia, ...
-- ALTER TABLE polizas_vehiculo DROP COLUMN nombre_aseguradora, DROP COLUMN numeral_asistencia, ...
-- ALTER TABLE polizas_otro_bien DROP COLUMN nombre_aseguradora, DROP COLUMN numeral_asistencia, ...
--
-- ============================================================================
