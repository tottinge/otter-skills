#!/usr/bin/env python3
"""Generate GovKit extension metadata from the canonical skill tree."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "otter-skills"

PREAMBLE = """id: otter-skills
name: Otter Skills
version: {version}
description: >-
  Portable software-craft skills for thin delivery, TDD, safe change, naming,
  refactoring, and trustworthy commits. Installs into your agent's skills
  directory as otter-<skill>.
extension_type: skills
contract_sets: []
origin:
  # govkit rewrites upstream_url and upstream_ref with the actual fetch
  # source and resolved commit at `extension add --from-git` time; the
  # values here are documentation for humans reading the repo.
  upstream_url: https://github.com/tottinge/otter-skills
  upstream_ref: HEAD
  upstream_version: {version}
  license: Apache-2.0
  license_files: [LICENSE, NOTICE]
"""


def render_manifest(skill_names: list[str], version: str) -> str:
    if not skill_names:
        return PREAMBLE.format(version=version) + "skills: []\n"
    declarations = "".join(
        f"  - path: plugins/otter-skills/skills/{name}\n"
        f"    install_as: otter-{name}\n"
        for name in sorted(skill_names)
    )
    return PREAMBLE.format(version=version) + "skills:\n" + declarations


def manifest_for_repository(root: Path) -> str:
    plugin = root / "plugins" / "otter-skills"
    plugin_manifest = json.loads(
        (plugin / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    skill_names = [path.name for path in (plugin / "skills").iterdir() if path.is_dir()]
    return render_manifest(skill_names, plugin_manifest["version"])


def update_manifest(root: Path) -> None:
    (root / "manifest.yaml").write_text(
        manifest_for_repository(root), encoding="utf-8"
    )


def main() -> None:
    update_manifest(ROOT)
    print("Updated manifest.yaml from the canonical skill tree.")


if __name__ == "__main__":
    main()
