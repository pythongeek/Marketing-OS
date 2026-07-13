"""
AgenticMarketingPro — WordPress REST API Client
===============================================
Handles publishing, updating, and managing WordPress content via REST API.
Supports: posts, pages, custom post types, featured images, meta fields,
SEO plugins (Yoast, Rank Math), categories, tags, and media uploads.

Usage:
    from api_client.wordpress import WordPressClient
    wp = WordPressClient("https://example.com", "username", "app_password")
    wp.test_connection()
    post = wp.create_post(title="My Article", content="...", status="draft")
"""

import base64
import json
import logging
from typing import Dict, List, Optional, Any

from config import Config
from api_client.base import APIClient

logger = logging.getLogger("amp.wordpress")


class WordPressClient:
    """WordPress REST API client for content publishing."""

    def __init__(
        self,
        site_url: str,
        username: str,
        app_password: str,
        seo_plugin: str = "None",
    ):
        self.site_url = site_url.rstrip("/")
        self.username = username
        self.app_password = app_password
        self.seo_plugin = seo_plugin
        self.api_base = f"{self.site_url}/wp-json/wp/v2"

        # Build auth header
        credentials = base64.b64encode(f"{username}:{app_password}".encode()).decode()

        self.client = APIClient(
            base_url=self.api_base,
            auth_header="Authorization",
            auth_value=f"Basic {credentials}",
            rate_limit_rps=2.0,  # WordPress is typically generous
            name="wordpress",
        )

    # -- Connection Test -----------------------------------------------------

    def test_connection(self) -> Dict[str, Any]:
        """Test WordPress REST API connectivity."""
        try:
            resp = self.client.get("/users/me")
            if resp.is_success:
                return {
                    "status": "connected",
                    "username": resp.body.get("name", "unknown"),
                    "user_id": resp.body.get("id", 0),
                    "site_url": self.site_url,
                }
            elif resp.is_auth_error:
                return {"status": "auth_error", "error": "Invalid username or application password"}
            else:
                return {"status": "error", "code": resp.status_code, "error": resp.body}
        except Exception as e:
            return {"status": "exception", "error": str(e)}

    # -- Posts ---------------------------------------------------------------

    def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        post_type: str = "post",
        author_id: int = None,
        categories: List = None,
        tags: List = None,
        featured_media: int = None,
        excerpt: str = None,
        slug: str = None,
        meta: Dict = None,
        seo_title: str = None,
        seo_description: str = None,
    ) -> Dict[str, Any]:
        """Create a new WordPress post or page.

        Args:
            tags: Can be either a list of integer tag IDs OR a list of tag name strings
                  (strings will be auto-resolved to IDs, creating missing tags).
            categories: Can be either a list of integer IDs OR a list of category name
                        strings (strings will be auto-resolved to IDs).
        """
        body = {
            "title": title,
            "content": content,
            "status": status,
            "slug": slug or self._slugify(title),
        }
        if author_id:
            body["author"] = author_id
        # Resolve categories: accept IDs or names
        if categories:
            resolved_cats = self._resolve_taxonomy_ids(categories, "categories")
            if resolved_cats:
                body["categories"] = resolved_cats
        # Resolve tags: accept IDs or names
        if tags:
            resolved_tags = self._resolve_taxonomy_ids(tags, "tags")
            if resolved_tags:
                body["tags"] = resolved_tags
        if featured_media:
            body["featured_media"] = featured_media
        if excerpt:
            body["excerpt"] = excerpt

        # Always inject SEO as HTML (universal fallback for any theme/plugin)
        if seo_title or seo_description:
            content = self._inject_seo_html(content, seo_title, seo_description)
            body["content"] = content

        # SEO plugin meta
        seo_meta = self._build_seo_meta(seo_title, seo_description)
        if seo_meta:
            body["meta"] = seo_meta

        # Custom meta
        if meta:
            if "meta" not in body:
                body["meta"] = {}
            body["meta"].update(meta)

        endpoint = f"/{post_type}s" if post_type != "post" else "/posts"
        resp = self.client.post(endpoint, json_body=body)

        if resp.is_success:
            return {
                "status": "created",
                "post_id": resp.body.get("id"),
                "post_type": post_type,
                "title": title,
                "url": resp.body.get("link"),
                "status": status,
                "date": resp.body.get("date"),
            }
        return {"status": "error", "code": resp.status_code, "error": resp.body}

    def update_post(
        self,
        post_id: int,
        title: str = None,
        content: str = None,
        status: str = None,
        seo_title: str = None,
        seo_description: str = None,
    ) -> Dict[str, Any]:
        """Update an existing post."""
        body = {}
        if title:
            body["title"] = title
        if content:
            body["content"] = content
        if status:
            body["status"] = status

        seo_meta = self._build_seo_meta(seo_title, seo_description)
        if seo_meta:
            body["meta"] = seo_meta

        # Inject SEO HTML if content is being updated
        if "content" in body and (seo_title or seo_description):
            body["content"] = self._inject_seo_html(body["content"], seo_title, seo_description)

        resp = self.client.post(f"/posts/{post_id}", json_body=body)
        return resp.body if resp.is_success else {"status": "error", "code": resp.status_code}

    def get_post(self, post_id: int) -> Dict[str, Any]:
        """Get a post by ID."""
        resp = self.client.get(f"/posts/{post_id}")
        return resp.body if resp.is_success else {}

    def list_posts(self, per_page: int = 10, status: str = "publish") -> List[Dict]:
        """List recent posts."""
        resp = self.client.get("/posts", params={"per_page": per_page, "status": status})
        return resp.body if isinstance(resp.body, list) else []

    # -- Media ---------------------------------------------------------------

    def upload_media(self, file_path: str, title: str = None) -> Dict[str, Any]:
        """Upload an image or media file."""
        try:
            from pathlib import Path
            path = Path(file_path)
            mime_type = {
                ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".png": "image/png", ".gif": "image/gif",
                ".webp": "image/webp", ".svg": "image/svg+xml",
                ".mp4": "video/mp4", ".pdf": "application/pdf",
            }.get(path.suffix.lower(), "application/octet-stream")

            with open(file_path, "rb") as f:
                file_data = f.read()

            import requests
            headers = self.client._get_auth_headers()
            headers["Content-Disposition"] = f'attachment; filename="{path.name}"'
            headers["Content-Type"] = mime_type

            resp = requests.post(
                f"{self.api_base}/media",
                data=file_data,
                headers=headers,
                timeout=60.0,
            )

            if resp.status_code == 201:
                data = resp.json()
                return {
                    "status": "uploaded",
                    "media_id": data.get("id"),
                    "url": data.get("source_url"),
                    "title": data.get("title", {}).get("rendered", ""),
                }
            return {"status": "error", "code": resp.status_code, "body": resp.text}

        except Exception as e:
            return {"status": "exception", "error": str(e)}

    # -- Taxonomies ----------------------------------------------------------

    def get_categories(self) -> List[Dict]:
        """Get all categories."""
        resp = self.client.get("/categories", params={"per_page": 100})
        return resp.body if isinstance(resp.body, list) else []

    def get_tags(self) -> List[Dict]:
        """Get all tags."""
        resp = self.client.get("/tags", params={"per_page": 100})
        return resp.body if isinstance(resp.body, list) else []

    # -- SEO Meta ------------------------------------------------------------

    def _build_seo_meta(self, title: str = None, description: str = None) -> Dict:
        """Build SEO meta fields based on configured plugin."""
        if not title and not description:
            return {}

        meta = {}
        if self.seo_plugin == "Yoast SEO":
            if title:
                meta["yoast_wpseo_title"] = title
            if description:
                meta["yoast_wpseo_metadesc"] = description
        elif self.seo_plugin == "Rank Math":
            if title:
                meta["rank_math_title"] = title
            if description:
                meta["rank_math_description"] = description
        elif self.seo_plugin == "All in One SEO":
            if title:
                meta["_aioseop_title"] = title
            if description:
                meta["_aioseop_description"] = description
        return meta

    # -- Helpers -------------------------------------------------------------


    def _inject_seo_html(self, content, seo_title=None, seo_description=None):
        """Inject SEO meta as HTML in the content (universal fallback when plugin meta is not writable).

        This prepends HTML meta tags and Open Graph tags to the post content. WordPress
        themes and SEO plugins typically render these tags in the page <head>. This is a
        safe universal approach that works regardless of which SEO plugin is installed.
        """
        if not seo_title and not seo_description:
            return content

        seo_lines = ["<!-- AgenticMarketingPro SEO Injection -->"]
        if seo_title:
            seo_lines.append("<title>" + seo_title.encode().decode() + "</title>")
            seo_lines.append('<meta name="description" content="' + (seo_description or "").encode().decode() + '">')
            seo_lines.append('<meta property="og:title" content="' + seo_title.encode().decode() + '">')
            seo_lines.append('<meta property="og:description" content="' + (seo_description or "").encode().decode() + '">')
            seo_lines.append('<meta name="twitter:title" content="' + seo_title.encode().decode() + '">')
            seo_lines.append('<meta name="twitter:description" content="' + (seo_description or "").encode().decode() + '">')
        elif seo_description:
            seo_lines.append('<meta name="description" content="' + seo_description.encode().decode() + '">')
            seo_lines.append('<meta property="og:description" content="' + seo_description.encode().decode() + '">')
            seo_lines.append('<meta name="twitter:description" content="' + seo_description.encode().decode() + '">')
        seo_lines.append("<!-- /AgenticMarketingPro SEO Injection -->")
        seo_block = "\n".join(seo_lines)

        if "AgenticMarketingPro SEO Injection" in content:
            import re
            content = re.sub(
                r"<!-- AgenticMarketingPro SEO Injection -->.*?<!-- /AgenticMarketingPro SEO Injection -->\n?",
                (seo_block + "\n"),
                content,
                flags=re.DOTALL,
            )
        else:
            content = (seo_block + "\n" + content).encode() if isinstance(content, str) else seo_block.encode() + b"\n" + content

        return content

    def _resolve_taxonomy_ids(self, items, taxonomy):
        """Resolve a list of IDs or names to integer IDs for WP taxonomy terms."""
        if not items:
            return []
        resolved = []
        for item in items:
            if isinstance(item, int):
                resolved.append(item)
            elif isinstance(item, str) and item.strip():
                existing = self.client.get(f"/{taxonomy}", params={"search": item.strip(), "per_page": 100}).body
                found_id = None
                for term in (existing or []):
                    if term.get("name", "").lower() == item.strip().lower():
                        found_id = term["id"]
                        break
                if found_id:
                    resolved.append(found_id)
                else:
                    create_resp = self.client.post(f"/{taxonomy}", json_body={"name": item.strip()})
                    if create_resp.is_success:
                        resolved.append(create_resp.body["id"])
        return resolved

    def _slugify(self, text: str) -> str:
        import re
        return re.sub(r'[^a-z0-9]+', '-', text.lower().strip()).strip('-')

    # -- Vault Write-Back ----------------------------------------------------

    def publish_from_vault(self, vault_file_path: str, client: str) -> Dict[str, Any]:
        """Publish a content piece from the vault to WordPress."""
        from pathlib import Path
        path = Path(vault_file_path)
        if not path.exists():
            return {"status": "error", "error": f"File not found: {path}"}

        text = path.read_text(encoding="utf-8")

        # Extract frontmatter
        fm = {}
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    fm = yaml.safe_load(parts[1]) or {}
                except ImportError:
                    pass
                text = parts[2].strip()

        # Extract title from first H1 or frontmatter
        import re
        title = fm.get("title", "")
        if not title:
            match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
            if match:
                title = match.group(1).strip()

        # Convert markdown to HTML (basic)
        content_html = self._markdown_to_html(text)

        # Build categories from tags
        categories = []
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        # Get category IDs from WordPress
        wp_cats = self.get_categories()
        for tag in tags:
            for cat in wp_cats:
                if cat.get("name", "").lower() == tag.lower():
                    categories.append(cat.get("id"))

        return self.create_post(
            title=title,
            content=content_html,
            status=fm.get("wp_status", "draft"),
            post_type=fm.get("wp_post_type", "post"),
            categories=categories,
            tags=tags,
            seo_title=fm.get("seo_title", ""),
            seo_description=fm.get("seo_description", ""),
        )

    def _markdown_to_html(self, markdown: str) -> str:
        """Basic markdown to HTML conversion."""
        import re
        html = markdown
        # Headers
        html = re.sub(r'^###\s+(.+)$', r'<h3>\\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^##\s+(.+)$', r'<h2>\\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^#\s+(.+)$', r'<h1>\\1</h1>', html, flags=re.MULTILINE)
        # Bold/italic
        html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\\1</em></strong>', html)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\\1</em>', html)
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href=\"\\2\">\\1</a>', html)
        # Paragraphs
        paragraphs = html.split('\\n\\n')
        html = '\\n'.join(f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs)
        # Lists
        html = re.sub(r'(?m)^-\\s+(.+)$', r'<li>\\1</li>', html)
        html = re.sub(r'(<li>.+</li>\\n)+', r'<ul>\\g<0></ul>', html)
        return html


if __name__ == "__main__":
    # Test with dummy credentials (will fail but shows structure)
    try:
        wp = WordPressClient("https://example.com", "admin", "dummy_password")
        print("WordPressClient initialized. Test connection:")
        print(wp.test_connection())
    except Exception as e:
        print(f"Error: {e}")
