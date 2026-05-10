from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding
from data_agent_doctor.rules.helpers import has_any_text


FRAMEWORK_PATTERNS = [
    r"\blanggraph\b",
    r"\bcrewai\b",
    r"\bautogen\b",
    r"\bllama_index\b|\bllama-index\b",
    r"\bopenai\b",
    r"\bairflow\b",
    r"\bdagster\b",
    r"\bdbt\b",
    r"\bspark\b|\bpyspark\b",
    r"\biceberg\b",
]


def run(context: ScanContext, rule: Rule):
    has_manifest = any(
        context.file_exists(path)
        for path in ["pyproject.toml", "requirements.txt", "setup.py", "environment.yml"]
    )
    if not has_manifest:
        return [finding(
            rule,
            "No Python project manifest was found.",
            recommendation="Add pyproject.toml or requirements.txt so contributors can install and run the project.",
        )]

    if not has_any_text(context, FRAMEWORK_PATTERNS):
        return [finding(
            rule,
            "No common AI-agent or data-engineering framework was detected.",
            severity="info",
            recommendation="Document the main frameworks used, such as Airflow, Dagster, Spark, dbt, LangGraph, CrewAI, LlamaIndex, or OpenAI.",
        )]

    return []

