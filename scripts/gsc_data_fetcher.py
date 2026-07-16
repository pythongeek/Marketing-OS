#!/usr/bin/env python3
"""
GSC Data Fetcher - Uses Service Account to pull Search Console data
"""
import json
import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
SITE_URL = 'https://agenticmarketingpro.com'
CREDENTIALS_FILE = 'pageforge-credentials.json'

def get_gsc_service():
    """Initialize GSC service with service account"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=SCOPES
        )
        service = build('searchconsole', 'v1', credentials=credentials)
        return service
    except Exception as e:
        print(f"Error initializing GSC service: {e}")
        return None

def get_search_queries(service, days=28):
    """Get top search queries"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    request = {
        'startDate': str(start_date),
        'endDate': str(end_date),
        'dimensions': ['query'],
        'rowLimit': 1000
    }
    
    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request
    ).execute()
    
    return response.get('rows', [])

def get_page_performance(service, days=28):
    """Get page-level performance"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    request = {
        'startDate': str(start_date),
        'endDate': str(end_date),
        'dimensions': ['page'],
        'rowLimit': 1000
    }
    
    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request
    ).execute()
    
    return response.get('rows', [])

def analyze_quick_wins(queries):
    """Find quick win opportunities (positions 4-15)"""
    quick_wins = []
    for row in queries:
        pos = row.get('keys', [''])[0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0) * 100
        
        # Look for position 4-15 with good impressions
        if isinstance(pos, (int, float)) and 4 <= pos <= 15 and impressions > 100:
            quick_wins.append({
                'query': row['keys'][0],
                'position': pos,
                'clicks': clicks,
                'impressions': impressions,
                'ctr': round(ctr, 2)
            })
    
    return sorted(quick_wins, key=lambda x: x['impressions'], reverse=True)

def analyze_content_gaps(queries, existing_titles):
    """Find queries without dedicated content"""
    existing_lower = [t.lower() for t in existing_titles]
    gaps = []
    
    for row in queries:
        query = row.get('keys', [''])[0].lower()
        pos = row.get('keys', [''])[0]
        
        # Check if query topic is covered
        covered = any(topic in query for topic in existing_lower)
        
        if not covered and isinstance(pos, (int, float)) and pos > 10:
            gaps.append({
                'query': row['keys'][0],
                'position': pos,
                'impressions': row.get('impressions', 0),
                'clicks': row.get('clicks', 0)
            })
    
    return sorted(gaps, key=lambda x: x['impressions'], reverse=True)[:20]

def main():
    print("=== GSC Data Fetcher ===")
    print(f"Site: {SITE_URL}")
    print()
    
    # Check credentials
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: Credentials file not found: {CREDENTIALS_FILE}")
        print("Please ensure pageforge-credentials.json is in the project root")
        return
    
    # Initialize service
    service = get_gsc_service()
    if not service:
        print("Failed to initialize GSC service")
        return
    
    # Verify site ownership
    try:
        service.sites().list().execute()
        print("✓ Connected to Google Search Console")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the service account email has been added to GSC")
        return
    
    # Get data
    print("\nFetching query data...")
    queries = get_search_queries(service, days=28)
    print(f"✓ Retrieved {len(queries)} queries")
    
    print("\nFetching page data...")
    pages = get_page_performance(service, days=28)
    print(f"✓ Retrieved {len(pages)} pages")
    
    # Analyze
    print("\n=== ANALYSIS RESULTS ===")
    
    # Quick wins
    quick_wins = analyze_quick_wins(queries)
    print(f"\n🚀 QUICK WINS (Position 4-15): {len(quick_wins)}")
    for qw in quick_wins[:10]:
        print(f"  - '{qw['query']}' | Pos: {qw['position']} | Impressions: {qw['impressions']}")
    
    # Save results
    results = {
        'generated': datetime.now().isoformat(),
        'site': SITE_URL,
        'period': 'last_28_days',
        'total_queries': len(queries),
        'total_pages': len(pages),
        'quick_wins': quick_wins[:20]
    }
    
    with open('gsc_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to gsc_analysis_results.json")

if __name__ == '__main__':
    main()
