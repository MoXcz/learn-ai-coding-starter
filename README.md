# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Quick start

```bash
uv run sloperator.py examples/fib.slop         # run a program
uv run sloperator.py --check examples/fib.slop # check syntax only
```

## Validation

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Playground

```bash
uv run playground/server.py
```

Then open <http://localhost:8080>.

## Language

Programs use the `.slop` extension. See [docs/spec.md](docs/spec.md) for the
syntax, keywords, values, operators, grammar, and error messages.

## Layout

| Path                    | What it is                                          |
| ----------------------- | --------------------------------------------------- |
| `sloperator.py`         | Command-line entrypoint                             |
| `sloperator/lexer/`     | Source text to tokens                               |
| `sloperator/parser/`    | Tokens to AST (`ast.py` holds the node definitions) |
| `sloperator/evaluator/` | Walks the AST: values, environments, interpreter    |
| `sloperator/runner.py`  | Runs source through all three stages                |
| `docs/spec.md`          | The language specification                          |
| `examples/`             | Example programs                                    |
| `tests/`                | Pytest suite                                        |
| `playground/`           | Web server and editor page for running programs     |
