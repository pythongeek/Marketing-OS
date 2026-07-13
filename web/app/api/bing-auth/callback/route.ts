/**
 * Bing Webmaster OAuth 2.0 callback.
 * Receives the authorization code from Microsoft, exchanges it for tokens,
 * and stores them in Supabase for long-term use.
 */
import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";
import { cookies } from "next/headers";
import { randomBytes } from "crypto";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const error = url.searchParams.get("error");

  let clientId = process.env.BING_CLIENT_ID;
  if (clientId && clientId.length === 32 && !clientId.includes("-")) {
    clientId = `${clientId.slice(0, 8)}-${clientId.slice(8, 12)}-${clientId.slice(12, 16)}-${clientId.slice(16, 20)}-${clientId.slice(20)}`;
  }
  const clientSecret = process.env.BING_CLIENT_SECRET;
  const redirectUri = process.env.BING_REDIRECT_URI;
  const tenant = process.env.BING_TENANT || "common";

  if (error) {
    return NextResponse.json(
      { error: `Microsoft returned error: ${error}`, description: url.searchParams.get("error_description") },
      { status: 400 }
    );
  }

  if (!code || !state) {
    return NextResponse.json({ error: "Missing code or state" }, { status: 400 });
  }

  // Verify state token (CSRF protection)
  const cookieStore = cookies();
  const storedState = cookieStore.get("bing_oauth_state")?.value;
  if (!storedState || storedState !== state) {
    return NextResponse.json({ error: "State mismatch - possible CSRF attack" }, { status: 400 });
  }

  // Clear the state cookie
  cookieStore.delete("bing_oauth_state");

  // Exchange authorization code for tokens
  const tokenUrl = `https://login.microsoftonline.com/${tenant}/oauth2/v2.0/token`;
  const tokenBody = new URLSearchParams({
    client_id: clientId!,
    client_secret: clientSecret!,
    code,
    redirect_uri: redirectUri!,
    grant_type: "authorization_code",
  });

  try {
    const tokenResp = await fetch(tokenUrl, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: tokenBody.toString(),
    });

    if (!tokenResp.ok) {
      const errText = await tokenResp.text();
      return NextResponse.json(
        { error: "Token exchange failed", details: errText },
        { status: 500 }
      );
    }

    const tokens = await tokenResp.json();
    // Expected fields: access_token, refresh_token, expires_in, scope, token_type

    // Store tokens in Supabase (encrypted at rest via RLS)
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
    if (!supabaseUrl || !supabaseKey) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 500 });
    }

    const supabase = createClient(supabaseUrl, supabaseKey);

    const expiresAt = new Date(Date.now() + (tokens.expires_in || 3600) * 1000).toISOString();

    const { error: dbError } = await supabase
      .from("bing_tokens")
      .upsert({
        id: "default", // single-row config
        access_token: tokens.access_token,
        refresh_token: tokens.refresh_token,
        expires_at: expiresAt,
        scope: tokens.scope,
        token_type: tokens.token_type,
        updated_at: new Date().toISOString(),
      }, { onConflict: "id" });

    if (dbError) {
      return NextResponse.json(
        { error: "Failed to store tokens", details: dbError.message },
        { status: 500 }
      );
    }

    // Redirect to admin success page
    return NextResponse.redirect(
      new URL("/credentials?bing_oauth=success", request.url)
    );
  } catch (e) {
    return NextResponse.json(
      { error: "OAuth callback failed", details: String(e) },
      { status: 500 }
    );
  }
}