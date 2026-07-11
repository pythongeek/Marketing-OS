# WordPress Integration Setup Guide

For AgenticMarketingPro to publish posts, update titles, change meta, and perform other WordPress edits automatically.

---

## What You Need From WordPress Admin

To connect AgenticMarketingPro to your WordPress site, you need 3 things:

### 1. WordPress Site URL
```
https://yoursite.com
```

### 2. WordPress Username
The username you'll use to authenticate via the REST API.
```
example: admin
```

### 3. WordPress Application Password (NOT your login password!)

**Step-by-step to create one (2 minutes):**

1. Log in to WordPress admin dashboard
2. Go to **Users → Profile** (or **Users → All Users → click your username**)
3. Scroll down to the **"Application Passwords"** section
4. Under **"New Application Password Name"**, type: `AgenticMarketingPro`
5. Click **"Add New Application Password"**
6. WordPress will generate a password like: `abcd EFGH ijkl MNOP qrst UVWX`
7. ⚠️ **Copy this password immediately** — you can never see it again!

The application password has spaces — remove them when pasting into AgenticMarketingPro:
```
abcdEFGHijklMNOPqrstUVWX
```

---

## How to Add to AgenticMarketingPro

### Option A: Add via Admin UI (Recommended for multiple sites)

1. Visit https://marketing-os-chi-three.vercel.app/credentials
2. Click **"+ Add"** next to **"WordPress"**
3. Fill in:
   - **Site URL**: `https://yoursite.com`
   - **Username**: `your-username`
   - **Client Slug**: `your-client-name` (optional, for multi-site)
   - **Label**: `Main Blog` or similar
   - **Application Password**: paste the password (no spaces)
4. Click **Save**

The credentials are encrypted and stored in the Supabase `credentials` table.

### Option B: Add via .env (Global default)

Add to `.env` (and Vercel environment variables):
```bash
WORDPRESS_SITE_URL=https://yoursite.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=abcdEFGHijklMNOPqrstUVWX
WORDPRESS_SEO_PLUGIN=Yoast SEO  # or "Rank Math" or "None"
```

---

## What AgenticMarketingPro Can Do With WordPress

Once connected, AgenticMarketingPro can:

| Action | Method | Use Case |
|--------|--------|----------|
| **Create post** | `POST /wp-json/wp/v2/posts` | Publish new articles from vault |
| **Update post** | `POST /wp-json/wp/v2/posts/{id}` | Update existing content |
| **Update SEO title** | meta field `yoast_wpseo_title` | Optimize for search |
| **Update meta description** | meta field `yoast_wpseo_metadesc` | Improve CTR |
| **Change post status** | `draft`, `publish`, `private`, `pending` | Schedule content |
| **Upload featured image** | `POST /media` | Set post thumbnails |
| **Add categories/tags** | `POST /categories`, `POST /tags` | Organize content |
| **Update slug** | field `slug` | SEO-friendly URLs |
| **Bulk update** | Loop over posts | Apply SEO fixes at scale |

### SEO Plugin Support

The WordPress client auto-detects and writes the correct meta keys for:
- **Yoast SEO** (most popular — installed on 5M+ sites)
- **Rank Math** (fast-growing alternative)
- **All in One SEO** (legacy plugin)
- **None** (just saves post without SEO meta)

---

## Automated Posting Workflow

Once connected, you can:

1. **Write content in Obsidian vault** → save as `.md` file with frontmatter
2. **Schedule a job** via cron-job.org → triggers Edge Function
3. **Edge Function reads vault → calls WordPress API → publishes post**

Example frontmatter:
```yaml
---
title: "How to Optimize Your Site for AEO"
wp_status: draft
wp_post_type: post
categories: [SEO, AI Search]
tags: [aeo, geo, optimization]
seo_title: "AEO Optimization Guide 2026"
seo_description: "Learn how to optimize for Answer Engine Optimization..."
date: 2026-07-15
author: AgenticMarketingPro
---
# Article content here...
```

The WordPress client extracts this frontmatter and:
- Sets the title
- Converts markdown to HTML
- Maps categories/tags to existing WordPress IDs
- Sets SEO meta fields (if plugin configured)
- Publishes (or saves as draft)

---

## Troubleshooting

### "401 Unauthorized"
- Wrong username or application password
- Regenerate the application password in WP admin → Users → Profile

### "403 Forbidden"
- Application passwords are disabled. Enable in `wp-config.php`:
  ```php
  define('WP_DISALLOW_FILE_MODS', false);
  ```
- Or check if a security plugin is blocking REST API access

### "404 Not Found"
- Pretty permalinks not enabled. Go to Settings → Permalinks → choose anything except "Plain"

### "cURL error 60: SSL certificate problem"
- Your SSL cert is invalid or self-signed
- Use HTTP for testing (not recommended for production)

### "Sorry, you are not allowed to create posts"
- The user account doesn't have Author/Editor/Admin role
- Application passwords inherit the user's permissions

---

## Files Modified for WordPress Support

| File | Purpose |
|------|---------|
| `infrastructure/api_client/wordpress.py` | Full WordPress REST API client (already exists) |
| `web/app/credentials/page.tsx` | WordPress credential form (already exists) |
| `infrastructure/webhooks/wp_handler.py` | NEW: Job handler for WordPress ops |
| `supabase/functions/execute-jobs/index.ts` | NEW: `wp_publish` job type |
| `.env` | Add global WordPress config |

---

*Last updated: 2026-07-12*
*Part of the AgenticMarketingPro operating system.*