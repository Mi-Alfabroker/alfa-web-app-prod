-- ============================================================================
-- MIGRACIÓN: Agregar soporte para rubros Hogar, Vehículos y Otros
-- Fecha: 2026-03-18
-- Descripción: Agrega campos de configuración para los rubros Hogar, Vehículos
--              y Otros a la tabla aseguradoras, y campos adicionales a tablas
--              de bienes (hogares, otros_bienes)
-- ============================================================================

-- ============================================================================
-- PARTE 1: ASEGURADORA - CAMPOS PARA HOGAR (~70 campos con prefijo hog_*)
-- ============================================================================

ALTER TABLE aseguradoras

-- Deducibles Daños - Hogar
ADD COLUMN hog_deducible_terremoto VARCHAR(255), -- formato: porcentaje,tipo,minimo
ADD COLUMN hog_deducible_amit VARCHAR(255),
ADD COLUMN hog_deducible_demas_eventos VARCHAR(255),

-- Deducibles Hurto Contenidos Normales - Hogar
ADD COLUMN hog_hurto_cn_terremoto VARCHAR(255),
ADD COLUMN hog_hurto_cn_demas_eventos VARCHAR(255),
ADD COLUMN hog_hurto_cn_hurto VARCHAR(255),

-- Deducibles Hurto Contenidos Especiales - Hogar
ADD COLUMN hog_hurto_ce_hurto VARCHAR(255),

-- Deducibles Hurto Equipo Electrónico - Hogar
ADD COLUMN hog_hurto_ee_hurto VARCHAR(255),

-- Valores Asegurados - Hogar
ADD COLUMN hog_valor_asegurado_inmueble VARCHAR(255),
ADD COLUMN hog_valor_asegurado_contenidos_normales VARCHAR(255),
ADD COLUMN hog_valor_asegurado_contenidos_especiales VARCHAR(255),
ADD COLUMN hog_valor_asegurado_equipo_electronico VARCHAR(255),

-- Coberturas Adicionales - Hogar (checks 1, 2, 3)
ADD COLUMN hog_cobertura_adicional_1 VARCHAR(255),
ADD COLUMN hog_cobertura_adicional_2 VARCHAR(255),
ADD COLUMN hog_cobertura_adicional_3 VARCHAR(255);

-- ============================================================================
-- PARTE 2: ASEGURADORA - CAMPOS PARA VEHÍCULOS (~100 campos con prefijo veh_*)
-- ============================================================================

ALTER TABLE aseguradoras

-- Valores Asegurados - Vehículos
ADD COLUMN veh_valor_asegurado_vehiculo VARCHAR(255),
ADD COLUMN veh_valor_asegurado_accesorios VARCHAR(255),
ADD COLUMN veh_valor_asegurado_rc VARCHAR(255),

-- Deducibles Daños Pérdida Parcial - Vehículos
ADD COLUMN veh_deducible_perdida_parcial VARCHAR(255), -- porcentaje,tipo,minimo
ADD COLUMN veh_deducible_perdida_total VARCHAR(255),
ADD COLUMN veh_deducible_terremoto VARCHAR(255),

-- Deducibles Hurto - Vehículos
ADD COLUMN veh_hurto_perdida_parcial VARCHAR(255),
ADD COLUMN veh_hurto_perdida_total VARCHAR(255),

-- Deducible RC - Vehículos
ADD COLUMN veh_deducible_rc VARCHAR(255),

-- Sublímites RC - Vehículos (4 sublímites)
ADD COLUMN veh_rc_sublimite_bienes_terceros VARCHAR(255),
ADD COLUMN veh_rc_sublimite_amparo_patrimonial VARCHAR(255),
ADD COLUMN veh_rc_sublimite_muerte_lesion_una VARCHAR(255),
ADD COLUMN veh_rc_sublimite_muerte_lesion_dos_mas VARCHAR(255),

-- Coberturas Adicionales - Vehículos (checks 1-7)
ADD COLUMN veh_cobertura_adicional_1 VARCHAR(255),
ADD COLUMN veh_cobertura_adicional_2 VARCHAR(255),
ADD COLUMN veh_cobertura_adicional_3 VARCHAR(255),
ADD COLUMN veh_cobertura_adicional_4 VARCHAR(255),
ADD COLUMN veh_cobertura_adicional_5 VARCHAR(255),
ADD COLUMN veh_cobertura_adicional_6 VARCHAR(255),
ADD COLUMN veh_cobertura_adicional_7 VARCHAR(255);

-- ============================================================================
-- PARTE 3: ASEGURADORA - CAMPOS PARA OTROS (~70 campos con prefijo otr_*)
-- ============================================================================

ALTER TABLE aseguradoras

-- Valores Asegurados - Otros
ADD COLUMN otr_valor_asegurado_inmueble VARCHAR(255),
ADD COLUMN otr_valor_asegurado_contenidos_normales VARCHAR(255),
ADD COLUMN otr_valor_asegurado_contenidos_especiales VARCHAR(255),
ADD COLUMN otr_valor_asegurado_equipo_electronico VARCHAR(255),

-- Deducibles Daños - Otros
ADD COLUMN otr_deducible_terremoto VARCHAR(255), -- porcentaje,tipo,minimo
ADD COLUMN otr_deducible_amit VARCHAR(255),
ADD COLUMN otr_deducible_demas_eventos VARCHAR(255),

-- Deducibles Hurto Contenidos Normales - Otros
ADD COLUMN otr_hurto_cn_deducible VARCHAR(255),

-- Deducibles Hurto Contenidos Especiales - Otros
ADD COLUMN otr_hurto_ce_deducible VARCHAR(255),

-- Deducibles Hurto Equipo Electrónico - Otros
ADD COLUMN otr_hurto_ee_deducible VARCHAR(255),

-- Coberturas Adicionales - Otros (checks 1, 2, 3)
ADD COLUMN otr_cobertura_adicional_1 VARCHAR(255),
ADD COLUMN otr_cobertura_adicional_2 VARCHAR(255),
ADD COLUMN otr_cobertura_adicional_3 VARCHAR(255);

-- ============================================================================
-- PARTE 4: TABLA HOGARES - Campos adicionales
-- ============================================================================

ALTER TABLE hogares
ADD COLUMN estado VARCHAR(100),
ADD COLUMN comentarios_detalles TEXT;

-- ============================================================================
-- PARTE 5: TABLA OTROS_BIENES - Campos adicionales
-- ============================================================================

ALTER TABLE otros_bienes
ADD COLUMN estado VARCHAR(100),
ADD COLUMN comentarios TEXT;

-- ============================================================================
-- VALIDACIÓN (comentar para ejecución en producción)
-- ============================================================================

-- Verificar columnas agregadas a aseguradoras
SELECT column_name, data_type, character_maximum_length 
FROM information_schema.columns 
WHERE table_name = 'aseguradoras' 
  AND (column_name LIKE 'hog_%' 
    OR column_name LIKE 'veh_%' 
    OR column_name LIKE 'otr_%')
ORDER BY column_name;

-- Verificar columnas agregadas a hogares
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'hogares' 
  AND column_name IN ('estado', 'comentarios_detalles');

-- Verificar columnas agregadas a otros_bienes
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'otros_bienes' 
  AND column_name IN ('estado', 'comentarios');

-- ============================================================================
-- ROLLBACK (en caso de necesitar revertir)
-- ============================================================================

/*
-- ROLLBACK - Aseguradoras - Hogar
ALTER TABLE aseguradoras
DROP COLUMN IF EXISTS hog_deducible_terremoto,
DROP COLUMN IF EXISTS hog_deducible_amit,
DROP COLUMN IF EXISTS hog_deducible_demas_eventos,
DROP COLUMN IF EXISTS hog_hurto_cn_terremoto,
DROP COLUMN IF EXISTS hog_hurto_cn_demas_eventos,
DROP COLUMN IF EXISTS hog_hurto_cn_hurto,
DROP COLUMN IF EXISTS hog_hurto_ce_hurto,
DROP COLUMN IF EXISTS hog_hurto_ee_hurto,
DROP COLUMN IF EXISTS hog_valor_asegurado_inmueble,
DROP COLUMN IF EXISTS hog_valor_asegurado_contenidos_normales,
DROP COLUMN IF EXISTS hog_valor_asegurado_contenidos_especiales,
DROP COLUMN IF EXISTS hog_valor_asegurado_equipo_electronico,
DROP COLUMN IF EXISTS hog_cobertura_adicional_1,
DROP COLUMN IF EXISTS hog_cobertura_adicional_2,
DROP COLUMN IF EXISTS hog_cobertura_adicional_3;

-- ROLLBACK - Aseguradoras - Vehículos
ALTER TABLE aseguradoras
DROP COLUMN IF EXISTS veh_valor_asegurado_vehiculo,
DROP COLUMN IF EXISTS veh_valor_asegurado_accesorios,
DROP COLUMN IF EXISTS veh_valor_asegurado_rc,
DROP COLUMN IF EXISTS veh_deducible_perdida_parcial,
DROP COLUMN IF EXISTS veh_deducible_perdida_total,
DROP COLUMN IF EXISTS veh_deducible_terremoto,
DROP COLUMN IF EXISTS veh_hurto_perdida_parcial,
DROP COLUMN IF EXISTS veh_hurto_perdida_total,
DROP COLUMN IF EXISTS veh_deducible_rc,
DROP COLUMN IF EXISTS veh_rc_sublimite_bienes_terceros,
DROP COLUMN IF EXISTS veh_rc_sublimite_amparo_patrimonial,
DROP COLUMN IF EXISTS veh_rc_sublimite_muerte_lesion_una,
DROP COLUMN IF EXISTS veh_rc_sublimite_muerte_lesion_dos_mas,
DROP COLUMN IF EXISTS veh_cobertura_adicional_1,
DROP COLUMN IF EXISTS veh_cobertura_adicional_2,
DROP COLUMN IF EXISTS veh_cobertura_adicional_3,
DROP COLUMN IF EXISTS veh_cobertura_adicional_4,
DROP COLUMN IF EXISTS veh_cobertura_adicional_5,
DROP COLUMN IF EXISTS veh_cobertura_adicional_6,
DROP COLUMN IF EXISTS veh_cobertura_adicional_7;

-- ROLLBACK - Aseguradoras - Otros
ALTER TABLE aseguradoras
DROP COLUMN IF EXISTS otr_valor_asegurado_inmueble,
DROP COLUMN IF EXISTS otr_valor_asegurado_contenidos_normales,
DROP COLUMN IF EXISTS otr_valor_asegurado_contenidos_especiales,
DROP COLUMN IF EXISTS otr_valor_asegurado_equipo_electronico,
DROP COLUMN IF EXISTS otr_deducible_terremoto,
DROP COLUMN IF EXISTS otr_deducible_amit,
DROP COLUMN IF EXISTS otr_deducible_demas_eventos,
DROP COLUMN IF EXISTS otr_hurto_cn_deducible,
DROP COLUMN IF EXISTS otr_hurto_ce_deducible,
DROP COLUMN IF EXISTS otr_hurto_ee_deducible,
DROP COLUMN IF EXISTS otr_cobertura_adicional_1,
DROP COLUMN IF EXISTS otr_cobertura_adicional_2,
DROP COLUMN IF EXISTS otr_cobertura_adicional_3;

-- ROLLBACK - Hogares
ALTER TABLE hogares
DROP COLUMN IF EXISTS estado,
DROP COLUMN IF EXISTS comentarios_detalles;

-- ROLLBACK - Otros Bienes
ALTER TABLE otros_bienes
DROP COLUMN IF EXISTS estado,
DROP COLUMN IF EXISTS comentarios;
*/
