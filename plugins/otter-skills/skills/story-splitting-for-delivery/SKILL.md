---
name: story-splitting-for-delivery
description: >
  Use when an oversized feature, epic, or story needs a thin, demonstrable,
  deployable delivery sequence. Choose slices through progressive admission:
  start with a closed end-to-end skeleton, then admit one message, schema,
  import, API, form, path, rule, persona, or channel case at a time. Do not use
  merely to format an already-chosen split as user-visible outcomes; that belongs
  to user-pov-sliced-stories.
---

# Story Splitting for Delivery

Choose and sequence thin, demonstrable, potentially deployable delivery slices.
Use progressive admission: build the end-to-end path closed, then admit one safe
case at a time while everything else remains rejected.

## Boundaries

Use this skill whenever work is too large for one iteration or needs a delivery
sequence, especially for message, schema, import, API, form, path, rule,
persona, or channel variation. If the admission boundary is unclear, derive it
from the variations in data shapes, rules, interfaces, paths, or roles; do not
fall back to component/task decomposition.

Use `user-pov-sliced-stories` only after the split exists and the main need is to
format it as explicit user-invokes/user-uses-result outcomes.

## Progressive loading

Read [references/progressive-admission.md](references/progressive-admission.md)
when producing an admission plan, choosing the next slice, or applying the
quality gate. It contains the required plan format, sequencing heuristics,
anti-patterns, and examples.

## Admission contract

Every plan must state:

- the admission boundary and the stable default rejection
- the complete end-to-end path from entry to result
- Slice 0: a closed skeleton that proves the path and reject behavior
- each later slice's one newly admitted case
- what remains rejected after every slice
- how each slice is invoked, observed, independently demonstrated, tested, and
  valuable now

## Core method

1. Name what varies and the default rejection (`invalid`, `unsupported`, or
   `not implemented`).
2. Build Slice 0 with the full path wired but no useful case admitted.
3. Prove reject, health, guard, error, and observability behavior.
4. Admit the simplest, most common, or highest-learning real case.
5. Widen exactly one case, shape, field set, path, or rule at a time.
6. Keep all non-admitted cases on the stable reject path.
7. After each demonstration, reassess value, uncertainty, and delivery
   constraint; continue, change direction, or stop based on evidence.

Do not complete the planned remainder merely because it is cheap to generate.
If a slice secretly requires many cases at once, split it again.

## Quality gate

Before accepting a slice, verify that the end-to-end path remains intact, only
one case was admitted, non-admitted cases still reject, the result is meaningful
and independently demonstrable, unit and end-to-end checks are clear, and the
system would remain coherent if work stopped there.

## Related skills

- `user-pov-sliced-stories` formats an existing split for user-visible wording.
- `unit-testing` protects each admitted behavior test-first.
- `legacy-code-safety` establishes a safe boundary in poorly understood code.
