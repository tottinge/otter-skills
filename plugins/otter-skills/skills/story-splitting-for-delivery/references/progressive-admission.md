# Progressive admission

Use this reference when writing the actual admission plan or reviewing whether a
slice is thin enough.

## Target shape

A good admission slice:

- keeps the full end-to-end path wired
- admits exactly one new case, shape, type, field set, or rule
- continues to reject all non-admitted cases with a stable response
- is unit-testable and end-to-end testable
- produces an observable result that can be demonstrated without later slices
- could be deployed without harming unhandled traffic
- leaves room to TDD and refactor after green

## Required plan format

```markdown
# Progressive admission plan: <capability>

## Admission boundary
- **Admits:** <what varies: messages, shapes, ops, fields, rules>
- **Default reject:** <stable not-implemented / invalid response>
- **End-to-end path:** <entry -> guard -> process -> result>

## Slice 0 — Start closed
- **Admits:** nothing useful
- **Behavior:** every input rejected by the established pattern
- **Someone invokes:** <how a client or stakeholder exercises the closed path>
- **Observable result:** <stable rejection, error, status, or diagnostic>
- **Independent demonstration:** <how to show it without later slices>
- **User/stakeholder value:** clients, errors, deploy path, and tests work end to end
- **Acceptance checks:**
  - <check>
  - <check>
- **Still rejected:** everything

## Slice 1 — <first admission title>
- **Admits:** <exact case>
- **Behavior:** <what happens for that case only>
- **Someone invokes:** <action or input>
- **Observable result:** <what the invoker can see or use>
- **Independent demonstration:** <how to show it without later admissions>
- **User/stakeholder value:** <why this admission matters now>
- **Acceptance checks:**
  - admitted case works
  - non-admitted cases still reject stably
- **Still rejected:** <explicit remainder>
```

For every slice after 0, keep both the newly admitted case and the still-rejected
remainder explicit.

## Sequencing heuristics

When uncertain, prefer:

1. closed skeleton
2. reject, health, and guard behavior
3. simplest valid admission
4. most common real case
5. high-risk or high-learning variants
6. polish, performance, and broad edge coverage

Bargain-hunt each next admission for learning or value per effort, deployment
safety, and ease of isolated testing. Reassess after each demonstration:

- **Value:** does the delivered behavior satisfy the need?
- **Uncertainty:** which consequential assumption is least supported?
- **Constraint:** where is delivery waiting or requiring rework?

Choose to continue, change direction, or stop from that evidence. If feedback is
unavailable, keep the uncertainty visible.

## Versioning

When interfaces are versioned, adding an admitted message or shape is usually a
minor bump; changing or removing a shipped contract is major. Only changes to
already-shipped contracts are breaking.

## Anti-patterns

- Build all processors first and wire the entry point last.
- Call “support all message types” one story.
- Split horizontally into schema, service, and UI stories.
- Open the guard to pass everything before implementations exist.
- Treat rejection as temporary junk instead of a productized path.
- Over-specify later admissions before Slice 0 and Slice 1 teach anything.
- Call component tasks admissions.

## Facilitation script

For a 20–30 minute planning session:

1. Name capability, users/clients, and input-process-output cycle.
2. Define the admission boundary and default rejection.
3. Write Slice 0 and its checks.
4. List candidate admissions; pick the first 2–4 by simplicity, value, and risk.
5. Write the exact admitted case and still-rejected remainder for the next slice.
6. Note versioning implications when contracts are external.

## Micro-example

For queue messages that update accounts:

1. Start closed: consume the message and return `not_implemented`.
2. Admit an ill-formed envelope with a structured `invalid_message` error.
3. Admit a health ping returning `ok`.
4. Admit the minimal `AccountOpened` shape.
5. Admit its optional display name.
6. Admit `AccountClosed`.

Unknown types remain on the stable rejection path. Demonstrate each admission
with the newly admitted message and an unadmitted message.
