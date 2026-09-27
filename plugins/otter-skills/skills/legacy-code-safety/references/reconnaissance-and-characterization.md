# Reconnaissance and characterization

Use this reference when the target's behavior, callers, or useful test point are
unclear.

## Frame the change

Record:

```text
Requested change:
Likely change point:
Relevant entry-to-exit path:
Behavior that must remain stable:
Dangerous or unavailable dependencies:
Target classification and evidence:
Caller context and compatibility assumptions:
Potential breaking changes and approval needed:
Current feedback and inherited failures:
```

Ask throughout: How will we know the requested change is correct? How will we
know relevant behavior remains intact? How cheaply can we recover from a wrong
step?

## Find the narrowest useful test point

Inspect the target, direct callers, relevant callees, and test execution path
statically before executing or refactoring. Trace where decisions and
transformations actually live; a requested function may only delegate to a
deeper owner.

Look for branching, policy, validation, boundaries, calculations,
transformations, result/event/request construction, error classification, retry,
and fallback decisions.

Classify the target:

- **READY** — relevant logic has sensitive tests and effects are contained.
- **GAPS** — a safe boundary exists, but named decisions or transformations lack
  protection.
- **NEEDS_SEAM** — worthwhile logic is entangled with dangerous effects.
- **COMPOSED** — the function only wires effectful operations together and has no
  meaningful decision or transformation.
- **BLOCKED** — reachable effects remain unknown or cannot be contained.

Static inspection can identify a probable target, but cannot establish **READY**.
Contained execution and evidence that assertions detect relevant behavioral
changes are required. Coverage locates omissions; it does not prove sensitivity.

Search backward as well as forward. Inspect every statically discoverable direct
caller and its relevant tests. Go farther upstream only when a direct caller does
not reveal why it calls the target or how it uses the result. Treat expected
inputs, results, errors, mutation/freshness, ordering, and other observable
dependencies as contract evidence, not unquestionable intent.

Pure functions that read only parameters, perform no mutation or side effects,
and return fresh values need no effect double. They still need contained import
and test lifecycle, and sensitive tests for meaningful decisions, transformations,
boundaries, corner cases, and distinct caller assumptions.

For **COMPOSED**, do not add indirection merely to obtain unit coverage. Use a
contained integration or contract test only when ordering, transactionality,
cleanup, or protocol compatibility is itself important; otherwise protect the
deeper decision owner.

## Characterize relevant behavior

Build a compact inventory of meaningful decisions and transformations. For each,
infer a behavioral rule from target logic, caller expectations, and callee
contracts; record evidence and uncertainty. Distinguish observed compatibility,
intended behavior, and suspected defects.

Through a contained boundary, capture actual results for examples and boundary
or counterexamples that distinguish each rule from plausible alternatives. Assert
observable results or contractual effect intentions without copying the
production algorithm into expected values or freezing private structure.

Map each rule to cases, assertions, and remaining gaps. Include relevant failure
paths and known production examples. Use ordinary assertions for focused results;
use approval testing for large structured output that is easier to review as a
diff. Read [characterization-and-approvals.md](characterization-and-approvals.md)
before creating approval artifacts.

## Prove the safety net

For every meaningful rule, establish that assertions detect a violation. Use an
observed relevant failure or a focused, reversible perturbation when sensitivity
is uncertain. One demonstrated failure does not prove every other rule is
protected. Before perturbing code, inspect mutation-tool execution and cleanup,
preserve the workspace, and restore only the experiment's edits.
