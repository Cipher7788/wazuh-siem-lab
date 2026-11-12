"""Regression tests for the fixture runner without a Wazuh installation."""

import runpy
import subprocess
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


runner = runpy.run_path(str(Path(__file__).with_name("test-lab-rules.py")))
document = runner["DOC"].read_text(encoding="utf-8")


class FixtureTests(unittest.TestCase):
    def test_documented_fixtures(self):
        self.assertEqual(set(runner["read_fixtures"](document)), set(runner["RULE_IDS"]))

    def test_rejects_duplicate_heading_without_input(self):
        with self.assertRaisesRegex(SystemExit, "Duplicate rule heading"):
            runner["read_fixtures"](document + "\n## 5763 Duplicate heading\n")

    def test_rejects_second_input_in_one_section(self):
        duplicate = "```text\nsecond input\n```\n\n"
        modified = document.replace("Expected Phase 3 excerpt", duplicate + "Expected Phase 3 excerpt", 1)
        with self.assertRaisesRegex(SystemExit, "exactly one single-line input fixture"):
            runner["read_fixtures"](modified)

    def test_timeout_returns_case_failure(self):
        error = subprocess.TimeoutExpired("wazuh-logtest", 45, output=b"partial output")
        output = StringIO()
        with patch.object(subprocess, "run", side_effect=error), redirect_stdout(output):
            self.assertFalse(runner["run_case"]("slow fixture", ["test input"], []))
        self.assertIn("slow fixture", output.getvalue())
        self.assertIn("partial output", output.getvalue())
        self.assertIn("timed out after 45 seconds", output.getvalue())


if __name__ == "__main__":
    unittest.main()
