# Otter-KR Provider Guide

Otter-KR is an optional deterministic evidence provider for this skill. It supplies citeable
observations; the review skill and maintainer remain responsible for interpretation, refactoring
choice, and behavioral verification.

## First query: bounded review packet

Use one of these operations for the baseline:

| Review scope | Operation | Use |
| --- | --- | --- |
| One selected file | `git.review_packet.file` | Names, dependencies, tests, history, and representation signals for one file |
| Several selected files | `git.review_packet.files` | The same evidence for a bounded set of files |
| Whole review scope | `git.review_packet` | Use only when the broader scope is intentional |
| Explicit historical revision | `git.review_packet.revision` | History-only context when current-tree Python evidence would mislead |

Every request needs an explicit repository root. Bounded history requests need an explicit positive
time boundary and limit. Preserve the packet's scope, revision, warnings, truncation, and source
locations in the review notes.

The packet can provide:

- names and symbols;
- Python import/dependency edges;
- candidate test mappings;
- history snapshots and hotspots;
- repeated groups and structural duplicate candidates;
- branch growth and ownership observations.

These are baseline observations. None proves semantic ownership, test execution, bad design, or a
required refactoring.

## Widen only on a signal

After reading the packet, request a narrower focused operation only when its evidence is relevant:

| Packet signal | Focused operation | Question |
| --- | --- | --- |
| repeated helpers or structures | `python.duplicates.compact` | Are these structurally repeated candidates? |
| repeated parameter/field groups | `python.groups` | Which ordered groups recur and where? |
| traveling variables | `python.variable_cluster` | Which names, scopes, guards, and construction sites co-occur? |
| carrier construction or mutation | `python.object_lifecycle` | How is the carrier built, changed, aliased, or transitioned? |
| repeated guard predicates | `python.carrier_guards` | Which guard shapes and effects recur? |
| branching/type pressure | `python.complexity` or `python.discriminations` | Where are paths or type distinctions represented? |
| changeability concern | `git.hotspots`, `git.cochange.file`, or `git.branch_additions` | What does bounded history say about coordinated change? |

Do not run every operation by default. A focused query should answer a live question raised by the
baseline or source reading.

## Structural evidence interpretation

Use these operations as a sequence of increasingly specific observations:

1. `python.duplicates.compact` identifies repeated helper structure with bounded shape facts and
   occurrence locations.
2. `python.groups` identifies repeated ordered parameter or field groups.
3. `python.variable_cluster` follows explicitly supplied names through scopes, guards, aliases,
   construction sites, tests, and bounded history.
4. `python.object_lifecycle` follows one carrier through construction, field operations,
   transitions, aliases, and boundaries.

The first two establish repetition; the latter two investigate whether the repetition has a
potential concept boundary. Keep the interpretations separate:

```text
Structural observation → candidate relationship → source/test inspection → refactoring choice
```

For example, a repeated parameter group is evidence that a value object may exist, not evidence
that one should be introduced. Shared construction rules, invariants, normalization, or behavior
are the additional evidence needed before recommending that move.

When a cluster or lifecycle report is broad, narrow the query with explicit names or a path bound
and preserve the report's warnings and parse failures. Do not infer object identity from a shared
identifier alone.

## Control-flow and boundary interpretation

Use the following operations to investigate Simple and Coherent pressure:

- `python.complexity` reports branch, nesting, line, and cyclomatic-style observations by function;
- `python.carrier_guards` reports repeated predicates, early exits, else guards, effects, and
  normalized shapes for a selected carrier;
- `python.discriminations` reports declarations, comparisons, and lookups for a selected type;
- `python.imports` and `python.neighborhood.*` report statically visible relationships around a
  module or seed;
- `python.graph_topology` reports graph structure, communities, bridges, and formulas.

Interpret these in stages:

```text
machinery count → repeated decision/boundary evidence → source/test inspection → representation choice
```

Complexity is not a badness score. A graph bridge is not automatically a boundary leak. A repeated
guard is not automatically one rule. A type discrimination is not automatically a demand for
polymorphism. The source, tests, local dialect, and likely change must justify the action.

For graph and neighborhood evidence, preserve the relationship reason, edge provenance, filters,
and topology formulas. Do not collapse structural, behavioral, historical, and import relationships
into one unexplained coupling claim.

## Manual fallback

When Otter-KR is absent, unavailable, or outside its Python/tracked-file boundary:

- inspect the selected files directly;
- use `rg` for names, literals, helpers, and guards;
- inspect imports and test references;
- use bounded Git history, diff, blame, and co-change commands where appropriate;
- record the same observations, locations, bounds, and uncertainty in the review.

Do not stage files merely to make them visible to Otter-KR. New or untracked files require direct
inspection or a separately controlled fixture.

## Interpretation guardrails

Otter-KR intentionally reports evidence rather than design conclusions. In particular:

- co-change is not semantic coupling;
- a duplicate fingerprint is not proof of duplicated knowledge;
- a variable cluster is not proof that a value object is warranted;
- a lifecycle report is not proof that a class should be extracted;
- branch growth is not proof of harmful complexity;
- test mapping is not runtime coverage;
- ownership observations are not blame.

Use each observation to form a hypothesis, inspect the source and tests, propose the smallest
representation change, and apply the improvement test.
