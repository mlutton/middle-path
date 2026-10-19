"""Run reusable agent contracts through a fresh configurable factory."""

import pytest
from mp_ports import MemoryAgents, contract_agents_cases

CASES = contract_agents_cases()


@pytest.mark.parametrize("case", [case for _, case in CASES], ids=[name for name, _ in CASES])
def test_contract_agents(case):
    case(MemoryAgents)
    print(f"Agents executed case; total={len(CASES)}")
