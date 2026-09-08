import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "update_govkit_manifest.py"
SPEC = importlib.util.spec_from_file_location("update_govkit_manifest", MODULE_PATH)
update_govkit_manifest = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(update_govkit_manifest)


class GovkitManifestRenderingTest(unittest.TestCase):
    def test_empty_inventory_is_an_empty_yaml_list(self):
        manifest = update_govkit_manifest.render_manifest([], "1.2.3")

        self.assertTrue(manifest.endswith("skills: []\n"), manifest)

    def test_one_skill_is_declared_from_its_directory_name(self):
        manifest = update_govkit_manifest.render_manifest(["unit-testing"], "1.2.3")

        self.assertIn("version: 1.2.3\n", manifest)
        self.assertIn("upstream_version: 1.2.3\n", manifest)
        self.assertIn(
            "  - path: plugins/otter-skills/skills/unit-testing\n"
            "    install_as: otter-unit-testing\n",
            manifest,
        )

    def test_skills_are_declared_in_stable_name_order(self):
        manifest = update_govkit_manifest.render_manifest(
            ["unit-testing", "atomic-commit"], "1.2.3"
        )

        self.assertLess(manifest.index("atomic-commit"), manifest.index("unit-testing"))

    def test_repository_manifest_discovers_skills_and_plugin_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "plugins" / "otter-skills"
            (plugin / ".codex-plugin").mkdir(parents=True)
            (plugin / ".codex-plugin" / "plugin.json").write_text(
                json.dumps({"version": "2.3.4"}), encoding="utf-8"
            )
            (plugin / "skills" / "unit-testing").mkdir(parents=True)
            (plugin / "skills" / "atomic-commit").mkdir()

            manifest = update_govkit_manifest.manifest_for_repository(root)

        self.assertIn("version: 2.3.4\n", manifest)
        self.assertLess(manifest.index("atomic-commit"), manifest.index("unit-testing"))

    def test_update_writes_the_discovered_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "plugins" / "otter-skills"
            (plugin / ".codex-plugin").mkdir(parents=True)
            (plugin / ".codex-plugin" / "plugin.json").write_text(
                json.dumps({"version": "3.4.5"}), encoding="utf-8"
            )
            (plugin / "skills" / "atomic-commit").mkdir(parents=True)

            update_govkit_manifest.update_manifest(root)

            manifest = (root / "manifest.yaml").read_text(encoding="utf-8")
        self.assertIn("version: 3.4.5\n", manifest)
        self.assertIn("install_as: otter-atomic-commit\n", manifest)


if __name__ == "__main__":
    unittest.main()
