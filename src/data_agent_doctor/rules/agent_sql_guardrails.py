from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding
from data_agent_doctor.rules.helpers import CODE_CONFIG_EXTENSIONS


SQL_ACCESS = [
    r"\bexecute\s*\(",
    r"\bcreate_engine\s*\(",
    r"\bspark\.sql\s*\(",
    r"\bread_sql\b",
    r"\bSELECT\b.+\bFROM\b",
    r"\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bTRUNCATE\b",
]

AGENT_OR_TOOL = [
    r"\bagent\b",
    r"\btool\b",
    r"\bfunction_call\b",
    r"\blanggraph\b",
    r"\bcrewai\b",
    r"\bllama_index\b",
    r"\bopenai\b",
]

GUARDRAILS = [
    r"\bread[-_ ]?only\b",
    r"\ballowlist\b|\bdenylist\b",
    r"\bsqlglot\b|\bsqlparse\b",
    r"\bquery[_-]?validator\b",
    r"\bmax_rows\b|\blimit\b",
    r"\bapproval\b|\bhuman[_-]?in[_-]?the[_-]?loop\b",
]


def run(context: ScanContext, rule: Rule):
    has_sql = _has_any_text(context, SQL_ACCESS)
    has_agent = _has_any_text(context, AGENT_OR_TOOL)
    if not has_sql or not has_agent:
        return []

    has_guardrails = _has_any_text(context, GUARDRAILS, include_tests=True)
    if has_guardrails:
        return []

    return [finding(
        rule,
        "Agent or tool code appears to access SQL without obvious query guardrails.",
        path=_first_match_path(context, SQL_ACCESS),
        recommendation="Add read-only scopes, SQL validation, table allowlists, row limits, and human approval for risky actions.",
    )]


def _has_any_text(context: ScanContext, patterns: list[str], *, include_tests: bool = False) -> bool:
    return any(
        context.grep(pattern, extensions=CODE_CONFIG_EXTENSIONS, include_tests=include_tests)
        for pattern in patterns
    )


def _first_match_path(context: ScanContext, patterns: list[str]) -> str | None:
    for pattern in patterns:
        matches = context.grep(pattern, extensions=CODE_CONFIG_EXTENSIONS, include_tests=False)
        if matches:
            match = matches[0]
            return f"{match.path}:{match.line}"
    return None
