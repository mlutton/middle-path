"""Boundary and purity of this subcomponent."""

from pathlib import Path

from mp_checks import boundary, check_tests_pure, pure

ROOT = Path(__file__).resolve().parents[1]


def test_slice_boundary():
    boundary(ROOT)


def test_slice_pure():
    pure(ROOT)


def test_slice_tests_pure():
    check_tests_pure(ROOT)
