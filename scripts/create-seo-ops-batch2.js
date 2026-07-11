/**
 * Create remaining SEO Ops deliverables
 */
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function supabaseRequest(table, method, body, query = '') {
  const url = `https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/${table}${query}`;
  const options = {
    method,
    headers: {
      'apikey': SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
    },
  };
  if (method === 'POST') {
    options.headers['Prefer'] = 'return=representation';
    options.body = JSON.stringify(body);
  } else if (method === 'PATCH') {
    options.headers['Prefer'] = 'return=minimal';
    options.body = JSON.stringify(body);
  }
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  if (res.status === 204) return { data: null, error: null };
  const data = await res.json();
  return { data, error: null };
}

const jobs = [
  // MASTERPLAN SECTION 1: Positioning & ICP (was failed)
  {
    type: 'skill_execution',
    skill_slug: 'content-strategist',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: 'ICP Definition Document',
      topic: 'AgenticMarketingPro Ideal Customer Profiles',
      prompt_override: `Create a comprehensive ICP document for AgenticMarketingPro (AI Automation Agency / B2B Services).

For EACH ICP, include:
- Firmographics (company size, revenue, team size)
- Psychographics (pain points, goals, fears)
- Buying triggers (when they decide to buy)
- Objections they raise
- Where they hang out online
- Content preferences
- Decision-making process

Format as a professional markdown document with tables and clear sections.`,
    },
  },

  // MASTERPLAN SECTION 2: SEO Strategy
  {
    type: 'skill_execution',
    skill_slug: 'keyword-researcher',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: 'Keyword Research & Topic Cluster Map',
      seed_keywords: ['AI marketing automation', 'marketing OS', 'AI agents for marketing', 'workflow automation agency', 'programmatic SEO'],
      prompt_override: `Create a comprehensive keyword research document for AgenticMarketingPro.

Include:
1. Primary keywords (high intent, commercial) - 20 keywords
2. Secondary keywords (informational, TOFU) - 30 keywords
3. Long-tail opportunities - 50 keywords
4. Topic clusters with pillar pages and supporting content
5. Keyword difficulty analysis
6. Search intent mapping
7. Priority scoring (Traffic Potential × Conversion Intent / Difficulty)

Format as markdown with tables.`,
    },
  },

  // MASTERPLAN SECTION 3: AEO/GEO
  {
    type: 'skill_execution',
    skill_slug: 'aeo-geo-strategist',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: 'AEO/GEO Strategy Document',
      topic: 'AI Search Optimization for AgenticMarketingPro',
      prompt_override: `Create a comprehensive AEO/GEO strategy document for AgenticMarketingPro.

Include:
1. Entity schema recommendations (Person, Organization, Service, FAQPage, HowTo)
2. Structured data markup plan with JSON-LD examples
3. Content optimization for AI citations
4. Knowledge graph presence strategy
5. Brand mention monitoring plan
6. Citation building strategy
7. "People Also Ask" optimization
8. Featured snippet targeting
9. AI platform-specific tactics (ChatGPT, Perplexity, Gemini)

Format as actionable markdown with code examples.`,
    },
  },

  // MASTERPLAN SECTION 4: Backlinks
  {
    type: 'skill_execution',
    skill_slug: 'link-building-outreach',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: 'Backlink Acquisition Strategy',
      current_domain_authority: 'New domain (DA ~1-5)',
      target_da: '30+ within 12 months',
      budget: '$2,000/month',
      prompt_override: `Create a comprehensive backlink strategy for AgenticMarketingPro.

Include:
1. Linkable asset ideas (tools, calculators, research, guides)
2. Guest posting targets (50 sites with DA 20-50)
3. Digital PR campaign ideas
4. Resource page link building
5. Broken link building opportunities
6. Competitor backlink gap analysis
7. HARO / journalist outreach plan
8. Directory and listing opportunities
9. Partnership and integration links
10. Monthly link building calendar

Format as markdown with tables and actionable templates.`,
    },
  },

  // MASTERPLAN SECTION 5: Content Plan
  {
    type: 'skill_execution',
    skill_slug: 'content-brief-writer',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: '90-Day Content Calendar',
      content_pillars: ['AI Marketing Education', 'Agentic Workflows', 'Case Studies', 'Industry Trends'],
      frequency: '3 posts/week',
      prompt_override: `Create a 90-day content calendar for AgenticMarketingPro focused on AI visibility and thought leadership.

Include:
1. Content pillars and themes
2. Weekly content schedule (3 posts/week)
3. Content types: blog posts, case studies, whitepapers, videos, infographics
4. Target keywords for each piece
5. Distribution channels
6. Content upgrade ideas (lead magnets)
7. Repurposing strategy
8. AI-specific content angles

Format as markdown with a calendar table.`,
    },
  },

  // MASTERPLAN SECTION 6: pSEO
  {
    type: 'skill_execution',
    skill_slug: 'pseo-pipeline',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: 'Programmatic SEO Content Plan',
      niche: 'AI marketing automation for specific industries',
      target_industries: ['Dental', 'Real Estate', 'E-commerce DTC', 'SaaS', 'Legal'],
      prompt_override: `Create a programmatic SEO (pSEO) content plan for AgenticMarketingPro.

Include:
1. pSEO opportunity analysis
2. Data sources for programmatic content
3. Template designs for industry-specific landing pages
4. URL structure and taxonomy
5. Content generation workflow
6. Internal linking strategy
7. Page template specifications
8. Quality control process
9. Expected traffic and conversion estimates

Format as markdown with technical specifications.`,
    },
  },

  // SEO OPS: Content Refresh SOP
  {
    type: 'skill_execution',
    skill_slug: 'content-strategist',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: 'Content Refresh SOP',
      topic: 'Systematic Content Decay Prevention',
      prompt_override: `Create a Content Refresh Standard Operating Procedure (SOP) for AgenticMarketingPro.

Include:
1. Content audit process (quarterly)
2. Decay detection signals and metrics
3. Refresh priority matrix
4. Step-by-step refresh workflow
5. Content update checklist
6. Before/after measurement framework
7. Tools and resources needed
8. Roles and responsibilities
9. Reporting template

Format as a professional SOP document with checklists and templates.`,
    },
  },

  // SEO OPS: GSC Weekly Audit
  {
    type: 'skill_execution',
    skill_slug: 'technical-seo-auditor',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      deliverable: 'GSC Weekly Audit Checklist',
      tool: 'Google Search Console',
      frequency: 'Weekly',
      prompt_override: `Create a comprehensive Google Search Console weekly audit checklist for AgenticMarketingPro.

Include:
1. Performance tab checks (clicks, impressions, CTR, position)
2. Query analysis (new queries, lost queries, position changes)
3. Page-level analysis (top pages, declining pages)
4. Index coverage checks (errors, warnings, valid)
5. Core Web Vitals review
6. Mobile usability checks
7. Structured data validation
8. Security issues scan
9. Manual actions check
10. Comparison with previous week
11. Action items template

Format as a checklist with specific metrics to check and thresholds for flagging issues.`,
    },
  },
];

async function createJobs() {
  const created = [];
  for (const job of jobs) {
    try {
      const result = await supabaseRequest('jobs', 'POST', job);
      created.push(result.data[0]);
      console.log(`✅ Created: ${job.payload.deliverable} (${result.data[0].id})`);
    } catch (err) {
      console.error(`❌ Failed: ${job.payload.deliverable} - ${err.message}`);
    }
  }
  console.log(`\n📊 Created ${created.length}/${jobs.length} jobs`);
}

createJobs().catch(console.error);
