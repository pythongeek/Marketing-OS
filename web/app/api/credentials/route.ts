import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";
import { requireEditor } from "@/lib/rbac";

export const dynamic = "force-dynamic";

// ─────────────────────────────────────────────────────────────────────────────
// GET /api/credentials — list all credentials (optionally filter by client/service)
// ─────────────────────────────────────────────────────────────────────────────
export async function GET(request: Request) {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }

    const { searchParams } = new URL(request.url);
    const clientSlug = searchParams.get("client");
    const service = searchParams.get("service");

    let query = supabase.from("credentials").select("*").order("created_at", { ascending: false });

    if (clientSlug) {
      query = query.eq("client_slug", clientSlug);
    }
    if (service) {
      query = query.eq("service", service);
    }

    const { data, error } = await query;

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    // Strip secrets from the response — never send them to the client
    const safeData = (data || []).map((cred: any) => ({
      id: cred.id,
      client_slug: cred.client_slug,
      service: cred.service,
      label: cred.label,
      config: cred.config,
      is_active: cred.is_active,
      last_tested_at: cred.last_tested_at,
      test_status: cred.test_status,
      test_error: cred.test_error,
      created_at: cred.created_at,
      updated_at: cred.updated_at,
      // secrets are intentionally OMITTED
      has_secrets: cred.secrets && Object.keys(cred.secrets).length > 0,
    }));

    return NextResponse.json({ credentials: safeData });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/credentials — create a new credential (editor/admin only)
// ─────────────────────────────────────────────────────────────────────────────
export const POST = requireEditor(async (request: Request) => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }

    const body = await request.json();
    const {
      client_slug,
      service,
      label,
      config = {},
      secrets = {},
    } = body;

    if (!service) {
      return NextResponse.json({ error: "Missing required field: service" }, { status: 400 });
    }

    const { data, error } = await supabase
      .from("credentials")
      .insert({
        client_slug: client_slug || null,
        service,
        label: label || `${service} credential`,
        config,
        secrets,
        is_active: true,
      })
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json(
      {
        credential: {
          id: data.id,
          client_slug: data.client_slug,
          service: data.service,
          label: data.label,
          config: data.config,
          is_active: data.is_active,
          created_at: data.created_at,
          has_secrets: true,
        },
      },
      { status: 201 }
    );
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
});
