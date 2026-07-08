import { NextResponse } from "next/server";
import { readFileSync, existsSync } from "fs";
import { join } from "path";

export const dynamic = "force-dynamic";

// GET /api/clients/[slug]/vault — read vault from local filesystem
export async function GET(
  _request: Request,
  { params }: { params: { slug: string } }
) {
  try {
    const vaultDir = join(process.cwd(), "..", "AgenticMarketingPro-Vault", "01-Clients", params.slug);
    
    // Check if vault directory exists
    if (!existsSync(vaultDir)) {
      return NextResponse.json({ error: "Vault not found" }, { status: 404 });
    }

    // Read all markdown files in the vault directory
    const vaultContent: Record<string, string> = {};
    
    const files = [
      "client-profile.md",
      "onboarding.md",
      "strategy-90-day.md",
      "kpis-and-goals.md",
      "website-manifest.md",
      "competitor-watch.md",
      "campaign-log.md",
      "technical-fix-queue.md",
    ];

    for (const file of files) {
      const filePath = join(vaultDir, file);
      if (existsSync(filePath)) {
        const content = readFileSync(filePath, "utf-8");
        // Map filename to tab key
        const tabKey = file.replace(".md", "");
        vaultContent[tabKey] = content;
      }
    }

    return NextResponse.json({ vault: vaultContent });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
