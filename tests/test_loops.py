from sloperator.runner import run_source


def test_ralph_with_false_condition_prints_nothing():
    source = """ralph ❌ {
    hallucinate(“never”)✨
}"""
    result = run_source(source)
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
