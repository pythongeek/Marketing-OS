"use client";

type Status = "pending" | "running" | "completed" | "failed" | "cancelled" | "active" | "paused" | "inactive";

const statusColors: Record<string, string> = {
  pending: "bg-warning/20 text-warning",
  running: "bg-accent/20 text-accent animate-pulse",
  completed: "bg-success/20 text-success",
  failed: "bg-danger/20 text-danger",
  cancelled: "bg-muted/20 text-muted",
  active: "bg-success/20 text-success",
  paused: "bg-warning/20 text-warning",
  inactive: "bg-muted/20 text-muted",
};

export function StatusBadge({ status }: { status: Status }) {
  const color = statusColors[status] || "bg-muted/20 text-muted";
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
      {status}
    </span>
  );
}
