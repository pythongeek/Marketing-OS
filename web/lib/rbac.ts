/**
 * AMP API Middleware — RBAC for Next.js App Router
 * =================================================
 * Checks user role on API routes. Used in route handlers.
 *
 * Usage:
 *   import { withRole } from "@/lib/rbac";
 *   export const GET = withRole(["admin", "editor"], async (request) => { ... });
 */

import { createClient } from "@supabase/supabase-js";
import { NextResponse } from "next/server";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const ROLE_LEVELS: Record<string, number> = { viewer: 0, editor: 1, admin: 2 };

export interface AuthUser {
  id: string;
  role: string;
  email: string;
  display_name?: string;
}

export function withRole(
  allowedRoles: string[],
  handler: (request: Request, user: AuthUser) => Promise<Response>,
) {
  return async (request: Request): Promise<Response> => {
    // Extract Bearer token from Authorization header
    const authHeader = request.headers.get("Authorization") || "";
    const token = authHeader.replace("Bearer ", "").trim();

    if (!token) {
      return NextResponse.json({ error: "Authentication required" }, { status: 401 });
    }

    try {
      // Validate token with Supabase Auth
      const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
        auth: { autoRefreshToken: false, persistSession: false },
      });

      const { data: authData, error: authError } = await supabase.auth.getUser(token);
      if (authError || !authData.user) {
        return NextResponse.json({ error: "Invalid or expired token" }, { status: 401 });
      }

      const userId = authData.user.id;

      // Fetch role from our users table (service role to bypass RLS)
      const serviceSupabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY, {
        auth: { autoRefreshToken: false, persistSession: false },
      });

      const { data: userData, error: userError } = await serviceSupabase
        .from("users")
        .select("role, display_name")
        .eq("id", userId)
        .single();

      if (userError || !userData) {
        return NextResponse.json({ error: "User profile not found" }, { status: 403 });
      }

      const userRole = userData.role || "viewer";
      const requiredLevel = Math.max(...allowedRoles.map((r) => ROLE_LEVELS[r] ?? 0));
      const userLevel = ROLE_LEVELS[userRole] ?? 0;

      if (userLevel < requiredLevel) {
        return NextResponse.json(
          {
            error: "Insufficient permissions",
            required: allowedRoles,
            your_role: userRole,
          },
          { status: 403 },
        );
      }

      // Attach user info and call handler
      const user: AuthUser = {
        id: userId,
        role: userRole,
        email: authData.user.email || "",
        display_name: userData.display_name || "",
      };

      return await handler(request, user);
    } catch (err: any) {
      console.error("RBAC middleware error:", err);
      return NextResponse.json({ error: "Auth validation failed", detail: err.message }, { status: 500 });
    }
  };
}

// Convenience exports with proper typing
export const requireAdmin = (handler: (request: Request, user?: AuthUser) => Promise<Response>) =>
  withRole(["admin"], handler);

export const requireEditor = (handler: (request: Request, user?: AuthUser) => Promise<Response>) =>
  withRole(["admin", "editor"], handler);

export const requireViewer = (handler: (request: Request, user?: AuthUser) => Promise<Response>) =>
  withRole(["admin", "editor", "viewer"], handler);
