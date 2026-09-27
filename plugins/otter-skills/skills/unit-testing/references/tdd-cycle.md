# TDD cycle and checkpoints

## Clean Start

Before unfamiliar setup, inspect imports, collection, fixtures, teardown, subprocesses, and
background work. Establish disposable test-owned resources, controlled credentials, and cleanup
limited to those resources. Before the first production edit, confirm the working tree is
intentional, dependencies use the repository's normal path, and the relevant baseline tests are
green. Run `./prepare` or `./run_tests` when the project provides them.

If the baseline is red, stop and report the inherited failure. Do not pile new work onto it.

## The cycle

1. Connect the requested change to a short Beck-style test list.
2. Choose one behavior, normally using ZOMBIES ordering.
3. Decide First, After, Later, or Never for tidying.
4. Write the smallest meaningful failing test.
5. Write the minimum production code that passes.
6. Refactor production and tests while green.
7. Run the focused test and the relevant fast suite.
8. At an authorized green checkpoint, use `atomic-commit` for Save Your Game.
9. Integrate shared changes separately and rerun verification on the combined state.

Red should fail because the behavior is missing or wrong, not because of a placeholder compile
error or bare `fail()`. Green should not include speculative branches. Refactor is required but
must preserve behavior. If confused for more than one small step, retreat to the last green state.

## Caller contracts

For an existing function, inspect direct callers and relevant tests before editing. If the change
may invalidate assumptions, add target-, contract-, integration-, or caller-level evidence first.
Show compatibility and migration options and obtain approval before intentionally breaking a
caller-visible contract.

## Save Your Game and integration

The local microcommit is a recoverable, human-reviewed green state. It is distinct from publishing.
Do not call a local commit integrated until shared changes have been combined and verified. Never
leave a test failure introduced by the session as the stopping state.
