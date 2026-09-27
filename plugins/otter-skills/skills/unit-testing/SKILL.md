---
name: unit-testing
description: Use when implementing or extending production behavior test-first, diagnosing focused unit-test quality or flakiness, or refactoring inside an active green cycle using red-green-refactor, ZOMBIES, FIRST, Tidy First?, and Save Your Game checkpoints. Do not use for delivery slicing, broad representation review, or focused naming.
---

# Unit testing

Own the behavior cycle that makes code safe to change in tiny steps. Work one behavior at a time:
write a meaningful failing test, make the smallest change green, refactor while green, and preserve
the result at an authorized checkpoint. Microtests support safe change; they do not replace
component, contract, end-to-end, or human testing.

## Boundaries

Use this skill for new behavior, behavior-changing bug fixes, test-first refactoring, focused test
quality, and flaky-test diagnosis.

Use `legacy-code-safety` first when the target is poorly understood or test access and side effects
are unknown. Use `story-splitting-for-delivery` to choose a delivery slice, `user-pov-sliced-stories`
to format an existing split, `representation-refactor-review` for broad craft review, and
`code-object-naming` for a focused identifier task.

## Progressive loading

Load only the guidance needed for the current move:

| Need | Read |
| --- | --- |
| Clean Start, Red-Green-Refactor, checkpoints, or integration | [`references/tdd-cycle.md`](references/tdd-cycle.md) |
| Choosing the next case or deciding whether to tidy first | [`references/test-selection-and-tidy.md`](references/test-selection-and-tidy.md) |
| FIRST microtests, doubles, structure-shy tests, or flake diagnosis | [`references/microtests-and-flakes.md`](references/microtests-and-flakes.md) |
| Refactoring toward the Eight Virtues or affordable feedback | [`references/virtue-refactoring.md`](references/virtue-refactoring.md) |
| Anti-pattern quick check | [`references/anti-patterns.md`](references/anti-patterns.md) |

Do not load every reference by default. Start with the cycle reference for implementation work;
add one specialized reference only when the task calls for it.

## Required safety and contract evidence

Before the first production edit:

1. Establish containment and inspect the project's safe baseline commands. If setup effects or
   test access are unknown, stop and use `legacy-code-safety`.
2. Inspect every statically discoverable direct caller and relevant existing tests for an existing
   function. Record assumptions about inputs, results, errors, mutation/freshness, ordering, and
   other observable behavior without turning incidental structure into contract.
3. Write a short, revisable Beck-style test list. Implement one test at a time.
4. If a proposed edit may break caller assumptions, add evidence at the narrowest faithful level,
   show the migration/compatibility choices, and obtain explicit approval before breaking the
   contract. Do not infer permission from a general change request.

## Core loop

```text
clean green baseline
  → test list and one next behavior
  → Tidy First? decision
  → meaningful Red
  → minimal Green
  → Refactor while green
  → authorized Save Your Game checkpoint
  → separately verified integration when authorized
```

Red must fail for the missing or wrong behavior, not for a placeholder compile error or bare
`fail()`. Green is the minimum production change. Refactor tests and production toward named
virtues without changing behavior. When a step goes sideways, retreat to the last green saved
state and choose a smaller behavior; never start another concern with the suite red.

## Test design rules

- Test observable behavior and meaningful effect intentions, not private structure, helper names,
  incidental call counts, or deep object graphs.
- Derive expected values independently from the production algorithm.
- Use real decisions and transformations at the unit boundary; replace collaborators only at a
  meaningful boundary and preserve their relevant result shapes, errors, mutation, ordering, and
  lifecycle.
- Keep tests one-behavior, diagnostic, deterministic, and resilient under behavior-preserving
  refactoring. Do not weaken or rewrite existing tests merely to restore green.
- Extract logic into a microtestable boundary when that improves the design; do not add tests for
  trivial wiring, accessors, generated code, or declarative configuration without a contract.

## Failure and completion rules

Diagnose a failure before editing either test or production. A behavior change, production defect,
over-specified test, and unknown cause require different responses. A flaky test is not repaired by
rerunning until green, weakening assertions, or quarantining it without an owner and repair path.

Before reporting completion, show the focused test result, the relevant suite result, any remaining
verification limits, and the behavior or maintenance difficulty removed. Do not commit or publish
unless the user authorizes it; use `atomic-commit` for an authorized green checkpoint.

## Related workflows

- `legacy-code-safety` establishes a trustworthy boundary around unknown existing behavior.
- `representation-refactor-review` owns broad representation and ZOM review.
- `atomic-commit` owns whole-repository verification and Save Your Game commits.
