---
name: create-test-program
description: Add a worked example and exact-output test for a SlopLang language feature. Use when asked to create a test program, example, or regression coverage for a feature, or when adding a feature that needs an example in examples/ plus an exact-output test in tests/test_example_outputs.py.
---

# Create Test Program

Given a language feature, produce an example program and a test that pins its exact
stdout.

## Steps

1. Read `docs/spec.md` and find the section that defines the feature. Use its exact
   syntax and vocabulary. If the spec does not define the feature, stop and report
   that before writing any code.
2. Write `examples/<feature>.slop` (kebab-case, no `test_` prefix). Keep it short and
   focused on the feature; one feature per file. It must print something.
3. Add an entry to `CASES` in `tests/test_example_outputs.py`:

   ```python
   (
       (
           "feature-name",  # matches examples/feature-name.slop
           "expected\noutput\n",  # exact stdout, including trailing newlines
       ),
   )
   ```

   If the file does not exist, create it with:

   ```python
   """Exact stdout for each example program."""

   from pathlib import Path

   import pytest

   from sloperator.runner import run_source

   EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

   CASES = [
       # (example stem, exact stdout)
   ]


   @pytest.mark.parametrize(("stem", "expected"), CASES, ids=[case[0] for case in CASES])
   def test_example_output(stem: str, expected: str):
       result = run_source((EXAMPLES / f"{stem}.slop").read_text(encoding="utf-8"))
       assert result.stderr == ""
       assert result.exit_code == 0
       assert result.stdout == expected
   ```

4. Derive the expected output by running the example, never by hand:

   ```sh
   uv run sloperator.py examples/<feature>.slop
   ```

   Copy the output byte for byte. Confirm it matches the spec, not just the
   interpreter, so the test catches a regression rather than enshrining a bug.
5. If the feature changed the language, update `docs/spec.md` too.
6. Run `uv run ruff format`, then the `validate` skill. Every example is also run by
   `tests/test_examples.py`, so it must exit 0 with non-empty stdout.

## Conventions

- Non-ASCII is intentional: `✨`, `“ ”`, `—`, `✅`/`❌`. Use them in examples; never
  normalize to ASCII, and never use straight quotes, semicolons, or en dashes.
- Comments start with an em dash (`—`); statements end with `✨`.
- The test asserts exact stdout, including blank lines. Do not strip or normalize.
