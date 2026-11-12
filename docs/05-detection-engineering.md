# Detection engineering

Apply the [lab rules](../configs/server/local_rules.xml) on the Wazuh manager. Confirm the rule IDs are free and the default local rules directory is enabled. If you previously copied the lab rules into the manager's `local_rules.xml`, remove that lab group from the old file before applying this script. The script manages `/var/ossec/etc/rules/wazuh-siem-lab.xml`, validates the configuration and checks that Wazuh selects the managed file before restart, and restores the previous file if validation or restart fails.

```bash
set -o pipefail
sudo bash scripts/apply-lab-rules.sh &&
  sudo python3 scripts/test-lab-rules.py --linux-only | tee wazuh-logtest-evidence.txt
```

Each rule section contains one single-line input in a `text` or `json` code block. Expected output uses `console` blocks. The Python runner opens a fresh Logtest session per case, verifies that each input reaches decoding, and checks the exact input position of every tracked rule match. The SSH threshold case expects rule 5763 only on input eight. The command saves raw output through `tee` and exits nonzero if any selected case fails. To test Linux cases manually, paste each fixture into a fresh `sudo /var/ossec/bin/wazuh-logtest` session.

On Wazuh 4.14.10, the CLI routes these Windows JSON fixtures through the generic JSON decoder. The Windows rule parents require the EventChannel decoder. The Windows Phase 3 excerpts below describe the expected rule match after EventChannel processing. Verify those matches from collected Windows agent events in Discover. Record the event ID, rule ID, agent, and timestamp. Running the script without `--linux-only` retains the strict fixture checks for environments that support EventChannel replay. [Wazuh EventChannel Logtest limitation](https://github.com/wazuh/wazuh/issues/30472)

Use [Active response](07-active-response.md) to verify live SSH alert delivery and enforcement.

## 5763 · SSH authentication failures from the same source

MITRE ATT&CK `T1110`. Paste this line eight times within 120 seconds in the same session. Check Phase 2 for the source IP. In separate fresh sessions, try seven identical events and eight events with distinct sources. Neither negative case should produce 5763. The lab uses stock rule 5763, which correlates password-failure rule 5760. Reapplying the lab rules removes the retired custom SSH rule from the managed file. If you previously enabled active response, update its rule ID as described in [Active response](07-active-response.md).

```text
Oct 15 21:07:00 linux-endpoint sshd[29205]: Failed password for labuser from 192.168.56.40 port 48928 ssh2
```

Expected Phase 3 excerpt

```console
id: '5763'
level: '10'
description: 'sshd: brute force trying to get access to the system. Authentication failed.'
```

## 100110 · Encoded PowerShell command line

MITRE ATT&CK `T1059.001`. Paste the fixture once.

```json
{"win":{"system":{"providerName":"Microsoft-Windows-Sysmon","channel":"Microsoft-Windows-Sysmon/Operational","eventID":"1","severityValue":"INFORMATION"},"eventdata":{"image":"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe","commandLine":"powershell.exe -EncodedCommand FIXTURE_ONLY"}}}
```

Expected Phase 3 excerpt

```console
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

```console
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

```console
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

```console
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

```console
id: '100150'
level: '8'
description: 'Linux local user created'
```

If a Windows fixture fails to decode, inspect Phase 2 and compare field names and value encoding with an actual collected `full_log` from the installed release. The Sysmon rules depend on informational events and the stock event-specific parents. The Linux account rule depends on stock rule 5902 and the syslog program name `useradd`.

[Wazuh rule testing](https://documentation.wazuh.com/current/user-manual/ruleset/testing.html) · [Rules syntax](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html)
