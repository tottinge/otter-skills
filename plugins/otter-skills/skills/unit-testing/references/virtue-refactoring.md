# Refactoring and affordable feedback

Refactor toward named virtues while green. Working is non-negotiable; Unique, Simple, Clear, Easy,
Developed, Brief, and Coherent are peers. Do not pursue fewer lines at the expense of behavior or
an understandable representation.

- **Unique / SPOT:** keep each fact in one authoritative home; do not abstract before a real second
  instance exists.
- **Simple:** reduce unnecessary operators, operands, paths, and machinery.
- **Clear:** make intent agree for multiple readers, independently of line count.
- **Easy:** make the likely next change local and understandable.
- **Developed:** introduce a meaningful type or abstraction when the domain has outgrown primitives.
- **Coherent:** align vocabulary and structure with the surrounding system.
- **Brief:** remove excess that adds no value, balanced against the other virtues.

After a green change, ask what was difficult: repeated searching, reconstructed intent, scattered
rules, hidden dependencies, or awkward setup. Give that knowledge a useful name, gather one rule
under one owner, make a dependency explicit, or preserve a surprising contract with a test. Assess
the maintenance work removed or introduced; do not manufacture cleanup.

Keep the coding suite fast enough to run after nearly every edit. Segregate slow tests and replace
slow broad tests of pure logic with microtests where that improves the boundary. Flaky tests destroy
trust; fix over-specification, shared state, time, services, or order dependence rather than
normalizing reruns.
