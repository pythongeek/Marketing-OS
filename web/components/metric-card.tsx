"use client";

import { ReactNode } from "react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: ReactNode;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
}

export function MetricCard({ title, value, subtitle, icon, trend, trendValue }: MetricCardProps) {
  const trendColors = {
    up: "text-success",
    down: "text-danger",
    neutral: "text-muted",
  };

  return (
    <div className="bg-card border border-border rounded-xl p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted">{title}</p>
          <p className="text-3xl font-bold text-text mt-2">{value}</p>
          {subtitle && <p className="text-xs text-muted mt-1">{subtitle}</p>}
        </div>
        <div className="text-muted">{icon}</div>
      </div>
      {trend && trendValue && (
        <div className={`text-xs mt-4 ${trendColors[trend]}`}>
          {trend === "up" ? "▲" : trend === "down" ? "▼" : "—"} {trendValue}
        </div>
      )}
    </div>
  );
}
