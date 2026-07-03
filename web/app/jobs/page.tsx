"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { StatusBadge } from "@/components/status-badge";
import { Activity, RefreshCw } from "lucide-react";
import { supabase } from "@/lib/supabase";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [liveStatus, setLiveStatus] = useState("🔴 Disconnected");

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
      .subscribe((status) => {
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
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={6} className="px-4 py-8 text-center text-muted">Loading...</td></tr>
              ) : filtered.length === 0 ? (
                <tr><td colSpan={6} className="px-4 py-8 text-center text-muted">No jobs found</td></tr>
              ) : (
                filtered.map((job: any) => (
                  <tr key={job.id} className="border-t border-border hover:bg-border/20">
                    <td className="px-4 py-3 text-text">{job.type}</td>
                    <td className="px-4 py-3 text-muted">{job.client_slug || "—"}</td>
                    <td className="px-4 py-3 text-muted">{job.skill_slug || "—"}</td>
                    <td className="px-4 py-3"><StatusBadge status={job.status} /></td>
                    <td className="px-4 py-3 text-muted text-xs">{new Date(job.created_at).toLocaleString()}</td>
                    <td className="px-4 py-3 text-muted text-xs">${job.cost_usd || 0}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
