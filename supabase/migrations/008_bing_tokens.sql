-- Migration: Bing Webmaster OAuth tokens table
-- ============================================
-- Stores OAuth 2.0 tokens for the Bing Webmaster API.
-- Single-row config (id='default') for the whole AgenticMarketingPro system.

CREATE TABLE IF NOT EXISTS public.bing_tokens (
    id TEXT PRIMARY KEY DEFAULT 'default',
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    scope TEXT,
    token_type TEXT DEFAULT 'Bearer',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_bing_tokens_updated ON public.bing_tokens(updated_at);

-- Row Level Security
ALTER TABLE public.bing_tokens ENABLE ROW LEVEL SECURITY;

-- Only service role can read/write tokens (never expose to client)
-- The anon/authenticated roles get NO access — only Edge Functions with service role can use these.
-- Idempotent: skip if policy already exists
DO $bing_tokens_policy$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE schemaname = 'public'
        AND tablename = 'bing_tokens'
        AND policyname = 'Service role only'
    ) THEN
        CREATE POLICY "Service role only" ON public.bing_tokens
            FOR ALL
            TO service_role
            USING (true)
            WITH CHECK (true);
    END IF;
END
$bing_tokens_policy$;

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_bing_tokens_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS bing_tokens_updated_at ON public.bing_tokens;
CREATE TRIGGER bing_tokens_updated_at BEFORE UPDATE ON public.bing_tokens
    FOR EACH ROW EXECUTE FUNCTION update_bing_tokens_updated_at();