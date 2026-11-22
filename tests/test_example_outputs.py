"""Exact stdout for each example program."""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

CASES = [
    # (example stem, exact stdout)
    ("equality", "✅\n❌\n❌\n"),
    ("short-circuit", "❌\n✅\n"),
]


@pytest.mark.parametrize(("stem", "expected"), CASES, ids=[case[0] for case in CASES])
def test_example_output(stem: str, expected: str):
    result = run_source((EXAMPLES / f"{stem}.slop").read_text(encoding="utf-8"))
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected
