# Troubleshooting

| Symptom | Check |
| --- | --- |
| Agent disconnected | Verify static IPs and host-only adapter membership. On the manager check `sudo ss -lntp` for 1514 and 1515. On Windows run `Test-NetConnection 192.168.56.10 -Port 1514` and repeat for 1515. Check agent service status and ossec.log for enrollment or duplicate-name errors. |
| Sysmon alerts missing | Run `Get-WinEvent -ListLog 'Microsoft-Windows-Sysmon/Operational'`. Confirm exact channel and eventchannel format, check that the Sysmon configuration emits the relevant event, and restart WazuhSvc. Inspect the Windows agent log and test rule selection on the manager. |
| Indexer fails to start | Read `sudo journalctl -u wazuh-indexer -b` and check `sysctl vm.max_map_count`. If below 262144, run `bash scripts/fix-vm-max-map-count.sh` and retry `sudo systemctl restart wazuh-indexer`. |
| Clock drift | Compare UTC on every VM. On Ubuntu use `timedatectl status`. On Windows use `w32tm /query /status`. Set a reachable lab time source or hypervisor guest synchronization and verify again after snapshot restore. |
| Low-RAM installer check | Restore the planned 8 GB allocation. For a deliberately undersized disposable VM, inspect the downloaded assistant's `--help` for `-i` or `--ignore-check`. If the release supports it, the flag bypasses prerequisite checks and does not increase available memory. The repository installer uses the normal hardware checks. |
