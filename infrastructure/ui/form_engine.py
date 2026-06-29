"""
AgenticMarketingPro — Interactive Form Engine
===============================================
Generates self-contained HTML forms for collecting user input.
Forms are schema-driven, support conditional fields, validation,
and auto-save to localStorage + JSON export for agent consumption.

Usage:
    from ui.form_engine import FormEngine, FormField

    engine = FormEngine()
    form = engine.create_form(
        title="Onboard New Client",
        description="Fill in client details to create their vault folder.",
        fields=[
            FormField("client_name", "text", required=True, label="Client Name"),
            FormField("website", "url", required=True, label="Website URL"),
            FormField("tier", "select", options=["Starter","Growth","Scale","Enterprise"]),
        ],
        output_path="forms/client-onboarding.html",
    )
    # User fills form, saves response to forms/client-onboarding-response.json
    response = engine.read_response("forms/client-onboarding-response.json")
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("amp.form_engine")


@dataclass
class FormField:
    """A single form field definition."""
    name: str                    # JSON key / field ID
    field_type: str             # text, email, url, password, number, select, textarea, checkbox, radio, date
    label: str = ""
    placeholder: str = ""
    required: bool = False
    options: List[str] = field(default_factory=list)  # For select, radio, checkbox
    default: Any = None
    help_text: str = ""          # Small helper text below field
    validation: str = ""         # Regex pattern for validation
    depends_on: Optional[str] = None  # Show only if another field has value
    depends_value: Optional[str] = None  # Specific value to match
    min: Optional[float] = None  # For number
    max: Optional[float] = None  # For number
    rows: int = 4                # For textarea


@dataclass
class FormDefinition:
    """Complete form definition."""
    title: str
    description: str = ""
    fields: List[FormField] = field(default_factory=list)
    submit_label: str = "Submit & Save"
    success_message: str = "Form saved successfully! Response written to:"
    output_filename: str = "response.json"


class FormEngine:
    """Schema-driven HTML form generator for agent-user interaction."""

    CSS_THEME = """
    :root { --bg: #0f0f1a; --card: #1a1a2e; --border: #2a2a40; --text: #e0e0e0; --muted: #888; --accent: #4A90D9; --accent-hover: #357ABD; --danger: #E74C3C; --success: #50C878; --warning: #F39C12; }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
    .container { max-width: 720px; margin: 0 auto; padding: 40px 24px; }
    .header { border-bottom: 1px solid var(--border); padding-bottom: 20px; margin-bottom: 32px; }
    .header h1 { margin: 0 0 8px 0; font-size: 24px; font-weight: 600; }
    .header p { margin: 0; color: var(--muted); font-size: 15px; }
    .field { margin-bottom: 24px; }
    .field.hidden { display: none; }
    label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px; color: var(--text); }
    .required { color: var(--danger); }
    .help { font-size: 12px; color: var(--muted); margin-top: 4px; }
    input, select, textarea { width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: 8px; background: var(--card); color: var(--text); font-size: 14px; transition: border-color 0.2s; }
    input:focus, select:focus, textarea:focus { outline: none; border-color: var(--accent); }
    input:invalid, select:invalid, textarea:invalid { border-color: var(--danger); }
    select { cursor: pointer; }
    textarea { resize: vertical; min-height: 80px; }
    .checkbox-group, .radio-group { display: flex; flex-direction: column; gap: 8px; }
    .checkbox-item, .radio-item { display: flex; align-items: center; gap: 8px; }
    .checkbox-item input, .radio-item input { width: auto; }
    .actions { display: flex; gap: 12px; margin-top: 32px; padding-top: 24px; border-top: 1px solid var(--border); }
    button { padding: 12px 24px; border: none; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: background 0.2s; }
    .btn-primary { background: var(--accent); color: white; }
    .btn-primary:hover { background: var(--accent-hover); }
    .btn-secondary { background: var(--card); color: var(--text); border: 1px solid var(--border); }
    .btn-secondary:hover { background: var(--border); }
    .status { padding: 12px 16px; border-radius: 8px; font-size: 13px; margin-top: 16px; display: none; }
    .status.success { background: rgba(80,200,120,0.1); border: 1px solid var(--success); color: var(--success); display: block; }
    .status.error { background: rgba(231,76,60,0.1); border: 1px solid var(--danger); color: var(--danger); display: block; }
    .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border); font-size: 12px; color: var(--muted); }
    .agent-id { font-family: monospace; background: var(--card); padding: 2px 6px; border-radius: 4px; }
    """

    def __init__(self, forms_dir: Path = None):
        self.forms_dir = forms_dir or Path("forms")
        self.forms_dir.mkdir(parents=True, exist_ok=True)

    def _render_field(self, field: FormField, index: int) -> str:
        """Render a single form field as HTML."""
        label_text = f"{field.label}{' <span class=\"required\">*</span>' if field.required else ''}"
        help_html = f'<div class="help">{field.help_text}</div>' if field.help_text else ""
        attrs = f'name="{field.name}" id="{field.name}"'
        if field.required:
            attrs += ' required'
        if field.placeholder:
            attrs += f' placeholder="{field.placeholder}"'
        if field.validation:
            attrs += f' pattern="{field.validation}"'
        if field.min is not None:
            attrs += f' min="{field.min}"'
        if field.max is not None:
            attrs += f' max="{field.max}"'

        # Conditional display
        conditional_attr = ""
        if field.depends_on:
            conditional_attr = f' data-depends-on="{field.depends_on}" data-depends-value="{field.depends_value or ""}"'

        html = f'<div class="field"{conditional_attr} id="field-{field.name}">\n'
        html += f'  <label for="{field.name}">{label_text}</label>\n'

        if field.field_type == "textarea":
            html += f'  <textarea {attrs} rows="{field.rows}">{field.default or ""}</textarea>\n'
        elif field.field_type == "select":
            html += f'  <select {attrs}>\n'
            if not field.default:
                html += '    <option value="">-- Select --</option>\n'
            for opt in field.options:
                selected = ' selected' if opt == field.default else ''
                html += f'    <option value="{opt}"{selected}>{opt}</option>\n'
            html += '  </select>\n'
        elif field.field_type == "checkbox":
            html += '  <div class="checkbox-group">\n'
            for opt in field.options:
                checked = ' checked' if opt == field.default else ''
                html += f'    <label class="checkbox-item"><input type="checkbox" name="{field.name}" value="{opt}"{checked}> {opt}</label>\n'
            html += '  </div>\n'
        elif field.field_type == "radio":
            html += '  <div class="radio-group">\n'
            for opt in field.options:
                checked = ' checked' if opt == field.default else ''
                html += f'    <label class="radio-item"><input type="radio" name="{field.name}" value="{opt}"{checked}{" required" if field.required else ""}> {opt}</label>\n'
            html += '  </div>\n'
        else:
            input_type = field.field_type
            html += f'  <input type="{input_type}" {attrs} value="{field.default or ""}">\n'

        html += help_html
        html += '</div>\n'
        return html

    def create_form(self, form_def: FormDefinition, output_path: Path = None) -> Path:
        """Generate a self-contained HTML form file."""
        fields_html = ""
        for i, field in enumerate(form_def.fields):
            fields_html += self._render_field(field, i)

        fields_json = json.dumps([{
            "name": f.name,
            "type": f.field_type,
            "required": f.required,
            "depends_on": f.depends_on,
            "depends_value": f.depends_value,
        } for f in form_def.fields])

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{form_def.title}</title>
    <style>{self.CSS_THEME}</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{form_def.title}</h1>
            <p>{form_def.description}</p>
        </div>
        <form id="agent-form">
            {fields_html}
            <div class="actions">
                <button type="submit" class="btn-primary">{form_def.submit_label}</button>
                <button type="button" class="btn-secondary" onclick="clearForm()">Clear</button>
            </div>
        </form>
        <div id="status" class="status"></div>
        <div class="footer">
            <p>Form ID: <span class="agent-id">{Path(output_path).stem if output_path else "form"}</span></p>
            <p>Generated by AgenticMarketingPro Form Engine</p>
        </div>
    </div>
    <script>
        const fields = {fields_json};
        const form = document.getElementById('agent-form');
        const status = document.getElementById('status');

        // Load from localStorage
        function loadForm() {{
            const saved = localStorage.getItem('form_' + form.id);
            if (saved) {{
                try {{
                    const data = JSON.parse(saved);
                    Object.keys(data).forEach(key => {{
                        const el = form.querySelector(`[name="${{key}}"]`);
                        if (el) {{
                            if (el.type === 'checkbox') {{
                                el.checked = data[key];
                            }} else {{
                                el.value = data[key];
                            }}
                        }}
                    }});
                    updateConditionalFields();
                }} catch (e) {{}}
            }}
        }}

        // Save to localStorage on change
        form.addEventListener('input', function() {{
            const data = {{}};
            fields.forEach(f => {{
                const el = form.querySelector(`[name="${{f.name}}"]`);
                if (el) {{
                    data[f.name] = el.type === 'checkbox' ? el.checked : el.value;
                }}
            }});
            localStorage.setItem('form_' + form.id, JSON.stringify(data));
        }});

        // Conditional fields
        function updateConditionalFields() {{
            fields.forEach(f => {{
                if (f.depends_on) {{
                    const parent = form.querySelector(`[name="${{f.depends_on}}"]`);
                    const fieldDiv = document.getElementById('field-' + f.name);
                    if (parent && fieldDiv) {{
                        const parentValue = parent.type === 'checkbox' ? parent.checked : parent.value;
                        const shouldShow = !f.depends_value || parentValue === f.depends_value;
                        fieldDiv.classList.toggle('hidden', !shouldShow);
                    }}
                }}
            }});
        }}

        form.addEventListener('change', updateConditionalFields);

        // Submit handler
        form.addEventListener('submit', function(e) {{
            e.preventDefault();
            const formData = new FormData(form);
            const result = {{}};
            fields.forEach(f => {{
                if (f.type === 'checkbox' && f.options.length > 1) {{
                    result[f.name] = formData.getAll(f.name);
                }} else if (f.type === 'checkbox') {{
                    result[f.name] = form.querySelector(`[name="${{f.name}}"]`).checked;
                }} else {{
                    result[f.name] = formData.get(f.name);
                }}
            }});

            // Add metadata
            result._meta = {{
                form_title: "{form_def.title}",
                submitted_at: new Date().toISOString(),
                form_id: "{Path(output_path).stem if output_path else 'form'}"
            }};

            const blob = new Blob([JSON.stringify(result, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '{form_def.output_filename}';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            status.textContent = "{form_def.success_message} " + a.download;
            status.className = "status success";
        }});

        function clearForm() {{
            form.reset();
            localStorage.removeItem('form_' + form.id);
            updateConditionalFields();
            status.className = "status";
        }}

        // Initialize
        loadForm();
        updateConditionalFields();
    </script>
</body>
</html>'''

        if output_path is None:
            safe_title = "".join(c if c.isalnum() else "_" for c in form_def.title).lower()
            output_path = self.forms_dir / f"{safe_title}.html"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        logger.info(f"Form generated: {output_path}")
        return output_path

    def read_response(self, response_path: Path) -> Dict[str, Any]:
        """Read a JSON form response file."""
        path = Path(response_path)
        if not path.exists():
            logger.warning(f"Response file not found: {path}")
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            logger.info(f"Response read: {path} ({len(data)} fields)")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {e}")
            return {}

    def create_client_onboarding_form(self, output_dir: Path = None) -> Path:
        """Pre-built form for onboarding a new client."""
        form = FormDefinition(
            title="🎯 Onboard New Client",
            description="Fill in the details below. This will create the client vault folder, website manifest, and initial strategy documents.",
            submit_label="Create Client Project",
            output_filename="client-onboarding-response.json",
            fields=[
                FormField("client_name", "text", required=True, label="Client Name", placeholder="e.g., Acme SaaS", help_text="This becomes the folder name in the vault"),
                FormField("website", "url", required=True, label="Primary Website", placeholder="https://example.com"),
                FormField("industry", "text", required=True, label="Industry / Vertical", placeholder="e.g., B2B SaaS, Fintech, E-commerce"),
                FormField("tier", "select", required=True, label="Service Tier", options=["Starter ($2,500/mo)", "Growth ($4,500/mo)", "Scale ($8,500/mo)", "Enterprise ($15,000+/mo)"], help_text="Determines velocity targets and agent allocation"),
                FormField("target_geo", "text", label="Target Geography", placeholder="e.g., US, Canada, UK", default="US"),
                FormField("primary_language", "select", label="Primary Language", options=["en", "es", "de", "fr", "ja", "zh"], default="en"),
                FormField("business_goal_1", "textarea", required=True, label="Primary Business Goal", placeholder="e.g., Increase organic SQLs from 12 to 50/month by Q3", rows=3),
                FormField("business_goal_2", "textarea", label="Secondary Goal", placeholder="e.g., Achieve AI citation in Perplexity for 5 keywords", rows=2),
                FormField("competitor_1", "url", label="Top Competitor #1", placeholder="https://competitor1.com"),
                FormField("competitor_2", "url", label="Top Competitor #2", placeholder="https://competitor2.com"),
                FormField("competitor_3", "url", label="Top Competitor #3", placeholder="https://competitor3.com"),
                FormField("cms", "select", required=True, label="CMS / Platform", options=["WordPress", "Webflow", "HubSpot", "Shopify", "Framer", "Custom / Other"], help_text="Determines on-page optimization strategy and schema approach"),
                FormField("cms_custom", "text", label="Custom CMS Name", placeholder="e.g., Next.js + Sanity", depends_on="cms", depends_value="Custom / Other"),
                FormField("has_wordpress_api", "checkbox", label="Enable WordPress Integration", options=["Connect to WordPress REST API for auto-publishing"], help_text="Check this if you want agents to publish content directly to WordPress"),
                FormField("wp_url", "url", label="WordPress Site URL", placeholder="https://example.com/wp-json", depends_on="has_wordpress_api", depends_value="Connect to WordPress REST API for auto-publishing"),
                FormField("wp_username", "text", label="WordPress Username", placeholder="admin", depends_on="has_wordpress_api", depends_value="Connect to WordPress REST API for auto-publishing"),
                FormField("wp_password", "password", label="WordPress Application Password", placeholder="xxxx xxxx xxxx xxxx xxxx xxxx", depends_on="has_wordpress_api", depends_value="Connect to WordPress REST API for auto-publishing", help_text="Generate at: WP Admin → Users → Profile → Application Passwords"),
                FormField("has_gsc", "checkbox", label="Google Search Console", options=["I have access"], help_text="Required for SEO monitoring and CTR opportunity detection"),
                FormField("gsc_property", "url", label="GSC Property URL", placeholder="https://example.com/", depends_on="has_gsc", depends_value="I have access"),
                FormField("has_ga4", "checkbox", label="Google Analytics 4", options=["I have access"]),
                FormField("ga4_property", "text", label="GA4 Property ID", placeholder="properties/123456789", depends_on="has_ga4", depends_value="I have access"),
                FormField("has_ahrefs", "checkbox", label="Ahrefs API", options=["I have an API key"]),
                FormField("has_semrush", "checkbox", label="Semrush API", options=["I have an API key"]),
                FormField("contact_name", "text", required=True, label="Primary Contact Name", placeholder="Jane Smith"),
                FormField("contact_email", "email", required=True, label="Primary Contact Email", placeholder="jane@example.com"),
                FormField("contact_slack", "text", label="Slack Handle", placeholder="@jane"),
                FormField("notes", "textarea", label="Additional Notes / Special Requirements", placeholder="Any unique constraints, brand guidelines, or context...", rows=4),
            ],
        )
        out_dir = output_dir or self.forms_dir
        return self.create_form(form, out_dir / "client-onboarding.html")

    def create_api_credentials_form(self, output_dir: Path = None) -> Path:
        """Pre-built form for collecting API credentials."""
        form = FormDefinition(
            title="🔐 API Credentials & Integrations",
            description="Provide API keys for the tools you want agents to use. Leave blank if you don't have access yet — agents will work with what's available.",
            submit_label="Save Credentials",
            output_filename="api-credentials-response.json",
            fields=[
                FormField("openai_api_key", "password", label="OpenAI API Key", placeholder="sk-...", help_text="Required for embeddings and LLM fallback. Get from platform.openai.com"),
                FormField("kimi_api_key", "password", label="Kimi API Key", placeholder="Optional — for Kimi Moonshot fallback"),
                FormField("minimax_api_key", "password", label="Minimax API Key", placeholder="Optional — for Minimax fallback"),
                FormField("ahrefs_api_key", "password", label="Ahrefs API Key", placeholder="Get from ahrefs.com/api"),
                FormField("semrush_api_key", "password", label="Semrush API Key", placeholder="Get from semrush.com/api"),
                FormField("serpapi_key", "password", label="SERPAPI Key", placeholder="For SERP scraping fallback"),
                FormField("dataforseo_login", "text", label="DataForSEO Login", placeholder="Email or API login"),
                FormField("dataforseo_password", "password", label="DataForSEO Password", placeholder="API password"),
                FormField("gsc_client_secrets", "text", label="Google Client Secrets File", placeholder="path/to/client_secrets.json", help_text="Download from Google Cloud Console → OAuth2 credentials"),
                FormField("ga4_property_id", "text", label="GA4 Property ID", placeholder="properties/123456789"),
                FormField("bing_api_key", "password", label="Bing Webmaster API Key", placeholder="From bing.com/webmaster"),
                FormField("google_ads_dev_token", "password", label="Google Ads Developer Token", placeholder="Required for Google Ads API"),
                FormField("google_ads_refresh_token", "password", label="Google Ads Refresh Token", placeholder="From OAuth flow"),
                FormField("meta_access_token", "password", label="Meta (Facebook) Access Token", placeholder="From business.facebook.com"),
                FormField("linkedin_ads_token", "password", label="LinkedIn Ads Token", placeholder="From linkedin.com/developers"),
                FormField("hubspot_api_key", "password", label="HubSpot API Key", placeholder="From app.hubspot.com → Settings → API"),
                FormField("slack_webhook_url", "url", label="Slack Webhook URL", placeholder="https://hooks.slack.com/...", help_text="For notifications and HITL gate alerts"),
                FormField("buffer_token", "password", label="Buffer Access Token", placeholder="For social media scheduling"),
                FormField("cloudflare_token", "password", label="Cloudflare API Token", placeholder="For site monitoring and cache purging"),
                FormField("cloudflare_zone_id", "text", label="Cloudflare Zone ID", placeholder="From Cloudflare dashboard"),
                FormField("pagespeed_key", "password", label="PageSpeed Insights API Key", placeholder="From Google Cloud Console"),
                FormField("perplexity_key", "password", label="Perplexity API Key", placeholder="For AI citation research"),
                FormField("elevenlabs_key", "password", label="ElevenLabs API Key", placeholder="For AI voice generation"),
            ],
        )
        out_dir = output_dir or self.forms_dir
        return self.create_form(form, out_dir / "api-credentials.html")

    def create_wordpress_config_form(self, output_dir: Path = None) -> Path:
        """Pre-built form for WordPress integration setup."""
        form = FormDefinition(
            title="🌐 WordPress Integration Setup",
            description="Configure WordPress REST API access for auto-publishing content from the vault.",
            submit_label="Test & Save Connection",
            output_filename="wordpress-config-response.json",
            fields=[
                FormField("wp_site_url", "url", required=True, label="WordPress Site URL", placeholder="https://example.com", help_text="Base URL — /wp-json/ will be appended automatically"),
                FormField("wp_username", "text", required=True, label="WordPress Username", placeholder="admin or service account"),
                FormField("wp_app_password", "password", required=True, label="Application Password", placeholder="xxxx xxxx xxxx xxxx xxxx xxxx", help_text="NOT your login password. Generate at: WP Admin → Users → Profile → Application Passwords → Add New"),
                FormField("wp_post_type", "select", label="Default Post Type", options=["post", "page", "custom"], default="post"),
                FormField("wp_post_type_custom", "text", label="Custom Post Type Slug", placeholder="e.g., case_study", depends_on="wp_post_type", depends_value="custom"),
                FormField("wp_author_id", "number", label="Default Author ID", placeholder="1", default="1", help_text="WordPress user ID to publish as"),
                FormField("wp_category_ids", "text", label="Default Category IDs", placeholder="1, 3, 5", help_text="Comma-separated category IDs to assign"),
                FormField("wp_tag_template", "text", label="Tag Template", placeholder="{{client}}-{{topic}}", help_text="How auto-generated tags are named. Use {{client}} and {{topic}} placeholders."),
                FormField("wp_featured_image", "select", label="Featured Image Strategy", options=["None", "Upload from URL", "Generate AI image", "Use first image in content"], default="None"),
                FormField("wp_seo_plugin", "select", label="SEO Plugin", options=["None", "Yoast SEO", "Rank Math", "All in One SEO"], default="Rank Math", help_text="Determines how meta title/description are sent"),
                FormField("wp_test_publish", "checkbox", label="Test Connection", options=["Publish a test draft post after saving"]),
                FormField("wp_notes", "textarea", label="Notes / Special Requirements", placeholder="Custom fields, taxonomies, or publishing constraints...", rows=3),
            ],
        )
        out_dir = output_dir or self.forms_dir
        return self.create_form(form, out_dir / "wordpress-config.html")

    def create_content_brief_form(self, output_dir: Path = None, client: str = "") -> Path:
        """Pre-built form for generating a content brief."""
        form = FormDefinition(
            title="📝 Content Brief Generator",
            description="Fill in the details for the content piece. The content strategist agent will use this to generate a full brief.",
            submit_label="Generate Brief",
            output_filename="content-brief-response.json",
            fields=[
                FormField("client", "text", required=True, label="Client", placeholder="e.g., acme-saas", default=client),
                FormField("title", "text", required=True, label="Working Title", placeholder="e.g., The Complete Guide to AI-Powered SEO"),
                FormField("target_keyword", "text", required=True, label="Primary Target Keyword", placeholder="e.g., ai seo tools"),
                FormField("secondary_keywords", "text", label="Secondary Keywords", placeholder="Comma-separated"),
                FormField("content_type", "select", required=True, label="Content Type", options=["Pillar Guide (2,000–5,000 words)", "Listicle", "Comparison Post", "Case Study", "How-To Tutorial", "Thought Leadership", "Product Page", "Landing Page"]),
                FormField("writer_persona", "select", required=True, label="Writer Persona", options=["Analyst (data-heavy)", "Educator (step-by-step)", "Provocateur (contrarian)", "Storyteller (narrative)", "Operator (practical / tactical)"]),
                FormField("target_audience", "textarea", required=True, label="Target Audience", placeholder="Who is this for? What do they already know? What keeps them up at night?", rows=3),
                FormField("pain_point", "textarea", required=True, label="Pain Point This Solves", placeholder="What specific problem does this content address?", rows=2),
                FormField("desired_outcome", "textarea", required=True, label="Desired Reader Outcome", placeholder="What should the reader be able to do after reading?", rows=2),
                FormField("competing_urls", "textarea", label="Top 3 Competing URLs", placeholder="Paste URLs of current top-ranking pages for this keyword", rows=3),
                FormField("unique_angle", "textarea", label="Unique Angle / Differentiator", placeholder="What will make this better than what's already ranking?", rows=2),
                FormField("cta", "text", label="Primary CTA", placeholder="e.g., Book a demo, Download the template, Subscribe to newsletter"),
                FormField("word_count_target", "number", label="Target Word Count", placeholder="2500", default="2500", min="800", max="8000"),
                FormField("due_date", "date", label="Target Due Date"),
                FormField("priority", "select", label="Priority", options=["P0 (Launch blocker)", "P1 (High — this week)", "P2 (Medium — next 2 weeks)", "P3 (Low — backlog)"], default="P1 (High — this week)"),
                FormField("special_requirements", "textarea", label="Special Requirements", placeholder="Brand voice notes, mandatory mentions, legal disclaimers, etc.", rows=3),
            ],
        )
        out_dir = output_dir or self.forms_dir
        return self.create_form(form, out_dir / "content-brief.html")


def main():
    """CLI: generate all pre-built forms."""
    import argparse
    parser = argparse.ArgumentParser(description="Generate interactive HTML forms")
    parser.add_argument("--all", action="store_true", help="Generate all pre-built forms")
    parser.add_argument("--client-onboarding", action="store_true", help="Client onboarding form")
    parser.add_argument("--api-credentials", action="store_true", help="API credentials form")
    parser.add_argument("--wordpress", action="store_true", help="WordPress config form")
    parser.add_argument("--content-brief", action="store_true", help="Content brief form")
    parser.add_argument("--output-dir", "-o", default="forms", help="Output directory")
    args = parser.parse_args()

    engine = FormEngine(forms_dir=Path(args.output_dir))
    paths = []

    if args.all or args.client_onboarding:
        paths.append(engine.create_client_onboarding_form())
    if args.all or args.api_credentials:
        paths.append(engine.create_api_credentials_form())
    if args.all or args.wordpress:
        paths.append(engine.create_wordpress_config_form())
    if args.all or args.content_brief:

        # Generate all preset forms (competitor, ad, social, local, etc.)
        from ui.form_presets import FormPresets
        presets = FormPresets(engine)
        preset_paths = presets.generate_all()
        paths.extend(preset_paths)

        paths.append(engine.create_client_onboarding_form())
        paths.append(engine.create_api_credentials_form())
        paths.append(engine.create_wordpress_config_form())
        paths.append(engine.create_content_brief_form())

    print("\nGenerated forms:")
    for p in paths:
        print(f"  {p}")
    print(f"\nFill the forms in your browser, then save the response JSON.")
    print(f"Agent will read from: {Path(args.output_dir)}/*-response.json")


if __name__ == "__main__":
    main()
