#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! $1 =~ ^4\.[0-9]+$ ]]; then
    printf 'Usage: %s <4.x series from the official Wazuh quickstart>\n' "$0" >&2
    exit 2
fi

scripts=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ ! -x /var/ossec/bin/wazuh-analysisd ]]; then
    bash "$scripts/install-server.sh" "$1"
fi
sudo bash "$scripts/apply-lab-rules.sh"
