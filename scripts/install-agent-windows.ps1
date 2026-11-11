#Requires -RunAsAdministrator
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$MsiPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$package = Get-Item -LiteralPath $MsiPath
if ($package.PSIsContainer -or $package.Extension -ne '.msi') {
    throw 'Provide an official Wazuh agent MSI file.'
}

$arguments = @(
    '/i', ('"{0}"' -f $package.FullName), '/qn', '/norestart',
    'WAZUH_MANAGER=192.168.56.10', 'WAZUH_REGISTRATION_SERVER=192.168.56.10',
    'WAZUH_AGENT_NAME=win-endpoint'
)
$process = Start-Process -FilePath msiexec.exe -ArgumentList $arguments -WindowStyle Hidden -Wait -PassThru
switch ($process.ExitCode) {
    0 { Start-Service -Name WazuhSvc }
    3010 { Write-Warning 'Reboot required. Start WazuhSvc after reboot if needed.' }
    default { throw "Wazuh MSI installation failed with exit code $($process.ExitCode)." }
}
