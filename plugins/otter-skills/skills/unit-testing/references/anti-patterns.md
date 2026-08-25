# Unit Testing Anti-Patterns (stop these)

## Process

- Production code before a failing test for that behavior
- Big-bang implementation, tests afterward ("new legacy")
- Writing a batch of tests before implementing any of them
- Skipping refactor because "it works"
- Leaving the suite red while starting another concern
- Huge uncommitted WIP — cannot retreat cheaply
- Mixing unrelated changes in one commit
- Ignoring failures / rerunning until flake passes
- Treating CI as a substitute for local continuous testing
- Using bare `fail()` or compile errors as the intended red without asserting behavior

## Test design

- Tests coupled to private structure, call graphs, or train-wreck navigation (`a.b.c.d`)
- One test asserting many unrelated behaviors (god test)
- Shared mutable fixtures that leak across tests
- Real time, network, DB, filesystem, or sleep in microtests
- Over-specified snapshots of entire HTML/JSON/DOM when one fact matters
- Assertions that only check `true`/`false` without useful expected/actual output
- Production code that detects test mode (high-fidelity violation)
- Test names that restate technical method names instead of domain situations

## Refactor

- Vague "cleanup" without targeting a named virtue
- Hand-editing renames or extracts across many files when LSP/`ast-grep` can do it exactly
- Pursuing Brief at the cost of Clear or Working
- Abstracting at first duplication hint without a second real instance (Unique violation)

## Scope confusion

- Expecting microtests alone to prove product fitness
- Treating coverage % as the goal rather than safe change
- Replacing BDD/example collaboration with guesswork microtests for unclear rules
- Expanding coverage metrics with empty tests that never assert
- Weakening or rewriting existing tests to accept broken behavior without explicit human approval
