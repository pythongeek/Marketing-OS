"""
AgenticMarketingPro — Supabase Migration Runner
================================================
Applies SQL migration files to Supabase without using the Supabase CLI.

This works around the 403 access error that occurs when the CLI is
authenticated to a different account than the one owning the project.

Requires:
- SUPABASE_URL (e.g. https://xxxxx.supabase.co)
- SUPABASE_SERVICE_ROLE_KEY (the service_role JWT, not the anon key)

Usage:
    python scripts/apply_migrations.py
    python scripts/apply_migrations.py --dry-run   # preview without executing
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env
_env_paths = [
    Path(__file__).parent.parent / ".env",
    Path(__file__).parent / ".env",
]
for p in _env_paths:
    if p.exists():
        load_dotenv(dotenv_path=p)
        break

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("[ERROR] SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    sys.exit(1)

MIGRATIONS_DIR = Path(__file__).parent.parent / "supabase" / "migrations"


def split_sql_statements(sql_content: str) -> list:
    """Split a SQL file into individual statements.

    Handles:
    - DO $$ ... $$ blocks (PostgreSQL anonymous code blocks)
    - Dollar-quoted strings (e.g. $tag$ ... $tag$)
    - Line comments (-- ...)
    - String literals ('...' and "...")
    """
    statements = []
    current = []
    in_dollar_quote = False
    dollar_tag = None
    in_single_quote = False
    in_double_quote = False
    in_line_comment = False

    i = 0
    lines = sql_content.split('\n')

    for line in lines:
        if in_line_comment:
            # Skip line comments
            in_line_comment = False
            continue

        stripped = line.strip()
        # Track line comments
        if stripped.startswith('--') and not in_dollar_quote and not in_single_quote and not in_double_quote:
            continue

        # Check for dollar-quote start/end
        # Look for $$ or $tag$ patterns
        j = 0
        while j < len(line):
            ch = line[j]
            if not in_dollar_quote and not in_single_quote and not in_double_quote:
                if ch == '$':
                    # Check if this starts a dollar-quote
                    end = line.find('$', j + 1)
                    if end != -1:
                        tag_candidate = line[j:end+1]
                        if tag_candidate == '$$' or (tag_candidate.startswith('$') and tag_candidate[1:-1].isalnum() and tag_candidate.endswith('$')):
                            if not in_dollar_quote:
                                in_dollar_quote = True
                                dollar_tag = tag_candidate
                                j = end + 1
                                continue
                elif ch == "'" and not in_double_quote:
                    in_single_quote = not in_single_quote
                elif ch == '"' and not in_single_quote:
                    in_double_quote = not in_double_quote
            elif in_dollar_quote:
                if line[j:].startswith(dollar_tag):
                    in_dollar_quote = False
                    dollar_tag = None
                    j += len(dollar_tag)
                    continue
            j += 1

        current.append(line)

        # Statement ends at semicolon OUTSIDE quotes
        if not in_dollar_quote and not in_single_quote and not in_double_quote:
            if line.rstrip().endswith(';'):
                stmt = '\n'.join(current).strip()
                if stmt:
                    statements.append(stmt)
                current = []

    # Catch any trailing statement
    if current:
        stmt = '\n'.join(current).strip()
        if stmt:
            statements.append(stmt)

    return statements


def apply_migration(sql_content: str, filename: str) -> bool:
    """Apply a single SQL migration via PostgREST rpc('exec_sql')."""
    # Use Supabase's pg_query or similar; but we need direct DB access.
    # PostgREST doesn't have an "exec arbitrary SQL" endpoint.
    # So we use the Supabase DB connection string instead.

    # Get the database connection string from Supabase
    # The format is: postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres

    # We need the DB password. Check env.
    db_password = os.getenv("SUPABASE_DB_PASSWORD")

    if not db_password:
        print(f"[SKIP] {filename}: SUPABASE_DB_PASSWORD not set")
        print("       Get it from: Supabase Dashboard → Settings → Database → Connection string")
        return False

    # Try using psycopg2 if available
    try:
        import psycopg2
    except ImportError:
        print(f"[SKIP] {filename}: psycopg2 not installed")
        print("       Run: pip install psycopg2-binary")
        return False

    # Extract project ref from SUPABASE_URL
    project_ref = SUPABASE_URL.replace("https://", "").replace(".supabase.co", "")

    conn_str = f"postgresql://postgres.{project_ref}:{db_password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True
        cur = conn.cursor()

        # Split into statements
        statements = split_sql_statements(sql_content)

        for stmt in statements:
            try:
                cur.execute(stmt)
            except Exception as e:
                print(f"[ERROR] {filename}: {e}")
                print(f"        Statement: {stmt[:200]}...")
                conn.close()
                return False

        conn.close()
        print(f"[OK] {filename}: applied {len(statements)} statement(s)")
        return True

    except Exception as e:
        print(f"[ERROR] {filename}: Connection failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Apply Supabase migrations via direct DB connection")
    parser.add_argument("--dry-run", action="store_true", help="Preview migrations without applying")
    parser.add_argument("--files", nargs="+", help="Specific migration files to apply")
    args = parser.parse_args()

    if not MIGRATIONS_DIR.exists():
        print(f"[ERROR] Migrations directory not found: {MIGRATIONS_DIR}")
        sys.exit(1)

    # Discover migration files
    if args.files:
        files = [MIGRATIONS_DIR / f for f in args.files]
    else:
        # Apply all migrations in order, but only the un-applied ones
        files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Applying {len(files)} migration(s) to {SUPABASE_URL}")
    print("=" * 70)

    success_count = 0
    fail_count = 0

    for filepath in files:
        if not filepath.exists():
            print(f"[SKIP] {filepath.name}: file not found")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if args.dry_run:
            statements = split_sql_statements(content)
            print(f"[DRY] {filepath.name}: {len(statements)} statement(s) would execute")
            success_count += 1
        else:
            if apply_migration(content, filepath.name):
                success_count += 1
            else:
                fail_count += 1

    print("=" * 70)
    print(f"Result: {success_count} succeeded, {fail_count} failed")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()