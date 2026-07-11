"""
Update cron-job.org job #8023152 to use ?mode=single.
Reads the API key by importing the existing scripts/cron-job-setup.py module.
"""
import sys
import os
import json
import requests

# Add the scripts directory to the path so we can import cron-job-setup
SCRIPTS_DIR = r"F:\Agentic Marketing Pro\marketing\scripts"
sys.path.insert(0, SCRIPTS_DIR)

# Import the module — this gives us CRON_API_KEY automatically
import importlib.util
spec = importlib.util.spec_from_file_location("cron_job_setup", os.path.join(SCRIPTS_DIR, "cron-job-setup.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

CRON_API_KEY = mod.CRON_API_KEY
CRON_API_URL = mod.CRON_API_URL
JOB_ID = 8023152
NEW_URL = "https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs?mode=single"

print(f"Loaded API key: {CRON_API_KEY[:8]}...{CRON_API_KEY[-6:]} (len={len(CRON_API_KEY)})")
print()

headers = {
    "Authorization": f"Bearer {CRON_API_KEY}",
    "Content-Type": "application/json",
}

# Get current job details
print("=" * 60)
print(f"Fetching current state of job #{JOB_ID}...")
print("=" * 60)
resp = requests.get(f"{CRON_API_URL}/jobs/{JOB_ID}", headers=headers, timeout=15)
print(f"GET status: {resp.status_code}")
if resp.status_code != 200:
    print(resp.text[:500])
    sys.exit(1)

job = resp.json().get("jobDetails", {})
print(f"Title:        {job.get('title')}")
print(f"Current URL:  {job.get('url')}")
print(f"Enabled:      {job.get('enabled')}")
print(f"Last status:  {job.get('lastStatus')}")
print(f"Last dur:     {job.get('lastDuration')}ms")
sched = job.get("schedule", {})
print(f"Schedule min: {sched.get('minutes')}")
print(f"Method:       {job.get('requestMethod')}")
print()

# Build update payload - change only the URL
update = {
    "jobId": JOB_ID,
    "job": {
        "url": NEW_URL,
        "enabled": True,
        "saveResponses": True,
        "schedule": sched,
        "requestMethod": job.get("requestMethod", 1),
        "headers": job.get("headers", {}),
    },
}

print("=" * 60)
print(f"Updating URL to: {NEW_URL}")
print("=" * 60)

# Try PATCH first
resp2 = requests.patch(f"{CRON_API_URL}/jobs/{JOB_ID}", headers=headers, json=update, timeout=15)
print(f"PATCH status: {resp2.status_code}")
print(f"Response: {resp2.text[:800]}")

if resp2.status_code not in (200, 204):
    print("\n[warn] PATCH failed - trying PUT")
    put_payload = {"job": dict(update["job"])}
    put_payload["job"]["jobId"] = JOB_ID
    resp3 = requests.put(f"{CRON_API_URL}/jobs/{JOB_ID}", headers=headers, json=put_payload, timeout=15)
    print(f"PUT status: {resp3.status_code}")
    print(f"Response: {resp3.text[:800]}")

# Verify
print()
print("=" * 60)
print("Verifying update...")
print("=" * 60)
resp4 = requests.get(f"{CRON_API_URL}/jobs/{JOB_ID}", headers=headers, timeout=15)
job2 = resp4.json().get("jobDetails", {})
print(f"New URL: {job2.get('url')}")
print(f"Enabled: {job2.get('enabled')}")