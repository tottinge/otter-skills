# Provider and Degraded-Mode Evaluation Cases

Use these cases to evaluate whether evidence providers strengthen the skill without becoming a
dependency. The same case should be run with no provider, with the strongest available provider,
and with an alternate provider when one exists.

These are review cases, not automatic smell tests. The expected result is a grounded investigation
with observations, inferences, actions, uncertainty, and a behavior-preservation check.

## Case 1 — Repeated helper knowledge

Plant two helpers with the same structural shape in different modules. Make one pair express the
same rule and another pair coincidentally similar but independently changeable.

Expected investigation:

- find both structural candidates;
- inspect names, callers, tests, and change history;
- consolidate only the duplicated rule;
- preserve the coincidental duplication when coupling it would be worse.

Provider value:

- structural duplicate locations and stable shapes;
- compact evidence suitable for side-by-side inspection.

Degraded mode:

- use `rg`, source reading, tests, and bounded history to establish the same distinction.

## Case 2 — Traveling values and lifecycle

Plant a group of values repeatedly passed together, constructed under shared rules, and manipulated
by several functions. Include one call site where the same names are incidental.

Expected investigation:

- distinguish a possible value object or owner from incidental co-occurrence;
- identify construction rules, invariants, normalization, operations, and aliases;
- propose extraction only when the boundary and behavior are meaningful.

Provider value:

- variable-cluster and object-lifecycle evidence with source coordinates.

Degraded mode:

- inspect signatures, call sites, assignments, constructors, and focused tests manually.

## Case 3 — Repeated decisions and boundary dialects

Plant repeated guards, type/enum checks, a growing conditional, and an import bridge that may be
either an intentional adapter or a missing boundary.

Expected investigation:

- measure paths and branches;
- compare raw and normalized predicates;
- inspect type discrimination and dependency relationships;
- preserve explicit logic when it communicates the domain better than a new abstraction.

Provider value:

- complexity, carrier-guard, discrimination, neighborhood, and topology observations.

Degraded mode:

- read branches, imports, tests, and call sites; count meaningful paths only as supporting evidence.

## Case 4 — Changeability and history

Plant a concept whose implementation spans files that repeatedly change together, plus a nearby
stable complex area that has not required repeated repair.

Expected investigation:

- use a real or imminent change as the boundary;
- distinguish scattered ownership from profitable domain complexity;
- use bounded hotspots, co-change, branch growth, and provenance as leads;
- avoid semantic coupling, causation, or blame claims.

Provider value:

- reproducible history windows, rename-aware co-change, branch additions, and topic provenance.

Degraded mode:

- use bounded Git history, diffs, blame, and source reading while reporting shallow-history limits.

## Acceptance matrix

| Check | No provider | Provider available | Alternate provider |
| --- | --- | --- | --- |
| Produces a useful review | Required | Required | Required when supported |
| Cites source locations | Required | Required | Required |
| Separates observation from inference | Required | Required | Required |
| States unavailable evidence | Required | Required for unsupported dimensions | Required |
| Preserves coincidental duplication | Required | Required | Required |
| Avoids automatic refactoring verdicts | Required | Required | Required |
| Re-evaluates after a change | Manual or tool-assisted | Provider-assisted where possible | Provider-assisted where possible |

An evaluation fails if the provider-enabled path is more authoritative in tone than its evidence,
if the no-provider path blocks, or if two providers produce incompatible reasoning merely because
their operation names differ.
