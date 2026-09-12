# otter-skills

Portable agent skills for software craft, drawn primarily from Tim Ottinger's writing (Agile Otter, Industrial Logic) and related practice notes.

The repository is both a plugin marketplace and a directly installable Agent Skills collection for Codex, Claude Code, GitHub Copilot CLI, Warp, and other tools that discover `SKILL.md` trees.

## Skills

| Skill | Purpose |
| --- | --- |
| `atomic-commit` | Preserve trustworthy history as complete, green, human-vetted repository states |
| `story-splitting-for-delivery` | Split work through progressive admission: start closed, admit one case, default-reject the rest |
| `user-pov-sliced-stories` | Format chosen slices as **User invokes** / **User uses result** |
| `unit-testing` | Protect evidence-backed behavioral rules with safe, isolated FIRST microtests |
| `representation-refactor-review` | Review through the Eight Code Virtues, including ZOM representation drift |
| `code-object-naming` | Improve code-object names using the naming short-guide workflow |
| `legacy-code-safety` | Infer rules from callers and callees, contain effects, and prove protection before risky changes |

The canonical skill trees live in [`plugins/otter-skills/skills/`](plugins/otter-skills/skills/). Each directory basename matches its `SKILL.md` frontmatter `name`.

## Host compatibility

The plugin keeps one canonical `skills/` tree and exposes host-specific discovery metadata around it:

| Host | Plugin manifest | Marketplace manifest |
| --- | --- | --- |
| Codex | `plugins/otter-skills/.codex-plugin/plugin.json` | `.agents/plugins/marketplace.json` |
| Claude Code | `plugins/otter-skills/.claude-plugin/plugin.json` | `.claude-plugin/marketplace.json` |
| GitHub Copilot CLI | `plugins/otter-skills/.github/plugin/plugin.json` | `.github/plugin/marketplace.json` |

Keeping the skills canonical avoids copies drifting between hosts. Each manifest points its host to the same `plugins/otter-skills/skills/` directories.

## Install

Install the complete collection as a plugin, or install/copy individual skill directories. See [Installation](docs/INSTALL.md) for Codex, Claude Code, Copilot CLI, project-local, and manual instructions.

## Repository layout

```text
otter-skills/
  manifest.yaml                           # generated GovKit extension manifest
  .agents/plugins/marketplace.json       # Codex marketplace
  .claude-plugin/marketplace.json        # Claude marketplace
  .github/plugin/marketplace.json        # Copilot marketplace
  plugins/otter-skills/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    .github/plugin/plugin.json
    skills/<skill-name>/SKILL.md
  scripts/
    package_skills.py
    update_govkit_manifest.py
    validate_repo.py
  dist/                                  # reproducible per-skill archives
  docs/
```

Run `python3 scripts/update_govkit_manifest.py` after adding or removing a skill, then run `python3 scripts/validate_repo.py` before publishing. The validator rejects a stale GovKit inventory. Run `python3 scripts/package_skills.py` to rebuild `dist/`.

## Dogfood evaluations

The `legacy-code-safety` skill has an opt-in behavioral A/B harness with disposable
Python and Node.js fixture repositories. Live trials require an explicit model and
do not run in CI:

```bash
python3 evals/legacy-code-safety/dogfood.py run --model MODEL --mode smoke
python3 evals/legacy-code-safety/dogfood.py run --model MODEL --mode release
```

To validate the current installed skills with Otter-KR MCP evidence on the fixtures,
use the single-arm workflow:

```bash
python3 evals/legacy-code-safety/dogfood.py run --model MODEL --mode smoke --keep-workspaces --otter-kr /absolute/path/to/otter-kr
```

This uses the checkout's existing `.venv/bin/python` and its `research` MCP tool.
It keeps installed skills enabled, requires MCP use, and records the workflow in
the result. Trials run sequentially, with one stdio support server owned by each
Codex invocation. Confirm support processes have stopped before final verification.
Otter-KR supplies static evidence; inspect sources and execute contained tests to
establish behavioral rules and sensitivity. Its Python and tracked-file limits
must remain visible in the assessment. This workflow is not an A/B comparison.

Smoke mode runs each control/treatment arm once; release mode runs each arm three
times. The command prints an ignored result directory containing transcripts,
diffs, deterministic scores, and `review.json`. Complete that human-review file,
then finalize the run:

```bash
python3 evals/legacy-code-safety/dogfood.py finalize RUN_DIR --review RUN_DIR/review.json
```

Any critical treatment safety failure blocks the run. Control failures remain in
the report as comparative evidence.

The fixtures cover caller compatibility, composed functions, misleading doubles,
multiple transformation rules, and effects during test collection. Treatment
trials receive matching snapshots of both testing skills. Reports record their
hashes, inferred rules, protection gaps, and containment evidence. Review includes
the generated tests, not just the model's summary.

Generated tests and mutations run through `codex sandbox -P :workspace`, with a
clean environment and bounded execution. A failed baseline skips mutation checks;
setup errors do not count as detected behavioral mutations. Use a CLI version
supporting that sandbox command and the explicitly selected model. The harness
stops on an execution failure and never falls back to unrestricted test execution.
Untracked generated files are saved with the transcripts for review.

## License

Licensed under Apache-2.0 for commercial and open-source use. See [LICENSE](LICENSE). The [NOTICE](NOTICE) file preserves credit for the writers and practitioners whose published work materially informed these skills; more specific source notes remain beside the relevant skills.

## Sources

- Agile Otter — progressive admission, story splitting, Eight Code Virtues, FIRST, and microtesting
- Industrial Logic — TDD purposes and practices, structure-shy tests, and software-craft writing
- Tim Ottinger's naming short-guide manuscript
- Kent Beck, Michael Feathers, Martin Fowler, Emily Bache, Llewellyn Falco, and GeePaw Hill — see [NOTICE](NOTICE) and skill-local source notes

## Contributing

Keep each change coherent and the repository green. Update the canonical plugin tree only; generated archives belong in `dist/`. Contributions are accepted under the repository's Apache-2.0 license.
