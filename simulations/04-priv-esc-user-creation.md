# Linux local account creation telemetry

> Controlled lab testing only. Use the isolated lab VMs.

## Objective

Verify detection of a Linux local account creation record.

## Prerequisites and procedure

Load the custom rules on the manager and start `sudo /var/ossec/bin/wazuh-logtest`. Paste the single syslog line from [case 100150](../docs/05-detection-engineering.md#100150--linux-local-user-created). Compare the Phase 3 rule ID with the expected ID. This fixture represents account creation telemetry.

## Expected detection

| Rule IDs | MITRE ATT&CK |
| --- | --- |
| 100150 | T1136.001 |

## Cleanup

Exit the Logtest session.

## Results

| Alert generated (Y/N) | Rule ID | Time-to-alert (s) | Notes |
| --- | --- | --- | --- |
| `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` |

Use the [incident report stub](../ir-reports/04-priv-esc-user-creation.md).
