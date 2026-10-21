from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_multiplication_binds_tighter_than_addition():
    # '*' first would give 20, '+' first would give 14
    assert run("hallucinate(2 + 3 * 4)✨") == "14\n"


def test_multiplication_binds_tighter_than_subtraction():
    # '*' first would give 28, '-' first would give 4
    assert run("hallucinate(10 - 2 * 3)✨") == "4\n"


def test_addition_still_groups_left_to_right():
    assert run("hallucinate(1 + 2 * 3 - 4 / 2)✨") == "5\n"
    assert run("hallucinate(2 * 3 + 4)✨") == "10\n"


def test_multiplication_groups_before_addition_in_the_ast():
    expr = only_expression("2 + 3 * 4✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.PLUS
    assert isinstance(expr.right, Binary) and expr.right.operator.type is TokenType.STAR
    assert isinstance(expr.left, Literal) and expr.left.value == 2
    assert isinstance(expr.right.left, Literal) and expr.right.left.value == 3
    assert isinstance(expr.right.right, Literal) and expr.right.right.value == 4


def test_grouping_overrides_multiplication_precedence():
    assert run("hallucinate((2 + 3) * 4)✨") == "20\n"
