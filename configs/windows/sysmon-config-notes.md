# Sysmon configuration

Review the [SwiftOnSecurity configuration](https://github.com/SwiftOnSecurity/sysmon-config) or [Olaf Hartong Sysmon Modular](https://github.com/olafhartong/sysmon-modular). Choose one reviewed configuration with Process Create (1), Process Access (10) for LSASS, and Registry value set (13) for Run or RunOnce. Confirm the filters retain the needed events on the endpoint. This repository links to upstream configurations.

Windows Security event 4698 comes from Windows auditing. Enable success auditing for Other Object Access Events and confirm the existing Wazuh Security channel subscription permits 4698.
