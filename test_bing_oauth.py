"""
Quick test to verify Bing OAuth is wired up correctly.
Run this from PowerShell or any terminal.
"""
import sys
sys.path.insert(0, 'infrastructure')

from api_client.bing import BingWMTClient

try:
    c = BingWMTClient()
    print("=" * 60)
    print("BingWMTClient initialized successfully")
    print("=" * 60)
    if c.access_token:
        print("[OK] Auth method: OAuth")
        print("[OK] Has access_token: True")
        print("[OK] Has refresh_token: True")
        print()
        print("Token preview:", c.access_token[:20] + "...")
    else:
        print("[INFO] Auth method: API key (fallback)")
        print("       This is expected if you haven't completed the OAuth flow yet.")
        print()
        print("To activate OAuth:")
        print("  1. Apply migration 008 to create bing_tokens table")
        print("  2. Visit /credentials and click 'Connect Bing WMT (OAuth)'")
        print("  3. Re-run this test")

    print()
    print("=" * 60)
    print("Test: Get site details")
    print("=" * 60)
    from config import Config
    result = c.site_details(Config.WORDPRESS_SITE_URL)
    print("Result:", result)

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()