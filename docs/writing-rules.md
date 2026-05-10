# Writing Rules

Rules are small functions that receive a `ScanContext` and return findings.

```python
from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    if context.file_exists("pyproject.toml"):
        return []

    return [finding(
        rule,
        "No pyproject.toml was found.",
        recommendation="Add pyproject.toml so contributors can install the project.",
    )]
```

Then register the rule in `src/data_agent_doctor/rules/__init__.py`:

```python
Rule(
    id="my-rule",
    title="My rule title",
    category="maintainability",
    default_severity="low",
    run=my_rule_run,
)
```

## Context Helpers

```python
context.cwd
context.files
context.file_exists("pyproject.toml")
context.read_text("README.md")
context.read_json("config.json")
context.find_files(lambda file: file.suffix == ".py")
context.grep(r"openai", extensions={".py", ".md"}, include_tests=False)
```

## Severity

- `high`: likely security, secret, data access, PII, or destructive-action risk
- `medium`: production-readiness gap that should be fixed before serious use
- `low`: contributor experience or maintainability issue
- `info`: useful context without a strong warning

## Test Pattern

Use temporary directories so tests do not depend on local state:

```python
import tempfile
import unittest
from pathlib import Path

from data_agent_doctor.scanner import scan_project


class MyRuleTest(unittest.TestCase):
    def test_rule_finds_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "agent.py").write_text("agent = 'demo'", encoding="utf-8")

            result = scan_project(root, only_rules=["my-rule"])
            self.assertEqual(result.findings[0].rule_id, "my-rule")
```

## Strong Rule Ideas

- Airflow DAGs with LLM calls but missing retries
- dbt sources feeding RAG without freshness tests
- Spark jobs creating embeddings without source metadata
- LangGraph tools without tracing or tool-call audit logs
- SQL agents that allow write queries by default
- notebooks with stored outputs or obvious secrets
- Iceberg tables with missing maintenance tasks

