import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET(request: Request, { params }: { params: { id: string } }) {
  try {
    if (!supabase) {
      return NextResponse.json(
        { error: "Supabase not configured. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in Vercel Environment Variables." },
        { status: 503 }
      );
    }
    const { data, error } = await supabase
      .from("agent_logs")
      .select("*")
      .eq("job_id", params.id)
      .order("created_at", { ascending: true });

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ logs: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function POST(request: Request, { params }: { params: { id: string } }) {
  try {
    if (!supabase) {
      return NextResponse.json(
        { error: "Supabase not configured. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in Vercel Environment Variables." },
        { status: 503 }
      );
    }
    const body = await request.json();
    const { level, message, metadata = {} } = body;

    const { data, error } = await supabase
      .from("agent_logs")
      .insert({
        job_id: params.id,
        level: level || "info",
        message,
        metadata,
      })
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ log: data }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
