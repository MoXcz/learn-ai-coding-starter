---
description: Review the diff, stage project changes, commit with the given message, then rebase onto origin/main
---

Commit the current project changes using this message: $ARGUMENTS

Steps:

1. If the message above is empty, stop and ask for a commit message. Do not commit.
2. Run `git status`, `git diff`, and `git diff --staged`. Read the changes and check for anything that should not be committed: secrets, credentials, `.env` files, `node_modules`, build output, or unrelated files. If you find any, leave them out and name them in your final answer.
3. Stage the project changes with `git add` on the specific paths that belong to the work. Do not stage files you excluded in step 2.
4. Run `git commit -m "<message>"` with the message from above. Do not amend, do not use `--no-verify`, and do not change the message.
5. Run `git pull --rebase origin main`.
6. If the rebase reports conflicts, stop, list the conflicting files, and do not force anything. Otherwise report the new commit hash and the result of the pull.

Report what was committed, which files were left out and why, and the outcome of the rebase.
