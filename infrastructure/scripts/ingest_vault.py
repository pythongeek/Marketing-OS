"""
AgenticMarketingPro — Vault Ingestion Script
============================================
One-shot or scheduled script to ingest all vault markdown into ChromaDB.

Usage:
    python scripts/ingest_vault.py [--force] [--verbose]

Schedules: Run daily at 3 AM via cron to keep embeddings fresh.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.pipeline import VaultRAG


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    parser = argparse.ArgumentParser(description="Ingest vault markdown into ChromaDB")
    parser.add_argument("--force", action="store_true", help="Force re-ingestion (clear existing)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger("amp.ingest")

    logger.info("=" * 60)
    logger.info("AgenticMarketingPro — Vault Ingestion")
    logger.info("=" * 60)

    try:
        rag = VaultRAG()
        stats = rag.ingest_vault(force=args.force)
        
        logger.info("-" * 60)
        logger.info("Ingestion Results:")
        logger.info(f"  Files processed:  {stats['files_processed']}")
        logger.info(f"  Chunks created:   {stats['chunks_created']}")
        logger.info(f"  Errors:           {stats['errors']}")
        logger.info("-" * 60)

        # Print final stats
        final_stats = rag.stats()
        logger.info(f"Total chunks in collection: {final_stats['total_chunks']}")
        logger.info("Source type distribution:")
        for st, count in final_stats.get("source_type_distribution", {}).items():
            logger.info(f"  {st}: {count}")

        if stats["errors"] > 0:
            logger.warning("Some files failed to ingest. Check logs above.")
            return 1
        return 0

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
