# Risky Data Agent Example

This fixture intentionally contains common production-readiness gaps:

- SQL execution from agent code
- vector ingestion with no metadata or PII handling
- Airflow DAG with an AI task and no data quality gate
- hard-coded secret-like value

Use it to see Data Agent Doctor findings:

```bash
python -m data_agent_doctor examples/risky-data-agent
```
