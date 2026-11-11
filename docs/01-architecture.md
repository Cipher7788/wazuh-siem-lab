# Architecture

Create an isolated host-only network for 192.168.56.0/24. Use the VM console to configure static IPs and confirm host-only connectivity. Leave the host-only adapter without a default gateway. Stage official packages before testing, then disconnect temporary NAT adapters. Avoid bridging or port forwarding.

| VM | Static address | Role |
| --- | --- | --- |
| wazuh-server | 192.168.56.10 | Ubuntu 22.04, all-in-one manager, indexer and dashboard, 4 vCPU, 8 GB RAM, 50 GB disk |
| win-endpoint | 192.168.56.20 | Windows 10/11, Wazuh agent, Sysmon |
| linux-endpoint | 192.168.56.30 | Ubuntu, Wazuh agent, auditd |
| kali-attacker | 192.168.56.40 | Kali Linux, reserved source identity for synthetic SSH exercises |

| TCP port | Path |
| --- | --- |
| 1514 | Endpoints to manager for events |
| 1515 | Endpoints to manager for enrollment |
| 443 | Lab administrator to dashboard |
| 55000 | Dashboard to manager API on the server |
| 9200 | Dashboard and Filebeat to indexer on the server |

Restrict API and indexer access to the server. Reserve an unused host address for the hypervisor adapter, such as 192.168.56.1. Snapshot clean VMs before configuring the lab.
