"""the public failure type future adapters inherit."""

import mp_ports
import pytest
from mp_ports import AgentsRefused, ForgeRefused, RecordsRefused


def test_adapter_error_carries_reason():
    error = mp_ports.AdapterError("synthetic-adapter-failure")
    assert error.reason == "synthetic-adapter-failure"
    assert str(error) == "synthetic-adapter-failure"
    print("AdapterError carries its supplied reason")


@pytest.mark.parametrize("error, reason", [
    (AgentsRefused(), "packet-unknown"),
    (ForgeRefused("issue-unknown"), "issue-unknown"),
    (ForgeRefused("pr-unknown"), "pr-unknown"),
    (ForgeRefused("head-moved"), "head-moved"),
    (ForgeRefused("already-merged"), "already-merged"),
    (ForgeRefused("verdict-refused"), "verdict-refused"),
    (RecordsRefused("record-duplicate"), "record-duplicate"),
    (RecordsRefused("record-unknown"), "record-unknown"),
    (RecordsRefused("version-stale"), "version-stale"),
    (RecordsRefused("record-closed"), "record-closed"),
])
def test_public_adapter_error_and_unchanged_reason(error, reason):
    assert "AdapterError" in mp_ports.__all__
    assert issubclass(mp_ports.AdapterError, Exception)
    assert issubclass(type(error), mp_ports.AdapterError)
    assert isinstance(error, mp_ports.AdapterError)
    assert error.reason == reason
    print(f"{type(error).__name__} is AdapterError; reason={reason}")
