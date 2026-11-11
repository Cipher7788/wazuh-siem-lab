# SSH authentication failure replay

> Controlled lab testing only. Use the isolated lab VMs.

## Objective

Validate correlation and, optionally, the endpoint firewall response.

## Prerequisites and procedure

First run the [100100 Logtest fixture](../docs/05-detection-engineering.md). For ingestion, use the Linux endpoint's console, confirm the manager reports the agent active, and create an empty dedicated file before adding this temporary agent input.

```bash
sudo install -m 0644 /dev/null /var/log/wazuh-lab-ssh-fixture.log
```

```xml
<localfile>
  <location>/var/log/wazuh-lab-ssh-fixture.log</location>
  <log_format>syslog</log_format>
</localfile>
```

Restart the agent and check its log for the new input. Record the start time and append eight fabricated auth lines.

```bash
date -u +%FT%TZ
for port in {48928..48935}; do
    printf '%s linux-endpoint sshd[29205]: Failed password for labuser from 192.168.56.40 port %s ssh2\n' \
        "$(LC_ALL=C date '+%b %e %T')" "$port"
done | sudo tee -a /var/log/wazuh-lab-ssh-fixture.log >/dev/null
```

Check Discover for agent `linux-endpoint`, source `192.168.56.40`, and rule 100100. If enabled, follow [Active response](../docs/07-active-response.md).

## Expected detection

| Rule IDs | MITRE ATT&CK |
| --- | --- |
| 100100 | T1110 |

## Cleanup

Wait for any response timeout, remove the temporary input, restart the agent, then remove `/var/log/wazuh-lab-ssh-fixture.log`.

## Results

| Alert generated (Y/N) | Rule ID | Time-to-alert (s) | Notes |
| --- | --- | --- | --- |
| `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` | `<FILL_FROM_LAB_RUN>` |

Use the [incident report stub](../ir-reports/01-ssh-bruteforce.md).
