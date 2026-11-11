#!/usr/bin/env python3
"""Replay the documented synthetic fixtures on the lab's Wazuh manager."""

import re
import subprocess
from pathlib import Path


LOGTEST = Path("/var/ossec/bin/wazuh-logtest")
DOC = Path(__file__).resolve().parents[1] / "docs/05-detection-engineering.md"
RULE_IDS = ("100100", "100110", "100120", "100130", "100140", "100150")


def run_case(label, events, expected_ids):
    result = subprocess.run(
        [str(LOGTEST)],
        input="\n".join(events) + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=45,
        check=False,
    )
    print(f"\n=== {label} ===\n{result.stdout}", flush=True)
    matches = re.findall(r"^\s*id:\s*'([0-9]+)'\s*$", result.stdout, re.MULTILINE)
    lab_ids = [rule_id for rule_id in matches if rule_id in RULE_IDS]
    if result.returncode != 0 or lab_ids != expected_ids:
        print(f"FAIL: expected {expected_ids}, observed {lab_ids}, exit {result.returncode}")
        return False
    print("PASS")
    return True


def main():
    if not LOGTEST.is_file():
        raise SystemExit("Run this on the lab Wazuh manager after applying the rules.")
    fixtures = dict(
        re.findall(
            r"^## (100\d{3}) [^\n]+\n.*?^```(?:text|json)\n([^\n]+)\n```",
            DOC.read_text(encoding="utf-8"),
            re.MULTILINE | re.DOTALL,
        )
    )
    if set(fixtures) != set(RULE_IDS):
        raise SystemExit("The detection guide must contain one fixture for each lab rule.")

    ssh_fixture = fixtures["100100"]
    source = "192.168.56.40"
    if source not in ssh_fixture:
        raise SystemExit("The documented SSH fixture source has changed.")
    mixed_sources = [
        ssh_fixture.replace(source, f"192.168.56.{host}") for host in range(40, 48)
    ]
    checks = [
        ("SSH below threshold", [ssh_fixture] * 7, []),
        ("SSH mixed source addresses", mixed_sources, []),
        ("SSH at threshold", [ssh_fixture] * 8, ["100100"]),
    ]
    checks.extend((rule_id, [fixtures[rule_id]], [rule_id]) for rule_id in RULE_IDS[1:])
    results = [run_case(*check) for check in checks]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
