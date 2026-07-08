# Cron-Job.org Integration for AMP
# ================================
# This script creates a cron job that triggers the Supabase Edge Function every 5 minutes.
#
# API Documentation: https://docs.cron-job.org/rest-api.html
# Your API Key: WJnmdRwO6iHDH7NIlyYadsQzniVxFctEDLKVZEtExoE=

import requests
import json

# Configuration
CRON_API_KEY = "WJnmdRwO6iHDH7NIlyYadsQzniVxFctEDLKVZEtExoE="
CRON_API_URL = "https://api.cron-job.org"

# Supabase Edge Function endpoint
SUPABASE_FUNCTION_URL = "https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MzkwNDQsImV4cCI6MjA5ODQxNTA0NH0.czorJe8WQ2mLliNQqHraU2E3Tqor7lE0hYaksLRPwmU"

headers = {
    "Authorization": f"Bearer {CRON_API_KEY}",
    "Content-Type": "application/json"
}

def list_jobs():
    """List all existing cron jobs."""
    resp = requests.get(f"{CRON_API_URL}/jobs", headers=headers)
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
    return resp.json()

def create_amp_job():
    """Create the AMP job polling cron job."""
    payload = {
        "job": {
            "url": SUPABASE_FUNCTION_URL,
            "enabled": True,
            "saveResponses": True,
            "schedule": {
                "timezone": "UTC",
                "hours": [-1],  # Every hour
                "mdays": [-1],  # Every day
                "minutes": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],  # Every 5 minutes
                "months": [-1],  # Every month
                "wdays": [-1],  # Every weekday
            },
            "requestMethod": 1,  # POST
            "headers": {
                "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                "Content-Type": "application/json"
            },
            "extendedData": json.dumps({"trigger": "cron-job-org", "source": "amp-scheduler"})
        }
    }
    
    resp = requests.put(f"{CRON_API_URL}/jobs", headers=headers, json=payload)
    print(f"Create job status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
    return resp.json()

def delete_job(job_id):
    """Delete a cron job by ID."""
    resp = requests.delete(f"{CRON_API_URL}/jobs/{job_id}", headers=headers)
    print(f"Delete job status: {resp.status_code}")
    return resp.status_code == 200

def get_job_history(job_id):
    """Get execution history for a job."""
    resp = requests.get(f"{CRON_API_URL}/jobs/{job_id}/history", headers=headers)
    print(f"History status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
    return resp.json()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python cron-job-setup.py <command>")
        print("Commands:")
        print("  list     - List all cron jobs")
        print("  create   - Create the AMP job polling cron job")
        print("  delete <id> - Delete a cron job")
        print("  history <id> - Get job execution history")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_jobs()
    elif command == "create":
        create_amp_job()
    elif command == "delete" and len(sys.argv) > 2:
        delete_job(sys.argv[2])
    elif command == "history" and len(sys.argv) > 2:
        get_job_history(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
