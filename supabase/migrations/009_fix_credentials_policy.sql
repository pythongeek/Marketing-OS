-- Migration 009: Fix duplicate policy on credentials table
-- ===========================================================
-- The "Users can read credentials" policy was created in a previous
-- failed run. Drop it before recreating to make migration idempotent.

DROP POLICY IF EXISTS "Users can read credentials" ON public.credentials;
DROP POLICY IF EXISTS "Editors can manage credentials" ON public.credentials;

-- Now safe to re-run migration 007 policies
-- (CREATE POLICY statements will be added below if they don't exist)

DO $$
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
END $$;