"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { signIn, user } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirect") || "/credentials";

  if (user) {
    router.push(redirectTo);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const result = await signIn(email, password);
    setLoading(false);
    if (result.error) {
      setError(result.error);
    } else {
      router.push(redirectTo);
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
      padding: "20px",
    }}>
      <div style={{
        background: "white",
        borderRadius: "16px",
        padding: "40px",
        maxWidth: "420px",
        width: "100%",
        boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
      }}>
        <h1 style={{
          margin: "0 0 8px",
          fontSize: "24px",
          fontWeight: 800,
          color: "#1a1a2e",
        }}>
          AgenticMarketingPro
        </h1>
        <p style={{
          margin: "0 0 32px",
          fontSize: "14px",
          color: "#636e72",
        }}>
          Sign in to manage credentials and integrations.
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "16px" }}>
            <label style={{
              display: "block",
              marginBottom: "6px",
              fontSize: "13px",
              fontWeight: 600,
              color: "#1a1a2e",
            }}>
              Email
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              style={{
                width: "100%",
                padding: "10px 12px",
                fontSize: "15px",
                border: "1px solid #e0dff8",
                borderRadius: "8px",
                outline: "none",
              }}
            />
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{
              display: "block",
              marginBottom: "6px",
              fontSize: "13px",
              fontWeight: 600,
              color: "#1a1a2e",
            }}>
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              style={{
                width: "100%",
                padding: "10px 12px",
                fontSize: "15px",
                border: "1px solid #e0dff8",
                borderRadius: "8px",
                outline: "none",
              }}
            />
          </div>

          {error && (
            <div style={{
              background: "#ffe5e5",
              border: "1px solid #ff7675",
              borderRadius: "8px",
              padding: "10px 12px",
              marginBottom: "16px",
              fontSize: "13px",
              color: "#c0392b",
            }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "12px",
              fontSize: "15px",
              fontWeight: 700,
              color: "white",
              background: loading ? "#a29bfe" : "#6c5ce7",
              border: "none",
              borderRadius: "8px",
              cursor: loading ? "wait" : "pointer",
            }}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p style={{
          marginTop: "20px",
          fontSize: "12px",
          color: "#636e72",
          textAlign: "center",
        }}>
          Don't have an account? Contact your administrator.
        </p>
      </div>
    </div>
  );
}