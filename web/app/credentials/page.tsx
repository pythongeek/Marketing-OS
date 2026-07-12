"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Nav } from "@/components/nav";
import { StatusBadge } from "@/components/status-badge";
import { useAuth } from "@/lib/auth";
import {
  Key, Plus, Trash2, Edit3, Save, X, ChevronDown, Check, AlertCircle,
  Globe, BarChart3, Search, FileText, MessageSquare, Megaphone,
  Linkedin, Facebook, ShoppingCart, Code, Database, Lock, Eye, EyeOff,
  RefreshCw, TestTube
} from "lucide-react";

// ── Service definitions with icons and fields ───────────────────────────────

interface ServiceDef {
  key: string;
  label: string;
  icon: React.ElementType;
  category: string;
  configFields: { key: string; label: string; type: string; placeholder?: string }[];
  secretFields: { key: string; label: string; type: string; placeholder?: string }[];
}

const SERVICE_DEFINITIONS: ServiceDef[] = [
  {
    key: "wordpress",
    label: "WordPress",
    icon: FileText,
    category: "CMS",
    configFields: [
      { key: "site_url", label: "Site URL", type: "url", placeholder: "https://example.com" },
      { key: "username", label: "Username", type: "text", placeholder: "admin" },
    ],
    secretFields: [
      { key: "app_password", label: "Application Password", type: "password", placeholder: "xxxx xxxx xxxx xxxx" },
    ],
  },
  {
    key: "ga4",
    label: "Google Analytics 4",
    icon: BarChart3,
    category: "Analytics",
    configFields: [
      { key: "property_id", label: "Property ID", type: "text", placeholder: "properties/123456789" },
    ],
    secretFields: [
      { key: "credentials_json", label: "Service Account JSON", type: "textarea", placeholder: "Paste service account JSON..." },
    ],
  },
  {
    key: "gsc",
    label: "Google Search Console",
    icon: Search,
    category: "SEO",
    configFields: [
      { key: "property_url", label: "Property URL", type: "url", placeholder: "https://example.com/" },
    ],
    secretFields: [
      { key: "credentials_json", label: "Service Account JSON", type: "textarea", placeholder: "Paste service account JSON..." },
    ],
  },
  {
    key: "bing_wmt",
    label: "Bing Webmaster Tools",
    icon: Search,
    category: "SEO",
    configFields: [
      { key: "site_url", label: "Site URL", type: "url", placeholder: "https://example.com" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "Bing API key" },
    ],
  },
  {
    key: "ahrefs",
    label: "Ahrefs",
    icon: Search,
    category: "SEO",
    configFields: [
      { key: "domain", label: "Domain", type: "text", placeholder: "example.com" },
    ],
    secretFields: [
      { key: "api_token", label: "API Token", type: "password", placeholder: "Ahrefs API token" },
    ],
  },
  {
    key: "semrush",
    label: "SEMrush",
    icon: Search,
    category: "SEO",
    configFields: [
      { key: "domain", label: "Domain", type: "text", placeholder: "example.com" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "SEMrush API key" },
    ],
  },
  {
    key: "google_ads",
    label: "Google Ads",
    icon: Megaphone,
    category: "Paid Ads",
    configFields: [
      { key: "customer_id", label: "Customer ID", type: "text", placeholder: "123-456-7890" },
      { key: "developer_token", label: "Developer Token", type: "text", placeholder: "Developer token" },
    ],
    secretFields: [
      { key: "refresh_token", label: "Refresh Token", type: "password", placeholder: "OAuth refresh token" },
      { key: "client_secret", label: "Client Secret", type: "password", placeholder: "OAuth client secret" },
    ],
  },
  {
    key: "meta_ads",
    label: "Meta Ads",
    icon: Facebook,
    category: "Paid Ads",
    configFields: [
      { key: "ad_account_id", label: "Ad Account ID", type: "text", placeholder: "act_123456789" },
    ],
    secretFields: [
      { key: "access_token", label: "Access Token", type: "password", placeholder: "Meta access token" },
    ],
  },
  {
    key: "linkedin_ads",
    label: "LinkedIn Ads",
    icon: Linkedin,
    category: "Paid Ads",
    configFields: [
      { key: "account_id", label: "Account ID", type: "text", placeholder: "LinkedIn account ID" },
    ],
    secretFields: [
      { key: "access_token", label: "Access Token", type: "password", placeholder: "LinkedIn access token" },
    ],
  },
  {
    key: "slack",
    label: "Slack",
    icon: MessageSquare,
    category: "Communication",
    configFields: [
      { key: "channel", label: "Channel", type: "text", placeholder: "#alerts" },
    ],
    secretFields: [
      { key: "webhook_url", label: "Webhook URL", type: "password", placeholder: "https://hooks.slack.com/..." },
    ],
  },
  {
    key: "hubspot",
    label: "HubSpot",
    icon: Database,
    category: "CRM",
    configFields: [
      { key: "portal_id", label: "Portal ID", type: "text", placeholder: "12345678" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "HubSpot API key" },
    ],
  },
  {
    key: "minimax",
    label: "MiniMax M3 (Primary AI)",
    icon: Code,
    category: "AI",
    configFields: [
      { key: "model", label: "Model", type: "text", placeholder: "MiniMax-M3" },
      { key: "base_url", label: "Base URL", type: "url", placeholder: "https://api.minimax.io/v1" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "MiniMax API key" },
    ],
  },
  {
    key: "n8n",
    label: "n8n (Workflow Automation)",
    icon: Code,
    category: "Automation",
    configFields: [
      { key: "instance_url", label: "Instance URL", type: "url", placeholder: "https://n8n.yourdomain.com" },
      { key: "webhook_base", label: "Webhook Base URL", type: "url", placeholder: "https://n8n.yourdomain.com/webhook" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "n8n_api_..." },
    ],
  },
  {
    key: "openai",
    label: "OpenAI",
    icon: Code,
    category: "AI",
    configFields: [
      { key: "model", label: "Model", type: "text", placeholder: "gpt-4o" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "sk-..." },
    ],
  },
  {
    key: "hermes_agent",
    label: "Hermes Agent Desktop",
    icon: Code,
    category: "AI",
    configFields: [
      { key: "model", label: "Model", type: "text", placeholder: "MiniMax-M3" },
      { key: "base_url", label: "Base URL", type: "url", placeholder: "https://hermes-agent.local/api" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "sk-..." },
    ],
  },
  {
    key: "shopify",
    label: "Shopify",
    icon: ShoppingCart,
    category: "E-commerce",
    configFields: [
      { key: "shop_domain", label: "Shop Domain", type: "text", placeholder: "my-store.myshopify.com" },
    ],
    secretFields: [
      { key: "api_key", label: "API Key", type: "password", placeholder: "Shopify API key" },
      { key: "api_secret", label: "API Secret", type: "password", placeholder: "Shopify API secret" },
    ],
  },
  {
    key: "woocommerce",
    label: "WooCommerce",
    icon: ShoppingCart,
    category: "E-commerce",
    configFields: [
      { key: "site_url", label: "Site URL", type: "url", placeholder: "https://example.com" },
    ],
    secretFields: [
      { key: "consumer_key", label: "Consumer Key", type: "password", placeholder: "ck_..." },
      { key: "consumer_secret", label: "Consumer Secret", type: "password", placeholder: "cs_..." },
    ],
  },
];

const SERVICE_MAP = Object.fromEntries(SERVICE_DEFINITIONS.map((s) => [s.key, s]));

// ── Types ───────────────────────────────────────────────────────────────────

interface Credential {
  id: string;
  client_slug: string | null;
  service: string;
  label: string;
  config: Record<string, any>;
  is_active: boolean;
  last_tested_at: string | null;
  test_status: "unknown" | "pass" | "fail";
  test_error: string | null;
  created_at: string;
  updated_at: string;
  has_secrets: boolean;
}

interface Client {
  id: string;
  slug: string;
  name: string;
}

export default function CredentialsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login?redirect=/credentials");
    }
  }, [authLoading, user, router]);

  // Helper to build Authorization header for fetch calls
  const authedFetch = async (url: string, init: RequestInit = {}) => {
    if (!user) throw new Error("Not authenticated");
    const session = await (window as any).__supabase?.auth?.getSession?.();
    const token = session?.data?.session?.access_token;
    return fetch(url, {
      ...init,
      headers: {
        ...(init.headers || {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
  };
  const [credentials, setCredentials] = useState<Credential[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterService, setFilterService] = useState("");
  const [filterClient, setFilterClient] = useState("");

  // Add/edit modal state
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [selectedService, setSelectedService] = useState("");
  const [formData, setFormData] = useState<{
    client_slug: string;
    label: string;
    config: Record<string, string>;
    secrets: Record<string, string>;
  }>({ client_slug: "", label: "", config: {}, secrets: {} });
  const [showSecrets, setShowSecrets] = useState<Record<string, boolean>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [credsRes, clientsRes] = await Promise.all([
              authedFetch("/api/credentials"),
              authedFetch("/api/clients"),
            ]);
      const credsData = await credsRes.json();
      const clientsData = await clientsRes.json();
      setCredentials(credsData.credentials || []);
      setClients(clientsData.clients || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  function openAddModal(serviceKey: string) {
    const def = SERVICE_MAP[serviceKey];
    setEditingId(null);
    setSelectedService(serviceKey);
    setFormData({
      client_slug: "",
      label: `${def.label} — ${new Date().toLocaleDateString()}`,
      config: Object.fromEntries(def.configFields.map((f) => [f.key, ""])),
      secrets: Object.fromEntries(def.secretFields.map((f) => [f.key, ""])),
    });
    setShowSecrets({});
    setShowModal(true);
  }

  function openEditModal(cred: Credential) {
    const def = SERVICE_MAP[cred.service];
    if (!def) return;
    setEditingId(cred.id);
    setSelectedService(cred.service);
    setFormData({
      client_slug: cred.client_slug || "",
      label: cred.label,
      config: { ...cred.config },
      secrets: {}, // secrets are not fetched — user must re-enter to update
    });
    setShowSecrets({});
    setShowModal(true);
  }

  async function saveCredential() {
    setSaving(true);
    try {
      const def = SERVICE_MAP[selectedService];
      const payload = {
        client_slug: formData.client_slug || null,
        service: selectedService,
        label: formData.label,
        config: formData.config,
        secrets: formData.secrets,
      };

      // Remove empty secrets on edit (don't overwrite existing ones)
      if (editingId) {
        const cleanedSecrets: Record<string, string> = {};
        for (const [k, v] of Object.entries(formData.secrets)) {
          if (v.trim()) cleanedSecrets[k] = v;
        }
        if (Object.keys(cleanedSecrets).length > 0) {
          payload.secrets = cleanedSecrets;
        } else {
          delete (payload as any).secrets;
        }
      }

      const url = editingId ? `/api/credentials/${editingId}` : "/api/credentials";
      const method = editingId ? "PATCH" : "POST";

      const res = await authedFetch(url, {
              method,
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload),
            });

      if (res.ok) {
        setShowModal(false);
        await loadData();
      } else {
        const data = await res.json();
        alert("Error: " + (data.error || "Failed to save"));
      }
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setSaving(false);
    }
  }

  async function deleteCredential(id: string) {
    if (!confirm("Delete this credential? This cannot be undone.")) return;
    try {
      const res = await authedFetch(`/api/credentials/${id}`, { method: "DELETE" });
      if (res.ok) {
        await loadData();
      } else {
        const data = await res.json();
        alert("Error: " + (data.error || "Failed to delete"));
      }
    } catch (e: any) {
      alert("Error: " + e.message);
    }
  }

  async function testCredential(id: string) {
    // Placeholder — actual test depends on service type
    alert("Test connection: This will be implemented per service type.");
  }

  const filtered = credentials.filter((c) => {
    if (filterService && c.service !== filterService) return false;
    if (filterClient && c.client_slug !== filterClient) return false;
    return true;
  });

  const groupedByCategory = SERVICE_DEFINITIONS.reduce((acc, s) => {
    if (!acc[s.category]) acc[s.category] = [];
    acc[s.category].push(s);
    return acc;
  }, {} as Record<string, ServiceDef[]>);

  if (loading) return <div className="p-8 text-muted">Loading...</div>;

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-text">Credentials</h1>
            <p className="text-muted text-sm mt-1">{credentials.length} API keys & service accounts</p>
          </div>
          <a
            href="/api/bing-auth/start"
            className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium transition"
          >
            Connect Bing WMT (OAuth)
          </a>
        </div>

        {/* Bing OAuth status banner */}
        {typeof window !== "undefined" && new URLSearchParams(window.location.search).get("bing_oauth") === "success" && (
          <div className="mb-6 p-4 rounded bg-green-900/30 border border-green-700 text-green-200">
            Bing Webmaster OAuth authorization successful! Tokens are stored and the API is now connected.
          </div>
        )}

        {/* Filters */}
        <div className="flex gap-3 mb-6">
          <select
            value={filterService}
            onChange={(e) => setFilterService(e.target.value)}
            className="bg-card border border-border rounded-lg px-3 py-2 text-sm text-text"
          >
            <option value="">All Services</option>
            {SERVICE_DEFINITIONS.map((s) => (
              <option key={s.key} value={s.key}>{s.label}</option>
            ))}
          </select>
          <select
            value={filterClient}
            onChange={(e) => setFilterClient(e.target.value)}
            className="bg-card border border-border rounded-lg px-3 py-2 text-sm text-text"
          >
            <option value="">All Clients + Global</option>
            <option value="__global__">Global (no client)</option>
            {clients.map((c) => (
              <option key={c.id} value={c.slug}>{c.name}</option>
            ))}
          </select>
          {(filterService || filterClient) && (
            <button
              onClick={() => { setFilterService(""); setFilterClient(""); }}
              className="text-xs text-muted hover:text-text px-2"
            >
              Clear
            </button>
          )}
        </div>

        {/* Add New — grouped by category */}
        <div className="mb-8">
          <h2 className="text-sm font-medium text-text mb-3">Add New Credential</h2>
          <div className="space-y-4">
            {Object.entries(groupedByCategory).map(([category, services]) => (
              <div key={category}>
                <h3 className="text-xs text-muted uppercase tracking-wide mb-2">{category}</h3>
                <div className="flex flex-wrap gap-2">
                  {services.map((s) => (
                    <button
                      key={s.key}
                      onClick={() => openAddModal(s.key)}
                      className="flex items-center gap-1.5 bg-card border border-border hover:border-accent rounded-lg px-3 py-2 text-xs text-text transition-colors"
                    >
                      <Plus className="w-3 h-3 text-accent" />
                      <s.icon className="w-3.5 h-3.5 text-muted" />
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Credentials List */}
        <div className="bg-card border border-border rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-border/30 text-muted text-xs uppercase">
              <tr>
                <th className="px-4 py-3 text-left">Service</th>
                <th className="px-4 py-3 text-left">Label</th>
                <th className="px-4 py-3 text-left">Client</th>
                <th className="px-4 py-3 text-left">Status</th>
                <th className="px-4 py-3 text-left">Last Tested</th>
                <th className="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-muted">
                    No credentials found. Add one above.
                  </td>
                </tr>
              ) : (
                filtered.map((cred) => {
                  const def = SERVICE_MAP[cred.service];
                  const clientName = clients.find((c) => c.slug === cred.client_slug)?.name || (cred.client_slug ? cred.client_slug : "Global");
                  return (
                    <tr key={cred.id} className="border-t border-border hover:bg-border/20">
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          {def && <def.icon className="w-4 h-4 text-accent" />}
                          <span className="text-text">{def?.label || cred.service}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-text">{cred.label}</td>
                      <td className="px-4 py-3 text-muted text-xs">{clientName}</td>
                      <td className="px-4 py-3">
                        <StatusBadge status={cred.is_active ? "active" : "inactive"} />
                      </td>
                      <td className="px-4 py-3 text-muted text-xs">
                        {cred.last_tested_at
                          ? new Date(cred.last_tested_at).toLocaleDateString()
                          : "Never"}
                        {cred.test_status === "pass" && <Check className="w-3 h-3 text-success inline ml-1" />}
                        {cred.test_status === "fail" && <AlertCircle className="w-3 h-3 text-danger inline ml-1" />}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex gap-1">
                          <button
                            onClick={() => openEditModal(cred)}
                            className="p-1.5 hover:bg-border/50 rounded-lg transition-colors"
                            title="Edit"
                          >
                            <Edit3 className="w-3.5 h-3.5 text-muted" />
                          </button>
                          <button
                            onClick={() => testCredential(cred.id)}
                            className="p-1.5 hover:bg-border/50 rounded-lg transition-colors"
                            title="Test"
                          >
                            <TestTube className="w-3.5 h-3.5 text-muted" />
                          </button>
                          <button
                            onClick={() => deleteCredential(cred.id)}
                            className="p-1.5 hover:bg-danger/10 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 className="w-3.5 h-3.5 text-danger" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </main>

      {/* ── Add/Edit Modal ── */}
      {showModal && selectedService && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-card border border-border rounded-xl w-full max-w-lg max-h-[90vh] overflow-hidden flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-border">
              <div className="flex items-center gap-2">
                {SERVICE_MAP[selectedService] && (
                  <>
                    <Key className="w-4 h-4 text-accent" />
                    <h2 className="text-lg font-semibold text-text">
                      {editingId ? "Edit" : "Add"} {SERVICE_MAP[selectedService].label}
                    </h2>
                  </>
                )}
              </div>
              <button onClick={() => setShowModal(false)} className="p-1 hover:bg-border/50 rounded-lg">
                <X className="w-5 h-5 text-muted" />
              </button>
            </div>

            {/* Body */}
            <div className="p-6 overflow-y-auto flex-1 space-y-4">
              {/* Client selection */}
              <div>
                <label className="block text-sm font-medium text-text mb-1">Client</label>
                <select
                  value={formData.client_slug}
                  onChange={(e) => setFormData({ ...formData, client_slug: e.target.value })}
                  className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm text-text"
                >
                  <option value="">Global (all clients)</option>
                  {clients.map((c) => (
                    <option key={c.id} value={c.slug}>{c.name}</option>
                  ))}
                </select>
              </div>

              {/* Label */}
              <div>
                <label className="block text-sm font-medium text-text mb-1">Label</label>
                <input
                  type="text"
                  value={formData.label}
                  onChange={(e) => setFormData({ ...formData, label: e.target.value })}
                  className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm text-text"
                />
              </div>

              {/* Config fields */}
              {SERVICE_MAP[selectedService]?.configFields.map((field) => (
                <div key={field.key}>
                  <label className="block text-sm font-medium text-text mb-1">{field.label}</label>
                  <input
                    type={field.type}
                    value={formData.config[field.key] || ""}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, [field.key]: e.target.value },
                      })
                    }
                    placeholder={field.placeholder}
                    className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm text-text placeholder:text-muted/50"
                  />
                </div>
              ))}

              {/* Secret fields */}
              <div className="border-t border-border pt-4">
                <div className="flex items-center gap-2 mb-3">
                  <Lock className="w-4 h-4 text-danger" />
                  <h3 className="text-sm font-medium text-text">Secrets</h3>
                  <span className="text-xs text-muted">(encrypted at rest)</span>
                </div>
                {editingId && (
                  <p className="text-xs text-muted mb-3">
                    Leave blank to keep existing secrets. Enter new values to overwrite.
                  </p>
                )}
                {SERVICE_MAP[selectedService]?.secretFields.map((field) => (
                  <div key={field.key} className="mb-3">
                    <label className="block text-sm font-medium text-text mb-1">{field.label}</label>
                    <div className="relative">
                      {field.type === "textarea" ? (
                        <textarea
                          value={formData.secrets[field.key] || ""}
                          onChange={(e) =>
                            setFormData({
                              ...formData,
                              secrets: { ...formData.secrets, [field.key]: e.target.value },
                            })
                          }
                          placeholder={field.placeholder}
                          rows={4}
                          className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm text-text placeholder:text-muted/50 font-mono"
                        />
                      ) : (
                        <>
                          <input
                            type={showSecrets[field.key] ? "text" : "password"}
                            value={formData.secrets[field.key] || ""}
                            onChange={(e) =>
                              setFormData({
                                ...formData,
                                secrets: { ...formData.secrets, [field.key]: e.target.value },
                              })
                            }
                            placeholder={field.placeholder}
                            className="w-full bg-background border border-border rounded-lg px-3 py-2 pr-10 text-sm text-text placeholder:text-muted/50 font-mono"
                          />
                          <button
                            onClick={() =>
                              setShowSecrets({ ...showSecrets, [field.key]: !showSecrets[field.key] })
                            }
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-text"
                          >
                            {showSecrets[field.key] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Footer */}
            <div className="px-6 py-4 border-t border-border flex justify-end gap-2">
              <button
                onClick={() => setShowModal(false)}
                className="bg-border/50 hover:bg-border text-text px-4 py-2 rounded-lg text-sm transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={saveCredential}
                disabled={saving}
                className="bg-accent hover:bg-accent-hover text-white px-4 py-2 rounded-lg text-sm transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                {saving ? <RefreshCw className="w-3 h-3 animate-spin" /> : <Save className="w-3 h-3" />}
                {saving ? "Saving..." : editingId ? "Update" : "Save"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
