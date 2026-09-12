# Characterization and Approval Testing

Read this reference when existing behavior is poorly understood or the useful observable result is too large for a few focused assertions.

## Characterization loop

1. Choose one input relevant to the requested change.
2. Invoke the current production path through the narrowest safe boundary.
3. Begin with an expectation known to be wrong, or with unapproved output.
4. Run the code and observe the actual result.
5. Inspect whether the observation is meaningful, stable, and safe to retain.
6. Record the observation and name the behavior it demonstrates.
7. Infer a rule using target, caller, and callee evidence; challenge it with distinguishing boundaries or counterexamples.
8. Map cases and assertions to that rule, and repeat for the selected unit’s meaningful decisions and transformations.

Expected values come from execution. Documentation, tickets, comments, and the agent's interpretation may explain an observation, but they do not replace it.

If behavior appears defective, record:

```text
Observed behavior:
Reason it may be defective:
Known consumers or compatibility risk:
Decision needed:
```

Do not silently repair it during baseline characterization.

## When approval testing fits

Prefer an approval artifact when the result is structured and broad enough that individual assertions would hide the whole:

- reports and rendered documents
- serializers, parsers, and transformations
- command-line output
- combinations of many business-rule cases
- a stable event or call trace at a subsystem boundary

Use focused assertions when the important result is small. Approval testing is not a reason to snapshot an entire application or object graph.

## Approval loop

1. Arrange representative input.
2. Act through a safe boundary.
3. Render only relevant results in a stable, human-readable form.
4. Diff received output against the approved artifact.
5. Inspect every meaningful difference.
6. Approve intentionally and keep the artifact with the test.

Before approval, control or remove timestamps, random identifiers, unstable ordering, machine paths, concurrency noise, secrets, personal data, and irrelevant bulk.

Never update approved output merely to make a failing suite green. A changed artifact is evidence requiring a decision.

## Demonstrate sensitivity

Execution and coverage are not enough. An initial incorrect expectation verifies
comparison, not sensitivity to a production regression. For each meaningful rule,
confirm that its assertions detect a violation using an observed relevant failure,
or a focused perturbation where evidence is missing. Temporarily alter a protected
value or decision, run the contained test, and restore only the experiment's edits;
or use a contained mutation tool and inspect relevant survivors. Preserve unrelated
work and inspect the tool's setup and cleanup before running it.

Record gaps per rule. A mutation caught for one branch does not establish protection
for another decision or transformation.

Use coverage to find relevant branches not exercised, not as a quality target.

## Retirement

Keep broad characterization while it provides unique protection. As understanding improves, replace noisy approval output with focused behavioral tests where that makes failures faster and clearer. Retire an artifact only when equivalent protection is demonstrated.
