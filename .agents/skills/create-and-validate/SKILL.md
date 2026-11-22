---
name: create-and-validate
description: Create a SlopLang example and exact-output test, then validate it. Use when asked to add a test program or regression coverage and run the checks in one pass.
---

# Create And Validate

Runs two existing skills in order. Do not restate their steps here; load each one and
follow it.

1. Load the `create-test-program` skill and complete it.
2. Load the `validate` skill and complete it.

If `create-test-program` stops because `docs/spec.md` does not define the feature, skip
`validate` and report why.
