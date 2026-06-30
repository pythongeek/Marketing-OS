CREATE TABLE public.clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    website TEXT,
    industry TEXT,
    tier TEXT,
    mrr INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    target_geo TEXT,
    primary_language TEXT DEFAULT 'en',
    business_goal_1 TEXT,
    business_goal_2 TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    status TEXT DEFAULT 'active',
    instructions TEXT,
    config JSONB DEFAULT '{}',
    last_updated TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_slug TEXT REFERENCES public.clients(slug),
    skill_slug TEXT REFERENCES public.skills(slug),
    type TEXT NOT NULL,
    payload JSONB DEFAULT '{}',
    status TEXT DEFAULT 'pending',
    result JSONB,
    logs TEXT[],
    cost_usd NUMERIC(10,4) DEFAULT 0,
    tokens_in INTEGER DEFAULT 0,
    tokens_out INTEGER DEFAULT 0,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES public.jobs(id),
    client_slug TEXT,
    skill_slug TEXT,
    level TEXT DEFAULT 'info',
    message TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.form_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    form_type TEXT NOT NULL,
    client_slug TEXT,
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.kpis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_slug TEXT REFERENCES public.clients(slug),
    metric_name TEXT NOT NULL,
    metric_value NUMERIC,
    target_value NUMERIC,
    unit TEXT,
    period TEXT,
    recorded_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_jobs_status ON public.jobs(status);
CREATE INDEX idx_jobs_client ON public.jobs(client_slug);
CREATE INDEX idx_jobs_skill ON public.jobs(skill_slug);
CREATE INDEX idx_jobs_created ON public.jobs(created_at);
CREATE INDEX idx_logs_job ON public.agent_logs(job_id);
CREATE INDEX idx_logs_client ON public.agent_logs(client_slug);
CREATE INDEX idx_kpis_client_metric ON public.kpis(client_slug, metric_name);
CREATE INDEX idx_form_responses_type ON public.form_responses(form_type);

ALTER PUBLICATION supabase_realtime ADD TABLE public.jobs;
ALTER PUBLICATION supabase_realtime ADD TABLE public.agent_logs;

ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.form_responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kpis ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all" ON public.clients FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.skills FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.jobs FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.agent_logs FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.form_responses FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.kpis FOR ALL USING (true);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER clients_updated_at BEFORE UPDATE ON public.clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER skills_updated_at BEFORE UPDATE ON public.skills
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER jobs_updated_at BEFORE UPDATE ON public.jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
