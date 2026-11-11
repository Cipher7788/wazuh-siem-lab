# Windows behavior fixtures

> Controlled lab testing only. Use the isolated lab VMs.

## Objective

Validate recognition of encoded PowerShell, LSASS process access and a Run key change.

## Prerequisites and procedure

Load the lab rules and start `sudo /var/ossec/bin/wazuh-logtest` on the manager. Paste cases 100110, 100120 and 100140 from [Detection engineering](../docs/05-detection-engineering.md), using a fresh session for each. Compare the Phase 3 IDs and record the source image, target image or registry path used for triage. These fixtures model telemetry associated with the requested Atomic Red Team techniques.

## Expected detection

| Rule IDs | MITRE ATT&CK |
| --- | --- |
| 100110, 100120, 100140 | T1059.001, T1003.001, T1547.001 |

## Cleanup

Exit each Logtest session.

## Results

| Alert generated (Y/N) | Rule ID | Time-to-alert (s) | Notes |
| --- | --- | --- | --- |
| `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` |

Use the [incident report stub](../ir-reports/05-atomic-red-team-windows.md).
