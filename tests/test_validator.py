"""Deterministic unit tests for local file and scenario validator."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_repo import ROOT, validate_repo, validate_scenarios, validate_skill  # noqa: E402


class ValidationTests(unittest.TestCase):
    def test_real_repo_passes(self):
        self.assertEqual(validate_repo(ROOT), [])

    def test_rejects_wrong_skill_directory_name(self):
        with tempfile.TemporaryDirectory() as directory:
            wrong = Path(directory) / "other-skill"
            wrong.mkdir()
            (wrong / "SKILL.md").write_text(
                "---\nname: tech-me\ndescription: Example\n---\n# Example\n", encoding="utf-8"
            )
            self.assertTrue(any("must match directory" in err for err in validate_skill(wrong)))

    def test_rejects_missing_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tech-me"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: tech-me\ndescription: Example\n---\nSee [missing](references/nope.md).\n",
                encoding="utf-8",
            )
            self.assertTrue(any("link not found" in err for err in validate_skill(skill)))

    def test_rejects_duplicate_scenario_ids(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        duplicate = dict(fixture["scenarios"][0])
        fixture["scenarios"].append(duplicate)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(any("Duplicate scenario id" in err for err in validate_scenarios(path)))

    def test_rejects_missing_categories(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        fixture["scenarios"] = fixture["scenarios"][:1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(any("Missing evaluation categories" in err for err in validate_scenarios(path)))

    def test_rejects_unsupported_frontmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tech-me"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: tech-me\ndescription: Example\nmagic: true\n---\n# Instructions\n",
                encoding="utf-8",
            )
            self.assertTrue(any("Unsupported frontmatter" in err for err in validate_skill(skill)))

    def test_accepts_scripted_turns(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        multi_turn = [s for s in fixture["scenarios"] if s.get("turns")]
        self.assertTrue(multi_turn, "The scenario set must include at least one multi-turn (turns) fixture.")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertEqual(validate_scenarios(path), [])

    def test_rejects_malformed_scripted_turns(self):
        fixture = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
        fixture["scenarios"][0]["turns"] = "recommend now"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenarios.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(
                any("turns must be a non-empty list of strings" in err for err in validate_scenarios(path))
            )


if __name__ == "__main__":
    unittest.main()
