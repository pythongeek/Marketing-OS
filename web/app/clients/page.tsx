"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { StatusBadge } from "@/components/status-badge";
import { Users, Plus, ExternalLink } from "lucide-react";
import Link from "next/link";

export default function ClientsPage() {
  const [clients, setClients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/clients")
      .then((r) => r.json())
      .then((d) => { setClients(d.clients || []); setLoading(false); })
      .catch(console.error);
  }, []);

  if (loading) return <div className="p-8 text-muted">Loading...</div>;

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-text">Clients</h1>
            <p className="text-muted text-sm mt-1">{clients.length} active clients</p>
          </div>
          <Link href="/forms/client-onboarding.html" target="_blank" className="flex items-center gap-2 bg-accent text-white px-4 py-2 rounded-lg text-sm hover:bg-accent-hover transition-colors">
            <Plus className="w-4 h-4" /> Onboard Client
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {clients.map((client) => (
            <div key={client.id} className="bg-card border border-border rounded-xl p-5">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-accent" />
                  <h3 className="text-sm font-semibold text-text">{client.name}</h3>
                </div>
                <StatusBadge status={client.status} />
              </div>
              <p className="text-xs text-muted mb-1">{client.industry || "—"}</p>
              <p className="text-xs text-muted mb-3">{client.website || "—"}</p>
              <div className="flex items-center gap-2 text-xs text-muted mb-4">
                <span className="bg-border/50 px-2 py-0.5 rounded">{client.tier}</span>
                <span>${client.mrr?.toLocaleString() || 0}/mo</span>
              </div>
              <div className="flex gap-2">
                <Link href={`/jobs?client=${client.slug}`} className="flex items-center gap-1 bg-border/50 hover:bg-border text-text px-3 py-1.5 rounded-lg text-xs transition-colors">
                  <ExternalLink className="w-3 h-3" /> Jobs
                </Link>
                <Link href={`/clients/${client.slug}`} className="flex items-center gap-1 bg-accent/20 hover:bg-accent/30 text-accent px-3 py-1.5 rounded-lg text-xs transition-colors">
                  <ExternalLink className="w-3 h-3" /> Vault
                </Link>
              </div>
            </div>
          ))}
        </div>

        {clients.length === 0 && (
          <div className="bg-card border border-border rounded-xl p-8 text-center">
            <p className="text-muted mb-4">No clients yet. Onboard your first client to get started.</p>
            <Link href="/forms/client-onboarding.html" target="_blank" className="bg-accent text-white px-4 py-2 rounded-lg text-sm hover:bg-accent-hover transition-colors">
              Onboard Client
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}
