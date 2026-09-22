# Optional Evidence Providers

Repository-analysis tools strengthen this review but do not own its judgment. The skill must work
without them and must be able to adopt a better provider without changing its reasoning method.

## Capability contract

Request evidence by capability rather than by product name:

| Capability | Questions it can support | Useful virtues | Manual fallback |
| --- | --- | --- | --- |
| Inventory and parse health | What files exist? What cannot be read or parsed? | Working, Coherent | tracked-file listing, test/build commands |
| Names and symbols | Where are definitions, parameters, assignments, and references? | Clear, Easy | `rg`, editor/LSP search, source reading |
| Dependencies and neighborhoods | What is structurally, behaviorally, or historically near this seed? | Coherent, Developed | imports, call sites, tests, Git search |
| Repeated representations | Which literals, groups, helpers, or structures recur? | Unique, Developed, Brief | `rg`, AST/LSP search, side-by-side reading |
| Variable clusters | Which values travel together through scopes, guards, and construction sites? | Developed, Unique, Clear | inspect signatures, call sites, and assignments |
| Object lifecycles | Where is a carrier constructed, changed, aliased, or transitioned? | Developed, Coherent, Easy | trace constructors, fields, and mutations |
| Guards and discriminations | Which predicates, exits, enum branches, or type checks repeat? | Simple, Unique, Coherent | search conditionals and branch bodies |
| Complexity | Where are paths, branches, nesting, or machinery concentrated? | Simple, Clear | read functions and count meaningful paths |
| Tests and mappings | Which tests appear to protect a symbol or rule? | Working, Clear, Easy | search test names/imports and run focused tests |
| Change history | Which files co-change, grow branches, or accumulate repairs? | Easy, Unique, Coherent | bounded Git log, blame, diff, and history search |
| Graph topology | Which modules cluster, bridge, or cross apparent boundaries? | Coherent, Developed | inspect imports and dependency paths |
| Provenance | Can another person reproduce and challenge the observation? | Working, Clear, Coherent | record commands, revisions, paths, and line ranges |

These are evidence categories, not quality scores. A provider may support some capabilities and not
others. A missing capability creates a verification gap, not a failed review.

## Provider selection

Use this order:

1. Ask which evidence capability is needed for the current question.
2. Prefer a connected provider with precise locations, stable ordering, explicit bounds, and
   provenance.
3. Compose providers when their evidence is complementary—for example, a symbol navigator with a
   Git-history analyzer.
4. Use manual repository tools when no provider is available or when the provider's boundary is
   too narrow.
5. Report uncertainty and provider limitations alongside the finding.

Current examples include:

- **Otter-KR:** deterministic Python and Git evidence, including review packets, representation
  inventories, duplicates, variable clusters, object lifecycles, carrier guards, complexity,
  neighborhoods, topology, co-change, and topic history.
- **Serena or similar symbol tools:** potentially strong symbol navigation, references, and
  mechanical source relationships.
- **Graphify or similar graph tools:** potentially strong dependency, topology, and relationship
  projections.

These examples are replaceable. Do not encode their operation names into the core review method.

## Evidence request patterns

### Baseline review

For a bounded change or review scope, obtain an inventory of names, dependencies, tests, history,
and representation signals if a provider can produce it. Otherwise gather the same categories with
ordinary repository tools.

### Focused representation concern

Widen only after an observation warrants it:

- repeated helpers or literals → repeated representations;
- traveling arguments or fields → variable clusters and lifecycle;
- repeated guards or type branches → guards and discriminations;
- difficult change sites → hotspots, co-change, branch growth, or ownership;
- suspected boundary leak → dependencies, neighborhoods, and topology.

Do not request every capability for every review. Prefer the smallest evidence bundle that can
distinguish the plausible interpretations.

### After a refactoring

Re-run the relevant narrow evidence queries when possible. Compare:

- whether the original duplication, cluster, branch, or boundary changed;
- whether ownership became more explicit;
- whether tests and behavior remain protected;
- what indirection, coupling, or uncertainty was introduced.

Changed counts alone do not prove improvement.

## Evidence discipline

For each provider-supported observation, preserve:

```text
Capability:
Provider:
Repository scope and revision:
Query bounds:
Observation and source locations:
Warnings or blind spots:
Manual verification still needed:
```

Then write the review finding separately:

```text
Inference:
Virtues under pressure:
Smallest representation change:
Why necessary:
```

Never turn these observations into automatic claims such as:

- “co-change proves semantic coupling”;
- “a graph bridge is an architectural defect”;
- “structural duplicates are one rule”;
- “a variable cluster requires a new class”;
- “high complexity means bad code.”

Those are judgment calls for the consuming skill and human maintainer.

## Degraded-mode guarantee

The review remains valid without an evidence provider. In degraded mode:

- use source reading, `rg`, tests, editor/LSP facilities, and bounded Git commands;
- preserve the same observation/inference/action format;
- mark unavailable evidence rather than inventing it;
- avoid history-based or topology-based conclusions when the required evidence was not gathered.

An evidence provider improves speed, coverage, reproducibility, and confidence. It does not become
a runtime, installation, or procedural prerequisite for the skill.

## Adding a provider

Document a provider by capability, not by replacing the skill's workflow:

```text
Provider:
Capabilities supported:
Evidence shape and source coordinates:
Bounds and performance considerations:
Known blind spots:
Manual fallback:
```

The provider is ready for use when the same review can run with it, without it, and with another
provider while preserving the skill's judgments, uncertainty, and improvement test.
