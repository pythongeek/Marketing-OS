-- Phase 4 Migration (Part A): Edge Function Schema
-- =================================================
-- Ensures all columns the Edge Function writes to exist.
-- Run this BEFORE deploying the Edge Function.

-- ── Ensure jobs table has all columns Edge Function needs ──────────
ALTER TABLE public.jobs
    ADD COLUMN IF NOT EXISTS started_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS completed_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS parent_job_id UUID REFERENCES public.jobs(id),
    ADD COLUMN IF NOT EXISTS logs JSONB DEFAULT '[]'::jsonb;

-- ── Ensure agent_logs table exists (if schema.sql was not applied) ─
CREATE TABLE IF NOT EXISTS public.agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES public.jobs(id) ON DELETE CASCADE,
    level TEXT NOT NULL CHECK (level IN ('debug', 'info', 'warning', 'error', 'success')),
    message TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Ensure qa-check skill exists ───────────────────────────────────
INSERT INTO public.skills (slug, name, description, category, status, instructions)
VALUES (
    'qa-check',
    'QA Pipeline Gate',
    'Binary and scored quality checks on content artifacts. Binary failures (legal, plagiarism) block deliverability. Scored checks log warnings.',
    'governance',
    'active',
    'You are a QA gatekeeper. Run binary checks (legal risk, plagiarism) that BLOCK deliverability if failed. Run scored checks (grammar, tone, brand voice) that log warnings but allow passage. Be strict on binary checks, lenient on scored checks.'
)
ON CONFLICT (slug) DO NOTHING;

-- ── Indexes for performance ────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_jobs_status_created ON public.jobs(status, created_at);
CREATE INDEX IF NOT EXISTS idx_jobs_parent ON public.jobs(parent_job_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_job_id ON public.agent_logs(job_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_created ON public.agent_logs(created_at);
