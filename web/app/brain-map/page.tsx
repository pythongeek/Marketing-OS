"use client";

import { Nav } from "@/components/nav";
import { Brain } from "lucide-react";

export default function BrainMapPage() {
  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-text">Brain Map</h1>
          <p className="text-muted text-sm mt-1">Interactive force-directed graph of all vault entities</p>
        </div>
        <div className="bg-card border border-border rounded-xl overflow-hidden" style={{ height: "calc(100vh - 200px)" }}>
          <iframe
            src="/AgenticMarketingPro-Vault/00-Agency-Core/_dashboards/brain-map.html"
            className="w-full h-full border-0"
            title="Brain Map"
          />
        </div>
      </main>
    </div>
  );
}
