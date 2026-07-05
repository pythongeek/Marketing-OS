-- Phase 4 Migration (Part B): Cron Schedule Setup
-- =================================================
-- Sets up the scheduled job that triggers the Edge Function every 5 minutes.
-- NOTE: pg_cron requires at least the Pro plan on Supabase.
-- Free tier: Use the Supabase Dashboard → Database → Cron Jobs instead.

-- ── Enable pg_cron extension (may require Pro plan) ────────────────
-- Uncomment if your plan supports it:
-- CREATE EXTENSION IF NOT EXISTS pg_cron;

-- ── Schedule the Edge Function trigger ─────────────────────────────
-- This calls the Edge Function via HTTP every 5 minutes.
-- Replace <project-ref> and <anon-key> with your actual values.

DO $$
DECLARE
    project_ref TEXT := 'pusttdxrtmgvhdzdyvbd';
    anon_key TEXT := '<your-anon-key>';  -- Replace with actual anon key
BEGIN
    -- Only schedule if pg_cron is available
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_cron') THEN
        PERFORM cron.unschedule('amp-execute-jobs');
        PERFORM cron.schedule(
            'amp-execute-jobs',
            '*/5 * * * *',
            format(
                $$SELECT net.http_post(
                    url:='https://%s.supabase.co/functions/v1/execute-jobs',
                    headers:='{"Authorization": "Bearer %s", "Content-Type": "application/json"}'::jsonb
                )$$,
                project_ref,
                anon_key
            )
        );
        RAISE NOTICE 'pg_cron job scheduled successfully.';
    ELSE
        RAISE NOTICE 'pg_cron not available. Please set up via Supabase Dashboard or use the local poller.';
    END IF;
END $$;

-- ── Alternative: Manual trigger function ───────────────────────────
-- Call this function manually or from an external cron service:
CREATE OR REPLACE FUNCTION public.trigger_execute_jobs()
RETURNS void AS $$
DECLARE
    response JSONB;
BEGIN
    SELECT content::jsonb INTO response
    FROM http(('
        GET',
        'https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs',
        ARRAY[
            http_header('Authorization', 'Bearer <anon-key>'),
            http_header('Content-Type', 'application/json')
        ],
        '',
        5000
    )::http_request);
    
    RAISE NOTICE 'Edge Function response: %', response;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
