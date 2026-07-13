/**
 * Refresh the Bing Webmaster access token.
 * Called automatically by the Bing API client when the access token expires.
 */
import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  let clientId = process.env.BING_CLIENT_ID;
  if (clientId && clientId.length === 32 && !clientId.includes("-")) {
    clientId = `${clientId.slice(0, 8)}-${clientId.slice(8, 12)}-${clientId.slice(12, 16)}-${clientId.slice(16, 20)}-${clientId.slice(20)}`;
  }
  const clientSecret = process.env.BING_CLIENT_SECRET;
  const tenant = process.env.BING_TENANT || "common";

  if (!clientId || !clientSecret) {
    return NextResponse.json(
      { error: "BING_CLIENT_ID or BING_CLIENT_SECRET not configured" },
      { status: 500 }
    );
  }

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!supabaseUrl || !supabaseKey) {
    return NextResponse.json({ error: "Supabase not configured" }, { status: 500 });
  }

  const supabase = createClient(supabaseUrl, supabaseKey);

  // Get current refresh token
  const { data: tokenRow, error: fetchErr } = await supabase
    .from("bing_tokens")
    .select("refresh_token")
    .eq("id", "default")
    .single();

  if (fetchErr || !tokenRow?.refresh_token) {
    return NextResponse.json(
      { error: "No refresh token stored - re-authorize at /api/bing-auth/start" },
      { status: 400 }
    );
  }

  // Exchange refresh token for new access token
  const tokenUrl = `https://login.microsoftonline.com/${tenant}/oauth2/v2.0/token`;
  const body = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    refresh_token: tokenRow.refresh_token,
    grant_type: "refresh_token",
  });

  try {
    const resp = await fetch(tokenUrl, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      return NextResponse.json(
        { error: "Refresh failed", details: errText, status: resp.status },
        { status: 500 }
      );
    }

    const tokens = await resp.json();
    const expiresAt = new Date(Date.now() + (tokens.expires_in || 3600) * 1000).toISOString();

    const { error: updateErr } = await supabase
      .from("bing_tokens")
      .update({
        access_token: tokens.access_token,
        // Microsoft sometimes rotates refresh tokens — use new one if returned
        refresh_token: tokens.refresh_token || tokenRow.refresh_token,
        expires_at: expiresAt,
        scope: tokens.scope || "webmaster.readwrite",
        updated_at: new Date().toISOString(),
      })
      .eq("id", "default");

    if (updateErr) {
      return NextResponse.json(
        { error: "Failed to update tokens", details: updateErr.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      ok: true,
      expires_at: expiresAt,
      refreshed_at: new Date().toISOString(),
    });
  } catch (e) {
    return NextResponse.json(
      { error: "Refresh exception", details: String(e) },
      { status: 500 }
    );
  }
}