import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


@pytest.mark.parametrize("ch", ["@", "#", "$", "%", "^", "~", "?", "`", "\\"])
def test_unhandled_character_reports_generic_unexpected_character_error(ch: str):
    with pytest.raises(LexicalError) as info:
        tokenize(f"a {ch} b")
    assert info.value.line == 1
    assert info.value.message == f"unexpected character '{ch}'"
    assert str(info.value) == (
        f"SlopLang lexical error at line 1: unexpected character '{ch}'"
    )


def test_unhandled_character_reports_the_line_it_occurs_on():
    with pytest.raises(LexicalError) as info:
        tokenize("slop x = ✅\n✅ ✨\n@")
    assert info.value.line == 3
    assert info.value.message == "unexpected character '@'"


def test_unterminated_string_reports_the_line_it_occurs_on():
    with pytest.raises(LexicalError) as info:
        tokenize("slop x = ✅\n“abc")
    assert info.value.line == 2
    assert info.value.message == "unterminated string"


def test_unknown_escape_reports_the_line_it_occurs_on():
    with pytest.raises(LexicalError) as info:
        tokenize("slop x = ✅\n“a\\q”")
    assert info.value.line == 2
    assert info.value.message == "unknown escape sequence '\\q'"
