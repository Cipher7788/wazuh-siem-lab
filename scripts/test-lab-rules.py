#!/usr/bin/env python3
"""Replay the documented synthetic fixtures on the lab's Wazuh manager."""

import re
import subprocess
from pathlib import Path


LOGTEST = Path("/var/ossec/bin/wazuh-logtest")
DOC = Path(__file__).resolve().parents[1] / "docs/05-detection-engineering.md"
RULE_IDS = ("100100", "100110", "100120", "100130", "100140", "100150")


def check_output(output, events, expected_matches):
    blocks = re.split(r"(?im)^\*\*Phase 1: completed pre-decoding\.[ \t]*$", output)[1:]
    if len(blocks) != len(events):
        return f"expected {len(events)} processed events, found {len(blocks)}"

    matches = []
    for index, (event, block) in enumerate(zip(events, blocks), start=1):
        echoed = re.search(r"(?m)^[ \t]*full event: '(.*)'[ \t]*$", block)
        if not echoed or echoed.group(1) != event:
            return f"event {index} was missing or differed from the submitted input"
        if not re.search(r"(?im)^\*\*Phase 2: completed decoding\.", block):
            return f"event {index} did not reach decoding"

        phase_three = re.search(r"(?im)^\*\*Phase 3: completed filtering \(rules\)\.", block)
        if phase_three:
            filtering = block[phase_three.end():]
            rule = re.search(r"(?m)^[ \t]*id:[ \t]*'([0-9]+)'[ \t]*$", filtering)
            if not rule:
                return f"event {index} reached filtering without a rule ID"
            if rule.group(1) in RULE_IDS:
                matches.append((index, rule.group(1)))

    if matches != expected_matches:
        return f"expected rule matches {expected_matches}, observed {matches}"
    return None


def run_case(label, events, expected_matches):
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
    problem = check_output(result.stdout, events, expected_matches)
    if result.returncode != 0 or problem:
        print(f"FAIL: {problem or 'Logtest exited with an error'} (exit {result.returncode})")
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
        ("SSH at threshold", [ssh_fixture] * 8, [(8, "100100")]),
    ]
    checks.extend((rule_id, [fixtures[rule_id]], [(1, rule_id)]) for rule_id in RULE_IDS[1:])
    results = [run_case(*check) for check in checks]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
