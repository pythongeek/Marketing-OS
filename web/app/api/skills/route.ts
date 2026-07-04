import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";
import { withRole, requireAdmin, requireEditor } from "@/lib/rbac";

export const dynamic = "force-dynamic";

// GET /api/skills — any authenticated user
export const GET = withRole(["viewer", "editor", "admin"], async () => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const { data, error } = await supabase
      .from("skills")
      .select("*")
      .order("name", { ascending: true });

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    return NextResponse.json({ skills: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
});

// PUT /api/skills — editors and admins can update skill instructions
export const PUT = requireEditor(async (request: Request) => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const body = await request.json();
    const { id, instructions, config } = body;

    const { data, error } = await supabase
      .from("skills")
      .update({ instructions, config, last_updated: new Date().toISOString() })
      .eq("id", id)
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    return NextResponse.json({ skill: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
});
