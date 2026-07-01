"""Pytest configuration for the Deadline Cloud library tests.

The library modules import each other as a top-level ``publish`` package (e.g.
``from publish.utils import ...``), mirroring how the engine adds the library
directory to ``sys.path`` at load time. Replicate that here so the tests can
import the modules directly.
"""

from __future__ import annotations

import sys
from pathlib import Path

_LIBRARY_DIR = Path(__file__).resolve().parent.parent / "griptape_nodes_library_deadline_cloud"
if str(_LIBRARY_DIR) not in sys.path:
    sys.path.insert(0, str(_LIBRARY_DIR))
