"""The component target runs its independently runnable subpackages."""

import os
from pathlib import Path
import subprocess


def test_middle_path_component_suite():
    runner = Path(__file__).resolve().parents[1] / "run-suite"
    result = subprocess.run(["bash", str(runner)], cwd=runner.parent,
                            env=os.environ.copy(), capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
