-- Phase 2 Governance Migration
-- Adds parent_job_id for QA pipeline linkage

ALTER TABLE public.jobs
    ADD COLUMN IF NOT EXISTS parent_job_id UUID REFERENCES public.jobs(id);

CREATE INDEX IF NOT EXISTS idx_jobs_parent ON public.jobs(parent_job_id);

-- Add qa-check skill (if not exists)
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
