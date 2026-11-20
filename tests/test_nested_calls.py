from sloperator.runner import run_source


def test_call_used_directly_as_an_argument():
    source = """clanker double(x) {
    ship x * 2✨
}

clanker add(left, right) {
    ship left + right✨
}

hallucinate(add(double(3), double(4)))✨"""
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "14\n"
