import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";
import { withRole, requireAdmin, requireEditor } from "@/lib/rbac";

export const dynamic = "force-dynamic";

// GET /api/jobs — any authenticated user (viewer+)
export const GET = withRole(["viewer", "editor", "admin"], async () => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const { data, error } = await supabase
      .from("jobs")
      .select("*, clients(name), skills(name)")
      .order("created_at", { ascending: false })
      .limit(100);

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    return NextResponse.json({ jobs: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
});

// POST /api/jobs — editors and admins can create jobs
export const POST = requireEditor(async (request: Request) => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const body = await request.json();
    const { type, client_slug, skill_slug, payload = {} } = body;

    const { data, error } = await supabase
      .from("jobs")
      .insert({
        type,
        client_slug: client_slug || null,
        skill_slug: skill_slug || null,
        payload,
        status: "pending",
      })
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    return NextResponse.json({ job: data }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
});
