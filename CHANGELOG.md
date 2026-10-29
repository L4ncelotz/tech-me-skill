# Changelog

All notable changes to this project should be documented here.

## [Unreleased]

### Fixed

- Documented fixture-preparation command now writes to git-ignored `dist/`, and `.gitignore` covers generated fixture files, so preparing fixtures no longer leaves an untracked file that blocks clean-tree release packaging.
- `run_evals.py` execution-mode check simplified to the plain `--dry-run`/`--prepare-fixtures` condition (dead code removed); behavior unchanged.

### Changed

- `pack_release.py` verifies that `--version` matches an annotated Git tag (`v<version>`) pointing at the packaged ref before creating the release ZIP; version/tag/commit mismatches and untagged releases fail closed. `--allow-untagged` bypasses tag verification for local archives only (see PUBLISHING.md).
- `evals/RESULTS.md` findings scoped to the three sampled scenarios (one response per condition) with explicit limitations; no cross-scenario generalization is implied.
- Evaluation fixtures gained an optional `turns` array of scripted user replies for multi-turn interviews, with focus on stopping discipline ("recommend now") and not re-asking answered constraints; validator and harness accept and export them. First multi-turn stopping scenario added.

## [0.1.0] - 2026-10-29

### Added

- Portable `tech-me` Agent Skill with adaptive requirements discovery and bias-controlled architecture evaluation.
- References for discovery, evidence-based comparison, and decision report structure.
- Optional Architecture Decision Record template.
- Scenario-based evaluation fixtures, human scoring rubric, and comparison runbook.
- Stdlib-only repository validator, tests, and validation CI workflow.

### Changed

- Updated canonical repository references and installation command to `L4ncelotz/tech-me-skills`.

### Limitations

- Initial draft: cross-agent behavior and comparative quality have **not yet been empirically verified**.
- No published GitHub release or skills.sh listing is implied by this local package.
