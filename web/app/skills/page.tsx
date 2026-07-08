"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { StatusBadge } from "@/components/status-badge";
import { Wrench, Edit3, Play, ExternalLink, X, ChevronDown, Sparkles } from "lucide-react";

interface Skill {
  id: string;
  slug: string;
  name: string;
  description: string | null;
  category: string | null;
  status: string;
  instructions: string | null;
  config: Record<string, unknown>;
  last_updated: string;
}

interface Client {
  id: string;
  slug: string;
  name: string;
  industry: string | null;
}

interface SkillRunConfig {
  skill: Skill;
  clientSlug: string;
  promptOverride: string;
  additionalContext: string;
}

export default function SkillsPage() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editInstructions, setEditInstructions] = useState("");
  const [runConfig, setRunConfig] = useState<SkillRunConfig | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [runResult, setRunResult] = useState<{ success: boolean; message: string; jobId?: string } | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [skillsRes, clientsRes] = await Promise.all([
        fetch("/api/skills"),
        fetch("/api/clients"),
      ]);
      const skillsData = await skillsRes.json();
      const clientsData = await clientsRes.json();
      setSkills(skillsData.skills || []);
      setClients(clientsData.clients || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function saveSkill(id: string) {
    const res = await fetch("/api/skills", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, instructions: editInstructions }),
    });
    if (res.ok) {
      setEditingId(null);
      await loadData();
    }
  }

  async function executeSkillRun() {
    if (!runConfig) return;
    setIsRunning(true);
    setRunResult(null);

    try {
      const res = await fetch("/api/jobs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "agent_run",
          skill_slug: runConfig.skill.slug,
          client_slug: runConfig.clientSlug,
          payload: {
            prompt_override: runConfig.promptOverride || undefined,
            additional_context: runConfig.additionalContext || undefined,
          },
        }),
      });

      const data = await res.json();
      if (res.ok) {
        setRunResult({ success: true, message: `Job queued successfully`, jobId: data.job?.id });
      } else {
        setRunResult({ success: false, message: data.error || "Failed to queue job" });
      }
    } catch (e: any) {
      setRunResult({ success: false, message: e.message });
    } finally {
      setIsRunning(false);
    }
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
          <button 
            onClick={loadData}
            className="bg-accent text-white px-4 py-2 rounded-lg text-sm hover:bg-accent-hover transition-colors"
          >
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
                    onClick={() => setRunConfig({ skill, clientSlug: "", promptOverride: "", additionalContext: "" })}
                    className="flex items-center gap-1 bg-accent/20 hover:bg-accent/30 text-accent px-3 py-1.5 rounded-lg text-xs transition-colors"
                  >
                    <Play className="w-3 h-3" /> Run
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      </main>

      {/* ── Skill Run Modal ── */}
      {runConfig && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-card border border-border rounded-xl w-full max-w-xl max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-border">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-accent" />
                <h2 className="text-lg font-semibold text-text">Run {runConfig.skill.name}</h2>
              </div>
              <button
                onClick={() => { setRunConfig(null); setRunResult(null); }}
                className="p-1 hover:bg-border/50 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-muted" />
              </button>
            </div>

            {/* Modal body */}
            <div className="p-6 overflow-y-auto flex-1 space-y-5">
              {/* Client Selection */}
              <div>
                <label className="block text-sm font-medium text-text mb-2">
                  👤 Client <span className="text-danger">*</span>
                </label>
                <p className="text-xs text-muted mb-2">Select the client this skill will work for</p>
                <div className="relative">
                  <select
                    value={runConfig.clientSlug}
                    onChange={(e) => setRunConfig({ ...runConfig, clientSlug: e.target.value })}
                    className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-text appearance-none cursor-pointer"
                  >
                    <option value="">-- Choose a client --</option>
                    {clients.map((client) => (
                      <option key={client.id} value={client.slug}>
                        {client.name} {client.industry ? `(${client.industry})` : ""}
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted pointer-events-none" />
                </div>
                {clients.length === 0 && (
                  <p className="text-xs text-danger mt-1">No clients found. <a href="/forms/client-onboarding.html" target="_blank" className="underline">Onboard a client first</a>.</p>
                )}
              </div>

              {/* Prompt Override */}
              <div>
                <label className="block text-sm font-medium text-text mb-2">
                  📝 Prompt Override <span className="text-muted font-normal">(optional)</span>
                </label>
                <p className="text-xs text-muted mb-2">
                  Override the default skill instructions. Leave empty to use the skill's built-in prompt.
                </p>
                <textarea
                  value={runConfig.promptOverride}
                  onChange={(e) => setRunConfig({ ...runConfig, promptOverride: e.target.value })}
                  placeholder="Enter custom instructions for this run..."
                  rows={4}
                  className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm text-text placeholder:text-muted/50"
                />
              </div>

              {/* Additional Context */}
              <div>
                <label className="block text-sm font-medium text-text mb-2">
                  📎 Additional Context <span className="text-muted font-normal">(optional)</span>
                </label>
                <p className="text-xs text-muted mb-2">
                  Extra data, URLs, or notes to pass to the skill for this run.
                </p>
                <textarea
                  value={runConfig.additionalContext}
                  onChange={(e) => setRunConfig({ ...runConfig, additionalContext: e.target.value })}
                  placeholder="e.g., Target keyword: 'n8n automation agency', Competitor URL: https://..."
                  rows={3}
                  className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm text-text placeholder:text-muted/50"
                />
              </div>

              {/* Skill Info */}
              <div className="bg-border/20 rounded-lg p-3">
                <h4 className="text-xs font-medium text-text mb-1">Skill Info</h4>
                <p className="text-xs text-muted">{runConfig.skill.description}</p>
                <div className="flex gap-2 mt-2">
                  <span className="text-xs bg-border/50 px-2 py-0.5 rounded">{runConfig.skill.category}</span>
                  <span className="text-xs bg-border/50 px-2 py-0.5 rounded">{runConfig.skill.slug}</span>
                </div>
              </div>

              {/* Result */}
              {runResult && (
                <div className={`rounded-lg p-3 ${runResult.success ? "bg-success/10 border border-success/30" : "bg-danger/10 border border-danger/30"}`}>
                  <p className={`text-sm ${runResult.success ? "text-success" : "text-danger"}`}>
                    {runResult.message}
                  </p>
                  {runResult.jobId && (
                    <a href={`/jobs`} className="text-xs text-accent underline mt-1 inline-block">
                      View in Jobs →
                    </a>
                  )}
                </div>
              )}
            </div>

            {/* Modal footer */}
            <div className="px-6 py-4 border-t border-border flex justify-end gap-2">
              <button
                onClick={() => { setRunConfig(null); setRunResult(null); }}
                className="bg-border/50 hover:bg-border text-text px-4 py-2 rounded-lg text-sm transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={executeSkillRun}
                disabled={!runConfig.clientSlug || isRunning}
                className="bg-accent hover:bg-accent-hover text-white px-4 py-2 rounded-lg text-sm transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                {isRunning ? (
                  <>
                    <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Queuing...
                  </>
                ) : (
                  <>
                    <Play className="w-3 h-3" /> Run Skill
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
