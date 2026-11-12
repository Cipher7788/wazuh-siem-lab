#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! $1 =~ ^4\.[0-9]+$ ]]; then
    printf 'Usage: %s <4.x series from the official Wazuh quickstart>\n' "$0" >&2
    exit 2
fi

scripts=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
services=(wazuh-manager wazuh-indexer wazuh-dashboard filebeat)
installed_units=$(systemctl list-unit-files --no-legend --no-pager "${services[@]/%/.service}")
if [[ ! -e /var/ossec/bin/wazuh-analysisd && -z $installed_units ]]; then
    bash "$scripts/install-server.sh" "$1"
fi

unready=()
for service in "${services[@]}"; do
    if ! systemctl is-active --quiet "$service.service"; then
        unready+=("$service")
    fi
done
if (( ${#unready[@]} > 0 )); then
    printf 'Complete or repair the Wazuh installation. Missing or inactive: %s\n' "${unready[*]}" >&2
    exit 1
fi

sudo bash "$scripts/apply-lab-rules.sh"
