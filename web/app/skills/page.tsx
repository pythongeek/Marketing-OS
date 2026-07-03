"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { StatusBadge } from "@/components/status-badge";
import { Wrench, Edit3, Play, ExternalLink } from "lucide-react";

const skillFormMap: Record<string, string> = {
  "content-strategist": "content-brief.html",
  "on-page-optimizer": "on-page-request.html",
  "technical-seo-auditor": "tech-audit.html",
  "keyword-researcher": "pseo-config.html",
  "competitor-intelligence": "competitor-intake.html",
  "aeo-geo-strategist": "aeo-entity-schema.html",
  "link-building-outreach": "outreach-prospect.html",
  "pseo-pipeline": "pseo-config.html",
  "content-brief-writer": "content-brief.html",
  "copywriter": "copy-request.html",
  "social-media-manager": "social-calendar.html",
  "paid-ads-manager": "ad-campaign.html",
  "analytics-expert": "analytics-report.html",
  "conversion-optimizer": "cro-experiment.html",
  "brand-voice-writer": "copy-request.html",
  "email-marketing-specialist": "email-sequence.html",
  "local-seo-manager": "local-seo.html",
  "video-script-writer": "video-image-brief.html",
  "reputation-manager": "reputation-monitoring.html",
  "market-researcher": "market-alert.html",
  "forecasting-revenue": "forecasting-request.html",
  "reporting-automation": "report-config.html",
  "playbook-creator": "playbook-request.html",
  "off-page-optimizer": "outreach-prospect.html",
  "agentic-marketing-os": "agent-config.html",
  "onboarding-agent": "client-onboarding.html",
  "martech-integration-agent": "api-credentials.html",
  "seo-data-pipeline": "gsc-property.html",
  "content-production-pipeline": "content-brief.html",
  "site-monitoring-pipeline": "qa-check-request.html",
  "competitor-intelligence-mesh": "competitor-intake.html",
};

export default function SkillsPage() {
  const [skills, setSkills] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editInstructions, setEditInstructions] = useState("");

  useEffect(() => {
    fetch("/api/skills")
      .then((r) => r.json())
      .then((d) => { setSkills(d.skills || []); setLoading(false); })
      .catch(console.error);
  }, []);

  async function saveSkill(id: string) {
    const res = await fetch("/api/skills", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, instructions: editInstructions }),
    });
    if (res.ok) {
      setEditingId(null);
      const updated = await fetch("/api/skills").then((r) => r.json());
      setSkills(updated.skills || []);
    }
  }

  async function triggerSkill(slug: string) {
    await fetch("/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "agent_run", skill_slug: slug, payload: {} }),
    });
    alert(`Job queued for ${slug}`);
  }

  if (loading) return <div className="p-8 text-muted">Loading...</div>;

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-text">Skills</h1>
            <p className="text-muted text-sm mt-1">{skills.length} agents loaded</p>
          </div>
          <button className="bg-accent text-white px-4 py-2 rounded-lg text-sm hover:bg-accent-hover transition-colors">
            Sync from Vault
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {skills.map((skill) => (
            <div key={skill.id} className="bg-card border border-border rounded-xl p-5">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Wrench className="w-4 h-4 text-accent" />
                  <h3 className="text-sm font-semibold text-text">{skill.name}</h3>
                </div>
                <StatusBadge status={skill.status} />
              </div>
              <p className="text-xs text-muted mb-3 line-clamp-2">{skill.description}</p>
              <div className="flex items-center gap-2 text-xs text-muted mb-4">
                <span className="bg-border/50 px-2 py-0.5 rounded">{skill.category}</span>
                <span>Updated {new Date(skill.last_updated).toLocaleDateString()}</span>
              </div>

              {editingId === skill.id ? (
                <div className="space-y-2">
                  <textarea
                    className="w-full bg-background border border-border rounded-lg p-2 text-xs text-text"
                    rows={6}
                    value={editInstructions}
                    onChange={(e) => setEditInstructions(e.target.value)}
                  />
                  <div className="flex gap-2">
                    <button onClick={() => saveSkill(skill.id)} className="bg-success text-white px-3 py-1 rounded text-xs">Save</button>
                    <button onClick={() => setEditingId(null)} className="bg-border text-text px-3 py-1 rounded text-xs">Cancel</button>
                  </div>
                </div>
              ) : (
                <div className="flex gap-2">
                  <button
                    onClick={() => { setEditingId(skill.id); setEditInstructions(skill.instructions || ""); }}
                    className="flex items-center gap-1 bg-border/50 hover:bg-border text-text px-3 py-1.5 rounded-lg text-xs transition-colors"
                  >
                    <Edit3 className="w-3 h-3" /> Edit
                  </button>
                  <button
                    onClick={() => triggerSkill(skill.slug)}
                    className="flex items-center gap-1 bg-accent/20 hover:bg-accent/30 text-accent px-3 py-1.5 rounded-lg text-xs transition-colors"
                  >
                    <Play className="w-3 h-3" /> Run
                  </button>
                  <a
                    href={`/forms/${skillFormMap[skill.slug] || skill.slug + ".html"}`}
                    target="_blank"
                    className="flex items-center gap-1 bg-border/50 hover:bg-border text-text px-3 py-1.5 rounded-lg text-xs transition-colors"
                  >
                    <ExternalLink className="w-3 h-3" /> Form
                  </a>
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
