"""
AgenticMarketingPro — Supabase REST Client (Python)
====================================================
Minimal Supabase client using the REST API (PostgREST).
Used for direct database reads/writes from local scripts
when the Supabase CLI is not authenticated.

Tables managed here:
- bing_tokens (OAuth token storage)
- credentials (API keys per client)
- jobs (background job queue)

Docs: https://postgrest.org/en/stable/api.html
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger("amp.supabase")


class SupabaseAPI:
    """Minimal PostgREST client for AgenticMarketingPro.

    Usage:
        from supabase_api import SupabaseAPI
        result = SupabaseAPI.select("bing_tokens", columns="access_token,refresh_token")
        if result.is_success:
            for row in result.body:
                print(row)
    """

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        from config import Config
        self.url = (url or Config.SUPABASE_URL or "").rstrip("/")
        self.key = key or Config.SUPABASE_SERVICE_ROLE_KEY
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")

    # ── Generic REST helpers ──────────────────────────────────────────

    def _headers(self) -> Dict[str, str]:
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def select(
        self,
        table: str,
        columns: str = "*",
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> "SupabaseResponse":
        url = f"{self.url}/rest/v1/{table}?select={columns}"
        if filters:
            for k, v in filters.items():
                url += f"&{k}={requests.utils.quote(str(v))}"
        if limit:
            url += f"&limit={limit}"
        try:
            r = requests.get(url, headers=self._headers(), timeout=30)
            body = r.json() if r.text else []
            return SupabaseResponse(r.status_code, body)
        except Exception as e:
            logger.error(f"Supabase select error: {e}")
            return SupabaseResponse(0, None, str(e))

    def insert(self, table: str, row: Dict[str, Any]) -> "SupabaseResponse":
        url = f"{self.url}/rest/v1/{table}"
        try:
            r = requests.post(url, headers=self._headers(), data=json.dumps(row), timeout=30)
            body = r.json() if r.text else None
            return SupabaseResponse(r.status_code, body)
        except Exception as e:
            logger.error(f"Supabase insert error: {e}")
            return SupabaseResponse(0, None, str(e))

    def upsert(self, table: str, row: Dict[str, Any], on_conflict: str = "id") -> "SupabaseResponse":
        url = f"{self.url}/rest/v1/{table}?on_conflict={on_conflict}"
        headers = self._headers()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"
        try:
            r = requests.post(url, headers=headers, data=json.dumps(row), timeout=30)
            body = r.json() if r.text else None
            return SupabaseResponse(r.status_code, body)
        except Exception as e:
            logger.error(f"Supabase upsert error: {e}")
            return SupabaseResponse(0, None, str(e))

    def update(
        self, table: str, filters: Dict[str, Any], updates: Dict[str, Any]
    ) -> "SupabaseResponse":
        url = f"{self.url}/rest/v1/{table}"
        for k, v in filters.items():
            url += f"?{k}=eq.{requests.utils.quote(str(v))}"
        try:
            r = requests.patch(url, headers=self._headers(), data=json.dumps(updates), timeout=30)
            body = r.json() if r.text else None
            return SupabaseResponse(r.status_code, body)
        except Exception as e:
            logger.error(f"Supabase update error: {e}")
            return SupabaseResponse(0, None, str(e))

    def delete(self, table: str, filters: Dict[str, Any]) -> "SupabaseResponse":
        url = f"{self.url}/rest/v1/{table}"
        for k, v in filters.items():
            url += f"?{k}=eq.{requests.utils.quote(str(v))}"
        try:
            r = requests.delete(url, headers=self._headers(), timeout=30)
            return SupabaseResponse(r.status_code, r.text)
        except Exception as e:
            logger.error(f"Supabase delete error: {e}")
            return SupabaseResponse(0, None, str(e))


class SupabaseResponse:
    """Wrapper around a Supabase API response."""

    def __init__(self, status_code: int, body: Any = None, error: Optional[str] = None):
        self.status_code = status_code
        self.body = body
        self.error = error

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def is_success_and_has_body(self) -> bool:
        return self.is_success and self.body

    def __repr__(self) -> str:
        return f"SupabaseResponse(status={self.status_code}, body_len={len(self.body) if isinstance(self.body, list) else (1 if self.body else 0)})"