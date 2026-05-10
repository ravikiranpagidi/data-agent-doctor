# Data Agent Doctor

Data Agent Doctor is a Python-first production-readiness scanner for AI agents that touch data systems.

It helps teams answer a practical question:

> Is this data/AI agent project ready to run near real data, real users, and real business workflows?

The first release focuses on the gaps that often appear when GenAI, agentic AI, and data engineering meet:

- agents with SQL access but no query guardrails
- RAG or vector ingestion without source metadata or sensitive-data hygiene
- Airflow/Dagster/Spark/dbt pipelines with AI steps but no data quality gate
- missing lineage, audit logging, tracing, cost, latency, retry, or fallback behavior
- committed `.env` files and hard-coded secrets
- notebook-heavy projects with little testable production code

## Quick Start

```bash
pipx run data-agent-doctor .
```

From a clone:

```bash
python -m data_agent_doctor .
python -m data_agent_doctor examples/risky-data-agent
python -m data_agent_doctor --list-rules
```

This project intentionally has **zero runtime dependencies**. Python 3.10+ is enough.

## Example Output

```text
Data Agent Doctor
Path: /workspace/customer-support-agent
Score: 37/100
Findings: 2 high, 2 medium, 1 low, 0 info

[HIGH] agent-sql-guardrails (agents/refund_agent.py:18)
  Agent or tool code appears to access SQL without obvious query guardrails.
  Fix: Add read-only scopes, SQL validation, table allowlists, row limits, and human approval for risky actions.
```

## CLI

```bash
data-agent-doctor [path]
data-agent-doctor [path] --json
data-agent-doctor [path] --fail-level high
data-agent-doctor [path] --only agent-sql-guardrails,pii-vector-hygiene
data-agent-doctor [path] --skip notebook-hygiene
data-agent-doctor --list-rules
```

Short alias:

```bash
dad .
```

## Configuration

Add `.data-agent-doctor.json` to the project you are scanning:

```json
{
  "skip_rules": ["notebook-hygiene"],
  "ignore_paths": ["examples/risky-data-agent/"],
  "max_files": 3000
}
```

## Built-In Rules

| Rule | Category | Purpose |
| --- | --- | --- |
| `framework-metadata` | maintainability | Checks whether Python/data/AI framework usage is discoverable. |
| `agent-sql-guardrails` | security | Flags agent or tool code that appears to access SQL without guardrails. |
| `pii-vector-hygiene` | data governance | Checks RAG/vector ingestion for metadata, redaction, and sensitive-data hygiene. |
| `data-quality-gate` | data quality | Looks for data quality checks before AI steps in pipelines. |
| `lineage-audit` | observability | Checks whether agent and data actions are traceable. |
| `cost-budget` | operations | Looks for token, cost, timeout, and latency controls around LLM usage. |
| `retry-fallback` | reliability | Checks whether agent workflows define retries, timeouts, or fallbacks. |
| `secret-hygiene` | security | Flags committed `.env` files and hard-coded secret-like values. |
| `notebook-hygiene` | maintainability | Warns when notebooks may need cleanup or modularization. |
| `tests-present` | contributor experience | Checks for tests. |

## Why This Exists

Most AI-agent demos avoid the hardest part: production data.

When agents can query databases, trigger data pipelines, read documents, generate SQL, call tools, or embed enterprise knowledge, the risk profile changes. The project needs data quality, lineage, access control, observability, cost boundaries, and failure handling.

Data Agent Doctor is not a replacement for security review or data governance. It is a fast first pass that gives maintainers and contributors a shared checklist.

## Contributor-Friendly Roadmap

Good first issues:

- add a rule for Airflow DAGs with AI tasks but no retry policy
- add a rule for dbt models feeding RAG without freshness checks
- add Spark/Iceberg table health checks
- add LangGraph-specific tool-call tracing checks
- add CrewAI and AutoGen adapters
- add SARIF output for GitHub code scanning
- add a GitHub Action wrapper
- add rules for notebook output cleanup
- add examples for Snowflake, BigQuery, Databricks, and Postgres agents

See [CONTRIBUTING.md](./CONTRIBUTING.md) and [docs/writing-rules.md](./docs/writing-rules.md).

## License

MIT
