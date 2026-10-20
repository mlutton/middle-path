"""Run reusable cases through this adapter's factory."""

import pytest
from mp_ports import EffectLog, MemoryRecords, contract_records_cases

CASES = contract_records_cases()


@pytest.mark.parametrize("case", [case for _, case in CASES], ids=[name for name, _ in CASES])
def test_contract_records(case):
    case(MemoryRecords(EffectLog()))
    print(f"Records executed case; total={len(CASES)}")
