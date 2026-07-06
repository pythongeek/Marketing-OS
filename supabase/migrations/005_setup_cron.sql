-- Phase 4 Migration (Part B): Manual Trigger Function
-- =====================================================
-- Creates a function to manually trigger the Edge Function.
-- Primary cron is handled by cron-job.org (job 8023152).
-- This function is for manual testing or fallback.

-- Drop existing function first (return type changed from void to text)
DROP FUNCTION IF EXISTS public.trigger_execute_jobs() CASCADE;

-- ── Manual trigger function ────────────────────────────────────────
-- Call with: SELECT public.trigger_execute_jobs();
CREATE OR REPLACE FUNCTION public.trigger_execute_jobs()
RETURNS text AS $func$
DECLARE
    response text;
BEGIN
    SELECT content INTO response
    FROM net.http_post(
        url := 'https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs',
        headers := '{"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MzkwNDQsImV4cCI6MjA5ODQxNTA0NH0.czorJe8WQ2mLliNQqHraU2E3Tqor7lE0hYaksLRPwmU", "Content-Type": "application/json"}'::jsonb
    );
    RETURN response;
END;
$func$ LANGUAGE plpgsql SECURITY DEFINER;

-- ── Grant execute to authenticated users ───────────────────────────
GRANT EXECUTE ON FUNCTION public.trigger_execute_jobs() TO authenticated;
GRANT EXECUTE ON FUNCTION public.trigger_execute_jobs() TO anon;

COMMENT ON FUNCTION public.trigger_execute_jobs() IS 'Manually trigger the AMP Edge Function. Primary scheduling is via cron-job.org job 8023152.';
