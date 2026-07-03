"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { StatusBadge } from "@/components/status-badge";
import { Activity, RefreshCw, Eye, X } from "lucide-react";
import { supabase } from "@/lib/supabase";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [liveStatus, setLiveStatus] = useState("🔴 Disconnected");
  const [selectedJob, setSelectedJob] = useState<any>(null);

  async function fetchJobs() {
    setLoading(true);
    try {
      const res = await fetch("/api/jobs");
      const data = await res.json();
      setJobs(data.jobs || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  // ── Supabase Realtime ─────────────────────────────────────
  useEffect(() => {
    if (!supabase) return;
    fetchJobs();

    const channel = supabase
      .channel("jobs-page-realtime")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "jobs" },
        (payload: any) => {
          console.log("Realtime job change:", payload);
          setLiveStatus("🟢 Live");
          fetchJobs();
        }
      )
      .subscribe((status: any) => {
        if (status === "SUBSCRIBED") setLiveStatus("🟢 Live");
      });

    return () => { supabase.removeChannel(channel); };
  }, []);

  const filtered = filter === "all" ? jobs : jobs.filter((j: any) => j.status === filter);

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-text">Jobs</h1>
            <p className="text-muted text-sm mt-1">Job queue and execution history</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-muted bg-card border border-border rounded-full px-3 py-1">{liveStatus}</span>
            <button onClick={fetchJobs} className="flex items-center gap-2 bg-border/50 hover:bg-border text-text px-3 py-2 rounded-lg text-sm transition-colors">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
          </div>
        </div>

        <div className="flex gap-2 mb-6">
          {["all", "pending", "running", "completed", "failed"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs capitalize transition-colors ${filter === f ? "bg-accent text-white" : "bg-border/50 text-muted hover:text-text"}`}
            >
              {f} ({f === "all" ? jobs.length : jobs.filter((j: any) => j.status === f).length})
            </button>
          ))}
        </div>

        <div className="bg-card border border-border rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-border/30 text-muted text-xs uppercase">
              <tr>
                <th className="px-4 py-3 text-left">Type</th>
                <th className="px-4 py-3 text-left">Client</th>
                <th className="px-4 py-3 text-left">Skill</th>
                <th className="px-4 py-3 text-left">Status</th>
                <th className="px-4 py-3 text-left">Created</th>
                <th className="px-4 py-3 text-left">Cost</th>
                <th className="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={7} className="px-4 py-8 text-center text-muted">Loading...</td></tr>
              ) : filtered.length === 0 ? (
                <tr><td colSpan={7} className="px-4 py-8 text-center text-muted">No jobs found</td></tr>
              ) : (
                filtered.map((job: any) => (
                  <tr key={job.id} className="border-t border-border hover:bg-border/20">
                    <td className="px-4 py-3 text-text">{job.type}</td>
                    <td className="px-4 py-3 text-muted">{job.client_slug || "—"}</td>
                    <td className="px-4 py-3 text-muted">{job.skill_slug || "—"}</td>
                    <td className="px-4 py-3"><StatusBadge status={job.status} /></td>
                    <td className="px-4 py-3 text-muted text-xs">{new Date(job.created_at).toLocaleString()}</td>
                    <td className="px-4 py-3 text-muted text-xs">${job.cost_usd || 0}</td>
                    <td className="px-4 py-3">
                      {(job.status === "completed" || job.status === "failed") && job.result ? (
                        <button
                          onClick={() => setSelectedJob(job)}
                          className="flex items-center gap-1 bg-accent/20 hover:bg-accent/30 text-accent px-2 py-1 rounded text-xs transition-colors"
                        >
                          <Eye className="w-3 h-3" /> View
                        </button>
                      ) : (
                        <span className="text-muted text-xs">—</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>

      {/* ── Job Result Modal ── */}
      {selectedJob && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-card border border-border rounded-xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-border">
              <div>
                <h2 className="text-lg font-semibold text-text">Job Result</h2>
                <p className="text-xs text-muted mt-0.5">
                  {selectedJob.type} / {selectedJob.skill_slug || "—"} / {selectedJob.client_slug || "—"}
                </p>
              </div>
              <button
                onClick={() => setSelectedJob(null)}
                className="p-1 hover:bg-border/50 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-muted" />
              </button>
            </div>

            {/* Modal body */}
            <div className="p-6 overflow-y-auto flex-1">
              {/* Status & meta */}
              <div className="flex items-center gap-3 mb-4">
                <StatusBadge status={selectedJob.status} />
                <span className="text-xs text-muted">
                  Created {new Date(selectedJob.created_at).toLocaleString()}
                </span>
                {(selectedJob.cost_usd || 0) > 0 && (
                  <span className="text-xs text-muted">Cost: ${selectedJob.cost_usd}</span>
                )}
                {(selectedJob.tokens_in || 0) > 0 && (
                  <span className="text-xs text-muted">Tokens: {selectedJob.tokens_in} in / {selectedJob.tokens_out} out</span>
                )}
              </div>

              {/* Result content */}
              {selectedJob.result?.content && (
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-text mb-2">Generated Content</h3>
                  <div className="bg-background border border-border rounded-lg p-4 max-h-96 overflow-y-auto">
                    <pre className="text-sm text-text whitespace-pre-wrap font-mono leading-relaxed">
                      {selectedJob.result.content}
                    </pre>
                  </div>
                </div>
              )}

              {/* Error display */}
              {selectedJob.status === "failed" && selectedJob.result?.error && (
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-danger mb-2">Error</h3>
                  <div className="bg-background border border-danger/30 rounded-lg p-4">
                    <pre className="text-sm text-danger whitespace-pre-wrap font-mono">
                      {selectedJob.result.error}
                    </pre>
                  </div>
                </div>
              )}

              {/* Raw JSON (collapsible) */}
              <div>
                <h3 className="text-sm font-medium text-text mb-2">Full Result JSON</h3>
                <div className="bg-background border border-border rounded-lg p-4 max-h-64 overflow-y-auto">
                  <pre className="text-xs text-muted whitespace-pre-wrap font-mono">
                    {JSON.stringify(selectedJob.result, null, 2)}
                  </pre>
                </div>
              </div>
            </div>

            {/* Modal footer */}
            <div className="px-6 py-4 border-t border-border flex justify-end">
              <button
                onClick={() => setSelectedJob(null)}
                className="bg-border/50 hover:bg-border text-text px-4 py-2 rounded-lg text-sm transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
