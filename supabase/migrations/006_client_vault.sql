-- Migration 006: Add vault_content JSONB to clients table
-- ================================================

ALTER TABLE public.clients
    ADD COLUMN IF NOT EXISTS vault_content JSONB DEFAULT NULL;

-- Index for JSONB queries (in case we search inside vault later)
CREATE INDEX IF NOT EXISTS idx_clients_vault ON public.clients USING gin (vault_content);

COMMENT ON COLUMN public.clients.vault_content IS 'JSON object storing client vault markdown files (client-profile, strategy, kpis, etc.)';
