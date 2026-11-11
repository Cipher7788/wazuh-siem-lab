# Incident response playbook

This controlled lab workflow uses the requested operational steps. [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) relates incident response to the CSF 2.0 Detect, Respond and Recover functions and continuous improvement.

## Detect

In Wazuh Discover, select the alerts data view (typically `wazuh-alerts-*`) and a UTC window around the exercise. Open the event JSON and capture the alert timestamp, rule ID, agent and original event reference.

## Triage

Confirm the expected exercise and agent. Apply the matrix using the evidence available. Escalate severity as scope or impact becomes clearer.

| Severity | Criteria | Action |
| --- | --- | --- |
| Low | Expected isolated marker or authorized change | Record baseline evidence |
| Medium | Single suspicious signal with unclear context | Check neighboring events and validate the source |
| High | Correlated unauthorized activity or multiple corroborating indicators | Contain the affected lab endpoint and preserve evidence |
| Critical | Confirmed impact across lab hosts or loss of visibility on the manager | Isolate the affected VMs and recover from known-good state |

## Investigate

Add Discover filters one at a time. Record UTC boundaries, raw event references, and any observations that contradict the initial hypothesis.

| Discover field | Example | Pivot |
| --- | --- | --- |
| `agent.name` | `linux-endpoint` | Reconstruct the endpoint timeline |
| `data.srcip` | `192.168.56.40` | Find SSH events attributed to the same source |
| `rule.id` | `100100` | Compare all matches for the correlation rule |
| `data.win.eventdata.image` | PowerShell executable path from the alert | Compare execution context across Windows events |

For Sysmon process access, pivot on `data.win.eventdata.sourceImage` and `data.win.eventdata.targetImage`. For file integrity, pivot on the affected path. Treat synthetic fixture indicators as exercise data.

## Contain

For the SSH replay, verify the response and affected IP using [Active response](07-active-response.md). For a broader containment decision, document the selected VM, preserve console access, and isolate its host-only adapter if warranted.

## Eradicate and recover

Use the scenario cleanup procedure or restore the clean VM snapshot. Verify agent connectivity, log delivery and removal of any temporary firewall entry or fixture artifacts.

## Lessons learned

Use the [incident report template](../ir-reports/TEMPLATE.md). Assign an owner to each gap or tuning action and record retest evidence before closing the exercise.
