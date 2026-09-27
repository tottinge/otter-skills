---
name: representation-refactor-review
description: Use when reviewing how code represents knowledge, identifying evidence-backed refactoring opportunities, applying the Eight Virtues, SPOT, ZOM, or the improvement test, or evaluating data and class boundaries. Do not use for bug/security-only review, test-first implementation, delivery slicing, or focused identifier naming.
---

# Representation refactor review

Review code as knowledge representation. Produce a short, prioritized set of evidence-backed
representation concerns and the smallest plausible refactoring for each. The skill owns the
interpretation and judgment; repository tools provide observations only.

## Boundaries

Use this skill for broad craft review, refactoring readiness, cumulative change review, data
clusters, data classes, class boundaries, SPOT, ZOM, the Eight Virtues, or the improvement test.

Hand off the primary task to the specialist workflow for correctness/security-only review,
test-first implementation, legacy characterization, delivery slicing, or focused identifier
naming. A broad review may still mention evidence from those areas.

## Progressive loading

Load only what the request needs:

| Need | Read |
| --- | --- |
| Virtue definitions or the improvement test | [`references/virtues.md`](references/virtues.md) |
| Data clusters, value objects, class extraction, or class splitting | [`references/class-boundaries.md`](references/class-boundaries.md) |
| Provider selection or fallback | [`references/evidence-providers.md`](references/evidence-providers.md) |
| Otter-KR is actually connected | [`references/provider-otter-kr.md`](references/provider-otter-kr.md) |
| Provider substitution or degraded-mode evaluation | [`references/evaluation-cases.md`](references/evaluation-cases.md) |

Do not read every reference by default. Read `virtues.md` before writing findings; read one
provider guide only when a provider is available; read `class-boundaries.md` only when a type or
boundary recommendation is plausible.

## Bounded review workflow

1. Establish Working: inspect project instructions, the requested diff or scope, and the narrowest
   relevant tests/checks. State verification limits.
2. Bound the review. Start from the diff, named files, project hotspots, or one provider packet.
   Select a small set of relevant files and symbols. Do not enumerate or read the whole repository
   unless the user explicitly requests a whole-repository review.
3. Read the selected code for the audience and identify where intent had to be reconstructed.
4. Observe representation pressure: repeated knowledge, traveling values, primitive clusters,
   competing dialects, growing decisions, scattered ownership, or dead representations.
5. Widen evidence only for a live question. Prefer one bounded baseline and at most two focused
   follow-ups. Never run every analyzer by default.
6. Separate observation, inference, and action. Provider output is evidence, never a diagnosis.
7. Propose the smallest mechanical move and apply the improvement test across Working and the peer
   virtues. Leave a concern out if no concrete improvement is justified.

## Evidence-provider contract

Providers are optional turbochargers, never prerequisites. Ask for capabilities, not products;
fall back to direct source reading, `rg`, tests, and bounded Git history when unavailable.

When Otter-KR is connected, make one bounded `git.review_packet.file`, `.files`, or `git.review_packet`
call appropriate to the scope. Preserve its revision, bounds, warnings, truncation, and locations.
Use a focused follow-up only when the packet raises a specific question. Do not issue repeated
overlapping research calls merely to gather more context.

When another provider is stronger for the question, use it instead or compose it deliberately.
Record unavailable dimensions and uncertainty. Co-change is not semantic coupling; duplication is
not proof of shared knowledge; a cluster or lifecycle is not proof that a class should be extracted.

## Representation questions

Use these as questions, not automatic prescriptions:

- Repeated helpers or facts: is one rule represented in multiple executable homes?
- Repeated parameter or field groups: do values travel together with shared rules or invariants?
- Several methods on one carrier: does a meaningful owner or lifecycle exist?
- Long conditionals, flags, or type checks: is variation better represented as data, policy, or state?
- Imports, bridges, or co-change: is the boundary intentional or is ownership scattered?
- Dead branches or obsolete parameters: is a ghost dialect misleading maintainers?

For ZOM, ask what multiplied: values suggest a collection, fields a value object, behavior an
owner, roles a strategy/table, states a state model, rules a policy, and scattered ownership one
authoritative home. Counts and patterns establish pressure; source, tests, and likely change decide.

## Class and value-object restraint

Do not recommend a class from size, field count, method count, or clumping alone. Introduce a type
when values repeatedly travel together and share construction rules, invariants, normalization, or
behavior worth owning. Split a class only when there are at least two meaningful clusters with a
small interaction boundary. Read `class-boundaries.md` before reporting such a recommendation.

## Finding format

Read `virtues.md` before assembling findings. Report findings in descending priority, with no empty
priority sections:

```markdown
### [P1–P4] Concrete imperative title
- Location: [file:line]
- Virtues under pressure: ...
- Observation: what the code demonstrates
- Inference: why that indicates representation pressure
- Action: the smallest refactoring move
- Why necessary: maintenance or behavioral consequence
```

Every finding needs all six fields. P1 threatens Working or Unique; P2 seriously pressures Simple,
Clear, Developed, or Coherent; P3 concerns likely changeability or mild drift; P4 is polish and
must not be inflated. Finish with verification gaps and a short verdict.

## Improvement test

Keep a recommendation only if behavior remains Working and the overall representation improves
across the peer virtues together. Name the tradeoff: vocabulary, ownership, path count,
changeability, indirection, or coupling. Do not refactor for fewer lines or smaller files alone.

For an implementation task, preserve or add tests and re-evaluate the same evidence afterward. For
a review-only task, do not edit production code, commit, or push.

## Related workflows

- `legacy-code-safety` owns characterization and dependency-breaking seams.
- `unit-testing` owns test-first behavior and focused test quality.
- `code-object-naming` owns focused identifier diagnosis and renames.
- `story-splitting-for-delivery` owns delivery-slice sequencing.
