"""It uses in-memory stand-ins for the work record, the code host and the build and review agents: there is no GitHub, no live model and no network.

Reviewer identity and roles are supplied by the caller; a checked registry is a later stage.
"""

import ast
from pathlib import Path
from typing import get_args

import pytest
from mp_ports import (
    BuildResult, Decision, EffectLog, MemoryAgents, MemoryForge, MemoryRecords,
    Reason, Refusal, Role, SuiteReport, Verdict,
)
from mp_slice import run
from mp_slice.wiring import layers

TRACE = ("story-received", "packet-ready", "record-opened", "issue-created",
         "build-requested", "build-returned", "pr-created", "verdict-posted",
         "suite-recorded", "merge-decided", "record-closed")
NOT_STORY_STAGE = (
    "packet-invalid", "verdict-missing", "verdict-surplus", "verdict-not-merge",
    "stale-head", "suite-missing", "suite-not-green", "suite-stale-head", "open-blocker",
    "record-duplicate", "record-unknown", "version-stale", "record-closed",
    "build-failed", "review-failed", "verdict-post-refused", "merge-refused",
    "issue-create-failed", "pr-create-failed", "close-refused", "unexpected-error",
    "invalid-head",
)


def test_story_1_merged_run():
    """As an outsider, I want to see one story reach a merge decision, so that I know what the walking skeleton does today.

    GIVEN a valid story and in-memory ports
    WHEN the real layers run with a green build and MERGE verdict
    THEN the trace matches the suite and the reviewed head is merged once
    """
    h1 = "a" * 40
    story = {"id": "S-001", "title": "Example change", "why": "Show the path",
             "acceptance": ["One observable result"], "risk_tier": "medium"}
    log = EffectLog()
    records = MemoryRecords(log)
    forge = MemoryForge(log)
    agents = MemoryAgents(log, {"S-001": BuildResult(h1, SuiteReport(h1, 0))},
                          {"S-001": Verdict(Decision.MERGE, h1, "reviewer-example", Role.PRIMARY)})
    trace = run(story, "base-0", layers=layers(), records=records, forge=forge,
                agents=agents, clock=lambda: "tick-1")
    assert trace.outcome == "MERGE"
    assert trace.steps == TRACE
    assert forge.merges == [(1, h1)]

    suite_tree = ast.parse((Path(__file__).parent / "test_mp_slice.py").read_text())
    suite_trace = next((node.value for node in suite_tree.body
                       if isinstance(node, ast.Assign) and
                       any(isinstance(target, ast.Name) and target.id == "TRACE"
                           for target in node.targets)), None)
    assert suite_trace is not None, "TRACE not found in test_mp_slice.py"
    assert ast.literal_eval(suite_trace) == TRACE


def test_story_2_says_reviewer_is_caller_supplied():
    """As an outsider reading the example, I want to know who supplies the reviewer, so that I do not mistake the canned verdict for a live reviewer.

    GIVEN the example module docstring
    WHEN its lines are read
    THEN it states the caller-supplied limit and in-memory stand-ins
    """
    assert "Reviewer identity and roles are supplied by the caller; a checked registry is a later stage." in __doc__.splitlines()
    assert "It uses in-memory stand-ins for the work record, the code host and the build and review agents: there is no GitHub, no live model and no network." in __doc__.splitlines()


def test_story_3_uses_only_published_names():
    """As a maintainer, I want the example to use published names, so that it shows what an outsider can use.

    GIVEN the example source
    WHEN its test-helper imports, calls and function definitions are inspected
    THEN no test_ module, tests, mp_examples or mp_checks module and no importlib is imported, no function named setup or drive is defined or called, and none of the names __import__, importlib, exec and eval is used
    """
    tree = ast.parse(Path(__file__).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] != "importlib"
                assert all(not part.startswith("test_") and part not in {"tests", "mp_examples", "mp_checks"}
                           for part in alias.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0
            assert (node.module or "").split(".")[0] != "importlib"
            assert all(not part.startswith("test_") and part not in {"tests", "mp_examples", "mp_checks"}
                       for part in (node.module or "").split("."))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assert node.name not in {"setup", "drive"}
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in {"setup", "drive"}
            elif isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {"setup", "drive"}
        elif isinstance(node, (ast.Name, ast.Attribute)):
            assert (node.id if isinstance(node, ast.Name) else node.attr) not in {
                "__import__", "importlib", "exec", "eval",
            }


def test_story_4_refuses_in_the_skeletons_own_reason():
    """As a maintainer, I want bad stories refused without effects, so that closed-by-default is visible.

    GIVEN invalid stories and the published refusal vocabulary
    WHEN each story runs through the real layers
    THEN its first reason wins and no port records an effect
    """
    valid = {"id": "S-001", "title": "Example change", "why": "Show the path",
             "acceptance": ["One observable result"], "risk_tier": "medium"}
    cases = []
    for field in valid:
        missing = dict(valid)
        del missing[field]
        cases.append((missing, "base-0", f"missing-field:{field}"))
        cases.append(({**valid, field: [] if field == "acceptance" else ""},
                      "base-0", f"empty-field:{field}"))
        cases.append(({**valid, field: [" "] if field == "acceptance" else " "},
                      "base-0", f"empty-field:{field}"))
        cases.append(({**valid, field: 1}, "base-0", f"wrong-type:{field}"))
    cases.extend((
        ({**valid, "id": "S-1"}, "base-0", "bad-id"),
        ({**valid, "risk_tier": "light"}, "base-0", "tier-unsupported"),
        ({**valid, "risk_tier": "heavy"}, "base-0", "tier-unsupported"),
        ({**valid, "risk_tier": "bogus"}, "base-0", "wrong-type:risk_tier"),
        ([], "base-0", "wrong-type:raw"),
        ({**valid, "extra": 1}, "base-0", "wrong-type:raw"),
        (valid, "", "empty-field:base_sha"),
        (valid, 1, "wrong-type:base_sha"),
        ({**valid, "acceptance": "x"}, "base-0", "wrong-type:acceptance"),
        ({**valid, "why": None, "risk_tier": "bogus"}, "base-0", "wrong-type:why"),
        ({k: v for k, v in valid.items() if k != "why"} | {"risk_tier": "bogus"},
         "base-0", "missing-field:why"),
        ({k: v for k, v in valid.items() if k not in {"id", "title"}},
         "base-0", "missing-field:id"),
        ({k: v for k, v in valid.items() if k != "why"} | {"extra": 1},
         "base-0", "missing-field:why"),
        ({k: v for k, v in valid.items() if k != "why"} | {"id": "S-1"},
         "base-0", "bad-id"),
        ({**valid, "risk_tier": "heavy", "acceptance": []},
         "base-0", "empty-field:acceptance"),
        ({**valid, "risk_tier": "heavy", "extra": 1},
         "base-0", "tier-unsupported"),
        ({**valid, "why": " ", "risk_tier": "bogus"},
         "base-0", "empty-field:why"),
        ({**valid, "acceptance": ["x", " "]},
         "base-0", "empty-field:acceptance"),
        ({**valid, "acceptance": [1]}, "base-0", "wrong-type:acceptance"),
        ({**valid, "id": "s-001"}, "base-0", "bad-id"),
        ({**valid, "id": "S-0001"}, "base-0", "bad-id"),
        ({**valid, "id": "S-001 "}, "base-0", "bad-id"),
        ({**valid, "id": " S-001"}, "base-0", "bad-id"),
        ({}, "base-0", "missing-field:id"),
        (None, "base-0", "wrong-type:raw"),
        ("x", "base-0", "wrong-type:raw"),
        (1, "base-0", "wrong-type:raw"),
    ))
    table_reasons = {reason for _, _, reason in cases}
    members = {member for group in get_args(Reason) for member in get_args(group)}
    assert table_reasons.isdisjoint(NOT_STORY_STAGE)
    assert table_reasons | set(NOT_STORY_STAGE) == members
    for story, base, reason in cases:
        log = EffectLog()
        records = MemoryRecords(log)
        forge = MemoryForge(log)
        h1 = "a" * 40
        agents = MemoryAgents(log, {"S-001": BuildResult(h1, SuiteReport(h1, 0))},
                              {"S-001": Verdict(Decision.MERGE, h1, "reviewer-example", Role.PRIMARY)})
        trace = run(story, base, layers=layers(), records=records, forge=forge,
                    agents=agents, clock=lambda: "tick-1")
        assert trace.outcome == Refusal(reason)
        assert trace.steps == ("story-received",)
        assert log.entries == []
