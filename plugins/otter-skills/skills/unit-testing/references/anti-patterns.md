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
- Configuring automatic reruns as a substitute for diagnosing a flake
- Quarantining or ignoring a flaky test without an owner and repair path
- Treating CI as a substitute for local continuous testing
- Using bare `fail()` or compile errors as the intended red without asserting behavior
- Running unfamiliar test collection, fixtures, cleanup, or mutation experiments before establishing containment

## Test design

- Tests coupled to private structure, call graphs, or train-wreck navigation (`a.b.c.d`)
- Copying the production algorithm into the oracle or deriving expected results by calling the target
- Mocking the unit's own decisions or transformations while claiming to test them
- Using doubles with results or failures the real collaborator cannot produce
- Asserting incidental interaction sequences rather than contractual effect intentions
- Editing existing tests alongside routine production edits merely to preserve green
- Treating widespread test maintenance after a behavior-preserving refactor as normal
- One test asserting many unrelated behaviors (god test)
- Shared mutable fixtures that leak across tests
- Real time, network, DB, filesystem, or sleep in microtests
- Depending on incidental order from an unordered or concurrently-produced result
- Sharing mutable environments, records, ports, credentials, or services across test runs
- Ordering tests alphabetically or otherwise to conceal cross-contamination
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
- Claiming whole-unit protection from one sensitive test while other named rules have no assertions
- Treating current output as the intended rule without caller/callee evidence or distinguishing examples
- Replacing BDD/example collaboration with guesswork microtests for unclear rules
- Expanding coverage metrics with empty tests that never assert
- Weakening or rewriting existing tests to accept broken behavior without explicit human approval
