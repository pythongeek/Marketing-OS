# Pytest configuration for AMP test suite
import pytest
import sys
from pathlib import Path

# Add infrastructure to path so tests can import scripts
INFRA = Path(__file__).parent.parent / "infrastructure"
if str(INFRA) not in sys.path:
    sys.path.insert(0, str(INFRA))
