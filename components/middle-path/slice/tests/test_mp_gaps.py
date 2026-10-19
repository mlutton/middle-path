"""post-open failures through the public slice and fake ports."""

import mp_ports
import pytest
from mp_examples import RAW
from mp_ports import (
    BuildResult,
    EffectLog,
    ForgeRefused,
    MemoryAgents,
    MemoryForge,
    MemoryRecords,
    RecordsRefused,
    Refusal,
    SuiteReport,
    Verdict,
)
from mp_slice import run
from mp_slice.wiring import layers


def state(forge_type=MemoryForge, records_type=MemoryRecords):
    log = EffectLog()
    return (log, records_type(log), forge_type(log),
            MemoryAgents(log, {"S-001": BuildResult("head-1", SuiteReport("head-1", 0))},
                         {"S-001": Verdict("head-1")}))


def drive(items):
    _, records, forge, agents = items
    return run(RAW, "base-0", layers=layers(), records=records, forge=forge,
               agents=agents, clock=lambda: "tick-1")


def calls(items, port, operation):
    return [entry.arguments for entry in items[0].entries
            if (entry.port, entry.operation) == (port, operation)]


def abandoned(items, trace, detail):
    assert trace.outcome == Refusal(detail)
    history = items[1].history("S-001")
    assert history[-1].step == "record-closed"
    assert dict(history[-1].payload) == {"reason": "abandoned", "detail": detail}
    assert len(calls(items, "records", "open")) == 1
    assert len(calls(items, "records", "close")) == 1
    assert not calls(items, "forge", "merge")
    assert items[2].merges == []


@pytest.mark.parametrize("operation", ["create_issue", "create_pr"])
@pytest.mark.parametrize("error_type", [ForgeRefused, RecordsRefused],
                         ids=["forge-refusal", "other-adapter-refusal"])
def test_creation_failure_closes(operation, error_type, monkeypatch):
    items = state()
    error = error_type("issue-unknown" if error_type is ForgeRefused else "version-stale")

    def refuse(*args):
        items[0].add("forge", operation, *args)
        raise error

    monkeypatch.setattr(items[2], operation, refuse)
    trace = drive(items)
    detail = "issue-create-failed" if operation == "create_issue" else "pr-create-failed"
    abandoned(items, trace, detail)
    expected = ("story-received", "packet-ready", "record-opened")
    if operation == "create_pr":
        expected += ("issue-created", "build-requested", "build-returned")
    assert trace.steps == (*expected, "record-closed")
    assert len(calls(items, "agents", "build")) == (operation == "create_pr")
    assert not calls(items, "agents", "review")
    assert not calls(items, "forge", "post_verdict")
    assert items[2].prs == {}
    if operation == "create_issue":
        assert items[2].issues == {}
    print(f"{operation}: "
          f"{detail}; closes=1; builds={len(calls(items, 'agents', 'build'))}; "
          "reviews=0; merges=0")


class CloseRefusingRecords(MemoryRecords):
    def close(self, record_id, reason, detail, expected_version):
        self.log.add("records", "close", record_id, reason, detail, expected_version)
        raise RecordsRefused("version-stale")


@pytest.mark.parametrize("failure", [None, "create_issue", "create_pr", "build", "review"])
def test_close_refusal_returns_named_trace(failure, monkeypatch):
    items = state(records_type=CloseRefusingRecords)
    if failure:
        target = items[3] if failure in {"build", "review"} else items[2]

        def refuse(*args):
            raise ForgeRefused("issue-unknown")

        monkeypatch.setattr(target, failure, refuse)
    trace = drive(items)
    assert trace.outcome == Refusal("close-refused")
    expected = ("story-received", "packet-ready", "record-opened")
    if failure != "create_issue":
        expected += ("issue-created", "build-requested")
    if failure not in {"create_issue", "build"}:
        expected += ("build-returned",)
    if failure not in {"create_issue", "build", "create_pr"}:
        expected += ("pr-created",)
    if failure is None:
        expected += ("verdict-posted", "suite-recorded", "merge-decided")
    assert trace.steps == expected
    history = items[1].history("S-001")
    assert all(event.step != "record-closed" for event in history)
    assert len(calls(items, "records", "open")) == 1
    assert len(calls(items, "records", "close")) == 1
    details = {"create_issue": "issue-create-failed", "create_pr": "pr-create-failed",
               "build": "build-failed", "review": "review-failed"}
    assert calls(items, "records", "close")[0][1:3] == (
        ("abandoned", details[failure]) if failure else ("done", "MERGE"))
    # A write still succeeds: the refused close did not mark the record closed.
    assert items[1].append("S-001", history[-1], len(history)) == len(history) + 1
    assert items[2].merges == ([] if failure else [(1, "head-1")])
    print(f"{failure=}: close-refused Trace; opens=1; close attempts=1; record remains writable")


@pytest.mark.parametrize("operation", ["build", "review"])
def test_adapter_error_has_existing_failure_reason(operation, monkeypatch):
    assert hasattr(mp_ports, "AdapterError"), "AdapterError must be public"

    class SyntheticAdapterError(mp_ports.AdapterError):
        pass

    items = state()

    def refuse(*args):
        items[0].add("agents", operation, *args)
        raise SyntheticAdapterError("synthetic-adapter-failure")

    monkeypatch.setattr(items[3], operation, refuse)
    trace = drive(items)
    abandoned(items, trace, f"{operation}-failed")
    assert trace.steps[-1] == "record-closed"
    if operation == "build":
        assert "build-returned" not in trace.steps
        assert not calls(items, "agents", "review")
    print(f"{operation}: AdapterError subclass -> {operation}-failed; closes=1")


@pytest.mark.parametrize("port, operation", [
    ("agents", "build"), ("agents", "review"),
    ("forge", "create_issue"), ("forge", "create_pr"), ("forge", "pr_head"),
    ("forge", "post_verdict"), ("forge", "merge"), ("records", "append"),
])
@pytest.mark.parametrize("records_type", [MemoryRecords, CloseRefusingRecords])
def test_non_adapter_error_propagates(port, operation, records_type, monkeypatch):
    items = state(records_type=records_type)
    error = RuntimeError("synthetic programming failure")

    def fail(*args, **kwargs):
        raise error

    target = {"records": items[1], "forge": items[2], "agents": items[3]}[port]
    monkeypatch.setattr(target, operation, fail)
    with pytest.raises(RuntimeError) as caught:
        drive(items)
    assert caught.value is error
    assert not calls(items, "forge", "merge")
    assert len(calls(items, "records", "open")) == 1
    assert len(calls(items, "records", "close")) == 1
    assert calls(items, "records", "close")[0][1:3] == ("abandoned", "unexpected-error")
    history = items[1].history("S-001")
    assert (history[-1].step == "record-closed") == (records_type is MemoryRecords)
    print(f"{port}.{operation}: original RuntimeError propagated; close attempts=1; "
          f"close refused={records_type is CloseRefusingRecords}")


def test_unexpected_close_error_is_not_retried(monkeypatch):
    items = state()
    error = RuntimeError("synthetic close bug")

    def fail(*args):
        items[0].add("records", "close", *args)
        raise error

    monkeypatch.setattr(items[1], "close", fail)
    with pytest.raises(RuntimeError) as caught:
        drive(items)
    assert caught.value is error
    assert len(calls(items, "records", "close")) == 1
    assert all(event.step != "record-closed" for event in items[1].history("S-001"))
    print("unexpected close bug propagates; close attempts=1; no retry")
