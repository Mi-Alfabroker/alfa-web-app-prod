-- Marca de que los documentos de una póliza ya fueron generados.
--
-- Nulo = nunca se generó. Las pólizas existentes se dejan en nulo a propósito:
-- nadie registró esos documentos, e inventar la fecha ensuciaría el histórico.
-- Las que ya están vigentes se verán con el paso "Propuesta" sin marcar; el
-- escape de administrador cubre la corrección puntual si hiciera falta.
--
-- Aplicar con:
--   docker exec -i alfabroker-db psql -U admin -d alfabroker < backend/migrations/add_documentos_generados.sql

ALTER TABLE polizas_hogar       ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_hogar       ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;

ALTER TABLE polizas_vehiculo    ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_vehiculo    ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;

ALTER TABLE polizas_copropiedad ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_copropiedad ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;

ALTER TABLE polizas_otro_bien   ADD COLUMN IF NOT EXISTS propuesta_generada_at TIMESTAMPTZ;
ALTER TABLE polizas_otro_bien   ADD COLUMN IF NOT EXISTS entrega_generada_at   TIMESTAMPTZ;
