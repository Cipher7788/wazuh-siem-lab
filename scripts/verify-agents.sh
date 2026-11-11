#!/usr/bin/env bash
set -euo pipefail

agents=$(sudo /var/ossec/bin/agent_control -lc)
printf '%s\n' "$agents"
for endpoint in win-endpoint linux-endpoint; do
    if ! grep -Fq "Name: $endpoint," <<< "$agents"; then
        printf 'Expected active agent missing: %s\n' "$endpoint" >&2
        exit 1
    fi
done
