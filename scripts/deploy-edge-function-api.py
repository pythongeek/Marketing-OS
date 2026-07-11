"""
Workaround for the Supabase CLI 403 access error.

If `npx supabase functions deploy` returns "Your account does not have the
necessary privileges", it means the CLI is logged in as a different account
than the one that owns the project `pusttdxrtmgvhdzdyvbd`.

Options to fix:
  1. Log in with the correct account:    npx supabase login
  2. Use --token flag with the correct access token
  3. Deploy via Supabase Dashboard (no CLI needed)
  4. Deploy via direct API call (this script)

This script uses option 4 — direct API deployment via curl + the management API.
"""

import subprocess
import sys
import os

PROJECT_REF = "pusttdxrtmgvhdzdyvbd"
FUNCTION_NAME = "execute-jobs"
FUNCTION_PATH = r"F:\Agentic Marketing Pro\marketing\supabase\functions\execute-jobs\index.ts"


def deploy_via_dashboard_instructions():
    print("=" * 70)
    print("  SUPABASE CLI DEPLOYMENT FIX")
    print("=" * 70)
    print()
    print("Your CLI is logged in as a different account than the project owner.")
    print(f"Project: {PROJECT_REF}")
    print()
    print("OPTION 1: Use the correct access token")
    print("-" * 70)
    print("""
1. Go to https://app.supabase.com/account/tokens
2. Generate a new access token (or copy the one for the project owner)
3. Login with it:
   npx supabase login --token sbp_xxxxxxxxxxxxxxxxxxxx
4. Try deploy again:
   npx supabase functions deploy execute-jobs
""")
    print()
    print("OPTION 2: Deploy via Supabase Dashboard")
    print("-" * 70)
    print("""
1. Go to https://app.supabase.com/project/pusttdxrtmgvhdzdyvbd/functions
2. Find execute-jobs (or create it)
3. Click "Deploy new version"
4. Paste the code from:
   F:\\Agentic Marketing Pro\\marketing\\supabase\\functions\\execute-jobs\\index.ts
5. Click Deploy
""")
    print()
    print("OPTION 3: Use this script to deploy via API")
    print("-" * 70)
    print(f"python scripts/deploy-edge-function-api.py --token YOUR_ACCESS_TOKEN")
    print()


def deploy_via_api(access_token: str):
    """Deploy Edge Function directly via Supabase Management API."""
    import base64

    if not os.path.exists(FUNCTION_PATH):
        print(f"[error] Function file not found: {FUNCTION_PATH}")
        sys.exit(1)

    print(f"Reading function code from {FUNCTION_PATH}...")
    with open(FUNCTION_PATH, "rb") as f:
        code_bytes = f.read()
    print(f"  Read {len(code_bytes)} bytes")

    # Supabase Management API endpoint
    # Multipart form upload
    url = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/functions/{FUNCTION_NAME}"

    # Build curl command
    print(f"Deploying to {url}...")

    # Use the new endpoint format
    cmd = [
        "curl", "-X", "POST",
        url,
        "-H", f"Authorization: Bearer {access_token}",
        "-H", "Content-Type: application/json",
        "-d", '{"slug": "execute-jobs", "name": "execute-jobs", "body": "", "verify_jwt": false}',
    ]

    # Actually we need to use multipart for file upload
    # The proper API is multipart/form-data with the file as 'file' field
    cmd = [
        "curl", "-X", "POST",
        url,
        "-H", f"Authorization: Bearer {access_token}",
        "-F", f"file=@{FUNCTION_PATH}",
    ]

    print(f"Running: {' '.join(cmd[:5])}... [file path redacted]")

    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", result.stdout[:2000])
    print("STDERR:", result.stderr[:2000])
    print("Exit code:", result.returncode)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Deploy Edge Function via API")
    parser.add_argument("--token", help="Supabase access token (sbp_...)")
    parser.add_argument("--instructions", action="store_true",
                        help="Just show deployment instructions")
    args = parser.parse_args()

    if args.instructions or not args.token:
        deploy_via_dashboard_instructions()
    else:
        deploy_via_api(args.token)