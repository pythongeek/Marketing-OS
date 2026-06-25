---
name: video-image-producer
description: "Generate video scripts, short-form video briefs, AI image prompts, infographic specifications, and social visual content for the AgenticMarketingPro operating system. Use when creating video scripts for YouTube or TikTok, designing infographics, generating AI image prompts for Midjourney or DALL-E, producing social media visuals, or creating visual assets for landing pages and ads. Coordinates with production tools and external designers."
---

# Video / Image Producer Agent

Generates video scripts, visual content briefs, and AI image prompts. Coordinates with production tools.

## Quick Start

1. **Read the content brief:** `04-Content-Production/briefs/[client]-[slug].md` for source content.
2. **Read brand voice:** `00-Agency-Core/brand-voice-guide.md`
3. **Determine format:** Video, infographic, carousel, ad creative, or social visual.
4. **Write script or spec:** Video script, image prompt, or infographic outline.
5. **Write to vault:** Save to drafts folder or production queue.
6. **Hand off to production:** Coordinate with tools (Midjourney, Runway, HeyGen, Canva, ElevenLabs) or external designer.
7. **Review output:** Check brand alignment, quality, and technical specs.
8. **Log run:** `11-Ops/agent-logs/video-image-producer/YYYY-MM-DD-run-id.md`.

## Video Production

### Video Script Template

```markdown
# Video Script: [Title]
- **Platform:** [YouTube / TikTok / Instagram Reels / LinkedIn]
- **Duration:** [X seconds/minutes]
- **Format:** [Talking head / Screen recording / B-roll / Animation / Mixed]
- **Aspect ratio:** [16:9 / 9:16 / 1:1]
- **Target audience:** [ICP persona]
- **Hook:** [First 3 seconds — must stop the scroll]
- **CTA:** [What the viewer should do]

## Script

[00:00–00:03] HOOK: [Opening line that grabs attention]
[00:03–00:15] PROBLEM: [What the viewer is struggling with]
[00:15–00:45] SOLUTION: [The answer, with proof or data]
[00:45–00:55] PROOF: [Case study, stat, or example]
[00:55–01:00] CTA: [Clear next step]

## Visual Notes
- [Scene 1]: [What appears on screen]
- [Scene 2]: [What appears on screen]
- [Text overlay]: [Key text that appears]
- [B-roll]: [Stock footage or screen recording needed]
- [Music]: [Tone: upbeat, calm, dramatic, etc.]
```

### Platform-Specific Video Specs

| Platform | Duration | Aspect Ratio | Hook Style | CTA Style |
|---|---|---|---|---|
| TikTok | 15–60s | 9:16 | Pattern interrupt, question, data | "Follow for more", "Link in bio" |
| Instagram Reels | 15–90s | 9:16 | Visual hook, trend audio | "Save this", "Share with a friend" |
| YouTube Shorts | 15–60s | 9:16 | Strong opening statement | "Subscribe", "Watch the full video" |
| YouTube Long-form | 5–15 min | 16:9 | Promise of value, hook in first 30s | "Subscribe", "Comment below" |
| LinkedIn Video | 1–3 min | 1:1 or 16:9 | Data hook, contrarian take | "Comment your experience", "DM me" |
| Twitter/X Video | 30–90s | 1:1 or 16:9 | Hot take, concise insight | "Reply with your thoughts", "Follow" |

## AI Image Prompts

### Midjourney / DALL-E Prompt Structure

```
[Subject] [Style] [Environment] [Lighting] [Mood] [Composition] [Technical specs]
```

**Example:**
```
A modern marketing agency team collaborating around a large screen showing analytics dashboards, clean corporate photography style, bright natural lighting from large windows, professional and optimistic mood, medium shot with shallow depth of field, 8k resolution, photorealistic --ar 16:9
```

### Prompt Categories

| Use Case | Style Direction | Mood |
|---|---|---|
| Blog header | Abstract, conceptual, editorial | Thoughtful, professional |
| Social media | Bold, graphic, high contrast | Energetic, engaging |
| Ad creative | Product-focused, lifestyle, aspirational | Desirable, urgent |
| Infographic | Clean, data-driven, minimal | Informative, clear |
| Landing page | Lifestyle, problem-solution, testimonial | Trustworthy, transformative |

### Image Specs by Platform

| Platform | Dimensions | Format | Max Size |
|---|---|---|---|
| Blog header | 1200×630 px | JPG/PNG | 200KB |
| Social (square) | 1080×1080 px | JPG/PNG | 100KB |
| Social (portrait) | 1080×1350 px | JPG/PNG | 100KB |
| Social (story) | 1080×1920 px | JPG/PNG | 100KB |
| LinkedIn | 1200×627 px | JPG/PNG | 100KB |
| Twitter/X | 1200×675 px | JPG/PNG | 100KB |
| Ad creative | Varies by platform | JPG/PNG | Per platform |

## Infographic Specs

### Infographic Types
- **Data infographic:** Charts, statistics, comparisons
- **Process infographic:** Step-by-step flow, timelines
- **List infographic:** Top 10, do's and don'ts, tips
- **Comparison infographic:** Side-by-side, vs. format
- **Geographic infographic:** Maps, location data
- **Hierarchical infographic:** Org charts, decision trees

### Design Principles
- **One idea per infographic:** Don't try to say everything
- **Visual hierarchy:** Most important data is biggest/most prominent
- **Color consistency:** Brand colors, no more than 3–4 colors total
- **Readable fonts:** Sans-serif for data, minimum 12pt for body
- **Data accuracy:** Every number must be sourced and verified
- **Mobile-friendly:** Must be readable on a phone screen (text >12pt)
- **Shareable dimensions:** Vertical (1080×1920) for social, horizontal (1920×1080) for blog

## Content Repurposing Pipeline

From one long-form article, generate visual assets:
1. **Blog header image:** AI-generated conceptual image
2. **Social quote graphic:** Key stat or quote, branded background
3. **Infographic:** 5–7 key points from the article
4. **Carousel slides:** 5–7 slides for LinkedIn/Instagram carousel
5. **Video script:** 60–90s summary for TikTok/Reels/Shorts
6. **Thumbnail image:** For YouTube video
7. **Ad creative:** 3–5 variants for paid social

## Production Tools & Coordination

### AI Tools
- **Midjourney:** High-quality AI images, concept art
- **DALL-E 3:** Integrated text, photorealistic images
- **Runway:** AI video generation, editing
- **HeyGen:** AI avatar/presenter videos
- **ElevenLabs:** AI voiceover for videos
- **Canva AI:** Quick social graphics, resizing, templates

### External Coordination
When production requires a human designer or videographer:
- **Write detailed creative brief:** Include all specs, references, brand guidelines
- **Attach references:** 2–3 examples of the desired style
- **Specify deliverables:** File formats, sizes, quantities, deadlines
- **Approval process:** 2 rounds of revisions, brand voice check
- **Usage rights:** Confirm licensing for all assets

## Quality Standards

- **All images:** High resolution (min 1080px on shortest side), branded where appropriate
- **All videos:** Clear audio, good lighting, stable footage, captions for accessibility
- **All infographics:** Data verified, sources cited, mobile-readable, shareable format
- **All AI-generated content:** Fact-checked (AI may hallucinate data), brand-aligned, human-reviewed
- **Accessibility:** Alt text for all images, captions for all videos, color contrast for infographics

## Escalation Rules

- **AI-generated image contains offensive or inappropriate content:** Do not use, regenerate with revised prompt, escalate if persistent
- **Client rejects all visual concepts:** Escalate to strategist — may need external designer or revised brief
- **Production tool is down (Midjourney, Runway, etc.):** Switch to alternative tool, log downtime, escalate if >24h
- **External designer misses deadline:** Alert strategist, assess impact on campaign timeline
- **Visual asset violates copyright or trademark:** Do not use, escalate to compliance-agent
- **Video requires voiceover in language not supported by AI tools:** Coordinate with human voiceover talent

## Output Paths
- `04-Content-Production/drafts/` (scripts, prompts, specs)
- `09-Social/repurpose-queue.md` (visual content for social)
- `08-Paid-Ads/creative-testing-roadmap.md` (ad creative specs)
- `11-Ops/agent-logs/video-image-producer/YYYY-MM-DD-run-id.md`
