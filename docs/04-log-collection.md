# Log collection

Back up each agent's configuration first. Merge the inner elements of each XML snippet into the agent's existing `<ossec_config>`. Preserve other configured inputs and avoid duplicate entries.

## Windows

Install Sysmon from [Microsoft Sysinternals](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) and apply a configuration reviewed using the [Sysmon notes](../configs/windows/sysmon-config-notes.md). Add the [event channel input](../configs/windows/ossec-sysmon-localfile.xml) to `C:\Program Files (x86)\ossec-agent\ossec.conf`. Keep the Security channel enabled for event 4698. Verify the exact Sysmon channel name and restart the agent.

```powershell
Get-WinEvent -ListLog 'Microsoft-Windows-Sysmon/Operational'
Restart-Service WazuhSvc
```

## Ubuntu

Install auditd and create the dedicated monitored directory. Copy the audit watches to a lab-owned rules file. Merge the directory entry in the [FIM snippet](../configs/linux/ossec-fim-syscheck.xml) into the existing `<syscheck>` section of `/var/ossec/etc/ossec.conf`.

```bash
sudo apt-get install auditd
sudo install -d -m 0755 /opt/wazuh-lab/fim
sudo install -m 0640 configs/linux/audit.rules /etc/audit/rules.d/60-wazuh-lab.rules
sudo augenrules --load
sudo auditctl -l
```

Add this audit source if missing. Also confirm SSH and useradd messages reach a configured source. Use the agent's existing journald input or, on a host with rsyslog writing `/var/log/auth.log`, configure a syslog input for that path. Choose one source per event to avoid double counting.

```xml
<localfile>
  <location>/var/log/audit/audit.log</location>
  <log_format>audit</log_format>
</localfile>
```

Run `sudo /var/ossec/bin/wazuh-logcollector -t` and `sudo systemctl restart wazuh-agent`. Review `/var/ossec/logs/ossec.log` for collection and FIM errors, then test a file change using the [FIM exercise](../simulations/03-fim-file-drop.md).
