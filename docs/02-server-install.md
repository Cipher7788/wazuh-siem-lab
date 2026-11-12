# Server installation

Use a fresh Ubuntu 22.04 server with the address and resources in [Architecture](01-architecture.md). Verify the current version at documentation.wazuh.com using the [official quickstart](https://documentation.wazuh.com/current/quickstart.html). Substitute its 4.x series when prompted below. The script downloads the official assistant and invokes the documented all-in-one mode.

```bash
read -r -p 'Wazuh 4.x series from the official quickstart: ' wazuh_series
bash scripts/setup-lab-manager.sh "$wazuh_series"
sudo systemctl status wazuh-manager wazuh-indexer wazuh-dashboard filebeat --no-pager
```

The setup script runs the official installer on a fresh server and applies the [lab detection rules](05-detection-engineering.md) once the manager, indexer, dashboard, and Filebeat are active. If setup lists missing or inactive services on an existing server, complete or repair that installation and rerun setup. ## First dashboard login

1. From the lab host, open [https://192.168.56.10](https://192.168.56.10) on TCP 443. If prompted about the installer-generated certificate, compare the SHA-256 fingerprint shown by the browser with the fingerprint of the certificate configured under `server.ssl.certificate` in `/etc/wazuh-dashboard/opensearch_dashboards.yml`. On the server, run `sudo openssl x509 -in /path/to/configured-certificate.pem -noout -fingerprint -sha256` with that path.
2. Sign in as `admin` with the password printed by the installer. If needed, retrieve it on the server from `wazuh-install-files/wazuh-passwords.txt` inside `wazuh-install-files.tar`. The wrapper prints the archive's directory, which is under `/var/tmp` by default. Keep the archive and credentials private.
3. After [agent enrollment](03-agent-enrollment.md), open **Agents management → Summary** and confirm both endpoints are **Active**. Use the [dashboard checklist](../README.md#dashboard) to verify indexed alerts.

If HTTPS is unreachable, confirm the dashboard service is active and listening on port 443. Run `sudo journalctl -u wazuh-dashboard -b -n 50 --no-pager` for startup errors and check the indexer status if the dashboard loads but reports a backend error.

Disconnect temporary package-download networking after installation and agent package staging. See the [Wazuh quickstart](https://documentation.wazuh.com/current/quickstart.html) for the installer output and credential archive layout.
