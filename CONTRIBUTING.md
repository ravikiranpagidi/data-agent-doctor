# Contributing to Data Agent Doctor

Thanks for helping make AI/data-agent projects safer and easier to ship.

This repo is designed so useful contributions can be small:

1. Add or improve one rule in `src/data_agent_doctor/rules/`.
2. Add or update a test in `tests/`.
3. Add a short README note if the behavior is user-facing.

## Local Setup

```bash
python -m unittest discover -s tests
python -m data_agent_doctor examples/risky-data-agent
python -m data_agent_doctor --list-rules
```

The scanner has no runtime dependencies. Python 3.10+ is enough.

## Project Shape

```text
src/data_agent_doctor/cli.py          CLI entrypoint
src/data_agent_doctor/scanner.py      Loads config and runs rules
src/data_agent_doctor/context.py      File discovery and grep helpers
src/data_agent_doctor/rules/          One file per rule
src/data_agent_doctor/reporters/      Console output
tests/                                unittest test suite
examples/                             Small sample projects
docs/writing-rules.md                 How to add a rule
```

## Rule Guidelines

Good rules are:

- useful for production readiness
- specific enough to avoid noisy findings
- actionable, with a clear recommendation
- easy to test with a small fixture
- helpful across data engineering, GenAI, or agentic AI projects

Avoid rules that only enforce personal style preferences.

## Pull Request Checklist

- [ ] I added or updated tests.
- [ ] I ran `python -m unittest discover -s tests`.
- [ ] I updated docs when behavior changed.
- [ ] I kept findings actionable and low-noise.

## Issue Labels We Like

- `good first issue`: small rule, docs, or test work
- `rule idea`: new scanner rule proposal
- `data-engineering`: Airflow, Spark, dbt, Iceberg, warehouse, or pipeline checks
- `agentic-ai`: agent, tool-call, workflow, memory, or evaluation checks
- `security`: secrets, permissions, PII, SQL, or governance checks
- `observability`: lineage, tracing, logging, metrics, or cost checks
