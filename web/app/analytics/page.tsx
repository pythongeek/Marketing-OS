"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { BarChart3, TrendingUp, Activity, DollarSign } from "lucide-react";

export default function AnalyticsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/jobs")
      .then((r) => r.json())
      .then((d) => {
        if (d.error) {
          setError(d.error);
        } else {
          setJobs(d.jobs || []);
        }
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  const completedJobs = jobs.filter((j: any) => j.status === "completed");
  const totalCost = jobs.reduce((sum: number, j: any) => sum + (j.cost_usd || 0), 0);
  const avgCost = completedJobs.length > 0 ? totalCost / completedJobs.length : 0;

  const statusCounts = jobs.reduce((acc: any, j: any) => {
    acc[j.status] = (acc[j.status] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-text">Analytics</h1>
          <p className="text-muted text-sm mt-1">Job execution metrics and cost tracking</p>
        </div>

        {error && (
          <div className="bg-danger/10 border border-danger/30 rounded-xl p-4 mb-6 text-danger text-sm">
            <strong>Configuration needed:</strong> {error}. Please set <code className="bg-background px-1 rounded">NEXT_PUBLIC_SUPABASE_URL</code> and <code className="bg-background px-1 rounded">NEXT_PUBLIC_SUPABASE_ANON_KEY</code> in Vercel Environment Variables.
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-accent" />
              <span className="text-sm text-muted">Total Jobs</span>
            </div>
            <div className="text-2xl font-bold text-text">{jobs.length}</div>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-success" />
              <span className="text-sm text-muted">Completed</span>
            </div>
            <div className="text-2xl font-bold text-text">{completedJobs.length}</div>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-4 h-4 text-warning" />
              <span className="text-sm text-muted">Total Cost</span>
            </div>
            <div className="text-2xl font-bold text-text">${totalCost.toFixed(2)}</div>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-2">
              <BarChart3 className="w-4 h-4 text-muted" />
              <span className="text-sm text-muted">Avg Cost/Job</span>
            </div>
            <div className="text-2xl font-bold text-text">${avgCost.toFixed(2)}</div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl p-6">
          <h2 className="text-lg font-semibold text-text mb-4">Job Status Distribution</h2>
          {Object.keys(statusCounts).length === 0 ? (
            <p className="text-muted text-sm">No data yet. Run some jobs to see analytics.</p>
          ) : (
            <div className="space-y-3">
              {Object.entries(statusCounts).map(([status, count]: [string, any]) => (
                <div key={status} className="flex items-center gap-3">
                  <span className="text-xs text-muted w-20 capitalize">{status}</span>
                  <div className="flex-1 bg-border/30 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${jobs.length > 0 ? (count / jobs.length) * 100 : 0}%`,
                        backgroundColor:
                          status === "completed"
                            ? "#50C878"
                            : status === "failed"
                            ? "#E74C3C"
                            : status === "running"
                            ? "#4A90D9"
                            : "#F39C12",
                      }}
                    />
                  </div>
                  <span className="text-xs text-text w-8 text-right">{count}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
