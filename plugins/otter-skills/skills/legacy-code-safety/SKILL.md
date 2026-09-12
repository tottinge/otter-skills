---
name: legacy-code-safety
description: >
  Find and protect the decisions and transformations in poorly understood or
  weakly tested existing code before changing behavior. Use for characterization
  or approval tests, side-effect reconnaissance, test-harness access, seams,
  sensing and separation, dependency breaking, and incremental replacement of
  risky live code. Once a fast trustworthy boundary exists, use unit-testing to
  drive the requested new behavior.
---

# Legacy Code Safety

Make one requested change safe without demanding a cleanup campaign or rewrite first.

Legacy code is code for which the relevant behavior cannot be verified quickly and reliably. Existing tests may be absent, slow, flaky, too broad, or coupled to irrelevant structure. The immediate job is to establish enough trustworthy feedback for the change at hand.

## Ownership and boundaries

Use this skill when:

- relevant behavior is undocumented, surprising, or poorly understood
- existing tests do not protect the intended change
- dependencies or side effects keep code out of a test harness
- the task calls for characterization, pinning, approval tests, seams, sensing, separation, or safe legacy-code change
- a large brownfield transformation needs an incremental path through live code

Do not use it as the primary skill when:

- a fast trustworthy test boundary already exists; use `unit-testing`
- the request is review-only; use `representation-refactor-review`
- the task is only to choose delivery slices; use `story-splitting-for-delivery`
- the user requested a wholesale replacement; do not silently turn this skill into authorization for one

This skill owns **establishing safety**. `unit-testing` owns specifying and implementing the new behavior after that boundary exists.

## Safety invariants

- Start from an intentional workspace and record relevant inherited failures before editing.
- Characterization describes observed behavior, not desired behavior.
- Separate observed compatibility, inferred rules, suspected defects, and intended changes.
- Establish containment before unfamiliar execution, including test collection and cleanup.
- Break only the dependencies that block sensing or separation for this change.
- Do not manufacture a unit-test target from code that merely composes effectful calls.
- Production code must not branch on whether it is under test.
- A test is not a safety net until it has demonstrated that it can fail for a relevant change.
- Every caller-visible regression within scope must be capable of failing a test somewhere.
- Prefer small, reversible changes through live code over a parallel rewrite.
- Preserve unrelated user work. Create commits or external changes only when authorized.

## Workflow

### 1. Frame the change and risk

Before editing, state:

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

Ask three questions throughout: How will we know the requested change is correct? How will we know relevant existing behavior remains intact? How cheaply can we recover from a wrong step?

### 2. Find the narrowest useful test point

Inspect the target, callers, relevant callees, and test execution path statically before executing or refactoring.
Trace where the relevant decisions and transformations actually live; the requested
function may only delegate to a deeper owner.

Look for logic worth protecting:

- branching, policy decisions, validation, and boundary rules
- calculations and data transformations
- result, event, request, or command construction
- error classification, retry decisions, and fallback selection

Then classify the target:

- **READY** — relevant logic already has sensitive tests and effects are contained
- **GAPS** — a safe boundary exists, but named decisions or transformations lack protection
- **NEEDS_SEAM** — worthwhile logic is entangled with dangerous effects
- **COMPOSED** — the function only wires effectful operations together and contains no meaningful decision or transformation
- **BLOCKED** — reachable effects remain unknown or cannot be contained

Static inspection can identify a probable target, but cannot establish **READY**.
That requires contained execution and evidence that assertions detect relevant
behavioral changes. High coverage alone is not sensitivity evidence.

During reconnaissance, search backward as well as forward. Inspect every
statically discoverable direct caller and its relevant tests. Inspect farther
upstream only when a direct caller does not reveal why it calls the target or how it
uses the result. Caller context supplies the meaning behind the target's mechanics:
expected input shapes, relied-upon results and errors, mutation or freshness,
ordering, and other compatibility assumptions. Treat these observable dependencies
as contract evidence, not as unquestionable intent; do not freeze incidental caller
mechanics such as local names, unused result details, or private sequencing.

A function that reads only its parameters, performs no mutation or other side
effects, and returns a fresh value needs no effect double. Establish that its import
and test lifecycle are contained before executing it. It is **READY** only
when sensitive tests already protect its meaningful decisions, transformations,
boundaries, corner cases, and distinct caller assumptions. Otherwise classify it as
**GAPS** and add focused input/output tests. Synthesize equivalent callers into one
behavioral case rather than mechanically writing one test per caller.

For **COMPOSED**, do not add indirection merely to obtain unit coverage. Use a
contained integration or contract test only when the composition itself carries an
important external guarantee such as ordering, transactionality, or protocol
compatibility. Otherwise locate and protect the deeper decision owner.

For **GAPS** or **NEEDS_SEAM**, prefer the cheapest boundary that protects the
requested change:

1. an existing focused public behavior
2. an existing seam near the change point
3. stable subsystem output suitable for approval testing
4. a pinch point through which several relevant effects pass
5. a minimal new seam

Do not default to a full end-to-end harness or mock every collaborator. Read
[references/seams-and-dependencies.md](references/seams-and-dependencies.md) when
code cannot run or relevant effects cannot be observed. Before executing code with
reachable database, messaging, network, filesystem, subprocess, background-work,
or global-state behavior, read
[references/effect-reconnaissance-and-scooping.md](references/effect-reconnaissance-and-scooping.md).

### 3. Characterize relevant behavior

Build a compact inventory of the selected unit's meaningful decisions and transformations. For each, infer a behavioral rule from target logic, caller expectations, and relevant callee contracts; record the evidence and uncertainty. Distinguish observed compatibility from intended behavior and suspected defects.

Through a contained boundary, capture actual results for examples and boundary or counterexamples that distinguish each inferred rule from plausible alternatives. Use these observations to confirm or revise the rule, then assert observable results or contractual effect intentions. Do not copy the production algorithm into the expected-value calculation or freeze incidental private structure. Tests should survive another implementation of the same rules.

Map each rule to its cases, assertions, and remaining gaps. Include relevant failure paths and known production examples; do not silently fix or bless suspected defects.

Use ordinary assertions for small focused results. Use approval testing for large structured output that is easier to review as a diff. Read [references/characterization-and-approvals.md](references/characterization-and-approvals.md) before creating approval artifacts.

### 4. Prove the safety net

For every meaningful rule in the selected unit, establish that its assertions detect a violation. Use an observed relevant failure or a focused, reversible perturbation of a decision, transformed value, or effect intention where sensitivity is uncertain. One demonstrated failure does not prove protection of other rules. An initially wrong expectation proves comparison works; it alone does not prove detection of a production regression.

Coverage helps locate omissions; neither a percentage nor exhaustive path combinations are the goal. Report unprotected rules as gaps rather than declaring **READY**. Before perturbing code, inspect the mutation tool's execution and cleanup, preserve the current workspace, and restore only the experiment's own edits immediately afterward.

### 5. Guard caller compatibility

If a proposed change may invalidate caller-visible behavior, gather evidence before
changing production behavior:

1. Name the affected callers and the assumptions at risk.
2. Add or strengthen tests so the current dependency and proposed incompatibility
   can cause a meaningful failure.
3. Add caller-level tests for graceful handling of the proposed result, error, or
   contract; use the smallest faithful test level that proves the handling.
4. Report the impact, migration or compatibility options, and unknown callers.
5. Stop and obtain explicit approval for the contract change and caller adaptations.

An initial request is not approval for newly discovered breakage unless it explicitly
identifies that break and its affected callers. After approval, adapt callers and the
target in small test-driven steps. Refuse the production change while material caller
risk is unknown, affected callers cannot be shown to handle it, or approval is absent.
The aim is not to forbid intentional contract change; it is to prevent accidental,
silent, or unreviewed breakage.

### 6. Introduce only necessary seams

For each blocking dependency, identify:

```text
Obstacle:
Need: sensing | separation
Seam and enabling point:
Smallest production edit:
Evidence behavior is preserved:
```

Keep preparatory edits structural and preserve available safe feedback. When remaining effects prevent execution, use static preservation checks for intermediate seam edits; require contained behavioral evidence once the boundary is runnable. Prefer explicit parameters or small adapters when natural in the codebase, but use language and build-system seams when they are safer than broad redesign.

After each extraction, review the improvement; establish executable sensitivity at the first contained boundary: meaningful policy or
transformation remains in the tested unit; its fake is smaller and safer than the
production dependency; its tests detect relevant changes; and the safety benefit
justifies the boundary. If extraction leaves a linear mirror of effect calls, revert
the experiment and classify the target as **COMPOSED**. A linear sequence may still
carry an ordering, transaction, or cleanup guarantee; protect that guarantee at a
contained integration or contract boundary rather than freezing incidental calls.

### 7. Hand new behavior to TDD

Once the boundary is fast, reliable, and capable of detecting relevant change, use `unit-testing`:

1. write one failing test for the requested behavior
2. make the minimum production change
3. refactor while green
4. retain characterization tests until focused tests safely supersede them

Do not confuse a characterization expectation with a test-first specification.

Preserve useful discoveries at this handoff so the next maintainer need not repeat
the reconnaissance. Keep confirmed rules and caller assumptions in distinguishing
tests; leave safe test access reproducible through the project's existing tooling.
Use names and small structural changes to expose intent when justified by the
safety work. Record essential rationale or unresolved uncertainty near its owner,
without turning observed quirks into intended behavior or copying the investigation
transcript into agent notes. Remove temporary probes once durable protection
supersedes them. Broader improvements belong in the subsequent green refactor loop.

### 8. Switch incrementally when the change is large

If the transformation cannot finish in a short safe cycle, keep old and new paths able to coexist, prove compatibility, and move one caller, case, or route at a time. Remove the old path only when evidence shows it is unused.

Read [references/incremental-switchover.md](references/incremental-switchover.md) before a parallel implementation, broad API change, or rewrite proposal.

### 9. Finish with evidence

Report:

```text
Requested change:
Observed legacy behavior:
Inferred rules and supporting evidence:
Characterization added:
Caller and callee assumptions protected:
Breaking-change approval:
Seams used or introduced:
Discovery preserved and future investigation avoided:
Rule protection and sensitivity evidence:
New behavior test and implementation:
Verification:
Temporary scaffolding:
Remaining unprotected risks:
Final target classification:
```

## Stop and report rather than guess

Stop or narrow the work when characterization would:

- execute destructive production effects
- capture secrets, personal data, or environment-specific credentials
- approve output nobody has inspected
- depend on uncontrolled nondeterminism that obscures meaningful changes
- require a public-contract change beyond the user's authorization
- leave affected callers unable to handle an approved contract change gracefully
- discard or overwrite unrelated work to regain a baseline

When a unit remains unreachable, report the smallest seam that would unlock it and the risk of that edit. Do not fabricate confidence.

## Related skills

- `unit-testing` — owns test-first implementation after a trustworthy boundary exists.
- `representation-refactor-review` — owns broad representation critique; this skill changes only enough representation to make the requested work safe.
- `story-splitting-for-delivery` — owns delivery-slice selection. Use incremental switchover here to execute a chosen brownfield slice safely.
- `code-object-naming` — owns focused naming analysis; routine names introduced by a seam should simply match the local dialect.

For source attribution and further reading, see [references/sources.md](references/sources.md).
