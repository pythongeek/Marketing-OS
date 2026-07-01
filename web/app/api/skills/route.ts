import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    if (!supabase) {
      return NextResponse.json(
        { error: "Supabase not configured. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in Vercel Environment Variables." },
        { status: 503 }
      );
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
}

export async function PUT(request: Request) {
  try {
    if (!supabase) {
      return NextResponse.json(
        { error: "Supabase not configured. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in Vercel Environment Variables." },
        { status: 503 }
      );
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
}
