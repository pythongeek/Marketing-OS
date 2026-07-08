import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";
import { generateVaultContent } from "@/lib/vault-generator";

export const dynamic = "force-dynamic";

// POST /api/clients/[slug]/generate-vault — generate vault for existing client
export async function POST(
  _request: Request,
  { params }: { params: { slug: string } }
) {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }

    // Fetch client
    const { data: client, error: fetchError } = await supabase
      .from("clients")
      .select("*")
      .eq("slug", params.slug)
      .single();

    if (fetchError || !client) {
      return NextResponse.json({ error: "Client not found" }, { status: 404 });
    }

    // Generate vault content
    const vaultContent = generateVaultContent({
      slug: client.slug,
      name: client.name,
      website: client.website,
      industry: client.industry,
      tier: client.tier,
      mrr: client.mrr,
      target_geo: client.target_geo,
      primary_language: client.primary_language,
      business_goal_1: client.business_goal_1,
      business_goal_2: client.business_goal_2,
      business_goal_3: client.business_goal_3,
      contact_name: client.contact_name,
      contact_email: client.contact_email,
      contact_phone: client.contact_phone,
      status: client.status,
    });

    // Update client with vault content
    const { data: updated, error: updateError } = await supabase
      .from("clients")
      .update({ vault_content: vaultContent })
      .eq("slug", params.slug)
      .select()
      .single();

    if (updateError) {
      return NextResponse.json({ error: updateError.message }, { status: 500 });
    }

    return NextResponse.json({ client: updated });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
