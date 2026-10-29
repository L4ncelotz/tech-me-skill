# Changelog

All notable changes to this project should be documented here.

## [Unreleased]

## [0.1.0] - 2026-10-29

### Added

- Portable `tech-me` Agent Skill with adaptive requirements discovery and bias-controlled architecture evaluation.
- References for discovery, evidence-based comparison, and decision report structure.
- Optional Architecture Decision Record template.
- Scenario-based evaluation fixtures, human scoring rubric, and comparison runbook.
- Stdlib-only repository validator, tests, and validation CI workflow.

### Fixed

- Documented fixture-preparation command now writes to git-ignored `dist/`, and `.gitignore` covers generated fixture files, so preparing fixtures no longer leaves an untracked file that blocks clean-tree release packaging.
- `run_evals.py` execution-mode check simplified to the plain `--dry-run`/`--prepare-fixtures` condition (dead code removed); behavior unchanged.
- Release packaging (`pack_release.py`) requires an annotated tag (`git tag -a`) in the `refs/tags/` namespace matching `--version`: untagged refs, lightweight tags, a branch sharing the tag name, and tag/ref commit mismatches all fail closed. `--allow-untagged` bypasses tag verification for local archives only (see PUBLISHING.md).
- `PUBLISHING.md` documents `pack_release.py` as the single supported release path and the manual `git archive` alternative (which skipped verification) was removed; the README install section now reflects the published canonical repository.

### Changed

- Updated canonical repository references and installation command to `L4ncelotz/tech-me-skills`.
- `evals/RESULTS.md` findings scoped to the three sampled scenarios (one response per condition) with explicit limitations; no cross-scenario generalization is implied.
- Evaluation fixtures gained an optional `turns` array of scripted user replies for multi-turn interviews, with focus on stopping discipline ("recommend now") and not re-asking answered constraints; validator and harness accept and export them. First multi-turn stopping scenario added.

### Limitations

- Initial draft: cross-agent behavior and comparative quality have **not yet been empirically verified**; this release is tagged as a GitHub **pre-release**.
- No skills.sh listing is implied by this package.
