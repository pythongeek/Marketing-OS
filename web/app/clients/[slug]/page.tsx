"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Nav } from "@/components/nav";
import { StatusBadge } from "@/components/status-badge";
import { Users, ExternalLink, FileText, Target, Globe, BarChart3, Zap, ChevronRight, RefreshCw, Edit3, Save, X } from "lucide-react";
import Link from "next/link";

const VAULT_TABS = [
  { key: "client-profile", label: "Profile", icon: FileText },
  { key: "strategy-90-day", label: "Strategy", icon: Target },
  { key: "kpis-and-goals", label: "KPIs", icon: BarChart3 },
  { key: "website-manifest", label: "Website", icon: Globe },
  { key: "onboarding", label: "Onboarding", icon: FileText },
  { key: "competitor-watch", label: "Competitors", icon: FileText },
  { key: "campaign-log", label: "Campaigns", icon: FileText },
  { key: "technical-fix-queue", label: "Tech Queue", icon: Zap },
];

const INDUSTRY_SKILLS: Record<string, string[]> = {
  healthcare: ["content-strategist", "local-seo-manager", "email-marketing-specialist", "analytics-expert"],
  "real estate": ["content-strategist", "local-seo-manager", "paid-ads-manager", "social-media-manager"],
  ecommerce: ["content-strategist", "paid-ads-manager", "email-marketing-specialist", "conversion-optimizer"],
  saas: ["content-strategist", "pseo-pipeline", "aeo-geo-strategist", "analytics-expert"],
  education: ["content-strategist", "social-media-manager", "email-marketing-specialist", "local-seo-manager"],
  manufacturing: ["content-strategist", "local-seo-manager", "analytics-expert", "technical-seo-auditor"],
  "professional services": ["content-strategist", "email-marketing-specialist", "conversion-optimizer", "analytics-expert"],
};

export default function ClientDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [client, setClient] = useState<any>(null);
  const [skills, setSkills] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [activeTab, setActiveTab] = useState("client-profile");
  const [activeSection, setActiveSection] = useState<"vault" | "skills">("vault");

  // ── Vault editing state ──
  const [isEditingVault, setIsEditingVault] = useState(false);
  const [editContent, setEditContent] = useState("");
  const [savingVault, setSavingVault] = useState(false);

  async function loadData() {
    try {
      const [clientRes, skillsRes] = await Promise.all([
        fetch(`/api/clients/${slug}`),
        fetch("/api/skills"),
      ]);
      const clientData = await clientRes.json();
      const skillsData = await skillsRes.json();
      setClient(clientData.client);
      setSkills(skillsData.skills || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [slug]);

  async function generateVault() {
    if (!client) return;
    setGenerating(true);
    try {
      const res = await fetch(`/api/clients/${slug}/generate-vault`, { method: "POST" });
      const data = await res.json();
      if (res.ok) {
        setClient(data.client);
      } else {
        alert("Failed to generate vault: " + (data.error || "Unknown error"));
      }
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setGenerating(false);
    }
  }

  // ── Start editing current vault tab ──
  function startEdit() {
    const vault = client?.vault_content || {};
    const content = vault[activeTab] || "";
    setEditContent(content);
    setIsEditingVault(true);
  }

  // ── Save edited vault tab ──
  async function saveVaultEdit() {
    if (!client) return;
    setSavingVault(true);
    try {
      const vault = { ...(client.vault_content || {}) };
      vault[activeTab] = editContent;

      const res = await fetch(`/api/clients/${slug}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ vault_content: vault }),
      });

      const data = await res.json();
      if (res.ok) {
        setClient(data.client);
        setIsEditingVault(false);
      } else {
        alert("Failed to save: " + (data.error || "Unknown error"));
      }
    } catch (e: any) {
      alert("Error saving: " + e.message);
    } finally {
      setSavingVault(false);
    }
  }

  // ── Cancel editing ──
  function cancelEdit() {
    setIsEditingVault(false);
    setEditContent("");
  }

  if (loading) return <div className="p-8 text-muted">Loading...</div>;
  if (!client) return <div className="p-8 text-muted">Client not found</div>;

  const vault = client.vault_content || {};
  const hasVault = Object.keys(vault).length > 0;
  const currentTabContent = vault[activeTab] || "No content available for this tab.";

  const clientIndustry = (client.industry || "").toLowerCase();
  const recommendedSlugs = INDUSTRY_SKILLS[clientIndustry] || INDUSTRY_SKILLS["saas"] || [];
  const recommendedSkills = skills.filter((s) => recommendedSlugs.includes(s.slug));
  const otherSkills = skills.filter((s) => !recommendedSlugs.includes(s.slug));

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-1">
            <Link href="/clients" className="text-muted text-sm hover:text-text">Clients</Link>
            <ChevronRight className="w-3 h-3 text-muted" />
            <span className="text-text text-sm font-medium">{client.name}</span>
          </div>
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-text">{client.name}</h1>
              <p className="text-muted text-sm mt-1">
                {client.industry || "—"} · {client.tier || "—"} · ${client.mrr?.toLocaleString() || 0}/mo
              </p>
            </div>
            <div className="flex items-center gap-2">
              <StatusBadge status={client.status} />
              {client.website && (
                <a href={client.website} target="_blank" className="flex items-center gap-1 bg-border/50 hover:bg-border text-text px-3 py-1.5 rounded-lg text-xs transition-colors">
                  <ExternalLink className="w-3 h-3" /> Visit
                </a>
              )}
              <Link href={`/jobs?client=${client.slug}`} className="flex items-center gap-1 bg-border/50 hover:bg-border text-text px-3 py-1.5 rounded-lg text-xs transition-colors">
                <Users className="w-3 h-3" /> Jobs
              </Link>
            </div>
          </div>
        </div>

        {/* Section tabs */}
        <div className="flex gap-2 mb-6 border-b border-border pb-1">
          <button
            onClick={() => setActiveSection("vault")}
            className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 ${activeSection === "vault" ? "text-accent border-accent" : "text-muted border-transparent hover:text-text"}`}
          >
            Client Vault
          </button>
          <button
            onClick={() => setActiveSection("skills")}
            className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 ${activeSection === "skills" ? "text-accent border-accent" : "text-muted border-transparent hover:text-text"}`}
          >
            Recommended Skills ({recommendedSkills.length})
          </button>
        </div>

        {activeSection === "vault" ? (
          <div className="flex gap-6">
            {/* Sidebar tabs */}
            <div className="w-64 shrink-0">
              <div className="bg-card border border-border rounded-xl overflow-hidden">
                {VAULT_TABS.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.key}
                      onClick={() => { setActiveTab(tab.key); setIsEditingVault(false); }}
                      className={`w-full flex items-center gap-2 px-4 py-2.5 text-left text-xs transition-colors ${
                        activeTab === tab.key
                          ? "bg-accent/10 text-accent border-l-2 border-accent"
                          : "text-muted hover:text-text hover:bg-border/20"
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      {tab.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Content */}
            <div className="flex-1 bg-card border border-border rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-text">
                  {VAULT_TABS.find((t) => t.key === activeTab)?.label}
                </h2>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted">Last updated: {new Date().toLocaleDateString()}</span>
                  {hasVault && !isEditingVault && (
                    <button
                      onClick={startEdit}
                      className="flex items-center gap-1 bg-border/50 hover:bg-border text-text px-3 py-1.5 rounded-lg text-xs transition-colors"
                    >
                      <Edit3 className="w-3 h-3" /> Edit
                    </button>
                  )}
                </div>
              </div>

              {!hasVault ? (
                <div className="text-center py-12">
                  <p className="text-muted mb-4">This client does not have a vault yet.</p>
                  <button
                    onClick={generateVault}
                    disabled={generating}
                    className="inline-flex items-center gap-2 bg-accent text-white px-4 py-2 rounded-lg text-sm hover:bg-accent-hover transition-colors disabled:opacity-50"
                  >
                    {generating ? (
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    ) : (
                      <FileText className="w-4 h-4" />
                    )}
                    {generating ? "Generating..." : "Generate Vault"}
                  </button>
                </div>
              ) : isEditingVault ? (
                /* ── Edit Mode ── */
                <div className="space-y-3">
                  <textarea
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                    rows={20}
                    className="w-full bg-background border border-border rounded-lg p-4 text-sm text-text font-mono leading-relaxed focus:outline-none focus:ring-2 focus:ring-accent/50"
                  />
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted">
                      Editing <strong className="text-text">{VAULT_TABS.find((t) => t.key === activeTab)?.label}</strong>
                    </span>
                    <div className="flex gap-2">
                      <button
                        onClick={cancelEdit}
                        className="flex items-center gap-1 bg-border/50 hover:bg-border text-text px-3 py-1.5 rounded-lg text-xs transition-colors"
                      >
                        <X className="w-3 h-3" /> Cancel
                      </button>
                      <button
                        onClick={saveVaultEdit}
                        disabled={savingVault}
                        className="flex items-center gap-1 bg-accent hover:bg-accent-hover text-white px-3 py-1.5 rounded-lg text-xs transition-colors disabled:opacity-50"
                      >
                        {savingVault ? (
                          <RefreshCw className="w-3 h-3 animate-spin" />
                        ) : (
                          <Save className="w-3 h-3" />
                        )}
                        {savingVault ? "Saving..." : "Save"}
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                /* ── View Mode ── */
                <div className="prose prose-sm max-w-none text-text">
                  <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-text bg-background border border-border rounded-lg p-4 overflow-auto max-h-[70vh]">
                    {currentTabContent}
                  </pre>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div>
            <p className="text-sm text-muted mb-4">
              Skills recommended for <strong className="text-text">{client.industry || "this industry"}</strong> based on the client profile.
            </p>

            {recommendedSkills.length > 0 && (
              <div className="mb-6">
                <h3 className="text-sm font-medium text-accent mb-3">Recommended for {client.name}</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {recommendedSkills.map((skill) => (
                    <SkillCard key={skill.id} skill={skill} clientSlug={client.slug} />
                  ))}
                </div>
              </div>
            )}

            {otherSkills.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-muted mb-3">All Skills</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {otherSkills.map((skill) => (
                    <SkillCard key={skill.id} skill={skill} clientSlug={client.slug} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

function SkillCard({ skill, clientSlug }: { skill: any; clientSlug: string }) {
  return (
    <div className="bg-card border border-border rounded-xl p-4">
      <div className="flex items-start justify-between mb-2">
        <h4 className="text-sm font-semibold text-text">{skill.name}</h4>
        <StatusBadge status={skill.status} />
      </div>
      <p className="text-xs text-muted mb-3 line-clamp-2">{skill.description}</p>
      <div className="flex items-center gap-2 text-xs text-muted mb-3">
        <span className="bg-border/50 px-2 py-0.5 rounded">{skill.category}</span>
      </div>
      <Link
        href={`/skills?run=${skill.slug}&client=${clientSlug}`}
        className="block w-full text-center bg-accent/20 hover:bg-accent/30 text-accent px-3 py-1.5 rounded-lg text-xs transition-colors"
      >
        Run for {clientSlug}
      </Link>
    </div>
  );
}
