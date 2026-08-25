# otter-skills

Portable agent skills for software craft, drawn primarily from Tim Ottinger's writing (Agile Otter, Industrial Logic) and related practice notes.

The repository is both a plugin marketplace and a directly installable Agent Skills collection for Codex, Claude Code, GitHub Copilot CLI, Warp, and other tools that discover `SKILL.md` trees.

## Skills

| Skill | Purpose |
| --- | --- |
| `atomic-commit` | Preserve trustworthy history as complete, green, human-vetted repository states |
| `story-splitting-for-delivery` | Split work through progressive admission: start closed, admit one case, default-reject the rest |
| `user-pov-sliced-stories` | Format chosen slices as **User invokes** / **User uses result** |
| `unit-testing` | Apply FIRST microtests and the Clean Start → Tidy? → Red → Green → Refactor → Atomic Commit → Integrate loop |
| `representation-refactor-review` | Review through the Eight Code Virtues, including ZOM representation drift |
| `code-object-naming` | Improve code-object names using the naming short-guide workflow |
| `legacy-code-safety` | Characterize behavior, create minimal seams, and change risky existing code safely |

The canonical skill trees live in [`plugins/otter-skills/skills/`](plugins/otter-skills/skills/). Each directory basename matches its `SKILL.md` frontmatter `name`.

## Install

Install the complete collection as a plugin, or install/copy individual skill directories. See [Installation](docs/INSTALL.md) for Codex, Claude Code, Copilot CLI, project-local, and manual instructions.

## Repository layout

```text
otter-skills/
  .agents/plugins/marketplace.json       # Codex marketplace
  .claude-plugin/marketplace.json        # Claude marketplace
  .github/plugin/marketplace.json        # Copilot marketplace
  plugins/otter-skills/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    skills/<skill-name>/SKILL.md
  scripts/
    package_skills.py
    validate_repo.py
  dist/                                  # reproducible per-skill archives
  docs/
```

Run `python3 scripts/validate_repo.py` before publishing. Run `python3 scripts/package_skills.py` to rebuild `dist/`.

## License

Licensed under Apache-2.0 for commercial and open-source use. See [LICENSE](LICENSE). The [NOTICE](NOTICE) file preserves credit for the writers and practitioners whose published work materially informed these skills; more specific source notes remain beside the relevant skills.

## Sources

- Agile Otter — progressive admission, story splitting, Eight Code Virtues, FIRST, and microtesting
- Industrial Logic — TDD purposes and practices, structure-shy tests, and software-craft writing
- Tim Ottinger's naming short-guide manuscript
- Kent Beck, Michael Feathers, Martin Fowler, Emily Bache, Llewellyn Falco, and GeePaw Hill — see [NOTICE](NOTICE) and skill-local source notes

## Contributing

Keep each change coherent and the repository green. Update the canonical plugin tree only; generated archives belong in `dist/`. Contributions are accepted under the repository's Apache-2.0 license.
