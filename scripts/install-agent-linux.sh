#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! -f $1 || $1 != *.deb ]]; then
    printf 'Usage: %s <official Wazuh agent DEB path>\n' "$0" >&2
    exit 2
fi

sudo env WAZUH_MANAGER=192.168.56.10 WAZUH_REGISTRATION_SERVER=192.168.56.10 \
    WAZUH_AGENT_NAME=linux-endpoint dpkg -i -- "$1"
sudo systemctl daemon-reload
sudo systemctl enable --now wazuh-agent
