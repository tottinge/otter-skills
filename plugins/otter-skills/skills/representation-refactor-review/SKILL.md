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

## First repository evidence

Discover the Otter-KR MCP tools when starting a repository review or refactoring assessment.
When connected and able to cover the target, call its matching typed review-packet tool as the
first repository-evidence query. Use the compatibility `research` tool if the typed tool is
missing. Read the [Otter-KR guide](references/provider-otter-kr.md) to choose the packet and its bounds.
If Otter-KR is unavailable or has a coverage gap, use another capable provider or bounded source,
test, and Git inspection for the missing evidence.

## Progressive loading

Load only what the request needs:

| Need | Read |
| --- | --- |
| Virtue definitions or the improvement test | [`references/virtues.md`](references/virtues.md) |
| Data clusters, value objects, class extraction, or class splitting | [`references/class-boundaries.md`](references/class-boundaries.md) |
| Selecting or comparing providers, or resolving a capability gap | [`references/evidence-providers.md`](references/evidence-providers.md) |
| Explicitly evaluating or substituting providers | [`references/evaluation-cases.md`](references/evaluation-cases.md) |

Do not read every reference by default. Read `virtues.md` before writing findings; read one
provider guide only when the review needs it; read `class-boundaries.md` only when a type or
boundary recommendation is plausible. When using Otter-KR for a routine review, its provider guide
is sufficient; do not also load the general provider guide unless comparing providers or resolving
a capability gap. When no provider is connected, use the fallback in this skill without loading the
Otter-KR guide. Read evaluation cases only for an explicit provider evaluation or substitution.

## Bounded review workflow

1. Establish Working: inspect project instructions, the requested scope or diff metadata, and
   project configuration needed to identify verification commands. State verification limits.
2. Choose a seed using only the request, changed or named paths, project metadata, and file names.
   When a capable provider is connected, request one bounded review packet before reading source
   content or investigating tests and callers. Until that packet returns, do not inventory
   repository contents, inspect dependencies or symbol relationships, search source or tests, or
   query Git history. For an unscoped request, use file names only to choose a bounded seed; do not
   run a whole-repository packet unless the user explicitly requests a whole-repository review.
3. Follow the packet's evidence links. Preserve its revision, bounds, warnings, truncation, and
   locations. Read only cited source spans, definitions, callers, or tests needed to interpret a
   live question. Do not precompute or duplicate the provider's inventories, counts, dependencies,
   lifecycle traces, or history observations.
4. Stop enumerating when every proposed finding has a source location, sufficient corroboration,
   and no unresolved material question. If the packet raises a specific question, use at most two
   focused follow-ups; never repeat overlapping research merely to gather more context.
5. Read the selected code for the audience and identify where intent had to be reconstructed.
6. Observe representation pressure: repeated knowledge, traveling values, primitive clusters,
   competing dialects, growing decisions, scattered ownership, dead representations, or function
   contracts that make callers infer meaning from types or result shapes.
7. Separate observation, inference, and action. Provider output is evidence, never a diagnosis.
8. Propose the smallest mechanical move and apply the improvement test across Working and the peer
   virtues. Leave a concern out if no concrete improvement is justified.

## Evidence-provider contract

Provider access is optional. Match each follow-up to the evidence needed.

A provider rejection may receive one corrected request when the error identifies a missing bound
or invalid path shape. Use the fallback if the corrected request cannot supply relevant evidence.

Otter-KR owns deterministic observations and provenance. This skill owns scope judgment, semantic
interpretation, virtue assessment, refactoring choice, the improvement test, and behavioral
verification. Do not manually redo provider-owned research before or alongside the packet.

Use another provider for questions outside Otter-KR's coverage.
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

### Preserve knowledge across boundaries

Trace a distinction from the producer that knows it to the consumer that needs it. Flag cases
where the producer drops or disguises that distinction and the consumer has to reconstruct it
from types, payload shape, sentinel values, parsing, or context. For example, if a producer
flattens a structured failure into text and callers parse that text to decide whether to
retry, carry the failure reason explicitly. A change in representation can preserve the
distinction through a named field, tag, or domain type. Details can be omitted when consumers
have no use for them.

- Flag parameters whose type changes the operation or side effect. Show what the caller has to
  know to select the intended action. Separate operations or an explicitly tagged request can
  express the choice. Multiple input forms can share a parameter when its purpose stays stable.
- Flag successful result shapes that vary only by count, such as `None`, a record, or a list of
  records for zero, one, or many matches. Once many is possible, use one collection shape for
  all counts. Give genuinely distinct outcomes explicit meanings, such as tagged variants or
  errors.

Cite where the producer knows the distinction, where it is obscured, and a representative
consumer that recovers it. Show the resulting work, such as parsing, type checks, extra paths,
or repeated interpretation rules. Record the finding for existing contracts and account for
caller compatibility when proposing a change.

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
