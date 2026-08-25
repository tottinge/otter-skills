# otter-skills

Portable agent skills for software craft, drawn primarily from Tim Ottinger’s writing (Agile Otter, Industrial Logic) and related practice notes.

These skills are meant to install cleanly for **Claude**, **Codex**, **Copilot**, and **Warp** (and other tools that discover `SKILL.md` trees).

## Skills

| Skill | Purpose |
|-------|---------|
| `atomic-commit` | Preserve trustworthy history as complete, green, human-vetted repository states |
| `story-splitting-for-delivery` | Primary story splitter via **progressive admission** (start closed → admit one case → default reject) |
| `user-pov-sliced-stories` | Format slices as **User invokes** / **User uses result** (formatter; defers split choice) |
| `unit-testing` | Microtests + TDD hygiene (FIRST, Canon TDD, ZOMBIES, Tidy First?, virtue-targeted refactor) |
| `representation-refactor-review` | Review through the **Eight Code Virtues**, including ZOM representation drift |
| `code-object-naming` | Naming guidance distilled from the short guide to naming manuscript |
| `legacy-code-safety` | Characterize poorly understood behavior, create minimal seams, and change risky existing code safely |

Skill bodies live under `skills/<name>/` with a required `SKILL.md`.

## Install

Each skill is a directory containing `SKILL.md` (and optional `references/`, `agents/openai.yaml`, etc.).

### Global (user home)

Copy or symlink a skill folder into any of:

- `~/.agents/skills/` (recommended for Warp)
- `~/.claude/skills/`
- `~/.codex/skills/`
- `~/.copilot/skills/`
- `~/.cursor/skills/` (and other tool-specific skill roots)

Example:

```bash
ln -s "$PWD/skills/story-splitting-for-delivery" ~/.agents/skills/story-splitting-for-delivery
ln -s "$PWD/skills/story-splitting-for-delivery" ~/.claude/skills/story-splitting-for-delivery
ln -s "$PWD/skills/story-splitting-for-delivery" ~/.codex/skills/story-splitting-for-delivery
ln -s "$PWD/skills/story-splitting-for-delivery" ~/.copilot/skills/story-splitting-for-delivery
```

### Project-local

The same directories work under a repo root, e.g. `.agents/skills/`, `.claude/skills/`, `.codex/skills/`, `.copilot/skills/`.

### Packaged `.skill` files

When present, zip packages will live in `dist/` (one `.skill` per skill directory). Install using your tool’s skill-package flow, or unzip into a skills root.

## Layout

```text
otter-skills/
  README.md
  LICENSE                 # pending final choice
  docs/
    PLAN.md               # consolidation / packaging plan
  skills/
    atomic-commit/
    story-splitting-for-delivery/
    user-pov-sliced-stories/
    unit-testing/
    representation-refactor-review/
    code-object-naming/
    legacy-code-safety/
  dist/                   # generated .skill packages
  vendor-sources/         # optional read-only snapshots used while authoring
```

## Status

**Content drafted; integration validation in progress.** See [docs/PLAN.md](docs/PLAN.md).

## License (pending)

Intended for free and commercial use. Final license text is **not** chosen yet (`LICENSE` is a stub). Options under consideration include MIT, Apache-2.0, and CC BY 4.0 (and similar). Decide after the skill set is populated.

## Sources (high level)

- Agile Otter — progressive admission, story splitting listicle, Eight Code Virtues, FIRST/microtesting
- Industrial Logic — TDD purposes/practices, structure-shy tests, craft writing
- Naming short guide manuscript (`naming_shortguide`)
- Local skill drafts under `~/.agents/skills`, `~/Projects/otter-skill`, `~/Projects/tdd-skill`, and `~/Downloads/canonical-tdd-skill.md`

## Contributing / working here

Work in this repository from here forward. Prefer small commits. Do not expand scope into license bikeshedding until skills are in place.
