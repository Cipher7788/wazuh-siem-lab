# Scheduled task and Run key fixtures

> Controlled lab testing only. Use the isolated lab VMs.

## Objective

Validate two common persistence indicators from Windows event fixtures.

## Prerequisites and procedure

Load the lab rules and start `sudo /var/ossec/bin/wazuh-logtest` on the manager. Paste cases 100130 and 100140 from [Detection engineering](../docs/05-detection-engineering.md) in separate sessions. Compare the Phase 3 IDs and record the task name or registry value path.

## Expected detection

| Rule IDs | MITRE ATT&CK |
| --- | --- |
| 100130, 100140 | T1053.005, T1547.001 |

## Cleanup

Exit each Logtest session.

## Results

| Alert generated (Y/N) | Rule ID | Time-to-alert (s) | Notes |
| --- | --- | --- | --- |
| `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` |

Use the [incident report stub](../ir-reports/06-persistence-schtask-runkey.md).
