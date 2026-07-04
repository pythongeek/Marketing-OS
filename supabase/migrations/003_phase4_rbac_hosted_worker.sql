-- Phase 4 Migration: RBAC + Hosted Worker
-- ========================================

-- ── Users table (extends Supabase Auth) ────────────────────────────
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    role TEXT NOT NULL DEFAULT 'viewer' CHECK (role IN ('admin', 'editor', 'viewer')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'suspended')),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ── User roles RLS ─────────────────────────────────────────────────
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Admins can manage all users" ON public.users
    FOR ALL USING (
        EXISTS (SELECT 1 FROM public.users WHERE id = auth.uid() AND role = 'admin')
    );

-- ── Trigger: auto-create user record on signup ─────────────────────
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, display_name, role)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
        COALESCE(NEW.raw_user_meta_data->>'role', 'viewer')
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ── API keys for service-to-service auth ───────────────────────────
CREATE TABLE IF NOT EXISTS public.api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    key_hash TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL DEFAULT 'service' CHECK (role IN ('service', 'webhook', 'cron')),
    created_by UUID REFERENCES public.users(id),
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    revoked_at TIMESTAMPTZ
);

-- ── Add user tracking to jobs ──────────────────────────────────────
ALTER TABLE public.jobs
    ADD COLUMN IF NOT EXISTS created_by UUID REFERENCES public.users(id),
    ADD COLUMN IF NOT EXISTS assigned_to UUID REFERENCES public.users(id);

-- ── pg_cron job to trigger edge function ──────────────────────────
-- This replaces the local laptop poller. Runs every 5 minutes.
-- Requires: CREATE EXTENSION pg_cron; (in Supabase dashboard)

DO $$
BEGIN
    -- Unschedule if exists (idempotent)
    PERFORM cron.unschedule('amp-execute-jobs');
EXCEPTION WHEN OTHERS THEN
    -- cron extension may not be available
    NULL;
END $$;

-- Note: The actual cron schedule is set via Supabase Dashboard or CLI:
-- SELECT cron.schedule('amp-execute-jobs', '*/5 * * * *', 
--   $$ SELECT net.http_post(
--        url:='https://<project-ref>.supabase.co/functions/v1/execute-jobs',
--        headers:='{"Authorization": "Bearer <anon-key>", "Content-Type": "application/json"}'::jsonb
--      ) $$);

-- ── Index for user queries ────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_jobs_created_by ON public.jobs(created_by);
CREATE INDEX IF NOT EXISTS idx_jobs_assigned_to ON public.jobs(assigned_to);
