"""Aggregate wrapper against disposable runners; only test subprocess site."""

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NAMES = ("ports", "story", "packet", "review", "merge", "slice")


@pytest.mark.parametrize("codes, expected", [
    ((0, 7, 3, 0, 0, 0), 7), ((0, 0, 0, 0, 0, 0), 0), ((0, 0, 0, 0, 0, 9), 9),
])
def test_wrapper_all_run_first_failure(tmp_path, codes, expected):
    shutil.copy2(ROOT / "run-suite", tmp_path / "run-suite")
    for name, code in zip(NAMES, codes, strict=True):
        directory = tmp_path / name
        directory.mkdir()
        runner = directory / "run-suite"
        runner.write_text(f"#!/bin/sh\nexit {code}\n")
        runner.chmod(0o755)
    result = subprocess.run([str(tmp_path / "run-suite")], cwd="/", capture_output=True, text=True, check=False)
    assert result.returncode == expected
    assert result.stdout.splitlines() == [
        *(f"SUBSUITE {name} rc={code}" for name, code in zip(NAMES, codes, strict=True)),
        f"middle-path rc={expected}",
    ]
    print(f"rc={result.returncode}\n{result.stdout}")


def test_wrapper_missing_runner_continues(tmp_path):
    shutil.copy2(ROOT / "run-suite", tmp_path / "run-suite")
    for name in NAMES[1:]:
        directory = tmp_path / name
        directory.mkdir()
        runner = directory / "run-suite"
        runner.write_text("#!/bin/sh\nexit 0\n")
        runner.chmod(0o755)
    result = subprocess.run([str(tmp_path / "run-suite")], cwd="/", capture_output=True, text=True, check=False)
    assert result.returncode != 0
    lines = result.stdout.splitlines()
    assert len(lines) == 7
    assert lines[0] == f"SUBSUITE ports rc={result.returncode}"
    assert lines[1:6] == [f"SUBSUITE {name} rc=0" for name in NAMES[1:]]
    assert lines[-1] == f"middle-path rc={result.returncode}"
    print(f"missing runner rc={result.returncode}\n{result.stdout}")
