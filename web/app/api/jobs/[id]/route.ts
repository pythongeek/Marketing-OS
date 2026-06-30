import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET(request: Request, { params }: { params: { id: string } }) {
  try {
    const { data, error } = await supabase
      .from("jobs")
      .select("*")
      .eq("id", params.id)
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ job: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function PATCH(request: Request, { params }: { params: { id: string } }) {
  try {
    const body = await request.json();
    const { status, result, logs, cost_usd, tokens_in, tokens_out } = body;

    const updates: any = {};
    if (status) updates.status = status;
    if (result) updates.result = result;
    if (logs) updates.logs = logs;
    if (cost_usd !== undefined) updates.cost_usd = cost_usd;
    if (tokens_in !== undefined) updates.tokens_in = tokens_in;
    if (tokens_out !== undefined) updates.tokens_out = tokens_out;
    if (status === "running") updates.started_at = new Date().toISOString();
    if (status === "completed" || status === "failed") updates.completed_at = new Date().toISOString();

    const { data, error } = await supabase
      .from("jobs")
      .update(updates)
      .eq("id", params.id)
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ job: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
