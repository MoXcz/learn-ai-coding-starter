# AGENTS.md

Sloperator is a from-scratch, tree-walking interpreter for SlopLang. Python 3.13,
no runtime dependencies. `README.md` covers setup.

## Project layout

- `sloperator.py` — CLI entry point (`run` / `--check`).
- `sloperator/lexer/` — `tokens.py` defines kinds; `scanner.py` produces tokens.
- `sloperator/parser/` — `ast.py` defines nodes; `parser.py` builds the tree.
- `sloperator/evaluator/` — `interpreter.py` walks the tree; `environment.py` handles scope.
- `sloperator/runner.py`, `sloperator/errors.py` — program execution and `SlopError` types.
- `playground/` — local web playground that shells out to the CLI.
- `examples/`, `tests/`, `docs/spec.md`.

A language feature usually spans `lexer/tokens.py` → `lexer/scanner.py` →
`parser/ast.py` → `parser/parser.py` → `evaluator/interpreter.py` → `docs/spec.md`.

## Validation commands

Run the formatter after any code change, before validation:

```sh
uv run ruff format
```

Run from the repo root with `uv`. All four must pass before a change is considered done:

```sh
uv run pytest
uv run ruff check
uv run ruff format --check
uv run ty check
```

`ty` is Astral's type checker, not mypy/pyright. The `validate` skill
(`.agents/skills/validate/SKILL.md`) runs the test, format, and lint steps and expects
failures reported before fixes.

Comparison and equality precedence tests live in `tests/test_comparisons.py`; run them
directly with:

```sh
uv run pytest tests/test_comparisons.py
```

## When to add regression tests

Add a test to `tests/` whenever a change fixes a bug, changes an error message or other
observable behavior, or adds a language feature. Bug fixes need a test that fails before
the fix and passes after it. Error-message tests belong in `tests/test_errors.py`, which
asserts exact `SlopLang <kind> error at line N: <message>` strings. New `examples/*.slop`
must produce non-empty stdout, because `tests/test_examples.py` runs every example.

## Language behavior

`docs/spec.md` is the language contract. Read it before touching syntax or semantics,
and update it alongside any language change. Do not normalize its non-ASCII characters
(keywords, `✨`, `“ ”`, `—`, `✅`/`❌`) to ASCII; straight quotes, semicolons, and en
dashes are deliberately rejected.
