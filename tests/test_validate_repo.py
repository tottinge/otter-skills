import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "validate_repo.py"
SPEC = importlib.util.spec_from_file_location("validate_repo", MODULE_PATH)
validate_repo = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_repo)


class ManifestVersionsTest(unittest.TestCase):
    def test_includes_marketplace_plugin_entry_versions(self):
        versions = validate_repo.manifest_versions(
            {"version": "codex-plugin"},
            {"version": "claude-plugin"},
            {
                "metadata": {"version": "claude-marketplace"},
                "plugins": [{"version": "claude-entry"}],
            },
            {
                "metadata": {"version": "copilot-marketplace"},
                "plugins": [{"version": "copilot-entry"}],
            },
        )

        self.assertEqual(
            versions,
            [
                "codex-plugin",
                "claude-plugin",
                "claude-marketplace",
                "copilot-marketplace",
                "claude-entry",
                "copilot-entry",
            ],
        )


if __name__ == "__main__":
    unittest.main()
