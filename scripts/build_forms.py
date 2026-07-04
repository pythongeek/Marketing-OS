"""
AgenticMarketingPro — Form Build Script
========================================
Generates all HTML forms from form_engine.py + form_presets.py
into web/public/forms/. Run this before deploy or in CI.

Usage:
    python scripts/build_forms.py
    python scripts/build_forms.py --check   # exit 1 if any form is stale
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from infrastructure.ui.form_engine import FormEngine
from infrastructure.ui.form_presets import FormPresets

logger = logging.getLogger("amp.build_forms")

OUTPUT_DIR = Path("web/public/forms")


def build_all(check: bool = False) -> int:
    """Generate all forms. Returns number of forms written."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = FormEngine(forms_dir=OUTPUT_DIR)
    presets = FormPresets(engine)

    if check:
        # Check mode: generate to temp dir and compare
        import tempfile
        all_ok = True
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            tmp_engine = FormEngine(forms_dir=tmp_path)
            tmp_presets = FormPresets(tmp_engine)
            tmp_presets.generate_all()
            # Core forms too
            tmp_engine.create_client_onboarding_form()
            tmp_engine.create_api_credentials_form()
            tmp_engine.create_wordpress_config_form()
            tmp_engine.create_content_brief_form()

            for f in tmp_path.glob("*.html"):
                existing = OUTPUT_DIR / f.name
                if not existing.exists():
                    logger.error(f"Missing form: {existing}")
                    all_ok = False
                elif existing.read_text() != f.read_text():
                    logger.error(f"Stale form: {existing}")
                    all_ok = False

            for f in OUTPUT_DIR.glob("*.html"):
                if not (tmp_path / f.name).exists():
                    logger.error(f"Extra file not in generator: {f}")
                    all_ok = False

        if all_ok:
            logger.info("All forms are up to date.")
            return 0
        else:
            logger.error("Form mismatch. Run: python scripts/build_forms.py")
            return 1

    # Build mode
    paths = presets.generate_all()
    paths.append(engine.create_client_onboarding_form())
    paths.append(engine.create_api_credentials_form())
    paths.append(engine.create_wordpress_config_form())
    paths.append(engine.create_content_brief_form())

    logger.info(f"Generated {len(paths)} forms in {OUTPUT_DIR}")
    for p in sorted(paths):
        print(f"  {p}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Build AMP forms")
    parser.add_argument("--check", action="store_true", help="Check if forms are up to date (CI)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    sys.exit(build_all(check=args.check))


if __name__ == "__main__":
    main()
