"""
AgenticMarketingPro — Form Presets (Additional Skills)
======================================================
Additional pre-built forms for all remaining agent skills.
Import from form_engine.py or use standalone.

Usage:
    from ui.form_presets import FormPresets
    presets = FormPresets(forms_dir)
    presets.create_competitor_intake_form()
    presets.create_ad_campaign_form()
    ... etc
"""

from pathlib import Path
from typing import Optional

from infrastructure.ui.form_engine import FormEngine, FormField, FormDefinition


class FormPresets:
    """Pre-built forms for all remaining agent skills."""

    def __init__(self, engine: FormEngine = None, forms_dir: Path = None):
        self.engine = engine or FormEngine(forms_dir)

    # ── Competitor Intelligence ───────────────────────────────────────

    def create_competitor_intake_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🕵️ Competitor Intelligence Intake",
            description="Provide competitor details so the intel agent can build a full competitive analysis.",
            submit_label="Start Competitor Analysis",
            output_filename="competitor-intake-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client Name", placeholder="e.g., acme-saas"),
                FormField("competitor_1_name", "text", required=True, label="Competitor #1 Name", placeholder="e.g., Competitor Inc."),
                FormField("competitor_1_url", "url", required=True, label="Competitor #1 Website", placeholder="https://competitor1.com"),
                FormField("competitor_1_notes", "textarea", label="What do you know about them?", placeholder="Their strengths, weaknesses, positioning, pricing...", rows=3),
                FormField("competitor_2_name", "text", label="Competitor #2 Name", placeholder="e.g., Rival Co."),
                FormField("competitor_2_url", "url", label="Competitor #2 Website", placeholder="https://competitor2.com"),
                FormField("competitor_2_notes", "textarea", label="What do you know about them?", placeholder="Their strengths, weaknesses, positioning, pricing...", rows=3),
                FormField("competitor_3_name", "text", label="Competitor #3 Name", placeholder="e.g., Alternative Ltd."),
                FormField("competitor_3_url", "url", label="Competitor #3 Website", placeholder="https://competitor3.com"),
                FormField("competitor_3_notes", "textarea", label="What do you know about them?", placeholder="Their strengths, weaknesses, positioning, pricing...", rows=3),
                FormField("focus_areas", "checkbox", label="Focus Areas", options=["SEO (keywords, backlinks, content)", "Paid Ads (campaigns, creatives, spend)", "Content (blog, resources, thought leadership)", "Social Media (presence, engagement, followers)", "Pricing & Positioning", "Product Features & UX", "Reviews & Reputation"], help_text="What aspects should the intel agent prioritize?"),
                FormField("known_gaps", "textarea", label="Known Gaps or Opportunities", placeholder="e.g., They don't have a pricing page, weak blog content, no video strategy...", rows=3),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "competitor-intake.html")

    # ── Ad Expert ─────────────────────────────────────────────────────

    def create_ad_campaign_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📢 Ad Campaign Setup",
            description="Configure a new paid advertising campaign across Google, Meta, LinkedIn, or TikTok.",
            submit_label="Create Campaign Brief",
            output_filename="ad-campaign-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("campaign_name", "text", required=True, label="Campaign Name", placeholder="e.g., Q3 SaaS Free Trial Push"),
                FormField("platform", "select", required=True, label="Platform", options=["Google Search", "Google Display", "Meta (Facebook/Instagram)", "LinkedIn", "TikTok", "Reddit", "Multi-platform"]),
                FormField("objective", "select", required=True, label="Campaign Objective", options=["Brand Awareness", "Website Traffic", "Lead Generation", "Conversions / Sales", "App Installs", "Retargeting / Remarketing"]),
                FormField("budget_daily", "number", required=True, label="Daily Budget (USD)", placeholder="100", min="10", max="100000"),
                FormField("budget_monthly", "number", label="Monthly Budget (USD)", placeholder="3000", min="100"),
                FormField("target_audience", "textarea", required=True, label="Target Audience", placeholder="Demographics, job titles, interests, behaviors, pain points...", rows=4),
                FormField("target_locations", "text", required=True, label="Target Locations", placeholder="e.g., US, Canada, UK, Australia"),
                FormField("landing_page_url", "url", required=True, label="Landing Page URL", placeholder="https://example.com/free-trial"),
                FormField("conversion_goal", "text", required=True, label="Primary Conversion Goal", placeholder="e.g., Free trial sign-up, Demo request, Ebook download"),
                FormField("conversion_value", "number", label="Estimated Conversion Value (USD)", placeholder="500", min="0", help_text="Used to calculate ROAS targets"),
                FormField("creative_assets", "textarea", label="Available Creative Assets", placeholder="Headlines, descriptions, images, videos, UGC... What do you have?", rows=3),
                FormField("exclusions", "textarea", label="Exclusions / Restrictions", placeholder="e.g., No competitors as keywords, avoid these placements, brand safety rules...", rows=2),
                FormField("start_date", "date", label="Campaign Start Date"),
                FormField("end_date", "date", label="Campaign End Date (optional)"),
                FormField("kpis", "text", label="Success KPIs", placeholder="e.g., CPA <$50, ROAS >3x, CTR >2%", default="CPA, ROAS, CTR"),
                FormField("notes", "textarea", label="Notes / Special Instructions", placeholder="Any unique campaign requirements, compliance notes, etc.", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "ad-campaign.html")

    # ── Social Media Manager ──────────────────────────────────────────

    def create_social_calendar_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📅 Social Media Calendar Request",
            description="Request a social content calendar or repurpose a published piece into 10+ formats.",
            submit_label="Generate Calendar",
            output_filename="social-calendar-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("content_to_repurpose", "url", label="Content to Repurpose (URL)", placeholder="https://example.com/blog/my-article", help_text="If blank, the agent will generate original content"),
                FormField("content_title", "text", label="Content Title", placeholder="The article or page title"),
                FormField("platforms", "checkbox", required=True, label="Target Platforms", options=["LinkedIn", "Twitter/X", "Instagram", "TikTok", "Facebook", "YouTube Shorts", "Reddit", "Threads", "Newsletter"]),
                FormField("posting_frequency", "select", required=True, label="Posting Frequency", options=["Daily", "3x per week", "2x per week", "Weekly", "As needed"], default="3x per week"),
                FormField("brand_voice", "select", label="Brand Voice for Social", options=["Professional / Thought leadership", "Casual / Conversational", "Witty / Humorous", "Educational / Helpful", "Bold / Provocative"], default="Professional / Thought leadership"),
                FormField("hashtag_strategy", "text", label="Hashtag Strategy", placeholder="e.g., #SaaS #AITools #Marketing (3-5 max per platform)"),
                FormField("cta", "text", label="Primary CTA", placeholder="e.g., Read the full article, Download the guide, Join the newsletter"),
                FormField("include_cta_link", "checkbox", label="Include CTA Link", options=["Add tracked link to landing page"]),
                FormField("content_pillars", "textarea", label="Content Pillars / Themes", placeholder="What topics should this calendar cover? e.g., Product tips, Industry news, Customer stories, Behind-the-scenes...", rows=3),
                FormField("avoid_topics", "textarea", label="Topics to Avoid", placeholder="Any sensitive subjects, competitor mentions, or off-brand topics...", rows=2),
                FormField("campaign_hashtag", "text", label="Campaign Hashtag (if applicable)", placeholder="e.g., #AcmeAI2026"),
                FormField("due_date", "date", label="Calendar Due Date"),
                FormField("notes", "textarea", label="Notes", placeholder="Any platform-specific requirements, character limits, or creative direction...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "social-calendar.html")

    # ── Local SEO Agent ───────────────────────────────────────────────

    def create_local_seo_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📍 Local SEO — Location Management",
            description="Add or update a local business location for GBP, citation, and review management.",
            submit_label="Save Location",
            output_filename="local-seo-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("business_name", "text", required=True, label="Business Name", placeholder="e.g., Acme Dental"),
                FormField("business_category", "text", required=True, label="Primary GBP Category", placeholder="e.g., Dental Clinic, Software Company, Restaurant"),
                FormField("address", "textarea", required=True, label="Full Address", placeholder="Street, City, State, ZIP, Country", rows=2),
                FormField("phone", "text", label="Phone Number", placeholder="+1-555-123-4567"),
                FormField("website", "url", label="Location Website", placeholder="https://example.com/location-name"),
                FormField("gbp_url", "url", label="Google Business Profile URL", placeholder="https://business.google.com/..."),
                FormField("service_area", "text", label="Service Area (if not storefront)", placeholder="e.g., 50-mile radius around Denver, CO"),
                FormField("hours", "textarea", label="Business Hours", placeholder="Mon-Fri: 9am-5pm, Sat: 10am-2pm, Sun: Closed", rows=2),
                FormField("target_keywords", "textarea", label="Local Target Keywords", placeholder="e.g., dentist near me, best dental clinic denver, emergency dentist...", rows=2),
                FormField("citations_needed", "checkbox", label="Citation Directories to Target", options=["Google Business Profile", "Yelp", "Bing Places", "Apple Maps", "Facebook", "Yellow Pages", "Industry-specific directories"], help_text="Which directories need updating or creation?"),
                FormField("review_platforms", "checkbox", label="Review Platforms to Monitor", options=["Google Reviews", "Yelp", "Trustpilot", "G2", "Capterra", "BBB", "Facebook Reviews"]),
                FormField("review_response_tone", "select", label="Review Response Tone", options=["Professional & Grateful", "Warm & Personal", "Concise & Business-like", "Humorous & Light"], default="Professional & Grateful"),
                FormField("geo_grid_cities", "text", label="Geo-Grid Cities", placeholder="e.g., Denver, Boulder, Aurora, Lakewood", help_text="Cities to track local rankings for"),
                FormField("competitor_locations", "textarea", label="Competitor Locations Nearby", placeholder="Names and addresses of nearby competitors...", rows=2),
                FormField("notes", "textarea", label="Notes", placeholder="Any unique local requirements, seasonal changes, or special events...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "local-seo.html")

    # ── Programmatic SEO ──────────────────────────────────────────────

    def create_pseo_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🤖 Programmatic SEO — Data Source & Template Setup",
            description="Configure a pSEO project: data source, template, URL pattern, and quality guardrails.",
            submit_label="Configure pSEO Project",
            output_filename="pseo-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("project_name", "text", required=True, label="Project Name", placeholder="e.g., City Landing Pages for HVAC"),
                FormField("data_source", "select", required=True, label="Data Source Type", options=["CSV Upload", "Google Sheets", "API Feed", "Database", "Internal data (from vault)", "Public dataset (Wikipedia, government, etc.)"]),
                FormField("data_source_url", "url", label="Data Source URL / Path", placeholder="https://docs.google.com/spreadsheets/... or /path/to/data.csv", help_text="Required for external data sources"),
                FormField("data_schema", "textarea", required=True, label="Data Schema", placeholder="What fields does each row have? e.g., city, state, population, avg_income, keyword_volume", rows=3),
                FormField("template_type", "select", required=True, label="Page Template Type", options=["Location / City page", "Comparison page", "Directory / List page", "Tool / Calculator", "FAQ / Knowledge page", "Product variant page", "Custom template"]),
                FormField("url_pattern", "text", required=True, label="URL Pattern", placeholder="e.g., /locations/{{city}}-hvac-services/", help_text="Use {{field_name}} for data substitution"),
                FormField("page_count_estimate", "number", label="Estimated Page Count", placeholder="100", min="10", max="100000"),
                FormField("content_quality", "select", required=True, label="Quality Guardrail", options=["High (unique content per page, human-reviewed)", "Medium (template + data, AI-enhanced)", "Low (template + data, minimal AI)"], default="Medium (template + data, AI-enhanced)"),
                FormField("min_word_count", "number", label="Minimum Word Count per Page", placeholder="500", default="500", min="100"),
                FormField("schema_type", "select", label="Schema Type", options=["LocalBusiness", "Organization", "Product", "FAQPage", "HowTo", "Service", "None"], default="LocalBusiness"),
                FormField("internal_linking", "checkbox", label="Internal Linking Strategy", options=["Auto-link to parent category page", "Auto-link to nearest 5 related pages", "Auto-link to all sibling pages", "Manual link list per page"]),
                FormField("publishing_schedule", "select", label="Publishing Schedule", options=["Batch (all at once)", "Staggered (10/day)", "Staggered (50/week)", "Drip (5/day)"], default="Staggered (10/day)"),
                FormField("indexing_strategy", "select", label="Indexing Strategy", options=["Submit all to GSC immediately", "Submit in batches of 50", "Let Google discover naturally", "Priority pages first"], default="Submit in batches of 50"),
                FormField("duplicate_content_check", "checkbox", label="Duplicate Content Check", options=["Run Copyscape on every page before publish"], help_text="HITL Gate: pSEO batches >50 pages need human approval"),
                FormField("notes", "textarea", label="Notes / Special Requirements", placeholder="Any unique data transformations, custom fields, or compliance requirements...", rows=3),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "pseo-config.html")

    # ── Off-Page Strategist ───────────────────────────────────────────

    def create_outreach_prospect_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🔗 Link Outreach — Prospect Intake",
            description="Add new link prospects or request an outreach campaign for a specific client or page.",
            submit_label="Add to Outreach Queue",
            output_filename="outreach-prospect-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("target_page", "url", required=True, label="Page to Build Links To", placeholder="https://example.com/blog/target-page"),
                FormField("target_keywords", "text", label="Target Keywords for This Page", placeholder="e.g., best CRM software, CRM for small business"),
                FormField("prospect_type", "select", required=True, label="Prospect Type", options=["Guest post opportunity", "Resource page link", "Broken link replacement", "Skyscraper outreach", "HARO / Connectively pitch", "Digital PR / Press mention", "Influencer collaboration", "Directory / List submission", "Forum / Community link"]),
                FormField("prospect_url", "url", required=True, label="Prospect Website / Page", placeholder="https://targetsite.com/blog/"),
                FormField("prospect_contact", "email", label="Contact Email (if known)", placeholder="editor@targetsite.com"),
                FormField("prospect_dr", "number", label="Prospect Domain Rating (DR)", placeholder="30", min="0", max="100"),
                FormField("outreach_angle", "textarea", required=True, label="Outreach Angle", placeholder="Why should they link to you? What value do you offer?", rows=3),
                FormField("personalization_notes", "textarea", label="Personalization Notes", placeholder="Anything specific about this prospect: their recent articles, their interests, mutual connections...", rows=2),
                FormField("follow_up_count", "select", label="Follow-up Sequence", options=["No follow-up", "1 follow-up", "2 follow-ups", "3 follow-ups (max)"], default="2 follow-ups"),
                FormField("template_style", "select", label="Email Template Style", options=["Value-first (no ask)", "Direct ask (polite)", "Collaboration pitch", "Data / study share", "Resource suggestion"], default="Value-first (no ask)"),
                FormField("batch_size", "number", label="Batch Size (prospects per week)", placeholder="10", default="10", min="1", max="100"),
                FormField("notes", "textarea", label="Notes", placeholder="Any special instructions for this outreach campaign...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "outreach-prospect.html")

    # ── On-Page Optimizer ─────────────────────────────────────────────

    def create_on_page_request_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🔧 On-Page Optimization Request",
            description="Request an on-page SEO audit or optimization for specific pages.",
            submit_label="Request Optimization",
            output_filename="on-page-request-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("pages_to_optimize", "textarea", required=True, label="Pages to Optimize", placeholder="One URL per line. e.g.,\nhttps://example.com/pricing\nhttps://example.com/blog/top-post", rows=4),
                FormField("optimization_scope", "checkbox", required=True, label="Optimization Scope", options=["Title tags & meta descriptions", "H1–H3 header structure", "Internal linking", "Schema markup (JSON-LD)", "Image alt text & optimization", "URL structure / redirects", "Cannibalization audit", "Content freshness update", "Mobile usability", "Page speed fixes"]),
                FormField("priority_pages", "text", label="Priority Pages (if not all)", placeholder="Comma-separated URLs that need immediate attention"),
                FormField("target_keywords", "textarea", label="Target Keywords to Map", placeholder="Keyword → URL mapping, one per line. e.g.,\nbest CRM software → /pricing\nCRM for small business → /features"),
                FormField("schema_types_needed", "checkbox", label="Schema Types Needed", options=["Organization", "Product", "FAQ", "HowTo", "BreadcrumbList", "Review / Rating", "Article", "LocalBusiness", "Service"]),
                FormField("cms", "select", label="CMS (for implementation notes)", options=["WordPress", "Webflow", "HubSpot", "Shopify", "Framer", "Custom / Other"]),
                FormField("seo_plugin", "select", label="SEO Plugin", options=["None", "Yoast SEO", "Rank Math", "All in One SEO", "SEOPress"], default="Rank Math"),
                FormField("competitor_urls_for_comparison", "textarea", label="Competitor URLs for Comparison", placeholder="Top-ranking pages to compare against (one per line)", rows=2),
                FormField("deadline", "date", label="Deadline for Optimizations"),
                FormField("notes", "textarea", label="Notes", placeholder="Any specific constraints, brand requirements, or technical limitations...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "on-page-request.html")

    # ── Technical SEO Auditor ─────────────────────────────────────────

    def create_tech_audit_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🛠️ Technical SEO Audit Request",
            description="Request a full technical SEO audit for a client website.",
            submit_label="Request Audit",
            output_filename="tech-audit-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("website", "url", required=True, label="Website to Audit", placeholder="https://example.com"),
                FormField("audit_type", "select", required=True, label="Audit Type", options=["Full 47-item audit (recommended)", "Quick crawl (top 100 pages)", "Core Web Vitals only", "Mobile usability only", "Security & HTTPS only", "Indexation & crawlability only", "Schema & structured data only", "Custom scope"]),
                FormField("audit_scope_custom", "textarea", label="Custom Audit Scope", placeholder="Specify what to check if 'Custom scope' selected", rows=2, depends_on="audit_type", depends_value="Custom scope"),
                FormField("page_count_estimate", "number", label="Estimated Total Pages", placeholder="500", min="1"),
                FormField("staging_site", "url", label="Staging Site URL (if different from production)", placeholder="https://staging.example.com"),
                FormField("has_javascript", "checkbox", label="JavaScript Rendering", options=["Site uses heavy JavaScript (React, Vue, Angular) — requires JS rendering audit"]),
                FormField("has_international", "checkbox", label="International / Multi-language", options=["Site has hreflang or multi-language versions"]),
                FormField("has_ecommerce", "checkbox", label="E-commerce", options=["Site has product pages, checkout, cart functionality"]),
                FormField("has_subdomains", "text", label="Subdomains to Include", placeholder="e.g., blog.example.com, shop.example.com"),
                FormField("exclusions", "textarea", label="Pages / Sections to Exclude", placeholder="e.g., /admin/, /cart/, /account/, user-generated content...", rows=2),
                FormField("previous_issues", "textarea", label="Known Previous Issues", placeholder="Any past manual actions, penalties, or major technical problems...", rows=2),
                FormField("priority", "select", label="Priority", options=["P0 (Urgent — site issues detected)", "P1 (High — within 3 days)", "P2 (Medium — within 1 week)", "P3 (Low — standard cadence)"], default="P1 (High — within 3 days)"),
                FormField("notes", "textarea", label="Notes", placeholder="Any special tools, access requirements, or context...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "tech-audit.html")

    # ── Analytics Expert ──────────────────────────────────────────────

    def create_analytics_report_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📊 Analytics Report Configuration",
            description="Configure the scope, metrics, and format for an analytics report or dashboard.",
            submit_label="Generate Report Config",
            output_filename="analytics-report-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("report_type", "select", required=True, label="Report Type", options=["Weekly Digest", "Monthly Performance Report", "Quarterly Business Review (QBR)", "Campaign Post-Mortem", "Channel Attribution Analysis", "Funnel Analysis", "Conversion Lift Study", "Custom Dashboard"]),
                FormField("date_range", "select", required=True, label="Date Range", options=["Last 7 days", "Last 30 days", "Last 90 days", "Year to date", "Custom range"]),
                FormField("date_range_custom_start", "date", label="Custom Start Date", depends_on="date_range", depends_value="Custom range"),
                FormField("date_range_custom_end", "date", label="Custom End Date", depends_on="date_range", depends_value="Custom range"),
                FormField("metrics", "checkbox", required=True, label="Metrics to Include", options=["Organic traffic (sessions, users)", "Keyword rankings & position changes", "CTR & click data (GSC)", "Conversions & conversion rate", "Revenue / MRR impact", "Cost per acquisition (CPA)", "Return on ad spend (ROAS)", "Channel mix (traffic sources)", "Device & geo breakdown", "Page-level performance", "Content performance (top/bottom)", "Core Web Vitals trends", "AEO/GEO citation metrics"]),
                FormField("comparison_period", "select", label="Comparison Period", options=["Previous period", "Year-over-year", "No comparison"], default="Previous period"),
                FormField("segments", "checkbox", label="Segments to Break Out", options=["New vs. returning visitors", "Mobile vs. desktop", "Geo / region", "Campaign / channel", "Content type", "Client-defined segments"]),
                FormField("output_format", "select", label="Output Format", options=["Markdown report (vault)", "HTML dashboard", "PDF export", "Slide deck (PPT)", "Email summary"], default="Markdown report (vault)"),
                FormField("include_recommendations", "checkbox", label="Include Recommendations", options=["Add actionable next steps and recommendations"], default="checked"),
                FormField("audience", "select", label="Report Audience", options=["Internal team (detailed)", "Client (executive summary)", "Client (detailed)", "Stakeholder / Investor"], default="Client (detailed)"),
                FormField("delivery_date", "date", label="Report Delivery Date"),
                FormField("notes", "textarea", label="Notes", placeholder="Any specific KPIs, custom metrics, or reporting requirements...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "analytics-report.html")

    # ── Copywriter ──────────────────────────────────────────────────────

    def create_copy_request_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="✍️ Copywriting Request",
            description="Request landing page copy, email copy, ad copy, or any short-form marketing copy.",
            submit_label="Request Copy",
            output_filename="copy-request-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("copy_type", "select", required=True, label="Copy Type", options=["Landing page (hero + sections)", "Email sequence (multiple emails)", "Ad copy (headlines + descriptions)", "Sales page", "Product description", "CTA buttons + microcopy", "Homepage rewrite", "About page", "Pricing page", "FAQ page", "Case study summary", "Social media captions", "Video script (short)", "Other"]),
                FormField("copy_type_other", "text", label="Other Copy Type", placeholder="Describe what you need", depends_on="copy_type", depends_value="Other"),
                FormField("target_audience", "textarea", required=True, label="Target Audience", placeholder="Who is this for? Their pain points, desires, and current state of awareness...", rows=3),
                FormField("value_proposition", "textarea", required=True, label="Value Proposition", placeholder="What makes this product/service uniquely valuable? What transformation does it create?", rows=3),
                FormField("tone", "select", required=True, label="Tone", options=["Professional / Authoritative", "Conversational / Friendly", "Bold / Provocative", "Warm / Empathetic", "Humorous / Witty", "Urgent / Scarcity-driven", "Luxury / Premium"], default="Professional / Authoritative"),
                FormField("word_count", "number", label="Target Word Count", placeholder="500", default="500", min="50", max="5000"),
                FormField("key_messages", "textarea", label="Key Messages to Include", placeholder="Must-include points, statistics, testimonials, or proof points...", rows=3),
                FormField("cta", "text", required=True, label="Primary Call to Action", placeholder="e.g., Start your free trial, Book a demo, Get the template"),
                FormField("cta_url", "url", label="CTA Destination URL", placeholder="https://example.com/signup"),
                FormField("objections_to_address", "textarea", label="Objections to Address", placeholder="What concerns might the reader have? Price, complexity, trust, timing...", rows=2),
                FormField("examples", "textarea", label="Examples of Copy You Like", placeholder="Paste URLs or copy of pages/emails you admire...", rows=2),
                FormField("forbidden_words", "text", label="Words / Phrases to Avoid", placeholder="e.g., revolutionary, game-changing, world-class, leverage"),
                FormField("seo_keywords", "text", label="SEO Keywords (if applicable)", placeholder="Primary and secondary keywords to weave in naturally"),
                FormField("deadline", "date", label="Deadline"),
                FormField("notes", "textarea", label="Notes", placeholder="Any brand guidelines, compliance requirements, or special formatting...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "copy-request.html")

    # ── CRO Agent ─────────────────────────────────────────────────────

    def create_cro_experiment_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🧪 CRO Experiment Setup",
            description="Design an A/B test, multivariate test, or landing page optimization experiment.",
            submit_label="Design Experiment",
            output_filename="cro-experiment-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("experiment_name", "text", required=True, label="Experiment Name", placeholder="e.g., Homepage Hero CTA Test — V1 vs V2"),
                FormField("page_url", "url", required=True, label="Page URL", placeholder="https://example.com/landing-page"),
                FormField("experiment_type", "select", required=True, label="Experiment Type", options=["A/B Test (2 variants)", "A/B/n Test (3+ variants)", "Multivariate Test", "Split URL Test", "Personalization / Targeting", "Before/After (no split)"]),
                FormField("hypothesis", "textarea", required=True, label="Hypothesis", placeholder="If we change [X], then [Y] will increase because [Z]...", rows=3),
                FormField("primary_metric", "select", required=True, label="Primary Success Metric", options=["Conversion rate", "Click-through rate (CTR)", "Form completion rate", "Revenue per visitor", "Average order value", "Time on page", "Bounce rate", "Scroll depth"]),
                FormField("secondary_metrics", "checkbox", label="Secondary Metrics", options=["Bounce rate", "Time on page", "Scroll depth", "Form starts", "Form abandonment", "Revenue per visitor", "Return visitor rate"]),
                FormField("variant_description", "textarea", required=True, label="Variant Description", placeholder="What exactly are you testing? e.g.,\nControl: Current headline 'The Best CRM'\nVariant: New headline 'Close More Deals in Half the Time'", rows=4),
                FormField("traffic_source", "text", label="Traffic Source", placeholder="e.g., Organic search, Paid search, Social, Email, All traffic"),
                FormField("audience_segments", "text", label="Audience Segments", placeholder="e.g., New visitors, Returning visitors, Mobile users, Desktop users"),
                FormField("minimum_sample_size", "number", label="Minimum Sample Size", placeholder="1000", default="1000", min="100"),
                FormField("minimum_duration_days", "number", label="Minimum Test Duration (days)", placeholder="14", default="14", min="3", max="90"),
                FormField("confidence_level", "select", label="Confidence Level", options=["90%", "95%", "99%"], default="95%"),
                FormField("tools", "select", label="Testing Tool", options=["Google Optimize (deprecated — suggest alternative)", "Optimizely", "VWO", "Unbounce", "Instapage", "HubSpot A/B", "Custom JS (developer required)", "Not sure — recommend best tool"], default="Not sure — recommend best tool"),
                FormField("implementation_notes", "textarea", label="Implementation Notes", placeholder="CMS, any existing testing infrastructure, developer availability...", rows=2),
                FormField("notes", "textarea", label="Notes", placeholder="Any prior test results, industry benchmarks, or constraints...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "cro-experiment.html")

    # ── Email Lifecycle Agent ─────────────────────────────────────────

    def create_email_sequence_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📧 Email Sequence Builder",
            description="Design an email lifecycle sequence: welcome, nurture, re-engagement, or promotional.",
            submit_label="Build Sequence",
            output_filename="email-sequence-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("sequence_name", "text", required=True, label="Sequence Name", placeholder="e.g., 7-Day Welcome Nurture"),
                FormField("sequence_type", "select", required=True, label="Sequence Type", options=["Welcome / Onboarding", "Lead Nurture (top of funnel)", "Product Trial Nurture", "Post-Purchase / Onboarding", "Re-engagement / Win-back", "Abandoned Cart", "Promotional / Launch", "Event / Webinar Follow-up", "Referral / Advocate", "Customer Success / Renewal"]),
                FormField("email_count", "number", required=True, label="Number of Emails", placeholder="5", default="5", min="1", max="20"),
                FormField("send_schedule", "textarea", required=True, label="Send Schedule", placeholder="Day 1: immediate\nDay 2: +1 day\nDay 3: +2 days\netc."),
                FormField("trigger", "select", required=True, label="Trigger", options=["User signs up", "User downloads lead magnet", "User starts free trial", "User makes purchase", "User abandons cart", "User becomes inactive (7 days)", "User becomes inactive (30 days)", "Manual / One-time broadcast", "Date-based (e.g., birthday, renewal)"]),
                FormField("audience_segment", "text", required=True, label="Audience Segment", placeholder="e.g., All new signups, Trial users who haven't converted, Lapsed customers..."),
                FormField("personalization_fields", "checkbox", label="Personalization Fields", options=["First name", "Company name", "Industry", "Last activity", "Product usage", "Purchase history", "Location / timezone"]),
                FormField("tone", "select", label="Email Tone", options=["Professional / Educational", "Conversational / Friendly", "Bold / Direct", "Warm / Supportive", "Urgent / Scarcity", "Humorous / Light"], default="Professional / Educational"),
                FormField("cta_per_email", "text", label="Primary CTA per Email", placeholder="e.g., Day 1: Read guide, Day 2: Watch demo, Day 3: Start trial..."),
                FormField("subject_line_style", "select", label="Subject Line Style", options=["Curiosity-driven", "Benefit-driven", "Question-based", "How-to", "Listicle", "Personalized", "Urgency / FOMO", "A/B test (multiple options)"], default="A/B test (multiple options)"),
                FormField("spam_check", "checkbox", label="Spam Compliance", options=["Run spam score check on every email", "Include unsubscribe link in every email", "Check against brand voice guide"]),
                FormField("email_platform", "select", label="Email Platform", options=["HubSpot", "Klaviyo", "Mailchimp", "ActiveCampaign", "ConvertKit", "MailerLite", "Customer.io", "Other"], default="HubSpot"),
                FormField("email_platform_other", "text", label="Other Platform", placeholder="Platform name", depends_on="email_platform", depends_value="Other"),
                FormField("existing_sequence", "url", label="Existing Sequence to Improve (URL)", placeholder="Link to current email sequence or template"),
                FormField("notes", "textarea", label="Notes", placeholder="Any brand-specific email requirements, compliance notes, or past performance data...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "email-sequence.html")

    # ── Influencer Agent ──────────────────────────────────────────────

    def create_influencer_campaign_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🤝 Influencer Campaign Setup",
            description="Design an influencer marketing campaign: goals, creator criteria, compensation, and content brief.",
            submit_label="Design Campaign",
            output_filename="influencer-campaign-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("campaign_name", "text", required=True, label="Campaign Name", placeholder="e.g., Q3 Micro-Influencer Awareness Push"),
                FormField("campaign_goal", "select", required=True, label="Campaign Goal", options=["Brand Awareness", "Product Launch", "Content Generation (UGC)", "Traffic / Clicks", "Conversions / Sales", "App Installs", "Community Building", "Event Promotion"]),
                FormField("product_description", "textarea", required=True, label="Product / Service to Promote", placeholder="What is the creator promoting? Key features, benefits, and unique selling points...", rows=3),
                FormField("target_audience", "textarea", required=True, label="Target Audience", placeholder="Who should the creator's audience be? Demographics, interests, behaviors...", rows=3),
                FormField("creator_criteria", "checkbox", required=True, label="Creator Criteria", options=["Follower count (micro: 10K-100K, macro: 100K-1M, mega: 1M+)", "Engagement rate (>3%)", "Niche relevance", "Location / Language", "Content quality (professional production)", "Authenticity / no fake followers", "Past brand collaborations", "Audience demographic match"]),
                FormField("follower_range", "select", label="Preferred Follower Range", options=["Nano (1K–10K)", "Micro (10K–100K)", "Mid-tier (100K–500K)", "Macro (500K–1M)", "Mega (1M+)", "Any size (relevance > reach)"], default="Micro (10K–100K)"),
                FormField("content_format", "checkbox", required=True, label="Content Format", options=["Instagram Feed Post", "Instagram Story / Reel", "TikTok Video", "YouTube Video (integrated)", "YouTube Short", "Twitter/X Thread", "LinkedIn Post", "Blog Post / Review", "Podcast Mention", "Newsletter Feature", "Live Stream"]),
                FormField("compensation_model", "select", required=True, label="Compensation Model", options=["Fixed fee per post", "Performance-based (CPA / sales)", "Product seeding (free product only)", "Affiliate commission", "Equity / Revenue share", "Hybrid (fixed + performance)"]),
                FormField("budget_per_creator", "number", label="Budget Per Creator (USD)", placeholder="500", min="0"),
                FormField("total_budget", "number", label="Total Campaign Budget (USD)", placeholder="5000", min="0"),
                FormField("creator_count", "number", label="Number of Creators", placeholder="10", default="10", min="1"),
                FormField("key_messages", "textarea", label="Key Messages / Talking Points", placeholder="What must the creator mention? What should they avoid?", rows=3),
                FormField("hashtags", "text", label="Required Hashtags / Tags", placeholder="e.g., #AcmePartner #SaaSForTeams @acme_official"),
                FormField("usage_rights", "select", label="Content Usage Rights", options=["Creator keeps rights (no reuse)", "Brand can reuse in organic social", "Brand can reuse in paid ads", "Brand can reuse everywhere (full rights)"], default="Brand can reuse in organic social"),
                FormField("campaign_dates", "text", label="Campaign Dates", placeholder="e.g., Start: 2026-07-01, End: 2026-08-15"),
                FormField("notes", "textarea", label="Notes", placeholder="Any specific creator wishlist, competitor collaborations to avoid, or compliance requirements...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "influencer-campaign.html")

    # ── Video / Image Producer ────────────────────────────────────────

    def create_video_image_brief_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🎬 Video & Image Production Brief",
            description="Request a video script, AI image prompt, infographic spec, or thumbnail design.",
            submit_label="Create Production Brief",
            output_filename="video-image-brief-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("asset_type", "select", required=True, label="Asset Type", options=["Video Script (explainer)", "Video Script (tutorial)", "Video Script (promotional)", "AI Image Prompt (hero image)", "AI Image Prompt (social graphic)", "Infographic Design Brief", "Thumbnail Design Brief", "Slide Deck Design Brief", "Animated GIF / Motion Graphic Brief", "Podcast Cover / Audio Graphic"]),
                FormField("content_topic", "text", required=True, label="Content Topic / Subject", placeholder="e.g., How our AI saves 10 hours/week on reporting"),
                FormField("target_audience", "textarea", required=True, label="Target Audience", placeholder="Who is watching / viewing this? What do they care about?", rows=2),
                FormField("duration_length", "text", label="Duration / Dimensions", placeholder="e.g., 60-second video, 1200x628 social graphic, 1920x1080 thumbnail"),
                FormField("style", "select", label="Visual Style", options=["Minimal / Clean", "Bold / High-contrast", "Warm / Friendly", "Corporate / Professional", "Playful / Illustrative", "Cinematic / Dramatic", "Retro / Nostalgic", "Tech / Futuristic"], default="Minimal / Clean"),
                FormField("tone", "select", label="Tone / Mood", options=["Educational / Informative", "Inspirational / Motivational", "Humorous / Light", "Urgent / Action-oriented", "Emotional / Story-driven", "Confident / Authoritative"], default="Educational / Informative"),
                FormField("key_visual_elements", "textarea", label="Key Visual Elements", placeholder="What must be included? Product screenshots, people, data visualizations, specific colors, logos...", rows=2),
                FormField("reference_examples", "textarea", label="Reference Examples", placeholder="URLs or descriptions of videos/images you like...", rows=2),
                FormField("brand_colors", "text", label="Brand Colors", placeholder="e.g., #4A90D9, #50C878, #FFD700"),
                FormField("text_overlay", "text", label="Required Text / Headline", placeholder="e.g., 'Save 10 Hours a Week' or 'The Complete Guide to AI SEO'"),
                FormField("cta", "text", label="Call to Action (if applicable)", placeholder="e.g., Watch the full video, Download the guide, Try it free"),
                FormField("platform", "select", label="Primary Platform", options=["YouTube", "TikTok", "Instagram", "LinkedIn", "Twitter/X", "Website / Blog", "Email", "Paid Ads (Meta)", "Paid Ads (Google)", "Multiple platforms"], default="YouTube"),
                FormField("ai_tools", "checkbox", label="AI Tools to Use", options=["HeyGen (AI avatars)", "Synthesia (AI video)", "ElevenLabs (AI voice)", "Midjourney (AI images)", "DALL-E (AI images)", "Runway (AI video)", "Canva (design)", "Figma (design)"]),
                FormField("deadline", "date", label="Production Deadline"),
                FormField("notes", "textarea", label="Notes", placeholder="Any technical constraints, accessibility requirements, or brand guidelines...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "video-image-brief.html")

    # ── Pitch Agent ───────────────────────────────────────────────────

    def create_pitch_proposal_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🎯 Pitch & Proposal Builder",
            description="Build a client proposal or competitive pitch deck with audit findings and strategic recommendations.",
            submit_label="Build Proposal",
            output_filename="pitch-proposal-response.json",
            fields=[
                FormField("client", "text", required=True, label="Prospect Name", placeholder="e.g., Prospect Corp"),
                FormField("client_website", "url", required=True, label="Prospect Website", placeholder="https://prospect.com"),
                FormField("industry", "text", required=True, label="Industry", placeholder="e.g., B2B SaaS, Healthcare, E-commerce"),
                FormField("company_size", "select", label="Company Size", options=["Startup (1-50)", "Small (51-200)", "Mid-market (201-1000)", "Enterprise (1000+)"], default="Mid-market (201-1000)"),
                FormField("proposal_type", "select", required=True, label="Proposal Type", options=["New client pitch", "Upsell / Expansion", "Renewal / Retention", "Competitive displacement (switch from another agency)", "Project-based proposal", "Retainer proposal"]),
                FormField("prospect_pain_points", "textarea", required=True, label="Prospect Pain Points", placeholder="What problems are they facing? What have they told you? What did the audit reveal?", rows=3),
                FormField("prospect_goals", "textarea", required=True, label="Prospect Goals", placeholder="What do they want to achieve? Revenue targets, traffic goals, brand awareness, etc.", rows=3),
                FormField("competitors", "textarea", label="Key Competitors", placeholder="Names and websites of their top competitors...", rows=2),
                FormField("audit_findings", "textarea", label="Audit Findings to Include", placeholder="What did the competitive audit or site audit reveal? Key gaps and opportunities...", rows=3),
                FormField("proposed_scope", "textarea", required=True, label="Proposed Scope of Work", placeholder="What services are you proposing? SEO, content, paid, social, etc.", rows=3),
                FormField("proposed_tier", "select", label="Proposed Tier", options=["Starter ($2,500/mo)", "Growth ($4,500/mo)", "Scale ($8,500/mo)", "Enterprise (custom)"], default="Growth ($4,500/mo)"),
                FormField("timeline", "text", label="Proposed Timeline", placeholder="e.g., 90-day initial engagement, then ongoing retainer"),
                FormField("differentiator", "textarea", label="Why Us? (Differentiator)", placeholder="What makes your agency the right choice? Unique methodology, case studies, team expertise...", rows=3),
                FormField("case_studies", "textarea", label="Relevant Case Studies", placeholder="Past clients in the same vertical with similar results...", rows=2),
                FormField("team_members", "textarea", label="Team Members to Mention", placeholder="Who will work on this account? Their roles and expertise...", rows=2),
                FormField("next_steps", "text", label="Proposed Next Steps", placeholder="e.g., Strategy call on [date], Contract review, Kickoff within 2 weeks"),
                FormField("delivery_format", "select", label="Output Format", options=["PDF proposal", "Google Slides deck", "Notion page", "Markdown document (vault)", "Loom video walkthrough + PDF"], default="PDF proposal"),
                FormField("notes", "textarea", label="Notes", placeholder="Any special requirements, pricing constraints, or deal-breakers...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "pitch-proposal.html")

    # ── Forecasting Agent ─────────────────────────────────────────────

    def create_forecasting_request_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🔮 Forecasting Request",
            description="Request a revenue, traffic, or conversion forecast with scenario modeling.",
            submit_label="Generate Forecast",
            output_filename="forecasting-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("forecast_type", "select", required=True, label="Forecast Type", options=["Revenue / MRR forecast", "Organic traffic forecast", "Paid traffic forecast", "Conversion rate forecast", "Lead volume forecast", "Full-funnel forecast (traffic → leads → revenue)", "Market share forecast"]),
                FormField("time_horizon", "select", required=True, label="Time Horizon", options=["30 days", "90 days", "6 months", "12 months", "24 months"], default="12 months"),
                FormField("historical_data", "textarea", required=True, label="Historical Data", placeholder="Paste or describe historical performance. e.g.,\nJan: 1,000 sessions, 50 leads, $10K revenue\nFeb: 1,200 sessions, 60 leads, $12K revenue\n...", rows=4),
                FormField("baseline_metrics", "text", label="Current Baseline Metrics", placeholder="e.g., 5,000 monthly sessions, 2% conversion rate, $50K MRR"),
                FormField("growth_assumptions", "textarea", label="Growth Assumptions", placeholder="What initiatives will drive growth? e.g., 4 new content pieces/month, $5K ad spend, schema deployment...", rows=3),
                FormField("seasonality", "textarea", label="Seasonality / Cyclical Patterns", placeholder="Any known seasonal effects? e.g., Q4 is peak, summer is slow, holiday dips...", rows=2),
                FormField("scenarios", "checkbox", label="Scenarios to Model", options=["Conservative (slow growth)", "Base case (expected)", "Optimistic (accelerated growth)", "Best case (viral / breakthrough)", "Downside (market downturn / competition)"]),
                FormField("confidence_interval", "select", label="Confidence Interval", options=["80%", "90%", "95%"], default="90%"),
                FormField("output_format", "select", label="Output Format", options=["Monthly table (markdown)", "Quarterly summary", "Chart + table (dashboard)", "Monte Carlo simulation (probabilistic)", "Executive summary only"], default="Monthly table (markdown)"),
                FormField("output_destination", "select", label="Save To", options=["Client vault folder", "Profit plan", "Both"], default="Both"),
                FormField("notes", "textarea", label="Notes", placeholder="Any specific models, assumptions, or constraints to include...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "forecasting-request.html")

    # ── Reputation Agent ──────────────────────────────────────────────

    def create_reputation_monitoring_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🛡️ Reputation Monitoring Setup",
            description="Configure brand mention monitoring, review tracking, and crisis response protocols.",
            submit_label="Configure Monitoring",
            output_filename="reputation-monitoring-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("brand_name", "text", required=True, label="Brand Name(s) to Monitor", placeholder="e.g., Acme, Acme Inc., Acme Software"),
                FormField("product_names", "text", label="Product Names to Monitor", placeholder="e.g., Acme CRM, Acme Analytics (comma-separated)"),
                FormField("executive_names", "text", label="Executive Names to Monitor", placeholder="e.g., CEO name, founder name (comma-separated)"),
                FormField("monitoring_sources", "checkbox", required=True, label="Sources to Monitor", options=["Google Reviews", "Yelp", "Trustpilot", "G2", "Capterra", "BBB", "App Store / Play Store", "Reddit", "Twitter/X", "LinkedIn", "News / Press", "Forums / Communities", "YouTube comments", "Glassdoor (employer reputation)"]),
                FormField("alert_threshold", "select", label="Alert Threshold", options=["Any new negative review (<3 stars)", "Negative sentiment spike (>2σ)", "Viral mention (shares >100)", "Crisis keyword detected (lawsuit, scam, fraud)", "Manual action only"], default="Any new negative review (<3 stars)"),
                FormField("response_protocol", "select", label="Review Response Protocol", options=["Auto-draft response (human approves)", "Auto-publish positive review thanks", "Human-only (no auto-response)", "Escalate to human for all negative reviews"], default="Auto-draft response (human approves)"),
                FormField("response_tone", "select", label="Response Tone", options=["Professional & Empathetic", "Direct & Solution-oriented", "Warm & Personal", "Legal / Formal (for serious issues)"], default="Professional & Empathetic"),
                FormField("competitor_mentions", "checkbox", label="Competitor Mention Tracking", options=["Track when competitors are mentioned alongside our brand"]),
                FormField("crisis_keywords", "text", label="Crisis Keywords to Watch", placeholder="e.g., lawsuit, scam, fraud, data breach, outage, refund"),
                FormField("escalation_contact", "text", label="Crisis Escalation Contact", placeholder="Name and email for immediate crisis alerts"),
                FormField("reporting_frequency", "select", label="Reporting Frequency", options=["Daily", "Weekly", "Monthly"], default="Weekly"),
                FormField("notes", "textarea", label="Notes", placeholder="Any past reputation issues, known detractors, or special monitoring requirements...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "reputation-monitoring.html")

    # ── GSC Expert ──────────────────────────────────────────────────────

    def create_gsc_property_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🔍 Google Search Console — Property Setup",
            description="Configure GSC property monitoring for a client website.",
            submit_label="Configure GSC Monitoring",
            output_filename="gsc-property-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("gsc_property_url", "url", required=True, label="GSC Property URL", placeholder="https://example.com/ or sc-domain:example.com"),
                FormField("property_type", "select", label="Property Type", options=["Domain (sc-domain:)", "URL prefix (https://)"], default="URL prefix (https://)"),
                FormField("verification_method", "select", label="Verification Method", options=["HTML file", "HTML tag", "DNS record", "Google Analytics"], default="HTML tag"),
                FormField("sitemap_url", "url", label="Sitemap URL", placeholder="https://example.com/sitemap.xml"),
                FormField("monitoring_focus", "checkbox", label="Monitoring Focus", options=["Search queries & CTR", "Index coverage & errors", "Core Web Vitals", "Mobile usability", "Manual actions", "Security issues", "Backlinks (internal + external)", "Structured data errors"], help_text="What should the GSC expert prioritize?"),
                FormField("ctr_alert_threshold", "number", label="CTR Drop Alert Threshold (%)", placeholder="20", default="20", min="5", max="50", help_text="Alert if CTR drops by more than this %"),
                FormField("position_alert_threshold", "number", label="Position Drop Alert Threshold", placeholder="5", default="5", min="1", max="20", help_text="Alert if average position drops by more than this many spots"),
                FormField("index_error_alert_threshold", "number", label="Index Error Alert Threshold", placeholder="10", default="10", min="1", max="100", help_text="Alert if new index errors exceed this count"),
                FormField("reporting_frequency", "select", label="Reporting Frequency", options=["Daily", "Weekly", "Bi-weekly"], default="Weekly"),
                FormField("notes", "textarea", label="Notes", placeholder="Any known GSC issues, manual actions, or special monitoring requirements...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "gsc-property.html")

    # ── Bing WMT Expert ───────────────────────────────────────────────

    def create_bing_property_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🔎 Bing Webmaster Tools — Property Setup",
            description="Configure Bing WMT property monitoring for a client website.",
            submit_label="Configure Bing Monitoring",
            output_filename="bing-property-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("bing_site_url", "url", required=True, label="Bing Site URL", placeholder="https://example.com/"),
                FormField("sitemap_url", "url", label="Sitemap URL", placeholder="https://example.com/sitemap.xml"),
                FormField("monitoring_focus", "checkbox", label="Monitoring Focus", options=["Search queries & traffic", "Index status & crawl issues", "Crawl stats", "Inbound links", "SEO recommendations (Bing)", "Core Web Vitals", "Mobile friendliness"]),
                FormField("traffic_alert_threshold", "number", label="Traffic Drop Alert Threshold (%)", placeholder="20", default="20", min="5", max="50"),
                FormField("crawl_error_alert_threshold", "number", label="Crawl Error Alert Threshold", placeholder="10", default="10", min="1", max="100"),
                FormField("reporting_frequency", "select", label="Reporting Frequency", options=["Daily", "Weekly", "Bi-weekly"], default="Weekly"),
                FormField("notes", "textarea", label="Notes", placeholder="Any known Bing-specific issues, URL submission requirements, or Copilot optimization goals...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "bing-property.html")

    # ── AEO/GEO Specialist ────────────────────────────────────────────

    def create_aeo_entity_schema_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🧠 AEO/GEO — Entity & Schema Registration",
            description="Register entities, schema types, and AI citation targets for Answer Engine Optimization.",
            submit_label="Register Entity",
            output_filename="aeo-entity-schema-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("entity_name", "text", required=True, label="Entity Name", placeholder="e.g., Acme Software"),
                FormField("entity_type", "select", required=True, label="Entity Type", options=["Organization", "Brand", "Product", "Person", "Service", "Event", "Place / Location", "CreativeWork (article, book, video)"]),
                FormField("entity_description", "textarea", required=True, label="Entity Description", placeholder="A concise, factual description of the entity (1-2 sentences). This is what AI engines should say about you.", rows=2),
                FormField("official_url", "url", required=True, label="Official Canonical URL", placeholder="https://example.com/about"),
                FormField("same_as_urls", "textarea", label="SameAs URLs (Knowledge Graph)", placeholder="Wikipedia, LinkedIn, Twitter, Crunchbase, etc. One per line.", rows=3, help_text="These corroborate your entity across the web"),
                FormField("schema_types", "checkbox", required=True, label="Schema Types to Deploy", options=["Organization", "Product", "Service", "FAQPage", "HowTo", "Article", "Person", "LocalBusiness", "Event", "BreadcrumbList", "Review / AggregateRating", "Speakable"]),
                FormField("target_ai_engines", "checkbox", label="Target AI Engines", options=["ChatGPT / OpenAI", "Perplexity", "Google SGE / Gemini", "Bing Copilot", "Claude (Anthropic)", "All of the above"], default="All of the above"),
                FormField("target_queries", "textarea", label="Target Queries for AI Citation", placeholder="What questions should cite this entity? e.g., 'best CRM for small business', 'what is Acme Software'...", rows=3),
                FormField("corroboration_sources", "textarea", label="Corroboration Sources Needed", placeholder="Where should we publish corroborating content? e.g., Industry publications, partner blogs, PR sites...", rows=2),
                FormField("citation_tracking", "checkbox", label="Citation Tracking", options=["Track weekly citation rate across all AI engines", "Alert if citation rate drops >20%", "Report monthly citation trends"]),
                FormField("notes", "textarea", label="Notes", placeholder="Any known entity confusion issues, disambiguation needs, or schema implementation constraints...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "aeo-entity-schema.html")

    # ── Reporting Agent ─────────────────────────────────────────────────

    def create_report_config_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📄 Reporting Agent — Report Configuration",
            description="Configure a custom report: scope, metrics, frequency, and delivery method.",
            submit_label="Configure Report",
            output_filename="report-config-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("report_name", "text", required=True, label="Report Name", placeholder="e.g., Monthly Performance Report"),
                FormField("report_type", "select", required=True, label="Report Type", options=["Executive Summary", "Detailed Performance", "Channel Breakdown", "Competitive Analysis", "Content Performance", "Technical SEO Health", "Paid Media Performance", "Social Media Performance", "Custom Report"]),
                FormField("frequency", "select", required=True, label="Frequency", options=["Daily", "Weekly", "Bi-weekly", "Monthly", "Quarterly", "Ad-hoc"], default="Monthly"),
                FormField("data_sources", "checkbox", required=True, label="Data Sources", options=["Google Analytics 4", "Google Search Console", "Bing Webmaster Tools", "Ahrefs", "Semrush", "Google Ads", "Meta Ads", "LinkedIn Ads", "HubSpot", "Social platforms (native)", "Custom data (vault)"]),
                FormField("metrics", "textarea", required=True, label="Key Metrics", placeholder="What numbers should this report include? e.g.,\n- Organic sessions, keyword rankings, CTR\n- Conversion rate, revenue, ROAS\n- Social engagement, follower growth"),
                FormField("comparison", "select", label="Comparison Period", options=["Previous period", "Year-over-year", "Benchmark / Target", "No comparison"], default="Previous period"),
                FormField("format", "select", label="Output Format", options=["Markdown (vault)", "HTML dashboard", "PDF", "Email summary", "Notion page", "Google Slides"], default="Markdown (vault)"),
                FormField("delivery", "select", label="Delivery Method", options=["Save to vault only", "Email to client", "Email to internal team", "Slack notification", "All of the above"], default="Save to vault only"),
                FormField("audience", "select", label="Target Audience", options=["Internal team", "Client (marketing manager)", "Client (executive / C-suite)", "External stakeholder"], default="Client (marketing manager)"),
                FormField("notes", "textarea", label="Notes", placeholder="Any special requirements, custom visualizations, or narrative style preferences...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "report-config.html")

    # ── Revenue Scout ───────────────────────────────────────────────────

    def create_revenue_opportunity_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="💰 Revenue Scout — Opportunity Intake",
            description="Submit a new revenue opportunity for evaluation: expansion, upsell, new channel, or partnership.",
            submit_label="Evaluate Opportunity",
            output_filename="revenue-opportunity-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas or Internal"),
                FormField("opportunity_name", "text", required=True, label="Opportunity Name", placeholder="e.g., Launch paid TikTok ads for Q3"),
                FormField("opportunity_type", "select", required=True, label="Opportunity Type", options=["New client / pitch", "Existing client upsell", "New service line", "New channel / platform", "Partnership / Co-marketing", "Pricing optimization", "Retention / Win-back", "Operational efficiency / Cost reduction"]),
                FormField("estimated_revenue", "number", label="Estimated Monthly Revenue Impact", placeholder="5000", min="0"),
                FormField("estimated_cost", "number", label="Estimated Monthly Cost", placeholder="2000", min="0"),
                FormField("time_to_revenue", "select", label="Time to Revenue", options=["Immediate (<1 month)", "Short-term (1-3 months)", "Medium-term (3-6 months)", "Long-term (6-12 months)"], default="Short-term (1-3 months)"),
                FormField("effort_required", "select", label="Effort Required", options=["Low (existing resources)", "Medium (some new investment)", "High (significant new investment)"], default="Medium (some new investment)"),
                FormField("strategic_fit", "select", label="Strategic Fit", options=["High (core to mission)", "Medium (adjacent opportunity)", "Low (exploratory)"], default="Medium (adjacent opportunity)"),
                FormField("description", "textarea", required=True, label="Description", placeholder="What is the opportunity? Why now? What problem does it solve?", rows=3),
                FormField("data_supporting", "textarea", label="Supporting Data", placeholder="Any metrics, market research, or evidence that supports this opportunity...", rows=2),
                FormField("risks", "textarea", label="Risks & Mitigations", placeholder="What could go wrong? How do we mitigate?", rows=2),
                FormField("next_steps", "text", label="Proposed Next Steps", placeholder="e.g., Run 2-week test, Present to client, Build prototype..."),
                FormField("priority", "select", label="Priority", options=["P0 (Act immediately)", "P1 (High priority)", "P2 (Medium priority)", "P3 (Low priority / backlog)"], default="P2 (Medium priority)"),
                FormField("notes", "textarea", label="Notes", placeholder="Any additional context...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "revenue-opportunity.html")

    # ── Market Signals ──────────────────────────────────────────────────

    def create_market_alert_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📡 Market Signals — Alert Configuration",
            description="Configure algorithm update alerts, SERP volatility monitoring, and trend detection.",
            submit_label="Configure Alerts",
            output_filename="market-alert-response.json",
            fields=[
                FormField("client", "text", label="Client (or 'All' for agency-wide)", placeholder="e.g., acme-saas or All"),
                FormField("alert_type", "checkbox", required=True, label="Alert Types", options=["Google algorithm update (confirmed)", "Google algorithm update (unconfirmed chatter)", "SERP volatility spike", "Competitor ranking surge", "Competitor ranking drop", "New competitor enters market", "Industry trend / news", "AI search engine change (SGE, Copilot, Perplexity)", "Regulatory / compliance change", "Seasonal trend shift"]),
                FormField("monitoring_tools", "checkbox", label="Monitoring Tools", options=["SEMrush Sensor", "SERPwoo", "Rank Ranger", "AccuRanker", "Google Search Status Dashboard", "Twitter / X SEO community", "Reddit r/SEO", "Industry newsletters", "Google Trends"]),
                FormField("alert_threshold", "select", label="SERP Volatility Threshold", options=["Low (notify on any significant movement)", "Medium (notify on >20% position change)", "High (notify only on major updates)"], default="Medium (notify on >20% position change)"),
                FormField("affected_keywords", "textarea", label="Keywords to Monitor Closely", placeholder="Critical keywords that would trigger immediate action if rankings change...", rows=2),
                FormField("notification_method", "select", label="Notification Method", options=["Vault log entry", "Slack alert", "Email alert", "All of the above"], default="All of the above"),
                FormField("response_protocol", "select", label="Response Protocol", options=["Auto-analyze and report", "Alert human + auto-report", "Alert human only (no auto-action)"], default="Alert human + auto-report"),
                FormField("reporting_frequency", "select", label="Trend Report Frequency", options=["Daily", "Weekly", "Monthly"], default="Weekly"),
                FormField("notes", "textarea", label="Notes", placeholder="Any specific sources, communities, or signals to watch...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "market-alert.html")

    # ── Playbook Librarian ────────────────────────────────────────────

    def create_playbook_request_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="📚 Playbook Creation Request",
            description="Request a new SOP, playbook, or process documentation for the agency.",
            submit_label="Request Playbook",
            output_filename="playbook-request-response.json",
            fields=[
                FormField("playbook_name", "text", required=True, label="Playbook Name", placeholder="e.g., Client Offboarding SOP"),
                FormField("playbook_type", "select", required=True, label="Playbook Type", options=["Standard Operating Procedure (SOP)", "Process flow", "Decision tree / Triage rules", "Checklist", "Template", "Reference guide", "Training material", "Policy / Compliance document"]),
                FormField("purpose", "textarea", required=True, label="Purpose", placeholder="What problem does this playbook solve? When should it be used?", rows=3),
                FormField("audience", "select", required=True, label="Target Audience", options=["All agents", "Specific agent (name below)", "Human team members", "Client-facing", "Internal only"], default="All agents"),
                FormField("specific_agent", "text", label="Specific Agent (if applicable)", placeholder="e.g., content-strategist", depends_on="audience", depends_value="Specific agent (name below)"),
                FormField("scope", "textarea", label="Scope / Boundaries", placeholder="What does this playbook cover? What does it NOT cover?", rows=2),
                FormField("inputs", "textarea", label="Required Inputs", placeholder="What data, tools, or context are needed to use this playbook?", rows=2),
                FormField("outputs", "textarea", label="Expected Outputs", placeholder="What does this playbook produce?", rows=2),
                FormField("steps_estimate", "number", label="Estimated Number of Steps", placeholder="10", min="1"),
                FormField("related_playbooks", "text", label="Related Playbooks", placeholder="Names of existing playbooks this relates to or replaces..."),
                FormField("priority", "select", label="Priority", options=["P0 (Urgent — blocking operations)", "P1 (High — needed within 1 week)", "P2 (Medium — needed within 1 month)", "P3 (Low — backlog)"], default="P2 (Medium — needed within 1 month)"),
                FormField("notes", "textarea", label="Notes", placeholder="Any examples, templates, or reference materials...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "playbook-request.html")

    # ── QA Pipeline ─────────────────────────────────────────────────────

    def create_qa_check_request_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="✅ QA Pipeline — Check Request",
            description="Submit a piece of content or an artifact for the 7-check QA pipeline.",
            submit_label="Submit for QA Review",
            output_filename="qa-check-request-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas"),
                FormField("artifact_type", "select", required=True, label="Artifact Type", options=["Blog post / Article", "Landing page copy", "Ad copy", "Email sequence", "Social media post", "Video script", "Technical SEO fix", "Schema markup", "Report / Dashboard", "Other"]),
                FormField("artifact_path", "text", required=True, label="Artifact Path (in vault)", placeholder="e.g., 04-Content-Production/briefs/acme-article.md"),
                FormField("checks_to_run", "checkbox", label="Checks to Run (leave blank for all 7)", options=["Brand Voice (≥4/5)", "Factual Accuracy (≥4/5)", "Legal / Compliance (5/5)", "Formatting (≥4/5)", "SEO Basics (≥4/5)", "Brief Alignment (≥4/5)", "Plagiarism (5/5)"]),
                FormField("deadline", "date", label="Review Deadline"),
                FormField("special_instructions", "textarea", label="Special Instructions", placeholder="Any specific concerns, sensitive topics, or compliance requirements to watch for...", rows=2),
                FormField("notes", "textarea", label="Notes", placeholder="Any context about the artifact or the client...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "qa-check-request.html")

    # ── Agent Prompt Engineer ─────────────────────────────────────────

    def create_agent_config_form(self, output_dir: Path = None) -> Path:
        form = FormDefinition(
            title="🤖 Agent Config — New Agent or Update",
            description="Create or update an agent configuration with the 5-layer template.",
            submit_label="Save Agent Config",
            output_filename="agent-config-response.json",
            fields=[
                FormField("agent_name", "text", required=True, label="Agent Name (kebab-case)", placeholder="e.g., new-specialist-agent"),
                FormField("action", "select", required=True, label="Action", options=["Create new agent", "Update existing agent"]),
                FormField("role_definition", "textarea", required=True, label="1. Role Definition", placeholder="What is this agent's role? What does it do? What does it NOT do?", rows=3),
                FormField("rag_context", "textarea", required=True, label="2. RAG Context Block", placeholder="What vault files does this agent read? What context does it need?", rows=3),
                FormField("toolset", "textarea", required=True, label="3. Toolset Declaration", placeholder="What tools, APIs, and integrations does this agent use?", rows=3),
                FormField("output_format", "textarea", required=True, label="4. Output Format Spec", placeholder="What does this agent produce? File format, structure, frontmatter requirements...", rows=3),
                FormField("escalation_rules", "textarea", required=True, label="5. Escalation Rules", placeholder="When does this agent escalate? To whom? What are the retry rules?", rows=3),
                FormField("related_agents", "text", label="Related Agents", placeholder="e.g., atlas-orchestrator, content-strategist, qa-pipeline"),
                FormField("cost_budget", "number", label="Daily Cost Budget (USD)", placeholder="5", default="5", min="0"),
                FormField("timeout_seconds", "number", label="Default Timeout (seconds)", placeholder="1800", default="1800", min="300"),
                FormField("notes", "textarea", label="Notes", placeholder="Any additional configuration, personality traits, or special instructions...", rows=2),
            ],
        )
        out_dir = output_dir or self.engine.forms_dir
        return self.engine.create_form(form, out_dir / "agent-config.html")

    # ── Generate All ──────────────────────────────────────────────────

    def generate_all(self, output_dir: Path = None) -> list:
        """Generate all preset forms. Returns list of paths."""
        paths = []
        methods = [
            self.create_competitor_intake_form,
            self.create_ad_campaign_form,
            self.create_social_calendar_form,
            self.create_local_seo_form,
            self.create_pseo_form,
            self.create_outreach_prospect_form,
            self.create_on_page_request_form,
            self.create_tech_audit_form,
            self.create_analytics_report_form,
            self.create_copy_request_form,
            self.create_cro_experiment_form,
            self.create_email_sequence_form,
            self.create_influencer_campaign_form,
            self.create_video_image_brief_form,
            self.create_pitch_proposal_form,
            self.create_forecasting_request_form,
            self.create_reputation_monitoring_form,
            self.create_gsc_property_form,
            self.create_bing_property_form,
            self.create_aeo_entity_schema_form,
            self.create_report_config_form,
            self.create_revenue_opportunity_form,
            self.create_market_alert_form,
            self.create_playbook_request_form,
            self.create_qa_check_request_form,
            self.create_agent_config_form,
        ]
        for method in methods:
            try:
                paths.append(method(output_dir))
            except Exception as e:
                logger.warning(f"Failed to generate form {method.__name__}: {e}")
        return paths


if __name__ == "__main__":
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="Generate all form presets")
    parser.add_argument("--output-dir", "-o", default="forms", help="Output directory")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    engine = FormEngine(forms_dir=Path(args.output_dir))
    presets = FormPresets(engine)
    paths = presets.generate_all()

    print(f"\nGenerated {len(paths)} forms:")
    for p in sorted(paths):
        print(f"  {p}")
    print(f"\nFill the forms in your browser, then save the response JSON.")
