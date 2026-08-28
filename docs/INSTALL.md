# Installation

The whole collection is available as the `otter-skills` plugin. Individual skills can also be installed from `plugins/otter-skills/skills/<name>`.

The examples below assume the repository is hosted as `tottinge/otter-skills`. When working from another fork, substitute that owner and repository.

## Codex

After cloning the repository, register its local marketplace and install the plugin:

```bash
codex plugin marketplace add /absolute/path/to/otter-skills
codex plugin add otter-skills@otter-skills
```

For one skill, ask Codex's built-in skill installer to install the GitHub directory URL, for example:

```text
$skill-installer install https://github.com/tottinge/otter-skills/tree/main/plugins/otter-skills/skills/unit-testing
```

Manual user-level installation also works by copying or linking a skill directory into `~/.codex/skills/`.

## Claude Code

From Claude Code:

```text
/plugin marketplace add tottinge/otter-skills
/plugin install otter-skills@otter-skills
```

For one skill, copy or link its directory into `~/.claude/skills/`. For a project-only installation, use `<project>/.claude/skills/`.

## GitHub Copilot CLI

The plugin includes an explicit Copilot manifest at `plugins/otter-skills/.github/plugin/plugin.json`; it does not depend on Copilot's Claude-manifest fallback.

From Copilot CLI:

```text
/plugin marketplace add tottinge/otter-skills
/plugin install otter-skills@otter-skills
```

Copilot also discovers individual skills in project-level `.github/skills/`, `.agents/skills/`, and `.claude/skills/`, or user-level `~/.copilot/skills/` and `~/.agents/skills/`.

## Warp and other Agent Skills clients

Copy or link an individual directory into a supported Agent Skills root. `~/.agents/skills/` is the most portable user-level choice when the client supports it; `.agents/skills/` is the corresponding project-local location.

Example from a clone:

```bash
ln -s /absolute/path/to/otter-skills/plugins/otter-skills/skills/story-splitting-for-delivery ~/.agents/skills/story-splitting-for-delivery
```

## Packaged archives

Run:

```bash
python3 scripts/package_skills.py
```

This creates one deterministic `dist/<skill-name>.skill` ZIP archive per skill. Use a client's archive-import flow when it has one, or unzip the archive into one of the skill roots above.

## Verify an installation

Ask the agent to list available skills, or invoke a skill by name—for example, “use `story-splitting-for-delivery` to split this feature.” Skill discovery and invocation wording differ slightly by client.
