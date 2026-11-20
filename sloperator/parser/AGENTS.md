# Parser conventions

`parser.py` is a recursive-descent parser for the grammar in `docs/spec.md`.
`ast.py` holds the frozen-dataclass nodes; the rest of the interpreter consumes them.

## One method per grammar rule

Each grammar rule gets its own method, named after the rule in snake_case, and the
methods call each other in precedence order:

```text
program        parse
topLevel       top_level
functionDecl   function_decl
declaration    declaration
variableDecl   var_decl
statement      statement
assignStmt     assign_stmt
ifStmt         if_stmt
loopStmt       while_stmt
returnStmt     ship_stmt
block          block
expression     expression
logicOr        logic_or
logicAnd       logic_and
equality       equality
comparison     comparison
term           term
factor         factor
unary          unary
call           call
arguments      inline in `call`
primary        primary
```

Add a new rule as a new method, not as extra branching in `statement` or `primary`.
Use the primitives `match`, `check`, `advance`, `peek`, `previous`, and `expect`
rather than indexing `self.tokens` directly.

## Syntax errors name the token found

Raise through `self.error(token, message)`, which appends `, found '<lexeme>'` or,
at end of input, `, but reached end of file`:

```python
self.expect(TokenType.EQUAL, "expected '=' after variable name, an initializer is required")
# -> SlopLang syntax error at line 1: expected '=' after variable name, an initializer is required, found '✨'
```

Pass the token that was actually encountered (`self.peek()` in `expect`, the advanced
token in `primary`), and keep the message about the expected construct. Only hand-write
a message when no found token applies (`ship` outside a `clanker`, nested `clanker`).

Messages are asserted exactly in `tests/test_errors.py`; update those and
`docs/spec.md` whenever the wording changes.
