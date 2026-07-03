"use client";

import { useEffect, useState } from "react";
import { Nav } from "@/components/nav";
import { MetricCard } from "@/components/metric-card";
import { StatusBadge } from "@/components/status-badge";
import { Users, Wrench, Activity, Zap, TrendingUp, DollarSign } from "lucide-react";
import Link from "next/link";
import { supabase } from "@/lib/supabase";

export default function DashboardPage() {
  const [stats, setStats] = useState({ clients: 0, skills: 0, jobs: 0, pendingJobs: 0, completedJobs: 0, totalCost: 0 });
  const [recentJobs, setRecentJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [liveStatus, setLiveStatus] = useState("🔴 Disconnected");

  useEffect(() => {
    async function fetchData() {
      try {
        const [clientsRes, skillsRes, jobsRes] = await Promise.all([
          fetch("/api/clients"),
          fetch("/api/skills"),
          fetch("/api/jobs"),
        ]);
        const clients = await clientsRes.json();
        const skills = await skillsRes.json();
        const jobs = await jobsRes.json();

        const jobsList = jobs.jobs || [];
        const pending = jobsList.filter((j: any) => j.status === "pending").length;
        const completed = jobsList.filter((j: any) => j.status === "completed").length;
        const totalCost = jobsList.reduce((sum: number, j: any) => sum + (j.cost_usd || 0), 0);

        setStats({
          clients: clients.clients?.length || 0,
          skills: skills.skills?.length || 0,
          jobs: jobsList.length,
          pendingJobs: pending,
          completedJobs: completed,
          totalCost: Math.round(totalCost * 100) / 100,
        });
        setRecentJobs(jobsList.slice(0, 5));
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // ── Supabase Realtime ─────────────────────────────────────────────
  useEffect(() => {
    if (!supabase) return;

    const channel = supabase
      .channel("jobs-realtime")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "jobs" },
        (payload: any) => {
          console.log("Realtime job change:", payload);
          setLiveStatus("🟢 Live");
          // Refresh all data when any job changes
          fetch("/api/jobs")
            .then((r) => r.json())
            .then((data) => {
              const jobsList = data.jobs || [];
              const pending = jobsList.filter((j: any) => j.status === "pending").length;
              const completed = jobsList.filter((j: any) => j.status === "completed").length;
              const totalCost = jobsList.reduce((sum: number, j: any) => sum + (j.cost_usd || 0), 0);
              setStats((prev) => ({
                ...prev,
                jobs: jobsList.length,
                pendingJobs: pending,
                completedJobs: completed,
                totalCost: Math.round(totalCost * 100) / 100,
              }));
              setRecentJobs(jobsList.slice(0, 5));
            });
        }
      )
      .subscribe((status: any) => {
        console.log("Realtime subscription status:", status);
        if (status === "SUBSCRIBED") {
          setLiveStatus("🟢 Live");
        }
      });

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  if (loading) return <div className="p-8 text-muted">Loading...</div>;

  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-text">Dashboard</h1>
            <p className="text-muted text-sm mt-1">AgenticMarketingPro Command Center</p>
          </div>
          <span className="text-xs text-muted bg-card border border-border rounded-full px-3 py-1">{liveStatus}</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <MetricCard title="Active Clients" value={stats.clients} icon={<Users className="w-5 h-5" />} trend="up" trendValue="3 this month" />
          <MetricCard title="Skills Loaded" value={stats.skills} icon={<Wrench className="w-5 h-5" />} subtitle="31 agents ready" />
          <MetricCard title="Total Jobs" value={stats.jobs} icon={<Activity className="w-5 h-5" />} />
          <MetricCard title="Pending Jobs" value={stats.pendingJobs} icon={<Zap className="w-5 h-5" />} trend={stats.pendingJobs > 0 ? "up" : "neutral"} trendValue={stats.pendingJobs > 0 ? "needs attention" : "all clear"} />
          <MetricCard title="Completed Jobs" value={stats.completedJobs} icon={<TrendingUp className="w-5 h-5" />} trend="up" trendValue="last 30 days" />
          <MetricCard title="Total Cost" value={`$${stats.totalCost}`} icon={<DollarSign className="w-5 h-5" />} subtitle="cumulative agent spend" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-xl p-6">
            <h2 className="text-lg font-semibold text-text mb-4">Recent Jobs</h2>
            {recentJobs.length === 0 ? (
              <p className="text-muted text-sm">No jobs yet. Trigger an agent run to get started.</p>
            ) : (
              <div className="space-y-3">
                {recentJobs.map((job: any) => (
                  <div key={job.id} className="flex items-center justify-between py-2 border-b border-border last:border-0">
                    <div>
                      <p className="text-sm text-text">{job.type}</p>
                      <p className="text-xs text-muted">{job.client_slug || "—"} / {job.skill_slug || "—"}</p>
                    </div>
                    <StatusBadge status={job.status} />
                  </div>
                ))}
              </div>
            )}
            <Link href="/jobs" className="text-accent text-sm mt-4 inline-block hover:underline">View all jobs →</Link>
          </div>

          <div className="bg-card border border-border rounded-xl p-6">
            <h2 className="text-lg font-semibold text-text mb-4">Quick Actions</h2>
            <div className="grid grid-cols-2 gap-3">
              <Link href="/forms" className="bg-border/30 hover:bg-border/50 rounded-lg p-4 text-sm text-text transition-colors">
                <span className="block text-lg mb-1">📝</span>
                Fill a Form
              </Link>
              <Link href="/clients" className="bg-border/30 hover:bg-border/50 rounded-lg p-4 text-sm text-text transition-colors">
                <span className="block text-lg mb-1">👤</span>
                Add Client
              </Link>
              <Link href="/skills" className="bg-border/30 hover:bg-border/50 rounded-lg p-4 text-sm text-text transition-colors">
                <span className="block text-lg mb-1">🛠️</span>
                Edit Skills
              </Link>
              <Link href="/brain-map" className="bg-border/30 hover:bg-border/50 rounded-lg p-4 text-sm text-text transition-colors">
                <span className="block text-lg mb-1">🧠</span>
                View Brain Map
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
