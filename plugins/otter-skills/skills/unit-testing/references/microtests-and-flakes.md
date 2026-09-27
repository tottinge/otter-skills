# FIRST microtests and flaky-test diagnosis

## FIRST

| Letter | Meaning |
| --- | --- |
| F | Fast: milliseconds preferred; no real services in a microtest |
| I | Isolated: no shared mutable state; any order |
| R | Repeatable: control time, randomness, threads, and environment |
| S | Self-verifying: assertions, not manual log inspection |
| T | Timely: written before or with the production behavior |

Keep decisions and transformations real. Fake collaborators only at meaningful boundaries. Do not
let production branch on whether it is being tested. Microtests do not replace higher-level tests.

Before accepting a test as green, inspect inputs that can affect its assertion: time zone, clock,
randomness, scheduling, iteration order, process environment, locale, files, ports, databases,
networks, credentials, permissions, and pre-existing records. Control each relevant input or use a
test-specific isolated environment.

Run a changed test alone and in its containing suite. Vary order or retain a runner seed when that
can reveal contamination. For concurrency or prior flakes, repeat enough to investigate likely
intermittency; rerun-until-green is not acceptance evidence. Synchronize on observable events,
not guessed sleeps. Assert unordered results without relying on incidental order.

## Diagnose before repairing

| Symptom | Investigate first |
| --- | --- |
| Intermittent failure | clock, threads, randomness, environment, or actual production race |
| Passes alone but fails in suite | shared state, static cache, database residue, fixture leakage |
| CI-only failure | environment, concurrency, permissions, or order dependence |
| Slow and unstable | real network/database/service calls or oversized fixtures |
| Weak failure signal | missing assertion or reliance on logs/manual inspection |

Do not assume a flaky test is defective: a reliable test may expose flaky production behavior such
as races, lost updates, nondeterministic ordering, overflow, or clock-boundary defects. Vary one
relevant dimension at a time, locate the uncontrolled input, and repair the cause. Do not weaken,
ignore, quarantine, or rerun past an assertion merely because it is intermittent.

## Structure-shy tests

Assert outcomes and contractual effects, not private fields, helper names, delegation sequences,
or deep navigation such as `a.b.c.d`. Test names and assertions should diagnose the mistake. Avoid
magic values and side-effect-heavy fixtures; if a test needs many shared effects, inspect cohesion
and the unit boundary.
