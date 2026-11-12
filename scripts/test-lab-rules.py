#!/usr/bin/env python3
"""Replay the documented synthetic fixtures on the lab's Wazuh manager."""

import argparse
import re
import subprocess
from pathlib import Path


LOGTEST = Path("/var/ossec/bin/wazuh-logtest")
DOC = Path(__file__).resolve().parents[1] / "docs/05-detection-engineering.md"
RULE_IDS = ("5763", "100110", "100120", "100130", "100140", "100150")


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
    try:
        result = subprocess.run(
            [str(LOGTEST)],
            input="\n".join(events) + "\n",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=45,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        print(f"\n=== {label} ===", flush=True)
        if error.stdout:
            print(error.stdout.decode("utf-8", errors="replace"), flush=True)
        print(f"FAIL: Logtest timed out after {error.timeout} seconds.")
        return False
    print(f"\n=== {label} ===\n{result.stdout}", flush=True)
    problem = check_output(result.stdout, events, expected_matches)
    if result.returncode != 0 or problem:
        print(f"FAIL: {problem or 'Logtest exited with an error'} (exit {result.returncode})")
        return False
    print("PASS")
    return True


def read_fixtures(document):
    fixtures = {}
    for section in re.split(r"(?m)^## ", document)[1:]:
        heading = re.match(r"(\d+)\b", section)
        if not heading:
            continue

        rule_id = heading.group(1)
        if rule_id in fixtures:
            raise SystemExit(f"Duplicate rule heading for {rule_id}.")
        blocks = re.findall(r"^```(?:text|json)[ \t]*\n(.*?)^```[ \t]*$", section, re.M | re.S)
        if len(blocks) != 1 or len(blocks[0].splitlines()) != 1 or not blocks[0].strip():
            raise SystemExit(f"Rule {rule_id} must have exactly one single-line input fixture.")
        fixtures[rule_id] = blocks[0].removesuffix("\n")

    if set(fixtures) != set(RULE_IDS):
        raise SystemExit("The detection guide must contain one fixture for each tracked rule.")
    return fixtures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--linux-only",
        action="store_true",
        help="Run the SSH and Linux account cases. Validate Windows rules with agent telemetry.",
    )
    args = parser.parse_args()
    if not LOGTEST.is_file():
        raise SystemExit("Run this on the lab Wazuh manager after applying the rules.")
    fixtures = read_fixtures(DOC.read_text(encoding="utf-8"))

    ssh_fixture = fixtures["5763"]
    source = "192.168.56.40"
    if source not in ssh_fixture:
        raise SystemExit("The documented SSH fixture source has changed.")
    mixed_sources = [
        ssh_fixture.replace(source, f"192.168.56.{host}") for host in range(40, 48)
    ]
    checks = [
        ("SSH below threshold", [ssh_fixture] * 7, []),
        ("SSH mixed source addresses", mixed_sources, []),
        ("SSH at threshold", [ssh_fixture] * 8, [(8, "5763")]),
    ]
    rule_ids = ("100150",) if args.linux_only else RULE_IDS[1:]
    checks.extend((rule_id, [fixtures[rule_id]], [(1, rule_id)]) for rule_id in rule_ids)
    results = [run_case(*check) for check in checks]
    if args.linux_only:
        print("SKIP: Windows EventChannel rules 100110, 100120, 100130, and 100140.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
