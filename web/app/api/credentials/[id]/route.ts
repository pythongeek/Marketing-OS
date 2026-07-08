import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";
import { requireEditor } from "@/lib/rbac";

export const dynamic = "force-dynamic";

// ─────────────────────────────────────────────────────────────────────────────
// GET /api/credentials/[id] — get a single credential (secrets stripped)
// ─────────────────────────────────────────────────────────────────────────────
export async function GET(
  _request: Request,
  { params }: { params: { id: string } }
) {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }

    const { data, error } = await supabase
      .from("credentials")
      .select("*")
      .eq("id", params.id)
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    if (!data) {
      return NextResponse.json({ error: "Credential not found" }, { status: 404 });
    }

    // Return safe version (no secrets)
    return NextResponse.json({
      credential: {
        id: data.id,
        client_slug: data.client_slug,
        service: data.service,
        label: data.label,
        config: data.config,
        is_active: data.is_active,
        last_tested_at: data.last_tested_at,
        test_status: data.test_status,
        test_error: data.test_error,
        created_at: data.created_at,
        updated_at: data.updated_at,
        has_secrets: data.secrets && Object.keys(data.secrets).length > 0,
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// PATCH /api/credentials/[id] — update credential config/label/active status
// ─────────────────────────────────────────────────────────────────────────────
export const PATCH = requireEditor(async (request: Request, { params }: { params: { id: string } }) => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }

    const body = await request.json();
    const { label, config, secrets, is_active } = body;

    const updates: any = {};
    if (label !== undefined) updates.label = label;
    if (config !== undefined) updates.config = config;
    if (secrets !== undefined) updates.secrets = secrets;
    if (is_active !== undefined) updates.is_active = is_active;

    const { data, error } = await supabase
      .from("credentials")
      .update(updates)
      .eq("id", params.id)
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    if (!data) {
      return NextResponse.json({ error: "Credential not found" }, { status: 404 });
    }

    return NextResponse.json({
      credential: {
        id: data.id,
        client_slug: data.client_slug,
        service: data.service,
        label: data.label,
        config: data.config,
        is_active: data.is_active,
        updated_at: data.updated_at,
        has_secrets: data.secrets && Object.keys(data.secrets).length > 0,
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// DELETE /api/credentials/[id] — delete a credential
// ─────────────────────────────────────────────────────────────────────────────
export const DELETE = requireEditor(async (_request: Request, { params }: { params: { id: string } }) => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }

    const { error } = await supabase
      .from("credentials")
      .delete()
      .eq("id", params.id);

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ success: true, message: "Credential deleted" });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
});
