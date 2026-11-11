# Network discovery telemetry review

> Controlled lab testing only. Use the isolated lab VMs.

## Objective

Practice identifying a one-source, multiple-destination-port pattern from a synthetic record.

## Prerequisites and procedure

On the Linux console, print a synthetic connection summary for tabletop analysis.

```bash
printf '%s\n' \
    'fixture src=192.168.56.40 dst=192.168.56.30 dport=22' \
    'fixture src=192.168.56.40 dst=192.168.56.30 dport=80' \
    'fixture src=192.168.56.40 dst=192.168.56.30 dport=443'
```

Identify the source, destination and port fan-out. Record the telemetry gap. The lab configuration has no scan sensor or detection for these records.

## Expected detection

| Rule IDs | MITRE ATT&CK |
| --- | --- |
| None in the supplied ruleset | T1046 |

## Cleanup

Close the console output.

## Results

| Alert generated (Y/N) | Rule ID | Time-to-alert (s) | Notes |
| --- | --- | --- | --- |
| `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` |

Use the [incident report stub](../ir-reports/02-port-scan.md).
