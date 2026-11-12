# Agent enrollment

Download official matching Windows MSI and Ubuntu DEB builds using the [Wazuh packages list](https://documentation.wazuh.com/current/installation-guide/packages-list.html). Choose the appropriate architecture and verify the published hashes. Run each installer from the repository root on its endpoint. The scripts set the manager and enrollment server to 192.168.56.10.

**Ubuntu**

```bash
read -r -p 'Path to official agent DEB: ' agent_deb
bash scripts/install-agent-linux.sh "$agent_deb"
sudo systemctl status wazuh-agent --no-pager
```

**Windows administrator PowerShell**

```powershell
$agentMsi = Read-Host 'Path to official agent MSI'
.\scripts\install-agent-windows.ps1 -MsiPath $agentMsi
Get-Service WazuhSvc
```

Run `Get-ExecutionPolicy` to check the effective PowerShell policy. If it blocks the repository script, run the [official Windows MSI installation](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-windows.html) directly from an administrator Command Prompt. Replace the example path with the verified MSI path.

```cmd
start "" /wait msiexec.exe /i "C:\path\to\wazuh-agent.msi" /qn /norestart WAZUH_MANAGER=192.168.56.10 WAZUH_REGISTRATION_SERVER=192.168.56.10 WAZUH_AGENT_NAME=win-endpoint
echo %ERRORLEVEL%
```

On exit code 0, run `net start WazuhSvc`. On exit code 3010, reboot and check the service before starting it manually if needed. For other exit codes, check the installer error before starting the service.

**Manager**

```bash
bash scripts/verify-agents.sh
```

Check the dashboard Agents view for both endpoint names and the Active status. Use [Troubleshooting](10-troubleshooting.md) for connection or enrollment errors.
