from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal, Logical
from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_comparison_result_compares_equal_to_a_boolean():
    # `2 == ✅` first would be a runtime type error.
    assert run("hallucinate(1 < 2 == ✅)✨") == "✅\n"
    assert run("hallucinate(1 < 2 == ❌)✨") == "❌\n"


def test_comparison_binds_tighter_than_equality_in_the_ast():
    expr = only_expression("1 < 2 == ✅✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, Binary) and expr.left.operator.type is TokenType.LESS
    assert isinstance(expr.right, Literal) and expr.right.value is True


def test_comparison_operands_use_arithmetic_precedence():
    assert run("hallucinate(1 + 1 < 3 == ✅)✨") == "✅\n"
    assert run("hallucinate(2 * 2 >= 4 == ✅)✨") == "✅\n"
    assert run("hallucinate(2 * 2 < 4 == ✅)✨") == "❌\n"


def test_equality_binds_tighter_than_logic_and():
    expr = only_expression("1 < 2 == ✅ && 3 > 2 == ✅✨")
    assert isinstance(expr, Logical) and expr.operator.type is TokenType.AND
    assert isinstance(expr.left, Binary) and expr.left.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.right, Binary) and expr.right.operator.type is TokenType.EQUAL_EQUAL
    assert run("hallucinate(1 < 2 == ✅ && 3 > 2 == ✅)✨") == "✅\n"


def test_logic_and_binds_tighter_than_logic_or():
    assert run("hallucinate(❌ && ❌ || ✅)✨") == "✅\n"
