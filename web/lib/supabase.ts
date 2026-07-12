import { createClient, type Session } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

// Type-safe client (returns null only when env vars missing)
export const supabase = supabaseUrl && supabaseKey
  ? createClient(supabaseUrl, supabaseKey)
  : null;

export type SupabaseClient = NonNullable<typeof supabase>;

export type Client = {
  id: string;
  slug: string;
  name: string;
  website: string | null;
  industry: string | null;
  tier: string | null;
  mrr: number;
  status: string;
  target_geo: string | null;
  primary_language: string;
  business_goal_1: string | null;
  business_goal_2: string | null;
  created_at: string;
  updated_at: string;
};

export type Skill = {
  id: string;
  slug: string;
  name: string;
  description: string | null;
  category: string | null;
  status: string;
  instructions: string | null;
  config: Record<string, unknown>;
  last_updated: string;
  created_at: string;
};

export type Job = {
  id: string;
  client_slug: string | null;
  skill_slug: string | null;
  type: string;
  payload: Record<string, unknown>;
  status: string;
  result: Record<string, unknown> | null;
  logs: string[] | null;
  cost_usd: number;
  tokens_in: number;
  tokens_out: number;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
};

export type AgentLog = {
  id: string;
  job_id: string | null;
  client_slug: string | null;
  skill_slug: string | null;
  level: string;
  message: string;
  metadata: Record<string, unknown>;
  created_at: string;
};
