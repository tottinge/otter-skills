#!/usr/bin/env python3
"""Build reproducible .skill archives from the canonical plugin tree."""

from __future__ import annotations

import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "otter-skills" / "skills"
DIST = ROOT / "dist"
ARCHIVE_TIME = (1980, 1, 1, 0, 0, 0)


def add_file(archive: ZipFile, path: Path, archive_name: str) -> None:
    info = ZipInfo(archive_name, ARCHIVE_TIME)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, path.read_bytes())


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    count = 0
    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        with ZipFile(DIST / f"{skill_dir.name}.skill", "w") as archive:
            for path in sorted(item for item in skill_dir.rglob("*") if item.is_file()):
                add_file(archive, path, str(path.relative_to(skill_dir.parent)))
            for legal_file in ("LICENSE", "NOTICE"):
                add_file(archive, ROOT / legal_file, legal_file)
        count += 1
    print(f"Built {count} skill archives in dist/.")


if __name__ == "__main__":
    main()
