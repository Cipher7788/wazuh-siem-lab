# Server installation

Use a fresh Ubuntu 22.04 server with the address and resources in [Architecture](01-architecture.md). Verify the current version at documentation.wazuh.com using the [official quickstart](https://documentation.wazuh.com/current/quickstart.html). Substitute its 4.x series when prompted below. The script downloads the official assistant and invokes the documented all-in-one mode.

```bash
read -r -p 'Wazuh 4.x series from the official quickstart: ' wazuh_series
bash scripts/install-server.sh "$wazuh_series"
sudo systemctl status wazuh-manager wazuh-indexer wazuh-dashboard filebeat --no-pager
```

Run the installer from a private working directory or keep its printed installation directory outside your Git staging area. The installer creates credentials and certificates there. Store them privately. Open `https://192.168.56.10` from the lab host. Verify the lab certificate against the one on the server before accepting it. Disconnect package-download networking after installation.
