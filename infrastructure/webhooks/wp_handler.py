"""
AgenticMarketingPro — WordPress Job Handler
============================================
Publishes posts, updates meta, and manages WordPress content via REST API.

Triggered by Edge Function when a job has type="wp_publish" or "wp_update".

Credential resolution order:
  1. Job payload: client_slug → look up credentials in Supabase credentials table
  2. Global env vars: WORDPRESS_SITE_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

logger = logging.getLogger("amp.wp_handler")


def _get_wp_credentials(client_slug: Optional[str] = None) -> Dict[str, str]:
    """
    Resolve WordPress credentials.
    Tries Supabase credentials table first, then env vars.
    """
    # Try Supabase first (per-client credentials)
    if client_slug:
        try:
            from supabase import create_client
            url = Config.SUPABASE_URL or os.getenv("SUPABASE_URL")
            key = Config.SUPABASE_SERVICE_ROLE_KEY or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            if url and key:
                sb = create_client(url, key)
                result = sb.table("credentials").select("*").eq(
                    "service", "wordpress"
                ).eq(
                    "client_slug", client_slug
                ).eq(
                    "is_active", True
                ).maybe_single().execute()

                if result and result.data:
                    cred = result.data
                    config = cred.get("config", {})
                    secrets = cred.get("secrets", {})
                    return {
                        "site_url": config.get("site_url", ""),
                        "username": config.get("username", ""),
                        "app_password": secrets.get("app_password", ""),
                        "seo_plugin": config.get("seo_plugin", Config.WORDPRESS_SEO_PLUGIN),
                    }
        except Exception as e:
            logger.warning(f"Could not fetch credentials from Supabase: {e}")

    # Fall back to global env vars
    if Config.WORDPRESS_SITE_URL and Config.WORDPRESS_USERNAME and Config.WORDPRESS_APP_PASSWORD:
        return {
            "site_url": Config.WORDPRESS_SITE_URL,
            "username": Config.WORDPRESS_USERNAME,
            "app_password": Config.WORDPRESS_APP_PASSWORD,
            "seo_plugin": Config.WORDPRESS_SEO_PLUGIN,
        }

    raise ValueError(
        "WordPress credentials not configured. Either:\\n"
        "  1. Add via /credentials UI for a specific client\\n"
        "  2. Set WORDPRESS_SITE_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD env vars"
    )


def execute_wp_job(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatch table for WordPress jobs.

    payload = {
        "mode": "publish" | "update" | "delete" | "from_vault",
        "client_slug": "..." (optional),
        # For publish mode:
        "title": "...",
        "content": "...",
        "status": "draft" | "publish",
        "categories": [1, 2],
        "tags": ["seo", "ai"],
        "seo_title": "...",
        "seo_description": "...",
        # For update mode:
        "post_id": 123,
        # For from_vault mode:
        "vault_file": "F:\\path\\to\\article.md",
    }
    """
    from datetime import datetime
    mode = payload.get("mode", "publish")
    client_slug = payload.get("client_slug")

    try:
        creds = _get_wp_credentials(client_slug)
    except ValueError as e:
        return {"ok": False, "error": str(e), "timestamp": datetime.utcnow().isoformat() + "Z"}

    # Import the WordPress client
    try:
        from api_client.wordpress import WordPressClient
    except ImportError as e:
        return {"ok": False, "error": f"WordPress client not available: {e}"}

    wp = WordPressClient(
        site_url=creds["site_url"],
        username=creds["username"],
        app_password=creds["app_password"],
        seo_plugin=creds.get("seo_plugin", "None"),
    )

    # Test connection first
    test = wp.test_connection()
    if test.get("status") != "connected":
        return {
            "ok": False,
            "error": f"WordPress connection failed: {test}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    try:
        if mode == "publish":
            result = wp.create_post(
                title=payload.get("title", "Untitled"),
                content=payload.get("content", ""),
                status=payload.get("status", "draft"),
                post_type=payload.get("post_type", "post"),
                categories=payload.get("categories"),
                tags=payload.get("tags"),
                excerpt=payload.get("excerpt"),
                slug=payload.get("slug"),
                seo_title=payload.get("seo_title"),
                seo_description=payload.get("seo_description"),
            )
            return {
                "ok": result.get("status") == "created",
                "mode": "publish",
                "site": creds["site_url"],
                "result": result,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        elif mode == "update":
            post_id = payload.get("post_id")
            if not post_id:
                return {"ok": False, "error": "post_id is required for update mode"}

            result = wp.update_post(
                post_id=post_id,
                title=payload.get("title"),
                content=payload.get("content"),
                status=payload.get("status"),
                seo_title=payload.get("seo_title"),
                seo_description=payload.get("seo_description"),
            )
            return {
                "ok": "status" not in result or result.get("status") != "error",
                "mode": "update",
                "post_id": post_id,
                "result": result,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        elif mode == "from_vault":
            vault_file = payload.get("vault_file")
            if not vault_file:
                return {"ok": False, "error": "vault_file is required for from_vault mode"}
            if not Path(vault_file).exists():
                return {"ok": False, "error": f"Vault file not found: {vault_file}"}
            result = wp.publish_from_vault(vault_file, client_slug or "default")
            return {
                "ok": result.get("status") == "created",
                "mode": "from_vault",
                "vault_file": vault_file,
                "result": result,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        elif mode == "delete":
            post_id = payload.get("post_id")
            if not post_id:
                return {"ok": False, "error": "post_id is required for delete mode"}
            from api_client.base import APIClient
            client = APIClient(
                base_url=f"{creds['site_url']}/wp-json/wp/v2",
                auth_header="Authorization",
                auth_value=f"Basic {__import__('base64').b64encode((creds['username'] + ':' + creds['app_password']).encode()).decode()}",
                name="wordpress_delete",
            )
            resp = client.delete(f"/posts/{post_id}", params={"force": True})
            return {
                "ok": resp.is_success,
                "mode": "delete",
                "post_id": post_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        else:
            return {
                "ok": False,
                "error": f"Unknown mode: {mode}. Use: publish, update, delete, from_vault",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

    except Exception as e:
        logger.exception("WordPress job failed")
        return {
            "ok": False,
            "error": str(e),
            "mode": mode,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a WordPress job")
    parser.add_argument("--mode", choices=["publish", "update", "delete", "from_vault"], default="publish")
    parser.add_argument("--title", default="Test Post")
    parser.add_argument("--content", default="Test content")
    parser.add_argument("--status", default="draft")
    parser.add_argument("--client-slug", default=None)
    parser.add_argument("--post-id", type=int, default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    payload = {
        "mode": args.mode,
        "client_slug": args.client_slug,
        "title": args.title,
        "content": args.content,
        "status": args.status,
    }
    if args.post_id:
        payload["post_id"] = args.post_id

    result = execute_wp_job(payload)
    print(json.dumps(result, indent=2, default=str))