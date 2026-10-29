"""Deterministic unit tests for packaging and evaluation scripts."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from pack_release import assert_clean_git_tree, is_forbidden, pack_release, verify_git_ref  # noqa: E402
from run_evals import filter_scenarios, load_scenarios, load_skill_prompt  # noqa: E402


def create_git_repo(tmp_dir: str, tag: str | None = None) -> Path:
    """Create a minimal committed Git repository for packaging tests."""
    repo_dir = Path(tmp_dir) / "test_repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@test.local"], cwd=repo_dir, check=True)
    (repo_dir / "file.txt").write_text("initial", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, capture_output=True, check=True)
    if tag:
        subprocess.run(["git", "tag", "-a", tag, "-m", f"Tag {tag}"], cwd=repo_dir, capture_output=True, check=True)
    return repo_dir


class ScriptTests(unittest.TestCase):
    def test_forbidden_patterns(self):
        self.assertTrue(is_forbidden(".git/config"))
        self.assertTrue(is_forbidden("sub/.git/HEAD"))
        self.assertTrue(is_forbidden("module/__pycache__/foo.cpython-310.pyc"))
        self.assertTrue(is_forbidden(".pytest_cache/v/cache/lastfailed"))
        self.assertTrue(is_forbidden(".venv/bin/python"))
        self.assertTrue(is_forbidden(".env"))
        self.assertTrue(is_forbidden(".env.local"))
        self.assertTrue(is_forbidden("dist/tech-me-0.1.0.zip"))
        self.assertFalse(is_forbidden("skills/tech-me/SKILL.md"))
        self.assertFalse(is_forbidden("evals/scenarios.json"))

    def test_run_evals_scenario_loading(self):
        data = load_scenarios(ROOT / "evals" / "scenarios.json")
        scenarios = data.get("scenarios", [])
        self.assertGreaterEqual(len(scenarios), 13)

        # Test valid filtering
        filtered = filter_scenarios(scenarios, ["historical-preference-bias"])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], "historical-preference-bias")

        # Test invalid filtering raises ValueError
        with self.assertRaises(ValueError):
            filter_scenarios(scenarios, ["non-existent-scenario-id"])

    def test_run_evals_skill_sha256(self):
        content, sha256 = load_skill_prompt(ROOT / "skills" / "tech-me" / "SKILL.md")
        self.assertIn("tech-me", content)
        self.assertEqual(len(sha256), 64)

    def test_run_evals_fails_without_runner_or_dryrun(self):
        """Harness must fail closed when executed without --dry-run or --prepare-fixtures."""
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_evals.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("Live evaluation runner is not configured", proc.stderr)

    def test_run_evals_dry_run_success(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "run_evals.py"),
                "--dry-run",
                "--scenarios",
                "historical-preference-bias",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("[DRY RUN] Scenario: historical-preference-bias", proc.stdout)
        self.assertIn("Scripted follow-up turns: 0", proc.stdout)
        self.assertIn("Dry-run completed", proc.stdout)

    def test_run_evals_prepare_fixtures(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "fixtures.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_evals.py"),
                    "--prepare-fixtures",
                    "--scenarios",
                    "historical-preference-bias",
                    "--output",
                    str(out_file),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0)
            self.assertTrue(out_file.is_file())
            data = json.loads(out_file.read_text(encoding="utf-8"))
            self.assertEqual(data.get("type"), "prepared_fixtures")
            self.assertEqual(data.get("status"), "not_evaluated")
            self.assertIn("historical-preference-bias", data.get("fixtures", {}))

    def test_run_evals_exports_predetermined_followups(self):
        """Multi-turn scenarios export their scripted turns for external runners."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "fixtures.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_evals.py"),
                    "--prepare-fixtures",
                    "--scenarios",
                    "multi-turn-honor-stop-trigger",
                    "--output",
                    str(out_file),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(out_file.read_text(encoding="utf-8"))
            payload = data["fixtures"]["multi-turn-honor-stop-trigger"]
            self.assertEqual(len(payload["predetermined_followups"]), 3)
            self.assertIn("recommend now", payload["predetermined_followups"][-1])

    def test_pack_release_rejects_missing_git(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "dist"
            non_git = Path(tmp_dir) / "plain_dir"
            non_git.mkdir()
            with self.assertRaises(RuntimeError) as ctx:
                pack_release(version="0.1.0", output_dir=out_dir, repo_root=non_git)
            self.assertIn("Git repository or metadata not found", str(ctx.exception))

    def test_pack_release_rejects_dirty_tree(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = create_git_repo(tmp_dir)

            # Introduce an untracked file
            (repo_dir / "untracked.txt").write_text("untracked", encoding="utf-8")

            out_dir = Path(tmp_dir) / "dist"
            with self.assertRaises(RuntimeError) as ctx:
                pack_release(version="0.1.0", output_dir=out_dir, repo_root=repo_dir)
            self.assertIn("Working tree contains uncommitted changes", str(ctx.exception))

    def test_pack_release_rejects_invalid_ref(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = create_git_repo(tmp_dir)

            out_dir = Path(tmp_dir) / "dist"
            with self.assertRaises(RuntimeError) as ctx:
                pack_release(
                    version="0.1.0",
                    output_dir=out_dir,
                    repo_root=repo_dir,
                    ref="invalid-tag-12345",
                )
            self.assertIn("not found or invalid", str(ctx.exception))

    def test_pack_release_clean_archive_excludes_secrets_and_caches(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = create_git_repo(tmp_dir, tag="v0.1.0")

            # Untracked .env and cache files in working tree
            (repo_dir / ".env").write_text("SECRET=123", encoding="utf-8")
            pycache = repo_dir / "__pycache__"
            pycache.mkdir()
            (pycache / "cached.pyc").write_text("fake bytecode", encoding="utf-8")

            # Packaging HEAD with check_clean=False simulates extracting committed ref
            out_dir = Path(tmp_dir) / "dist"
            zip_path = pack_release(
                version="0.1.0",
                output_dir=out_dir,
                repo_root=repo_dir,
                ref="HEAD",
                check_clean=False,
            )
            self.assertTrue(zip_path.is_file())

            with zipfile.ZipFile(zip_path, "r") as zf:
                names = zf.namelist()
                file_entries = [n for n in names if not n.endswith("/")]
                self.assertEqual(len(file_entries), 1)
                self.assertEqual(file_entries[0], "tech-me-0.1.0/file.txt")
                for name in names:
                    self.assertNotIn(".env", name)
                    self.assertNotIn("__pycache__", name)
                    self.assertNotIn(".git", name)

    def test_pack_release_rejects_untagged_release_version(self):
        """Reproduces the reported issue: an arbitrary --version without a matching tag must fail."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = create_git_repo(tmp_dir)
            out_dir = Path(tmp_dir) / "dist"
            with self.assertRaises(RuntimeError) as ctx:
                pack_release(version="9.9.9", output_dir=out_dir, repo_root=repo_dir, check_clean=False)
            self.assertIn("Release tag 'v9.9.9' not found", str(ctx.exception))
            self.assertFalse((out_dir / "tech-me-9.9.9.zip").exists())

    def test_pack_release_allows_untagged_when_explicit(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = create_git_repo(tmp_dir)
            out_dir = Path(tmp_dir) / "dist"
            zip_path = pack_release(
                version="9.9.9",
                output_dir=out_dir,
                repo_root=repo_dir,
                check_clean=False,
                require_tag=False,
            )
            self.assertEqual(zip_path.name, "tech-me-9.9.9.zip")
            self.assertTrue(zip_path.is_file())

    def test_pack_release_rejects_tag_ref_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = create_git_repo(tmp_dir, tag="v0.1.0")
            (repo_dir / "file.txt").write_text("changed", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
            subprocess.run(["git", "commit", "-m", "second"], cwd=repo_dir, capture_output=True, check=True)

            out_dir = Path(tmp_dir) / "dist"
            with self.assertRaises(RuntimeError) as ctx:
                pack_release(version="0.1.0", output_dir=out_dir, repo_root=repo_dir, ref="HEAD")
            self.assertIn("does not point at ref", str(ctx.exception))

    def test_pack_release_accepts_matching_tag_at_head(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = create_git_repo(tmp_dir, tag="v0.1.0")
            out_dir = Path(tmp_dir) / "dist"
            zip_path = pack_release(version="0.1.0", output_dir=out_dir, repo_root=repo_dir)
            self.assertTrue(zip_path.is_file())


if __name__ == "__main__":
    unittest.main()
