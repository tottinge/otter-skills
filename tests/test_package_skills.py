import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "package_skills.py"
SPEC = importlib.util.spec_from_file_location("package_skills", MODULE_PATH)
package_skills = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(package_skills)


class PackageDeterminismTest(unittest.TestCase):
    def test_same_inputs_produce_identical_archive_bytes(self):
        source = ROOT / "plugins" / "otter-skills" / "skills" / "representation-refactor-review"
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.skill"
            second = Path(directory) / "second.skill"
            for target in (first, second):
                with ZipFile(target, "w") as archive:
                    for path in sorted(item for item in source.rglob("*") if item.is_file()):
                        package_skills.add_file(
                            archive,
                            path,
                            str(path.relative_to(source.parent)),
                        )
                    for legal_file in ("LICENSE", "NOTICE"):
                        package_skills.add_file(
                            archive,
                            ROOT / legal_file,
                            legal_file,
                        )

            self.assertEqual(
                hashlib.sha256(first.read_bytes()).digest(),
                hashlib.sha256(second.read_bytes()).digest(),
            )
