# Metrics

Fill every measurement from a documented lab run. Record the UTC window, time source, dashboard filters, and evidence references. Keep Logtest matches and tabletop exercises out of end-to-end alert metrics and record them in their scenario reports.

| Metric | Lab result | How to measure |
| --- | --- | --- |
| Agents active | `<FILL_FROM_LAB_RUN>` | Count enrolled endpoints in Active state at the recorded time. Exclude the manager. |
| Events/day | `<FILL_FROM_LAB_RUN>` | Count ingested event documents in an enabled archive data view for a full UTC day. If only alert indexing is available, leave this metric open. |
| Scenarios run | `<FILL_FROM_LAB_RUN>` | Count completed ingestion exercises with a defined expected alert. |
| Scenarios with expected alert | `<FILL_FROM_LAB_RUN>` | Count qualifying runs with at least one expected alert tied to that run's timestamp and agent. |
| Alerts generated | `<FILL_FROM_LAB_RUN>` | Count matching alert documents for qualifying runs and report duplicate alerts separately. |
| Detection rate (%) | `<FILL_FROM_LAB_RUN>` | Divide runs with an expected alert by qualifying runs and multiply by 100. Record N/A if the denominator is zero. |
| Mean time-to-alert (s) | `<FILL_FROM_LAB_RUN>` | Average elapsed time from recorded stimulus start to first matching alert over detected qualifying runs. |
| Active response block time (s) | `<FILL_FROM_LAB_RUN>` | Compare observed add and removal timestamps in the endpoint response log, corroborated by firewall state. |
| Custom rules written | `<FILL_FROM_LAB_RUN>` | Count lab rule definitions installed on the tested manager and record the tested revision. |
| False positives tuned out | `<FILL_FROM_LAB_RUN>` | Replay the same labeled benign corpus before and after tuning. Count benign events that stop alerting and retest expected positives. |

UTC measurement window and evidence references `<FILL_FROM_LAB_RUN>`. Redacted screenshots `<FILL_FROM_LAB_RUN>`.
