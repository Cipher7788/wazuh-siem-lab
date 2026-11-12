#!/usr/bin/env bash
set -euo pipefail

if (( EUID != 0 )); then
    printf 'Run with sudo on the lab manager.\n' >&2
    exit 2
fi

repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
rules_dir=/var/ossec/etc/rules
target="$rules_dir/wazuh-siem-lab.xml"
analysisd=/var/ossec/bin/wazuh-analysisd

if [[ ! -x $analysisd || ! -d $rules_dir ]]; then
    printf 'Install the Wazuh manager before applying the lab rules.\n' >&2
    exit 2
fi

exec 9>/var/ossec/etc/.wazuh-siem-lab.lock
flock -x 9

backup=$(mktemp -d /var/ossec/etc/.wazuh-siem-lab.XXXXXXXX)
if [[ -e $target ]]; then
    cp -p -- "$target" "$backup/previous"
fi
install -o root -g wazuh -m 0640 "$repo/configs/server/local_rules.xml" "$backup/next"

restore_rules() {
    if [[ -f $backup/previous ]]; then
        mv -f -- "$backup/previous" "$target"
    else
        rm -f -- "$target"
    fi
    rmdir -- "$backup"
}

mv -f -- "$backup/next" "$target"
if ! validation=$("$analysisd" -t -d 2>&1); then
    printf '%s\n' "$validation" >&2
    restore_rules
    printf 'Wazuh rejected the configuration. The previous rules were restored.\n' >&2
    exit 1
fi

# The rule reader logs each file selected by Wazuh's effective ruleset in debug mode.
rulefile=${target#/var/ossec/}
if ! grep -Fq -e "DEBUG: $rulefile is the rulefile" \
    -e "DEBUG: ./$rulefile is the rulefile" \
    -e "DEBUG: /$rulefile is the rulefile" <<< "$validation"; then
    restore_rules
    printf 'Wazuh did not select %s. Check the ruleset includes and exclusions.\n' "$rulefile" >&2
    exit 1
fi

if ! systemctl restart wazuh-manager; then
    restore_rules
    if ! systemctl restart wazuh-manager; then
        printf 'The previous rules were restored. Check the manager service journal.\n' >&2
    fi
    exit 1
fi

rm -f -- "$backup/previous"
rmdir -- "$backup"
printf 'Lab rules installed and manager restarted.\n'
