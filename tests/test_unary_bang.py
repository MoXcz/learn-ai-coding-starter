import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("!✅", "❌"),
        ("!❌", "✅"),
        ("!!✅", "✅"),
        ("!!❌", "❌"),
        ("!(1 == 1)", "❌"),
        ("!✅ == ❌", "✅"),
    ],
)
def test_unary_bang_flips_booleans(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")
    assert result.stderr == "", result.stderr
    assert result.stdout == f"{expected}\n"


@pytest.mark.parametrize("value", ["1", "“hi”", "0"])
def test_unary_bang_rejects_non_booleans(value: str):
    result = run_source(f"hallucinate(!{value})✨")
    assert result.exit_code == 1
    type_name = "number" if value != "“hi”" else "string"
    assert result.stderr.rstrip("\n") == (
        f"SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got {type_name}"
    )
