"""
AgenticMarketingPro API Client Wrappers
=======================================

All SEO, analytics, and ads API clients live here.

Usage:
    from api_client.gsc import GSCClient
    from api_client.ga4 import GA4Client
    from api_client.ahrefs import AhrefsClient
    from api_client.semrush import SemrushClient
    from api_client.bing import BingWMTClient
    from api_client.base import APIClient

Each client wraps the generic APIClient with endpoint-specific methods
and returns structured data ready for vault write-back.
"""
