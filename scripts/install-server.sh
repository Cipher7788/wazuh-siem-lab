#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! $1 =~ ^4\.[0-9]+$ ]]; then
    printf 'Usage: %s <4.x series from the official Wazuh quickstart>\n' "$0" >&2
    exit 2
fi

umask 077
install_dir=$(mktemp -d "$PWD/wazuh-install.XXXXXXXX")
printf 'Installer and generated credentials directory: %s\n' "$install_dir"
cd "$install_dir"
curl --fail --silent --show-error --location --output wazuh-install.sh \
    "https://packages.wazuh.com/$1/wazuh-install.sh"
sudo bash ./wazuh-install.sh -a
