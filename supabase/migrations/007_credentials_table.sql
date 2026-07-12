-- Migration 007: Credentials table for API keys and service accounts
-- ================================================================
-- Stores encrypted credentials for WordPress, GA4, GSC, Bing, etc.
-- Each credential is scoped to a client (or global if client_slug is NULL).

CREATE TABLE IF NOT EXISTS public.credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_slug TEXT REFERENCES public.clients(slug) ON DELETE CASCADE,
    service TEXT NOT NULL,                    -- e.g. 'wordpress', 'ga4', 'gsc', 'bing_wmt', 'ahrefs', etc.
    label TEXT NOT NULL DEFAULT '',           -- human-readable label, e.g. "Main WP Site"
    config JSONB NOT NULL DEFAULT '{}',       -- service-specific config (non-sensitive)
    secrets JSONB NOT NULL DEFAULT '{}',      -- encrypted secrets (API keys, passwords, tokens)
    is_active BOOLEAN NOT NULL DEFAULT true,
    last_tested_at TIMESTAMPTZ,
    test_status TEXT CHECK (test_status IN ('unknown', 'pass', 'fail')),
    test_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_credentials_client ON public.credentials(client_slug);
CREATE INDEX IF NOT EXISTS idx_credentials_service ON public.credentials(service);
CREATE INDEX IF NOT EXISTS idx_credentials_active ON public.credentials(is_active);

-- Row Level Security (RLS)
ALTER TABLE public.credentials ENABLE ROW LEVEL SECURITY;

-- Policy: authenticated users can read all credentials
-- Idempotent: skip if policy already exists (Postgres has no CREATE POLICY IF NOT EXISTS)
DO $create_policies$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE schemaname = 'public'
        AND tablename = 'credentials'
        AND policyname = 'Users can read credentials'
    ) THEN
        CREATE POLICY "Users can read credentials"
            ON public.credentials
            FOR SELECT
            TO authenticated
            USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE schemaname = 'public'
        AND tablename = 'credentials'
        AND policyname = 'Editors can manage credentials'
    ) THEN
        CREATE POLICY "Editors can manage credentials"
            ON public.credentials
            FOR ALL
            TO authenticated
            USING (
                EXISTS (
                    SELECT 1 FROM public.users
                    WHERE public.users.id = auth.uid()
                    AND public.users.role IN ('admin', 'editor')
                )
            )
            WITH CHECK (
                EXISTS (
                    SELECT 1 FROM public.users
                    WHERE public.users.id = auth.uid()
                    AND public.users.role IN ('admin', 'editor')
                )
            );
    END IF;
END
$create_policies$;

-- Comments
COMMENT ON TABLE public.credentials IS 'Encrypted API credentials and service accounts for client integrations';
COMMENT ON COLUMN public.credentials.service IS 'Service type: wordpress, ga4, gsc, bing_wmt, ahrefs, semrush, google_ads, meta_ads, linkedin_ads, slack, hubspot, etc.';
COMMENT ON COLUMN public.credentials.config IS 'Non-sensitive configuration (URLs, property IDs, account IDs)';
COMMENT ON COLUMN public.credentials.secrets IS 'Encrypted sensitive data (API keys, passwords, tokens). NEVER log or expose.';

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION public.update_credentials_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_credentials_updated_at ON public.credentials;
CREATE TRIGGER trg_credentials_updated_at
    BEFORE UPDATE ON public.credentials
    FOR EACH ROW
    EXECUTE FUNCTION public.update_credentials_updated_at();
