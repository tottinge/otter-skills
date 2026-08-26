#!/usr/bin/env python3
"""Validate the portable skill tree and its marketplace manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "otter-skills"
SKILLS = PLUGIN / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^]]*]\((?![a-z]+:|#)([^)]+)\)")


def load_json(path: Path, failures: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("top level must be an object")
        return value
    except (OSError, json.JSONDecodeError, ValueError) as error:
        failures.append(f"{path.relative_to(ROOT)}: {error}")
        return {}


def frontmatter_name(path: Path, failures: list[str]) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        failures.append(f"{path.relative_to(ROOT)}: invalid YAML frontmatter")
        return None
    frontmatter = text[4:text.find("\n---\n", 4)]
    match = re.search(r"(?m)^name:\s*([^\n]+)$", frontmatter)
    if not match:
        failures.append(f"{path.relative_to(ROOT)}: missing frontmatter name")
        return None
    return match.group(1).strip().strip("'\"")


def validate_links(path: Path, failures: list[str]) -> None:
    for target in LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
        local_target = target.split("#", 1)[0]
        if local_target and not (path.parent / local_target).exists():
            failures.append(f"{path.relative_to(ROOT)}: broken relative link {target!r}")


def manifest_versions(
    codex_plugin: dict,
    claude_plugin: dict,
    claude_market: dict,
    copilot_market: dict,
) -> list[object]:
    return [
        codex_plugin.get("version"),
        claude_plugin.get("version"),
        claude_market.get("metadata", {}).get("version"),
        copilot_market.get("metadata", {}).get("version"),
        claude_market.get("plugins", [{}])[0].get("version"),
        copilot_market.get("plugins", [{}])[0].get("version"),
    ]


def main() -> int:
    failures: list[str] = []
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            failures.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
            continue
        name = frontmatter_name(skill_file, failures)
        if name != skill_dir.name:
            failures.append(f"{skill_file.relative_to(ROOT)}: name {name!r} does not match directory")
        if name and not NAME_PATTERN.fullmatch(name):
            failures.append(f"{skill_file.relative_to(ROOT)}: invalid portable skill name {name!r}")

    for markdown in ROOT.rglob("*.md"):
        if ".git" not in markdown.parts and "vendor-sources" not in markdown.parts:
            validate_links(markdown, failures)

    for legal_file in ("LICENSE", "NOTICE"):
        root_copy = ROOT / legal_file
        plugin_copy = PLUGIN / legal_file
        if not plugin_copy.is_file() or plugin_copy.read_bytes() != root_copy.read_bytes():
            failures.append(f"plugins/otter-skills/{legal_file} must match the repository copy")

    codex_plugin = load_json(PLUGIN / ".codex-plugin" / "plugin.json", failures)
    claude_plugin = load_json(PLUGIN / ".claude-plugin" / "plugin.json", failures)
    codex_market = load_json(ROOT / ".agents" / "plugins" / "marketplace.json", failures)
    claude_market = load_json(ROOT / ".claude-plugin" / "marketplace.json", failures)
    copilot_market = load_json(ROOT / ".github" / "plugin" / "marketplace.json", failures)

    versions = manifest_versions(codex_plugin, claude_plugin, claude_market, copilot_market)
    if len(set(versions)) > 1:
        failures.append(f"manifest versions disagree: {versions}")

    codex_source = codex_market.get("plugins", [{}])[0].get("source", {}).get("path")
    if codex_source != "./plugins/otter-skills":
        failures.append("Codex marketplace does not target the canonical plugin")
    for label, document in (("Claude", claude_market), ("Copilot", copilot_market)):
        source = document.get("plugins", [{}])[0].get("source")
        if source != "./plugins/otter-skills":
            failures.append(f"{label} marketplace does not target the canonical plugin")

    if failures:
        print("Repository validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"Validated {len(skill_dirs)} skills and all plugin manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
