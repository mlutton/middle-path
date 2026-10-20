"""Adapter-owned snapshot excludes diagnostic calls, includes all domain state."""

import pytest
from mp_ports import EffectLog, MemoryForge, contract_forge_cases

CASES = contract_forge_cases()


def factory():
    forge = MemoryForge(EffectLog())
    return forge, lambda: (dict(forge.issues), dict(forge.prs), tuple(forge.verdicts), tuple(forge.merges))


@pytest.mark.parametrize("case", [case for _, case in CASES], ids=[name for name, _ in CASES])
def test_contract_forge(case):
    forge, snapshot = factory()
    case(forge, snapshot)
    print(f"Forge executed case; total={len(CASES)}")
