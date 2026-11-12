# Active response

After rule 5763 passes its positive and negative tests, back up the manager's `/var/ossec/etc/ossec.conf`. Merge the inner elements from [the active response snippet](../configs/server/ossec-active-response.xml). If upgrading an existing lab, change `<rules_id>100100</rules_id>` to `<rules_id>5763</rules_id>` in the existing lab response block. Reuse the existing `firewall-drop` command if present and confirm it permits a timeout. Local execution targets the Linux endpoint that generated the alert. The timeout is configured for 300 seconds.

```bash
sudo /var/ossec/bin/wazuh-analysisd -t &&
  sudo /var/ossec/bin/wazuh-execd -t &&
  sudo systemctl restart wazuh-manager &&
  sudo /var/ossec/bin/agent_control -lc
```

Use the Linux VM console for the [synthetic SSH ingestion exercise](../simulations/01-ssh-bruteforce.md). Verify rule 5763, agent name and decoded `data.srcip` in Discover. On the Linux endpoint, capture firewall state and the response log before the exercise, after the alert, and after the configured timeout.

```bash
sudo iptables -L -n --line-numbers
sudo iptables -S
sudo tail -n 50 /var/ossec/logs/active-responses.log
```

Look for an entry matching only the lab source and confirm it disappears. Compare the block and unblock evidence to record observed duration `<FILL_FROM_LAB_RUN>`. A Logtest match alone is insufficient for this check.

## Rollback

Use the VM console. Allow any pending timeout to expire where practical. Remove the rule-specific `<active-response>` block or restore the backed-up manager configuration and restart the manager. Keep any command block shared by other rules. If a residual lab drop remains on the endpoint, inspect `sudo iptables -S` and remove only the exact matching rule by replacing its leading `-A` with `-D` in the corresponding `sudo iptables` command. Recheck the firewall and confirm the agent is still active.

[Wazuh firewall-drop example](https://documentation.wazuh.com/current/user-manual/capabilities/active-response/ar-use-cases/blocking-ssh-brute-force.html)
