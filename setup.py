"""
AgenticMarketingPro — Setup Script
==================================
Installs dependencies, checks environment, and runs initial health check.

Usage:
    python setup.py
    python setup.py --install    # Install requirements
    python setup.py --test       # Run health check after install
"""

import argparse
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Ensure Python 3.9+."""
    if sys.version_info < (3, 9):
        print("ERROR: Python 3.9+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def install_requirements():
    """Install Python packages."""
    req_file = Path(__file__).parent / "infrastructure" / "requirements.txt"
    if not req_file.exists():
        print(f"ERROR: {req_file} not found")
        return False
    
    print(f"Installing dependencies from {req_file}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: pip install failed:\n{result.stderr}")
        return False
    print("✅ Dependencies installed")
    return True


def check_env():
    """Check for required environment variables."""
    from infrastructure.config import Config
    
    deps = Config.check_deps()
    print("\nEnvironment configuration:")
    
    critical = ["openai", "chroma"]
    optional = ["ahrefs", "semrush", "gsc", "ga4", "bing"]
    
    for key in critical:
        status = "✅" if deps[key] else "❌"
        print(f"  {status} {key}")
    
    for key in optional:
        status = "✅" if deps[key] else "⚠️"
        print(f"  {status} {key} (optional)")
    
    return all(deps[k] for k in critical)


def run_health_check():
    """Run the health check script."""
    health_script = Path(__file__).parent / "infrastructure" / "scripts" / "health_check.py"
    result = subprocess.run(
        [sys.executable, str(health_script)],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"Health check exit code: {result.returncode}")
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="AgenticMarketingPro Setup")
    parser.add_argument("--install", "-i", action="store_true", help="Install requirements")
    parser.add_argument("--test", "-t", action="store_true", help="Run health check")
    args = parser.parse_args()

    print("=" * 60)
    print("AgenticMarketingPro — Setup")
    print("=" * 60)

    # Check Python version
    if not check_python_version():
        return 1

    # Install requirements
    if args.install:
        if not install_requirements():
            return 1
    else:
        print("\nTip: Run with --install to install dependencies")

    # Check environment
    try:
        import infrastructure.config
        env_ok = check_env()
    except ImportError:
        print("\n⚠️  Cannot check environment — run with --install first")
        env_ok = False

    # Run health check
    if args.test:
        print("\nRunning health check...")
        run_health_check()

    print("\n" + "=" * 60)
    print("Setup complete")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Create .env file with your API keys")
    print("  2. Run: python setup.py --install --test")
    print("  3. Run: python infrastructure/scripts/ingest_vault.py")
    print("  4. Run: python infrastructure/scripts/health_check.py --verbose")

    return 0


if __name__ == "__main__":
    sys.exit(main())
