import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

// GET /api/clients/[slug] — get single client with vault content
export async function GET(
  _request: Request,
  { params }: { params: { slug: string } }
) {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const { data, error } = await supabase
      .from("clients")
      .select("*")
      .eq("slug", params.slug)
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    if (!data) {
      return NextResponse.json({ error: "Client not found" }, { status: 404 });
    }
    return NextResponse.json({ client: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

// PATCH /api/clients/[slug] — update client vault or other fields
export async function PATCH(
  request: Request,
  { params }: { params: { slug: string } }
) {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const body = await request.json();
    const { vault_content, ...otherFields } = body;

    const updates: any = { ...otherFields };
    if (vault_content !== undefined) {
      updates.vault_content = vault_content;
    }

    const { data, error } = await supabase
      .from("clients")
      .update(updates)
      .eq("slug", params.slug)
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    return NextResponse.json({ client: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
