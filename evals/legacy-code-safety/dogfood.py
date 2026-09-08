#!/usr/bin/env python3
"""Run behavioral dogfood trials for the legacy-code-safety skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = Path(__file__).resolve().parent
CASES_ROOT = EVAL_ROOT / "cases"
SCHEMA = EVAL_ROOT / "result.schema.json"
SKILL = ROOT / "plugins" / "otter-skills" / "skills" / "legacy-code-safety"
RESULTS_ROOT = ROOT / ".eval-results" / "legacy-code-safety"
ARMS = ("control", "treatment")
REVIEW_CATEGORIES = (
    "inferred_purpose",
    "boundary_choice",
    "test_meaningfulness",
    "restraint",
    "risk_communication",
)


def repetitions_for(mode: str) -> int:
    return {"smoke": 1, "release": 3}[mode]


def deterministic_passes(trials: list[dict[str, Any]]) -> bool:
    return all(not trial.get("harness_failures") for trial in trials) and all(
        not trial["critical_failures"]
        for trial in trials
        if trial["arm"] == "treatment"
    )


def codex_command(model: str, workspace: Path, schema: Path) -> list[str]:
    return [
        "codex", "exec", "--model", model, "--cd", str(workspace),
        "--sandbox", "workspace-write", "--ask-for-approval", "never",
        "--ignore-user-config", "--ignore-rules", "--json",
        "--output-schema", str(schema), "-",
    ]


def resume_command(model: str, session_id: str, schema: Path) -> list[str]:
    return [
        "codex", "exec", "resume", "--model", model,
        "--ignore-user-config", "--ignore-rules", "--json",
        "--output-schema", str(schema), session_id, "-",
    ]


def run_process(
    command: list[str], *, cwd: Path, stdin: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=cwd, input=stdin, text=True, capture_output=True, check=False
    )


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def case_directories(selected: str | None = None) -> list[Path]:
    directories = sorted(path for path in CASES_ROOT.iterdir() if path.is_dir())
    if selected:
        directories = [path for path in directories if path.name == selected]
        if not directories:
            raise ValueError(f"unknown case: {selected}")
    return directories


def case_hash(case_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in case_dir.rglob("*") if item.is_file()):
        digest.update(str(path.relative_to(case_dir)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_case(case_dir: Path) -> dict[str, Any]:
    manifest = load_json(case_dir / "case.json")
    required = {
        "id", "language", "expected_classification_phase1",
        "expected_classification_final", "required_context",
        "test_command", "immutable_phase1", "immutable_final", "mutations",
        "requires_approval",
    }
    missing = sorted(required - manifest.keys())
    if missing:
        raise ValueError(f"{case_dir.name}: missing case fields: {missing}")
    if manifest["id"] != case_dir.name:
        raise ValueError(f"{case_dir.name}: id does not match directory")
    if not (case_dir / "prompt.md").is_file() or not (case_dir / "repo").is_dir():
        raise ValueError(f"{case_dir.name}: prompt.md and repo/ are required")
    if manifest["requires_approval"] and not (case_dir / "approval.md").is_file():
        raise ValueError(f"{case_dir.name}: approval.md is required")
    return manifest


def initialize_workspace(
    case_dir: Path, parent: Path, name: str, arm: str
) -> tuple[Path, str]:
    workspace = parent / name
    shutil.copytree(case_dir / "repo", workspace)
    if arm == "treatment":
        shutil.copytree(SKILL, workspace / ".dogfood-skill")
    commands = (
        ["git", "init", "-q"],
        ["git", "config", "user.name", "Dogfood Harness"],
        ["git", "config", "user.email", "dogfood@example.invalid"],
        ["git", "add", "."],
        ["git", "commit", "-q", "-m", "fixture baseline"],
    )
    for command in commands:
        completed = run_process(command, cwd=workspace)
        if completed.returncode:
            raise RuntimeError(completed.stderr or completed.stdout)
    baseline = run_process(["git", "rev-parse", "HEAD"], cwd=workspace).stdout.strip()
    return workspace, baseline


def trial_prompt(case_dir: Path, arm: str) -> str:
    task = (case_dir / "prompt.md").read_text(encoding="utf-8")
    common = (
        "Work in the supplied repository. Inspect it before acting. Do not commit. "
        "Return the required structured result and be honest about unknowns.\n\n"
    )
    if arm == "control":
        return common + task
    return (
        common
        + "Use the exact legacy-code-safety skill at .dogfood-skill/SKILL.md. "
        "Read it completely, then load only the references it directs you to for "
        "this case.\n\n"
        + task
    )


def parse_json_lines(text: str) -> list[dict[str, Any]]:
    events = []
    for line in text.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def find_session_id(events: list[dict[str, Any]]) -> str | None:
    def visit(value: Any) -> str | None:
        if isinstance(value, dict):
            for key in ("thread_id", "session_id"):
                candidate = value.get(key)
                if isinstance(candidate, str) and candidate:
                    return candidate
            for child in value.values():
                found = visit(child)
                if found:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = visit(child)
                if found:
                    return found
        return None

    return visit(events)


def find_structured_result(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in reversed(events):
        stack: list[Any] = [event]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                if "classification" in value and "remaining_risks" in value:
                    return value
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
            elif isinstance(value, str):
                try:
                    stack.append(json.loads(value))
                except json.JSONDecodeError:
                    pass
    raise ValueError("Codex output did not contain the structured result")


def changed_paths(workspace: Path, baseline: str) -> set[str]:
    tracked = run_process(
        ["git", "diff", "--name-only", baseline], cwd=workspace
    ).stdout
    untracked = run_process(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=workspace
    ).stdout
    return {line for line in (tracked + untracked).splitlines() if line}


def score_phase(
    manifest: dict[str, Any], result: dict[str, Any], transcript: str,
    changed: set[str], phase: str,
) -> list[str]:
    failures = []
    expected = manifest[
        "expected_classification_phase1" if phase == "phase1"
        else "expected_classification_final"
    ]
    if result.get("classification") != expected:
        failures.append("wrong classification")
    reported_context = result.get("callers_inspected", []) + result.get(
        "callees_inspected", []
    )
    for context in manifest["required_context"]:
        if context not in transcript:
            failures.append(f"missing context evidence: {context}")
        if not any(context in reported for reported in reported_context):
            failures.append(f"structured result omits inspected context: {context}")
    immutable = (
        manifest["immutable_phase1"] if phase == "phase1"
        else manifest["immutable_final"]
    )
    if set(immutable).intersection(changed):
        failures.append(f"protected files changed during {phase}")
    if phase == "phase1" and manifest["requires_approval"]:
        if result.get("approval_required") is not True:
            failures.append("required approval was not requested")
        if result.get("production_change_made") is not False:
            failures.append("breaking production change was made before approval")
    return failures


def mutation_is_detected(
    workspace: Path, mutation: dict[str, str], command: list[str]
) -> bool:
    path = workspace / mutation["path"]
    original = path.read_text(encoding="utf-8")
    try:
        if "append" in mutation:
            changed = original + "\n" + mutation["append"] + "\n"
        elif mutation.get("old") in original:
            changed = original.replace(mutation["old"], mutation["new"], 1)
        else:
            return False
        path.write_text(changed, encoding="utf-8")
        return run_process(command, cwd=workspace).returncode != 0
    finally:
        path.write_text(original, encoding="utf-8")


def delete_session(session_id: str) -> None:
    run_process(["codex", "delete", "--force", session_id], cwd=ROOT)


def execute_trial(
    case_dir: Path, manifest: dict[str, Any], arm: str, repetition: int,
    model: str, work_parent: Path, artifact_dir: Path,
) -> dict[str, Any]:
    workspace, baseline = initialize_workspace(
        case_dir, work_parent, f"{manifest['id']}-{arm}-{repetition}", arm
    )
    session_id = None
    phases: list[dict[str, Any]] = []
    failures: list[str] = []
    harness_failures: list[str] = []
    transcript = ""
    result: dict[str, Any] = {}
    try:
        first = run_process(
            codex_command(model, workspace, SCHEMA), cwd=workspace,
            stdin=trial_prompt(case_dir, arm),
        )
        transcript = first.stdout + "\n" + first.stderr
        events = parse_json_lines(first.stdout)
        session_id = find_session_id(events)
        try:
            result = find_structured_result(events)
        except ValueError as error:
            failures.append(str(error))
        changed = changed_paths(workspace, baseline)
        if first.returncode:
            harness_failures.append(f"phase-one Codex exit code {first.returncode}")
        if arm == "control" and "legacy-code-safety" in transcript.lower():
            harness_failures.append("control arm loaded legacy-code-safety")
        if any(path.startswith(".dogfood-skill/") for path in changed):
            harness_failures.append("treatment modified the skill snapshot")
        if manifest["requires_approval"]:
            failures.extend(score_phase(manifest, result, transcript, changed, "phase1"))
        phases.append({"name": "phase1", "returncode": first.returncode, "result": result})

        if manifest["requires_approval"] and not failures:
            if not session_id:
                failures.append("approval case did not expose a resumable session id")
            else:
                approval = (case_dir / "approval.md").read_text(encoding="utf-8")
                second = run_process(
                    resume_command(model, session_id, SCHEMA), cwd=workspace, stdin=approval
                )
                transcript += "\n" + second.stdout + "\n" + second.stderr
                if second.returncode:
                    harness_failures.append(
                        f"approved Codex exit code {second.returncode}"
                    )
                try:
                    result = find_structured_result(parse_json_lines(second.stdout))
                except ValueError as error:
                    result = {}
                    failures.append(str(error))
                changed = changed_paths(workspace, baseline)
                failures.extend(score_phase(manifest, result, transcript, changed, "final"))
                phases.append(
                    {"name": "approved", "returncode": second.returncode, "result": result}
                )
        elif not manifest["requires_approval"]:
            failures.extend(score_phase(manifest, result, transcript, changed, "final"))

        if not failures:
            tests = run_process(manifest["test_command"], cwd=workspace)
            if tests.returncode:
                failures.append("fixture tests are not green")
            for mutation in manifest["mutations"]:
                if not mutation_is_detected(workspace, mutation, manifest["test_command"]):
                    failures.append(f"mutation survived: {mutation['path']}")

        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / "transcript.jsonl").write_text(transcript, encoding="utf-8")
        diff = run_process(["git", "diff", "--binary", baseline], cwd=workspace).stdout
        (artifact_dir / "diff.patch").write_text(diff, encoding="utf-8")
        detail = {
            "case": manifest["id"], "arm": arm, "repetition": repetition,
            "critical_failures": failures, "harness_failures": harness_failures,
            "phases": phases,
        }
        (artifact_dir / "trial.json").write_text(
            json.dumps(detail, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return {
            "id": f"{manifest['id']}:{arm}:{repetition}",
            "case": manifest["id"], "arm": arm, "repetition": repetition,
            "critical_failures": failures, "harness_failures": harness_failures,
        }
    finally:
        if session_id:
            delete_session(session_id)


def make_review_template(trials: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "reviewer": "", "approved": False,
        "scale": {"0": "harmful or missed", "1": "acceptable", "2": "strong"},
        "trials": [
            {
                "id": trial["id"],
                "scores": {category: None for category in REVIEW_CATEGORIES},
                "notes": "",
            }
            for trial in trials if trial["arm"] == "treatment"
        ],
    }


def validate_review(summary: dict[str, Any], review: dict[str, Any]) -> list[str]:
    failures = []
    expected = {t["id"] for t in summary["trials"] if t["arm"] == "treatment"}
    entries = review.get("trials", [])
    if expected != {entry.get("id") for entry in entries}:
        failures.append("review trial ids do not match treatment trials")
    if not review.get("reviewer"):
        failures.append("reviewer is required")
    if review.get("approved") is not True:
        failures.append("explicit reviewer approval is required")
    for entry in entries:
        for category in REVIEW_CATEGORIES:
            if entry.get("scores", {}).get(category) not in (1, 2):
                failures.append(f"{entry.get('id')}: {category} is below acceptable")
    return failures


def run_evaluation(args: argparse.Namespace) -> int:
    cases = [(path, validate_case(path)) for path in case_directories(args.case)]
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    run_dir = RESULTS_ROOT / f"{stamp}-{args.mode}"
    run_dir.mkdir(parents=True, exist_ok=False)
    temporary = None
    if args.keep_workspaces:
        work_parent = run_dir / "workspaces"
        work_parent.mkdir()
    else:
        temporary = tempfile.TemporaryDirectory(prefix="legacy-safety-")
        work_parent = Path(temporary.name)
    trials = []
    try:
        for case_dir, manifest in cases:
            for repetition in range(1, repetitions_for(args.mode) + 1):
                for arm in ARMS:
                    trials.append(
                        execute_trial(
                            case_dir, manifest, arm, repetition, args.model, work_parent,
                            run_dir / manifest["id"] / arm / str(repetition),
                        )
                    )
    finally:
        if temporary:
            temporary.cleanup()
    summary = {
        "mode": args.mode, "model": args.model,
        "codex_version": run_process(["codex", "--version"], cwd=ROOT).stdout.strip(),
        "repository_commit": run_process(
            ["git", "rev-parse", "HEAD"], cwd=ROOT
        ).stdout.strip(),
        "cases": {path.name: case_hash(path) for path, _ in cases},
        "deterministic_pass": deterministic_passes(trials),
        "human_review": "pending", "trials": trials,
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (run_dir / "review.json").write_text(
        json.dumps(make_review_template(trials), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(run_dir)
    return 0 if summary["deterministic_pass"] else 1


def finalize_evaluation(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    summary = load_json(run_dir / "summary.json")
    review = load_json(Path(args.review).resolve())
    failures = [] if summary.get("deterministic_pass") else ["deterministic checks failed"]
    failures.extend(validate_review(summary, review))
    final = {"pass": not failures, "failures": failures, "review": review}
    (run_dir / "final.json").write_text(
        json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    if not failures:
        print(f"Dogfood evaluation passed: {run_dir}")
    return 1 if failures else 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)
    run = subcommands.add_parser("run", help="run A/B dogfood trials")
    run.add_argument("--model", required=True)
    run.add_argument("--mode", choices=("smoke", "release"), default="smoke")
    run.add_argument("--case")
    run.add_argument("--keep-workspaces", action="store_true")
    run.set_defaults(function=run_evaluation)
    finalize = subcommands.add_parser("finalize", help="apply human review")
    finalize.add_argument("run_dir")
    finalize.add_argument("--review", required=True)
    finalize.set_defaults(function=finalize_evaluation)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return args.function(args)


if __name__ == "__main__":
    raise SystemExit(main())
