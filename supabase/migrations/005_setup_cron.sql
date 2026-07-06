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
-- Using the actual Supabase anon key for the Edge Function.

DO $$
BEGIN
    -- Only schedule if pg_cron is available
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_cron') THEN
        PERFORM cron.unschedule('amp-execute-jobs');
        PERFORM cron.schedule(
            'amp-execute-jobs',
            '*/5 * * * *',
            'SELECT net.http_post(''
                https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs'',
                ''{"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MzkwNDQsImV4cCI6MjA5ODQxNTA0NH0.czorJe8WQ2mLliNQqHraU2E3Tqor7lE0hYaksLRPwmU", "Content-Type": "application/json"}''::jsonb
            )'
        );
        RAISE NOTICE 'pg_cron job scheduled successfully.';
    ELSE
        RAISE NOTICE 'pg_cron not available. Please set up via Supabase Dashboard or use the local poller.';
    END IF;
END $$;

-- ── Alternative: Manual trigger function ───────────────────────────
-- Call this function manually or from an external cron service.
-- Requires: CREATE EXTENSION IF NOT EXISTS http;
CREATE OR REPLACE FUNCTION public.trigger_execute_jobs()
RETURNS void AS $$
DECLARE
    response JSONB;
BEGIN
    SELECT content::jsonb INTO response
    FROM net.http_post(
        url := 'https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs',
        headers := '{"Authorization": "Bearer <your-anon-key>", "Content-Type": "application/json"}'::jsonb
    );
    
    RAISE NOTICE 'Edge Function response: %', response;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
