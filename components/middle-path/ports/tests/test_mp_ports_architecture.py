"""Boundary and purity of this subcomponent."""

from pathlib import Path

from mp_checks import boundary, check_tests_pure, pure

ROOT = Path(__file__).resolve().parents[1]


def test_ports_boundary():
    boundary(ROOT)


def test_ports_pure():
    pure(ROOT)


def test_ports_tests_pure():
    check_tests_pure(ROOT)
