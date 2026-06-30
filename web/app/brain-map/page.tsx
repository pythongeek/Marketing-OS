"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { Brain, Users, Wrench, Link2 } from "lucide-react";

export default function BrainMapPage() {
  const [skills, setSkills] = useState<any[]>([]);
  const [clients, setClients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("/api/skills").then((r) => r.json()),
      fetch("/api/clients").then((r) => r.json()),
    ])
      .then(([skillsData, clientsData]) => {
        setSkills(skillsData.skills || []);
        setClients(clientsData.clients || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen">
        <Nav />
        <main className="flex-1 p-8">
          <div className="text-muted">Loading brain map...</div>
        </main>
      </div>
    );
  }

  const colors = ["#4A90D9", "#50C878", "#FFD700", "#E74C3C", "#9B59B6", "#F39C12", "#1ABC9C", "#E67E22"];

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-text">Brain Map</h1>
          <p className="text-muted text-sm mt-1">
            {clients.length} clients × {skills.length} skills = {clients.length * skills.length} possible connections
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Clients column */}
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <Users className="w-4 h-4 text-accent" />
              <h2 className="text-sm font-semibold text-text">Clients</h2>
              <span className="text-xs text-muted ml-auto">{clients.length}</span>
            </div>
            <div className="space-y-2">
              {clients.map((client) => (
                <div
                  key={client.id}
                  className="bg-border/30 rounded-lg p-3 text-sm text-text hover:bg-border/50 transition-colors"
                >
                  <div className="font-medium">{client.name}</div>
                  <div className="text-xs text-muted mt-1">{client.industry || "—"}</div>
                </div>
              ))}
              {clients.length === 0 && (
                <div className="text-xs text-muted text-center py-4">No clients yet</div>
              )}
            </div>
          </div>

          {/* Connections column */}
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <Link2 className="w-4 h-4 text-success" />
              <h2 className="text-sm font-semibold text-text">Connections</h2>
            </div>
            <div className="space-y-3">
              {clients.length > 0 && skills.length > 0 ? (
                <div className="text-xs text-muted space-y-2">
                  {clients.slice(0, 3).map((client) => (
                    <div key={client.id}>
                      <div className="text-text font-medium mb-1">{client.name}</div>
                      <div className="flex flex-wrap gap-1">
                        {skills.slice(0, 8).map((skill, i) => (
                          <span
                            key={skill.id}
                            className="px-2 py-0.5 rounded text-xs"
                            style={{ backgroundColor: colors[i % colors.length] + "20", color: colors[i % colors.length] }}
                          >
                            {skill.name}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-xs text-muted text-center py-8">
                  Add clients and skills to see connections
                </div>
              )}
            </div>
          </div>

          {/* Skills column */}
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <Wrench className="w-4 h-4 text-warning" />
              <h2 className="text-sm font-semibold text-text">Skills</h2>
              <span className="text-xs text-muted ml-auto">{skills.length}</span>
            </div>
            <div className="space-y-2 max-h-[500px] overflow-y-auto">
              {skills.map((skill, i) => (
                <div
                  key={skill.id}
                  className="flex items-center gap-2 bg-border/30 rounded-lg p-2 text-xs text-text hover:bg-border/50 transition-colors"
                >
                  <div
                    className="w-2 h-2 rounded-full shrink-0"
                    style={{ backgroundColor: colors[i % colors.length] }}
                  />
                  <span className="truncate">{skill.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-6 bg-card border border-border rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <Brain className="w-4 h-4 text-accent" />
            <h2 className="text-sm font-semibold text-text">Full Interactive Brain Map</h2>
          </div>
          <p className="text-xs text-muted mb-3">
            The full D3.js force-directed graph is generated locally by running:
          </p>
          <code className="block bg-background border border-border rounded-lg p-3 text-xs text-text font-mono">
            python infrastructure/scripts/generate_brain_map.py
          </code>
          <p className="text-xs text-muted mt-3">
            Open the generated HTML file in your browser: <code className="text-accent">AgenticMarketingPro-Vault/00-Agency-Core/_dashboards/brain-map.html</code>
          </p>
        </div>
      </main>
    </div>
  );
}
