-- Migration 009: Fix duplicate policies from partial runs
-- ===========================================================
-- Previous failed runs of migrations 007 and 008 left orphaned
-- policies. Drop them so the migrations can complete cleanly.
-- Also makes future re-runs of 007 and 008 safe (idempotent).

DROP POLICY IF EXISTS "Users can read credentials" ON public.credentials;
DROP POLICY IF EXISTS "Editors can manage credentials" ON public.credentials;
DROP POLICY IF EXISTS "Service role only" ON public.bing_tokens;

-- Verify drops succeeded
DO $verify_drops$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_policies
        WHERE schemaname = 'public'
        AND tablename IN ('credentials', 'bing_tokens')
    ) THEN
        RAISE NOTICE 'Some policies remain — check manually: %',
            (SELECT string_agg(tablename || '.' || policyname, ', ')
             FROM pg_policies
             WHERE schemaname = 'public'
             AND tablename IN ('credentials', 'bing_tokens'));
    ELSE
        RAISE NOTICE 'All orphaned policies dropped. Safe to re-run 007 and 008.';
    END IF;
END
$verify_drops$;