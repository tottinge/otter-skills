import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "validate_repo.py"
SPEC = importlib.util.spec_from_file_location("validate_repo", MODULE_PATH)
validate_repo = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_repo)


def matching_manifests():
    return {
        "codex_plugin": {"version": "1.2.3"},
        "claude_plugin": {"version": "1.2.3"},
        "copilot_plugin": {"version": "1.2.3"},
        "codex_market": {
            "plugins": [{"source": {"path": "./plugins/otter-skills"}}]
        },
        "claude_market": {
            "metadata": {"version": "1.2.3"},
            "plugins": [
                {
                    "source": "./plugins/otter-skills",
                    "version": "1.2.3",
                }
            ],
        },
        "copilot_market": {
            "metadata": {"version": "1.2.3"},
            "plugins": [
                {
                    "source": "./plugins/otter-skills",
                    "version": "1.2.3",
                }
            ],
        },
    }


class ManifestValidationTest(unittest.TestCase):
    def test_matching_versions_and_sources_are_valid(self):
        failures = validate_repo.validate_manifests(**matching_manifests())

        self.assertEqual(failures, [])

    def test_nested_marketplace_version_disagreement_is_invalid(self):
        manifests = matching_manifests()
        manifests["claude_market"]["plugins"][0]["version"] = "different"

        failures = validate_repo.validate_manifests(**manifests)

        self.assertTrue(
            any("manifest versions disagree" in failure for failure in failures),
            failures,
        )

    def test_copilot_plugin_version_disagreement_is_invalid(self):
        manifests = matching_manifests()
        manifests["copilot_plugin"]["version"] = "different"

        failures = validate_repo.validate_manifests(**manifests)

        self.assertTrue(
            any("manifest versions disagree" in failure for failure in failures),
            failures,
        )

    def test_empty_plugin_collection_is_reported(self):
        manifests = matching_manifests()
        manifests["claude_market"]["plugins"] = []

        failures = validate_repo.validate_manifests(**manifests)

        self.assertIn("Claude marketplace has no plugin entry", failures)


if __name__ == "__main__":
    unittest.main()
