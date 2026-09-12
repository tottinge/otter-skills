# Effect Reconnaissance and Scooping

Read this reference before executing code with reachable database, messaging,
network, filesystem, subprocess, background-work, or global-state behavior. Also
read it when a meaningful decision is interleaved with several related effects.

## Inspect before execution

Inspect the test command and trace the target and relevant callees far enough to identify:

- effects during imports, test discovery/collection, fixtures, setup, teardown, and cleanup
- direct and transitive effects, including framework hooks and lifecycle callbacks
- resource, credential, endpoint, queue, process, path, and global-state selection
- effect ordering, transaction or cleanup boundaries, retries, and exception behavior
- existing seams and the actual owner of each decision or transformation

Do not characterize against production resources or credentials. If a reachable
effect remains unknown or cannot be redirected to a disposable, observable target,
classify the boundary as **BLOCKED** and report what must be learned or contained.
Use disposable resources with explicit paths and endpoints; prevent fallback to live
credentials or production defaults. Contain subprocesses and background work and
ensure cleanup touches only resources owned by this run. A pure target does not
make an effectful import or fixture safe. Apply this check before the first baseline
run and before unfamiliar mutation tooling. Once containment is known, routine
runs need no new permission. Static checks may support an intermediate extraction,
but they do not prove the boundary safe.

## Escalate containment gradually

Use the least intrusive move that provides control and observation:

1. Reuse an existing seam.
2. Extract one dangerous call into a replaceable function.
3. Parameterize the effectful dependency.
4. If substantial logic is interleaved with several related effects, use a staged
   support-adapter scoop.

For a single-call seam, preserve the exact arguments, result, exception behavior,
ordering, and lifecycle while moving only that call. Prove preservation before
changing behavior.

## Staged support-adapter scoop

Use a scoop only when the target retains substantial decisions or transformations.
The intended shape is:

```text
x(...) -> constructs ProductionXSupport -> do_x(..., support)
ProductionXSupport -> performs dangerous operations
do_x -> owns decisions, transformations, and effect intentions
tests -> call do_x with a minimal FakeXSupport
```

Keep `x(...)` as the unchanged production entry point. Extract effects one at a
time, preserving arguments, results, exceptions, ordering, resource ownership, and
cleanup. Shape support methods around capabilities the logic needs, rather than
copying an external library's full API.

Tests should protect decisions, transformations, and generated effect intentions.
Do not assert every incidental top-to-bottom delegation step. A fake should be a
small, safe implementation or recorder, not a simulation of the production system.

## Improvement and reversion test

Review the improvement after each extraction. During a staged scoop, use static preservation checks while remaining effects prevent safe execution; keep the classification **NEEDS_SEAM** or **BLOCKED**. At the first contained boundary, require executable evidence for all of the following:

- `do_x` still contains meaningful policy or transformation.
- `FakeXSupport` is smaller and safer than `ProductionXSupport`.
- tests can fail for a relevant behavioral mutation, not merely execute the lines.
- the safety gained is worth the added boundary.

If `do_x` becomes empty or a linear mirror of support calls, revert the extraction
experiment and classify the target as **COMPOSED**. Consider a contained integration
or contract test only for an important external composition guarantee, or inspect a
deeper callee for the decision that deserves focused protection.
