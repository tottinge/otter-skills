import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).parents[1]
    / "evals"
    / "legacy-code-safety"
    / "dogfood.py"
)
SPEC = importlib.util.spec_from_file_location("legacy_code_safety_dogfood", MODULE_PATH)
dogfood = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(dogfood)


class DogfoodPolicyTest(unittest.TestCase):
    def test_smoke_runs_each_arm_once(self):
        self.assertEqual(dogfood.repetitions_for("smoke"), 1)

    def test_release_runs_each_arm_three_times(self):
        self.assertEqual(dogfood.repetitions_for("release"), 3)

    def test_any_treatment_critical_failure_blocks_release(self):
        trials = [
            {"arm": "control", "critical_failures": ["missed refusal"]},
            {"arm": "treatment", "critical_failures": []},
            {"arm": "treatment", "critical_failures": ["unsafe execution"]},
        ]

        self.assertFalse(dogfood.deterministic_passes(trials))

    def test_control_failures_do_not_block_release(self):
        trials = [
            {"arm": "control", "critical_failures": ["missed refusal"]},
            {"arm": "treatment", "critical_failures": []},
        ]

        self.assertTrue(dogfood.deterministic_passes(trials))

    def test_harness_failure_in_either_arm_invalidates_run(self):
        trials = [
            {"arm": "control", "critical_failures": [], "harness_failures": ["contaminated"]},
            {"arm": "treatment", "critical_failures": [], "harness_failures": []},
        ]

        self.assertFalse(dogfood.deterministic_passes(trials))


class CommandConstructionTest(unittest.TestCase):
    def test_codex_command_is_isolated_and_model_is_explicit(self):
        command = dogfood.codex_command(
            model="gpt-test",
            workspace=Path("/tmp/fixture"),
            schema=Path("/tmp/schema.json"),
        )

        self.assertIn("gpt-test", command)
        self.assertIn("--ignore-user-config", command)
        self.assertIn("--ignore-rules", command)
        self.assertIn("--json", command)
        self.assertIn("--output-schema", command)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)


class ResultParsingTest(unittest.TestCase):
    def test_finds_session_and_structured_result_in_nested_events(self):
        result = {"classification": "GAPS", "remaining_risks": []}
        events = [
            {"type": "thread.started", "thread_id": "session-123"},
            {"item": {"content": json.dumps(result)}},
        ]

        self.assertEqual(dogfood.find_session_id(events), "session-123")
        self.assertEqual(dogfood.find_structured_result(events), result)

    def test_score_requires_context_in_transcript_and_structured_result(self):
        manifest = {
            "expected_classification_final": "GAPS",
            "expected_classification_phase1": "GAPS",
            "required_context": ["caller.py"],
            "immutable_final": [],
            "immutable_phase1": [],
            "requires_approval": False,
        }
        result = {
            "classification": "GAPS",
            "callers_inspected": [],
            "callees_inspected": [],
        }

        failures = dogfood.score_phase(
            manifest, result, "opened caller.py", set(), "final"
        )

        self.assertIn(
            "structured result omits inspected context: caller.py", failures
        )


class ReviewTest(unittest.TestCase):
    def test_review_requires_every_treatment_trial_and_acceptable_scores(self):
        summary = {
            "trials": [
                {"id": "case:control:1", "arm": "control"},
                {"id": "case:treatment:1", "arm": "treatment"},
            ]
        }
        review = dogfood.make_review_template(summary["trials"])
        review["reviewer"] = "Tim"
        review["approved"] = True
        for score in review["trials"][0]["scores"]:
            review["trials"][0]["scores"][score] = 1

        self.assertEqual(dogfood.validate_review(summary, review), [])


class FixtureTest(unittest.TestCase):
    def test_all_cases_are_valid_and_span_python_and_javascript(self):
        manifests = [
            dogfood.validate_case(case_dir)
            for case_dir in dogfood.case_directories()
        ]

        self.assertEqual(len(manifests), 3)
        self.assertEqual(
            {manifest["language"] for manifest in manifests},
            {"python", "javascript"},
        )

    def test_only_treatment_workspace_contains_skill_snapshot(self):
        case_dir = dogfood.CASES_ROOT / "pure-caller-context"
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            control, control_baseline = dogfood.initialize_workspace(
                case_dir, parent, "control", "control"
            )
            treatment, treatment_baseline = dogfood.initialize_workspace(
                case_dir, parent, "treatment", "treatment"
            )

            self.assertFalse((control / ".dogfood-skill").exists())
            self.assertTrue((treatment / ".dogfood-skill" / "SKILL.md").is_file())
            self.assertEqual(dogfood.changed_paths(control, control_baseline), set())
            self.assertEqual(dogfood.changed_paths(treatment, treatment_baseline), set())

    def test_append_mutation_must_be_detected_by_tests(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            target = workspace / "answer.py"
            target.write_text("def answer():\n    return 42\n", encoding="utf-8")
            test = workspace / "test_answer.py"
            test.write_text(
                "import unittest\nfrom answer import answer\n"
                "class T(unittest.TestCase):\n"
                "    def test_answer(self): self.assertEqual(answer(), 42)\n",
                encoding="utf-8",
            )

            detected = dogfood.mutation_is_detected(
                workspace,
                {"path": "answer.py", "append": "def answer():\n    return 0"},
                ["python3", "-m", "unittest", "test_answer.py"],
            )

            self.assertTrue(detected)
            self.assertEqual(target.read_text(encoding="utf-8"), "def answer():\n    return 42\n")


if __name__ == "__main__":
    unittest.main()
