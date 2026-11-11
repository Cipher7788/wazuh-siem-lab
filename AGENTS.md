# Repository conventions

- Keep all testing on the isolated host-only lab network. This repository is for controlled lab testing only.
- Preserve `<FILL_FROM_LAB_RUN>` until there is real evidence. Label fixture output as expected and avoid committing credentials or raw sensitive logs.
- Use official Wazuh documentation and packages. Verify the current 4.x version before installation.
- Validate every XML file with `xmllint --noout` and every Bash script with `shellcheck`. Keep shell files in LF format.
- Maintain one reproducible Wazuh Logtest case for each custom rule. Run manager configuration checks before restarting it.
- Use `Set-StrictMode -Version Latest` in PowerShell scripts.
