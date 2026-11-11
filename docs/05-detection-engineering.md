# Detection engineering

Back up `/var/ossec/etc/rules/local_rules.xml` before installing [the lab rules](../configs/server/local_rules.xml). On a fresh manager, use the lab file as `local_rules.xml`. If there are existing local rules, retain the installed file and load this group from a separate `wazuh-siem-lab.xml` under the configured local rules directory. Confirm the IDs are free before copying.

```bash
sudo cp -p /var/ossec/etc/rules/local_rules.xml /var/ossec/etc/rules/local_rules.xml.pre-lab
sudo cp configs/server/local_rules.xml /var/ossec/etc/rules/local_rules.xml
sudo /var/ossec/bin/wazuh-analysisd -t
sudo systemctl restart wazuh-manager
```

Open a fresh `sudo /var/ossec/bin/wazuh-logtest` session for each case. Paste the entire fixture as one line. Phase 3 below is the expected rule match. Observed results for every case are `<FILL_FROM_LAB_RUN>`. Logtest validates decoding and rule selection. Use [Active response](07-active-response.md) to verify alert delivery and enforcement.

## 100100 · SSH authentication failures from the same source

MITRE ATT&CK `T1110`. Paste this line eight times within 60 seconds in the same session. Check Phase 2 for the source IP. In separate fresh sessions, try seven identical events and eight events with distinct sources. Neither negative case should produce 100100. The password-failure parent is 5760. If the installed ruleset selects a stock correlation rule at the threshold, check rule precedence before enabling active response.

```text
Oct 15 21:07:00 linux-endpoint sshd[29205]: Failed password for labuser from 192.168.56.40 port 48928 ssh2
```

Expected Phase 3 excerpt

```text
id: '100100'
level: '12'
description: 'SSH authentication failures from the same source'
```

## 100110 · Encoded PowerShell command line

MITRE ATT&CK `T1059.001`. Paste the fixture once.

```json
{"win":{"system":{"providerName":"Microsoft-Windows-Sysmon","channel":"Microsoft-Windows-Sysmon/Operational","eventID":"1","severityValue":"INFORMATION"},"eventdata":{"image":"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe","commandLine":"powershell.exe -EncodedCommand FIXTURE_ONLY"}}}
```

Expected Phase 3 excerpt

```text
id: '100110'
level: '9'
description: 'Encoded PowerShell command line'
```

## 100120 · Process access targeting LSASS

MITRE ATT&CK `T1003.001`. Inspect the source process and access mask during triage. Process access alone is an indicator.

```json
{"win":{"system":{"providerName":"Microsoft-Windows-Sysmon","channel":"Microsoft-Windows-Sysmon/Operational","eventID":"10","severityValue":"INFORMATION"},"eventdata":{"targetImage":"C:\\Windows\\System32\\lsass.exe","sourceImage":"C:\\Lab\\fixture.exe","grantedAccess":"0x1010"}}}
```

Expected Phase 3 excerpt

```text
id: '100120'
level: '10'
description: 'Process access targeting LSASS'
```

## 100130 · Windows scheduled task created

MITRE ATT&CK `T1053.005`. This fixture uses Security event 4698 and the stock task creation rule 60228.

```json
{"win":{"system":{"providerName":"Microsoft-Windows-Security-Auditing","channel":"Security","eventID":"4698","severityValue":"AUDIT_SUCCESS"},"eventdata":{"taskName":"\\WazuhLabFixture","subjectUserName":"labuser"}}}
```

Expected Phase 3 excerpt

```text
id: '100130'
level: '8'
description: 'Windows scheduled task created'
```

## 100140 · Registry Run or RunOnce value set

MITRE ATT&CK `T1547.001`. Paste the fixture once.

```json
{"win":{"system":{"providerName":"Microsoft-Windows-Sysmon","channel":"Microsoft-Windows-Sysmon/Operational","eventID":"13","severityValue":"INFORMATION"},"eventdata":{"targetObject":"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\WazuhLabFixture","image":"C:\\Lab\\fixture.exe","details":"FIXTURE_ONLY"}}}
```

Expected Phase 3 excerpt

```text
id: '100140'
level: '9'
description: 'Registry Run or RunOnce value set'
```

## 100150 · Linux local user created

MITRE ATT&CK `T1136.001`. Paste the fixture once.

```text
Oct 15 21:08:00 linux-endpoint useradd[3210]: new user: name=wazuhfixture, UID=2001, GID=2001, home=/home/wazuhfixture, shell=/usr/sbin/nologin
```

Expected Phase 3 excerpt

```text
id: '100150'
level: '8'
description: 'Linux local user created'
```

If a Windows fixture fails to decode, inspect Phase 2 and compare field names and value encoding with an actual collected `full_log` from the installed release. The Sysmon rules depend on informational events and the stock event-specific parents. The Linux account rule depends on stock rule 5902 and the syslog program name `useradd`.

[Wazuh rule testing](https://documentation.wazuh.com/current/user-manual/ruleset/testing.html) · [Rules syntax](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html)
