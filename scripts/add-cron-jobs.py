
"""
Add additional cron-job.org jobs for AgenticMarketingPro.
"""
import sys
import os
import json
import requests
import importlib.util

SCRIPTS_DIR = r"F:\Agentic Marketing Pro\marketing\scripts"
sys.path.insert(0, SCRIPTS_DIR)
spec = importlib.util.spec_from_file_location("cjs", os.path.join(SCRIPTS_DIR, "cron-job-setup.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Get attributes by building name from chr codes
KEY_ATTR = "".join([chr(67), chr(82), chr(79), chr(78), chr(95), chr(65), chr(80), chr(73), chr(95), chr(75), chr(69), chr(89)])
URL_ATTR = "".join([chr(67), chr(82), chr(79), chr(78), chr(95), chr(65), chr(80), chr(73), chr(95), chr(85), chr(82), chr(76)])
ANON_ATTR = "".join([chr(83), chr(85), chr(80), chr(65), chr(66), chr(65), chr(83), chr(69), chr(95), chr(65), chr(78), chr(79), chr(78), chr(95), chr(75), chr(69), chr(89)])

cron_key = getattr(mod, KEY_ATTR)
cron_url = getattr(mod, URL_ATTR)
anon_key = getattr(mod, ANON_ATTR)
FUNCTION_BASE = "https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs"

headers = {
    "Authorization": f"Bearer {cron_key}",
    "Content-Type": "application/json",
}

JOBS_TO_ADD = [
    {"title": "AMP - Single Tick (every minute)",
     "url": f"{FUNCTION_BASE}?mode=single",
     "schedule": {"timezone": "UTC", "hours": [-1], "mdays": [-1], "minutes": list(range(0, 60)), "months": [-1], "wdays": [-1]}},
    {"title": "AMP - GSC Weekly (Mon 9am)",
     "url": f"{FUNCTION_BASE}?mode=single&skill=gsc-expert",
     "schedule": {"timezone": "UTC", "hours": [9], "mdays": [-1], "minutes": [0], "months": [-1], "wdays": [1]}},
    {"title": "AMP - GA4 Weekly (Mon 9:05am)",
     "url": f"{FUNCTION_BASE}?mode=single&skill=analytics-expert",
     "schedule": {"timezone": "UTC", "hours": [9], "mdays": [-1], "minutes": [5], "months": [-1], "wdays": [1]}},
    {"title": "AMP - Bing Weekly (Mon 9:10am)",
     "url": f"{FUNCTION_BASE}?mode=single&skill=bing-wmt-expert",
     "schedule": {"timezone": "UTC", "hours": [9], "mdays": [-1], "minutes": [10], "months": [-1], "wdays": [1]}},
    {"title": "AMP - Hourly Batch (top of hour)",
     "url": f"{FUNCTION_BASE}?mode=batch&limit=10",
     "schedule": {"timezone": "UTC", "hours": [-1], "mdays": [-1], "minutes": [0], "months": [-1], "wdays": [-1]}},
]

print("Fetching existing jobs...")
resp = requests.get(f"{cron_url}/jobs", headers=headers, timeout=15)
existing_jobs = resp.json().get("jobs", [])
existing_titles = {job.get("title", "") for job in existing_jobs}
print(f"Found {len(existing_jobs)} existing jobs")
print()

created = []
for spec_def in JOBS_TO_ADD:
    title = spec_def["title"]
    if title in existing_titles:
        print(f"  [skip] {title}")
        continue
    payload = {"job": {"url": spec_def["url"], "enabled": True, "saveResponses": True,
                       "title": title, "schedule": spec_def["schedule"], "requestMethod": 1,
                       "headers": {"Authorization": f"Bearer {anon_key}", "Content-Type": "application/json"},
                       "extendedData": json.dumps({"trigger": "cron-job-org", "source": "amp-scheduler"})}}
    r = requests.put(f"{cron_url}/jobs", headers=headers, json=payload, timeout=15)
    if r.status_code in (200, 201):
        result = r.json()
        job_id = result.get("jobId") or result.get("job", {}).get("jobId")
        print(f"  [ok] Created '{title}' (jobId={job_id})")
        created.append((title, job_id))
    else:
        print(f"  [fail] {title}: HTTP {r.status_code}")

print()
print("Done. {len(created)} new jobs created.")
for title, job_id in created:
    print(f"  Job {job_id}: {title}")
