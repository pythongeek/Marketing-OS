"use client";

import { useState } from "react";
import { Activity, Brain, Users, FileText, Wrench, BarChart3, FormInput, Home, Key } from "lucide-react";

const navItems = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/clients", label: "Clients", icon: Users },
  { href: "/credentials", label: "Credentials", icon: Key },
  { href: "/skills", label: "Skills", icon: Wrench },
  { href: "/jobs", label: "Jobs", icon: Activity },
  { href: "/forms", label: "Forms", icon: FormInput },
  { href: "/brain-map", label: "Brain Map", icon: Brain },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
];"lucide-react";
import Link from "next/link";

const navItems = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/clients", label: "Clients", icon: Users },
  { href: "/skills", label: "Skills", icon: Wrench },
  { href: "/jobs", label: "Jobs", icon: Activity },
  { href: "/forms", label: "Forms", icon: FormInput },
  { href: "/brain-map", label: "Brain Map", icon: Brain },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
];

export function Nav() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <nav className="h-screen bg-card border-r border-border flex flex-col w-64">
      <div className="p-6 border-b border-border">
        <h1 className="text-xl font-bold text-accent">AMP</h1>
        <p className="text-xs text-muted mt-1">Agentic Marketing Pro</p>
      </div>
      <div className="flex-1 py-4">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex items-center gap-3 px-6 py-3 text-sm text-text hover:bg-border/50 transition-colors"
          >
            <item.icon className="w-4 h-4 text-muted" />
            {item.label}
          </Link>
        ))}
      </div>
      <div className="p-4 border-t border-border text-xs text-muted">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
          System Online
        </div>
      </div>
    </nav>
  );
}
