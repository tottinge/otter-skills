---
name: legacy-code-safety
description: >
  Use when changing poorly understood, weakly tested, or risky existing code
  whose behavior, side effects, or test access are not yet trustworthy. Establish
  safety with characterization or approval tests, reconnaissance, seams, sensing
  and separation, dependency breaking, or incremental replacement. Once a fast
  trustworthy boundary exists, use unit-testing to drive new behavior.
---

# Legacy Code Safety

Make one requested change safe without demanding a cleanup campaign or rewrite
first. Legacy code is code whose relevant behavior cannot be verified quickly
and reliably. Establish enough trustworthy feedback for the change at hand,
then hand new behavior to `unit-testing`.

## Boundaries

Use this skill when behavior is undocumented, surprising, or poorly understood;
existing tests do not protect the intended change; dependencies or side effects
block a test harness; or the task calls for characterization, approval tests,
seams, sensing, separation, or incremental replacement.

Do not use it as the primary skill when a fast trustworthy boundary already
exists (`unit-testing`), the request is review-only
(`representation-refactor-review`), the task is only delivery-slice selection
(`story-splitting-for-delivery`), or the user requested a wholesale replacement.

## Progressive loading

Read only the guidance needed for the current risk:

| Need | Read |
| --- | --- |
| Choose a test point, classify the target, or establish characterization | [references/reconnaissance-and-characterization.md](references/reconnaissance-and-characterization.md) |
| Reach code with effects | [references/effect-reconnaissance-and-scooping.md](references/effect-reconnaissance-and-scooping.md) |
| Introduce a seam or make a structural change safe | [references/seams-and-dependencies.md](references/seams-and-dependencies.md) |
| Replace a path incrementally or change a public contract | [references/incremental-switchover.md](references/incremental-switchover.md) |
| Source attribution and further reading | [references/sources.md](references/sources.md) |

Do not load every reference by default. Start with reconnaissance for an
unfamiliar target; add effects, seams, or compatibility guidance only when the
current change requires it.

## Safety contract

Before the first production edit:

1. Start from an intentional workspace and record relevant inherited failures.
2. Inspect the target, every statically discoverable direct caller, relevant
   callees, and the test execution path before executing or refactoring.
3. Record expected inputs, results, errors, mutation/freshness, ordering, and
   other caller-visible assumptions. Treat them as evidence, not unquestionable
   intent; do not freeze incidental mechanics.
4. Separate observed compatibility, inferred rules, suspected defects, and
   intended changes.
5. Establish containment before unfamiliar execution, including test collection
   and cleanup.
6. If a proposed edit may break callers, prove graceful handling at the
   narrowest faithful level and obtain explicit approval before the contract
   change.

## Core workflow

1. Frame the requested change, likely change point, entry-to-exit path, stable
   behavior, dangerous dependencies, caller assumptions, and current feedback.
2. Find the narrowest useful test point. Trace decisions and transformations to
   their real owner rather than manufacturing a unit target from composition.
3. Classify the target as `READY`, `GAPS`, `NEEDS_SEAM`, `COMPOSED`, or `BLOCKED`.
4. For `GAPS` or `NEEDS_SEAM`, characterize meaningful rules with focused
   examples and counterexamples; prove assertions can detect relevant change.
5. Introduce only the smallest seam needed for sensing or separation. Preserve
   safe feedback and reject linear mirrors of effect calls as unnecessary
   indirection.
6. Once the boundary is fast, reliable, and sensitive, hand new behavior to
   `unit-testing`: failing test, minimum production change, refactor green.
7. Finish by reporting observed behavior, inferred rules, protection and
   sensitivity evidence, caller risks, seams, verification, and remaining gaps.

## Non-negotiable stop conditions

Stop or narrow the work rather than guessing when execution could cause
destructive effects, capture secrets or personal data, approve uninspected
output, depend on uncontrolled nondeterminism, or require an unauthorized
public-contract change. Do not discard unrelated work to regain a baseline.

## Related skills

- `unit-testing` owns test-first implementation after a trustworthy boundary.
- `representation-refactor-review` owns broad representation critique.
- `story-splitting-for-delivery` owns delivery-slice selection.
- `code-object-naming` owns focused naming analysis.
