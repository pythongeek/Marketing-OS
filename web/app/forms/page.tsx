"use client";

import { Nav } from "@/components/nav";
import { FormInput } from "lucide-react";

const forms = [
  { name: "Client Onboarding", file: "client-onboarding.html", icon: "🎯", desc: "Onboard a new client with business goals, competitors, and website details" },
  { name: "API Credentials", file: "api-credentials.html", icon: "🔐", desc: "Collect API keys for all 23+ integrations (OpenAI, Ahrefs, Semrush, etc.)" },
  { name: "WordPress Config", file: "wordpress-config.html", icon: "🌐", desc: "Configure WordPress REST API for auto-publishing content from the vault" },
  { name: "Content Brief", file: "content-brief.html", icon: "📝", desc: "Generate a detailed content brief for the longform writer" },
  { name: "Competitor Intake", file: "competitor-intake.html", icon: "🕵️", desc: "Seed competitor intelligence with target competitors and focus areas" },
  { name: "Ad Campaign", file: "ad-campaign.html", icon: "📢", desc: "Set up a paid advertising campaign across Google, Meta, LinkedIn, or TikTok" },
  { name: "Social Calendar", file: "social-calendar.html", icon: "📅", desc: "Request a social content calendar or repurpose existing content" },
  { name: "Local SEO", file: "local-seo.html", icon: "📍", desc: "Add a local business location for GBP and citation management" },
  { name: "pSEO Config", file: "pseo-config.html", icon: "🤖", desc: "Configure a programmatic SEO project with data sources and templates" },
  { name: "Outreach Prospect", file: "outreach-prospect.html", icon: "🔗", desc: "Add link prospects or request an outreach campaign" },
  { name: "On-Page Request", file: "on-page-request.html", icon: "🔧", desc: "Request an on-page SEO audit or optimization for specific pages" },
  { name: "Tech Audit", file: "tech-audit.html", icon: "🛠️", desc: "Request a full technical SEO audit with custom scope" },
  { name: "Analytics Report", file: "analytics-report.html", icon: "📊", desc: "Configure an analytics report or dashboard" },
  { name: "Copy Request", file: "copy-request.html", icon: "✍️", desc: "Request landing page, email, or ad copy" },
  { name: "CRO Experiment", file: "cro-experiment.html", icon: "🧪", desc: "Design an A/B test or landing page optimization experiment" },
  { name: "Email Sequence", file: "email-sequence.html", icon: "📧", desc: "Build an email lifecycle sequence" },
  { name: "Influencer Campaign", file: "influencer-campaign.html", icon: "🤝", desc: "Design an influencer marketing campaign" },
  { name: "Video & Image Brief", file: "video-image-brief.html", icon: "🎬", desc: "Request a video script, AI image prompt, or infographic" },
  { name: "Pitch & Proposal", file: "pitch-proposal.html", icon: "🎯", desc: "Build a client proposal or competitive pitch deck" },
  { name: "Forecasting", file: "forecasting-request.html", icon: "🔮", desc: "Request a revenue, traffic, or conversion forecast" },
  { name: "Reputation Monitoring", file: "reputation-monitoring.html", icon: "🛡️", desc: "Configure brand mention and review monitoring" },
  { name: "GSC Property", file: "gsc-property.html", icon: "🔍", desc: "Configure Google Search Console property monitoring" },
  { name: "Bing Property", file: "bing-property.html", icon: "🔎", desc: "Configure Bing Webmaster Tools property monitoring" },
  { name: "AEO Entity Schema", file: "aeo-entity-schema.html", icon: "🧠", desc: "Register entities and schema for AI citation optimization" },
  { name: "Report Config", file: "report-config.html", icon: "📄", desc: "Configure a custom report with metrics and delivery" },
  { name: "Revenue Opportunity", file: "revenue-opportunity.html", icon: "💰", desc: "Submit a new revenue opportunity for evaluation" },
  { name: "Market Alert", file: "market-alert.html", icon: "📡", desc: "Configure algorithm update and SERP volatility alerts" },
  { name: "Playbook Request", file: "playbook-request.html", icon: "📚", desc: "Request a new SOP or playbook creation" },
  { name: "QA Check", file: "qa-check-request.html", icon: "✅", desc: "Submit content for the 7-check QA pipeline" },
  { name: "Agent Config", file: "agent-config.html", icon: "🤖", desc: "Create or update an agent with the 5-layer template" },
];

export default function FormsPage() {
  return (
    <div className="flex min-h-screen">
      <Nav />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-text">Interactive Forms</h1>
          <p className="text-muted text-sm mt-1">{forms.length} forms available — fill in your browser, save the JSON response, then tell the agent</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {forms.map((form) => (
            <a
              key={form.file}
              href={`/forms/${form.file}`}
              target="_blank"
              className="bg-card border border-border rounded-xl p-5 hover:border-accent/50 transition-colors group"
            >
              <div className="flex items-start justify-between mb-3">
                <span className="text-2xl">{form.icon}</span>
                <FormInput className="w-4 h-4 text-muted group-hover:text-accent transition-colors" />
              </div>
              <h3 className="text-sm font-semibold text-text mb-1">{form.name}</h3>
              <p className="text-xs text-muted">{form.desc}</p>
            </a>
          ))}
        </div>
      </main>
    </div>
  );
}
