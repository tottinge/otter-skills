# Test selection and Tidy First?

## ZOMBIES

Maintain the test list and choose one next case:

1. **Zero** — null, empty, or trivial input.
2. **One** — one simple instance.
3. **Many** — the general case after Zero and One pass.
4. At each level consider **Boundary**, **Interface**, and **Exception** separately.

Do not write a Many-complexity test before Zero and One are understood. Write one test at a time;
batching tests commits to an interface before the first implementation can teach you.

## Tidy First?

Before each next test, choose explicitly:

- **First** — structure blocks the test. Make a behavior-preserving structural change, verify green
  before and after, then write the test.
- **After** — structure is adequate. Implement behavior, then tidy in the green refactor step.
- **Later** — useful but not blocking. Record it in the project's normal tracking place.
- **Never** — the cost exceeds the demonstrated benefit. Say why and move on.

Prefer LSP or `ast-grep` for mechanical renames and extracts. Use judgment to choose the target
representation, not to hand-type a mechanical transformation across many call sites.
