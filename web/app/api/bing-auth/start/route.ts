/**
 * Initiate Bing Webmaster OAuth 2.0 authorization flow.
 * Redirects the user to Microsoft's login page.
 */
import { NextResponse } from "next/server";
import { randomBytes } from "crypto";

export const dynamic = "force-dynamic";

export async function GET() {
  const clientId = process.env.BING_CLIENT_ID;
  const redirectUri = process.env.BING_REDIRECT_URI;
  const tenant = process.env.BING_TENANT || "common";

  if (!clientId || !redirectUri) {
    return NextResponse.json(
      { error: "BING_CLIENT_ID or BING_REDIRECT_URI not configured" },
      { status: 500 }
    );
  }

  // Generate state token to prevent CSRF
  const state = randomBytes(16).toString("hex");

  // Microsoft identity platform v2.0 authorize endpoint
  const authUrl = new URL(`https://login.microsoftonline.com/${tenant}/oauth2/v2.0/authorize`);
  authUrl.searchParams.set("client_id", clientId);
  authUrl.searchParams.set("response_type", "code");
  authUrl.searchParams.set("redirect_uri", redirectUri);
  authUrl.searchParams.set("response_mode", "query");
  authUrl.searchParams.set("scope", "https://api.bing.microsoft.com/webmaster.readwrite offline_access");
  authUrl.searchParams.set("state", state);

  // Store state in a short-lived cookie so we can verify on callback
  const response = NextResponse.redirect(authUrl.toString());
  response.cookies.set("bing_oauth_state", state, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 600, // 10 minutes
    path: "/",
  });

  return response;
}