# File integrity monitoring

> Controlled lab testing only. Use the isolated lab VMs.

## Objective

Verify real-time FIM alerting for an inert text marker.

## Prerequisites and procedure

Create the FIM directory, apply the configuration, confirm the agent is active, and wait for its baseline scan to finish.

```bash
date -u +%FT%TZ
marker=$(sudo mktemp /opt/wazuh-lab/fim/wazuh-lab-marker.XXXXXXXX)
printf '%s\n' 'Wazuh lab file-integrity marker' | sudo tee "$marker" >/dev/null
printf '%s\n' "$marker"
```

Filter Discover on the Linux agent and the marker path. Expect stock rule 554 for creation. A separate update can produce stock rule 550.

## Expected detection

| Rule IDs | MITRE ATT&CK |
| --- | --- |
| 554 for file creation (stock) | None assigned to the benign marker |

## Cleanup

Keep the same shell and run `sudo rm -- "$marker"` after preserving evidence. Removal can generate stock rule 553.

## Results

| Alert generated (Y/N) | Rule ID | Time-to-alert (s) | Notes |
| --- | --- | --- | --- |
| `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` |

Use the [incident report stub](../ir-reports/03-fim-file-drop.md).
