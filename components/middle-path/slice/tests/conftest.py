"""Make this subcomponent and the published ports available."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "ports"))
sys.path.insert(0, str(ROOT.parent / "ports" / "tests"))
for name in ("story", "packet", "review", "merge"):
    sys.path.insert(0, str(ROOT.parent / name))
