import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";
import { requireEditor } from "@/lib/rbac";
import { generateVaultContent } from "@/lib/vault-generator";

export const dynamic = "force-dynamic";

// GET /api/clients — public (no auth required)
export async function GET() {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const { data, error } = await supabase
      .from("clients")
      .select("*")
      .order("name", { ascending: true });

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    return NextResponse.json({ clients: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

// POST /api/clients — editors and admins only (RBAC protected)
export const POST = requireEditor(async (request: Request) => {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }
    const body = await request.json();
    const { slug, name, website, industry, tier, mrr, target_geo, primary_language, business_goal_1, business_goal_2, business_goal_3, contact_name, contact_email, contact_phone } = body;

    // Generate vault content from templates
    const vaultContent = generateVaultContent({
      slug,
      name,
      website,
      industry,
      tier,
      mrr,
      target_geo,
      primary_language,
      business_goal_1,
      business_goal_2,
      business_goal_3,
      contact_name,
      contact_email,
      contact_phone,
      status: "active",
    });

    const { data, error } = await supabase
      .from("clients")
      .insert({
        slug,
        name,
        website,
        industry,
        tier,
        mrr,
        target_geo,
        primary_language,
        business_goal_1,
        business_goal_2,
        vault_content: vaultContent,
      })
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }
    return NextResponse.json({ client: data }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
});
