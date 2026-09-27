# Contributing to otter-skills

Contributions are welcome. Please open an issue for substantial changes before
starting work, then submit a focused pull request with tests or other relevant
validation.

## License and authorship

The project is distributed under the [Apache License, Version 2.0](LICENSE).
Contributions submitted for inclusion are accepted under that same license.
By submitting a contribution, you confirm that you have the right to submit it
under these terms.

Contributors retain copyright in their original contributions. The canonical
otter-skills project, its direction, and its published skill collection remain
maintained by Tim Ottinger. Inclusion in this repository does not imply
endorsement of a contributor's separate projects or products.

Please preserve existing copyright, license, attribution, and `NOTICE`
information when copying or redistributing material. Add a prominent notice to
substantially modified files when Apache-2.0 requires one.

## Attribution and citation

If you build a skill, workflow, agent, or derivative practice substantially
from otter-skills or otter-kr, retain the applicable notices and credit the
source. Link to the relevant repository when possible:

- [otter-skills](https://github.com/tottinge/otter-skills)
- [otter-kr](https://github.com/tottinge/otter-kr)

For published work, please identify Tim Ottinger and cite the repositories or
the specific skill and evidence provider that materially informed the work.

## Pull requests

- Keep each change coherent and reasonably small.
- Update the canonical files under `plugins/otter-skills/`.
- Regenerate `dist/` when skill sources change.
- Run `python3 scripts/validate_repo.py` before submitting.
- Include the reasoning and evidence for behavior or workflow changes.
- Do not add dependencies on otter-kr; skills should remain useful without it.

Maintainers may revise, combine, or decline contributions so the canonical
collection remains coherent and consistent with its craft principles.
