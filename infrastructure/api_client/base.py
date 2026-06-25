"""
AgenticMarketingPro — Generic API Client
========================================
Base HTTP client with:
- Automatic retry with exponential backoff
- Rate-limit handling (429 + custom headers)
- Auth injection (Bearer, API key, OAuth2 refresh)
- Structured error logging
- Request/response cost tracking
"""

import time
import json
import logging
from typing import Optional, Dict, Any, Callable
from datetime import datetime
from dataclasses import dataclass

import requests
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import Config


logger = logging.getLogger("amp.api_client")


@dataclass
class APIResponse:
    status_code: int
    headers: Dict[str, str]
    body: Any
    latency_ms: float
    retry_count: int
    url: str
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def is_rate_limited(self) -> bool:
        return self.status_code == 429

    @property
    def is_auth_error(self) -> bool:
        return self.status_code in (401, 403)


class APIClient:
    """Generic HTTP client for all marketing tool APIs."""

    def __init__(
        self,
        base_url: str,
        auth_header: Optional[str] = None,
        auth_value: Optional[str] = None,
        api_key_param: Optional[str] = None,
        api_key_value: Optional[str] = None,
        oauth_refresh_token: Optional[str] = None,
        oauth_client_id: Optional[str] = None,
        oauth_client_secret: Optional[str] = None,
        oauth_token_url: Optional[str] = None,
        rate_limit_rps: float = Config.DEFAULT_RATE_LIMIT_RPS,
        max_retries: int = Config.DEFAULT_MAX_RETRIES,
        timeout: float = 30.0,
        name: str = "generic",
    ):
        self.base_url = base_url.rstrip("/")
        self.auth_header = auth_header
        self.auth_value = auth_value
        self.api_key_param = api_key_param
        self.api_key_value = api_key_value
        self.oauth_refresh_token = oauth_refresh_token
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret
        self.oauth_token_url = oauth_token_url
        self.rate_limit_rps = rate_limit_rps
        self.max_retries = max_retries
        self.timeout = timeout
        self.name = name
        self._session = requests.Session()
        self._last_request_time: float = 0.0
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

        # Default headers
        self._session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "AgenticMarketingPro/1.0",
        })

    # ── Rate Limiting ───────────────────────────────────────────────────

    def _rate_limit_wait(self):
        """Ensure we don't exceed rate limit RPS."""
        elapsed = time.time() - self._last_request_time
        min_interval = 1.0 / self.rate_limit_rps
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last_request_time = time.time()

    # ── Auth ────────────────────────────────────────────────────────────

    def _get_auth_headers(self) -> Dict[str, str]:
        """Build auth headers for the request."""
        headers = {}

        # OAuth2: refresh token if needed
        if self.oauth_refresh_token and self.oauth_token_url:
            if time.time() >= self._token_expires_at - 60:  # 60s buffer
                self._refresh_oauth_token()
            if self._access_token:
                headers["Authorization"] = f"Bearer {self._access_token}"

        # Static Bearer / API key header
        elif self.auth_header and self.auth_value:
            headers[self.auth_header] = self.auth_value

        return headers

    def _refresh_oauth_token(self):
        """Refresh OAuth2 access token."""
        try:
            resp = requests.post(
                self.oauth_token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.oauth_refresh_token,
                    "client_id": self.oauth_client_id,
                    "client_secret": self.oauth_client_secret,
                },
                timeout=10.0,
            )
            data = resp.json()
            self._access_token = data.get("access_token")
            expires_in = data.get("expires_in", 3600)
            self._token_expires_at = time.time() + expires_in
            logger.info(f"[{self.name}] OAuth token refreshed, expires in {expires_in}s")
        except Exception as e:
            logger.error(f"[{self.name}] OAuth refresh failed: {e}")
            raise

    # ── Request ─────────────────────────────────────────────────────────

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_body: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        raw: bool = False,
    ) -> APIResponse:
        """Make an HTTP request with retry, rate limiting, and auth."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        merged_headers = {**self._get_auth_headers(), **(headers or {})}

        # Inject API key param if configured
        if self.api_key_param and self.api_key_value:
            params = {**(params or {}), self.api_key_param: self.api_key_value}

        retry_count = 0
        start_time = time.time()
        last_error: Optional[str] = None

        for attempt in range(self.max_retries + 1):
            self._rate_limit_wait()
            try:
                logger.debug(f"[{self.name}] {method} {url} (attempt {attempt + 1})")
                resp = self._session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    json=json_body,
                    headers=merged_headers,
                    timeout=self.timeout,
                )
                latency_ms = (time.time() - start_time) * 1000

                # Parse response
                if raw:
                    body = resp.content
                else:
                    try:
                        body = resp.json()
                    except Exception:
                        body = resp.text

                api_resp = APIResponse(
                    status_code=resp.status_code,
                    headers=dict(resp.headers),
                    body=body,
                    latency_ms=latency_ms,
                    retry_count=retry_count,
                    url=url,
                )

                # Handle rate limit
                if api_resp.is_rate_limited:
                    retry_after = int(resp.headers.get("Retry-After", 60))
                    logger.warning(f"[{self.name}] Rate limited. Retry-After: {retry_after}s")
                    if attempt < self.max_retries:
                        time.sleep(retry_after)
                        retry_count += 1
                        continue
                    return api_resp

                # Handle auth error (try refresh once)
                if api_resp.is_auth_error and self.oauth_refresh_token and attempt == 0:
                    self._refresh_oauth_token()
                    retry_count += 1
                    continue

                return api_resp

            except requests.exceptions.Timeout as e:
                last_error = f"Timeout: {e}"
                logger.warning(f"[{self.name}] Timeout on attempt {attempt + 1}")
            except requests.exceptions.ConnectionError as e:
                last_error = f"ConnectionError: {e}"
                logger.warning(f"[{self.name}] Connection error on attempt {attempt + 1}")
            except Exception as e:
                last_error = f"Exception: {e}"
                logger.warning(f"[{self.name}] Error on attempt {attempt + 1}: {e}")

            if attempt < self.max_retries:
                backoff = min(2 ** attempt * Config.DEFAULT_BACKOFF_BASE, 60)
                logger.info(f"[{self.name}] Backing off {backoff}s before retry")
                time.sleep(backoff)
                retry_count += 1

        # All retries exhausted
        latency_ms = (time.time() - start_time) * 1000
        return APIResponse(
            status_code=0,
            headers={},
            body=None,
            latency_ms=latency_ms,
            retry_count=retry_count,
            url=url,
            error=last_error or "All retries exhausted",
        )

    # ── Convenience methods ───────────────────────────────────────────

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> APIResponse:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json_body: Optional[Dict] = None, **kwargs) -> APIResponse:
        return self.request("POST", endpoint, json_body=json_body, **kwargs)

    def put(self, endpoint: str, json_body: Optional[Dict] = None, **kwargs) -> APIResponse:
        return self.request("PUT", endpoint, json_body=json_body, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> APIResponse:
        return self.request("DELETE", endpoint, **kwargs)

    # ── Health check ────────────────────────────────────────────────────

    def health_check(self) -> Dict[str, Any]:
        """Quick connectivity + auth check. Returns status dict."""
        start = time.time()
        try:
            # Try a lightweight endpoint or HEAD request
            resp = self._session.head(self.base_url, timeout=10.0, headers=self._get_auth_headers())
            latency_ms = (time.time() - start) * 1000
            return {
                "name": self.name,
                "status": "healthy" if resp.status_code < 500 else "degraded",
                "status_code": resp.status_code,
                "latency_ms": round(latency_ms, 2),
                "auth_ok": not (resp.status_code in (401, 403)),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        except Exception as e:
            return {
                "name": self.name,
                "status": "down",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }


if __name__ == "__main__":
    # Example: test with a public API
    client = APIClient(
        base_url="https://api.github.com",
        auth_header="Authorization",
        auth_value="token test",
        name="github_test",
    )
    print(client.health_check())
