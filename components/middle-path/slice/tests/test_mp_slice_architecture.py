"""Boundary and purity of this subcomponent."""

import ast
from pathlib import Path

from mp_checks import boundary, check_tests_pure, pure

ROOT = Path(__file__).resolve().parents[1]


def test_slice_boundary():
    boundary(ROOT)


def test_slice_pure():
    pure(ROOT)


def test_slice_tests_pure():
    check_tests_pure(ROOT)


def test_recorded_steps_use_event_first_helper():
    tree = ast.parse((ROOT / "mp_slice" / "orchestrator.py").read_text())
    runner = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                  and node.name == "_Run")
    methods = {node.name: node for node in runner.body if isinstance(node, ast.FunctionDef)}
    assert "step" in methods and "note" in methods
    # This explicitly guards this source shape: event write, then Trace note.
    helper = methods["step"]
    assert len(helper.body) == 2
    first, second = [node.value for node in helper.body]
    assert isinstance(first, ast.Call) and isinstance(second, ast.Call)
    assert ast.unparse(first.func) == "self.append"
    assert ast.unparse(second.func) == "self.note"
    assert ast.unparse(first.args[0]) == ast.unparse(second.args[0]) == "name"
    assert [(kw.arg, ast.unparse(kw.value)) for kw in first.keywords] == [(None, "payload")]
    for name, method in methods.items():
        if name in {"step", "note"}:
            continue
        assert not any(isinstance(node, ast.Call) and
                       ast.unparse(node.func) == "self.steps.append" for node in ast.walk(method))
    print("event-first step helper; Trace writes confined to note")
