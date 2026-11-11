#!/usr/bin/env bash
set -euo pipefail

minimum=262144
current=$(sysctl -n vm.max_map_count)
if (( current < minimum )); then
    printf 'vm.max_map_count = %s\n' "$minimum" |
        sudo tee /etc/sysctl.d/99-wazuh-lab-max-map-count.conf >/dev/null
    sudo sysctl -p /etc/sysctl.d/99-wazuh-lab-max-map-count.conf
fi
sysctl vm.max_map_count
