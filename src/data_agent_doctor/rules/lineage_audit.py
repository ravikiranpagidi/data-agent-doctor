from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding
from data_agent_doctor.rules.helpers import has_any_text


ACTION_PATTERNS = [
    r"\bagent\b|\btool\b|\bexecute\b|\btask\b|\boperator\b",
    r"\bopenai\b|\bllm\b|\bembedding\b|\bretriever\b",
]

TRACE_PATTERNS = [
    r"\blogger\b|\blogging\b|\baudit\b|\btrace\b|\bspan\b|\bmetrics\b",
    r"\bopentelemetry\b|\botel\b|\bmlflow\b|\blangsmith\b|\bphoenix\b",
    r"\blineage\b|\bopenlineage\b|\bmarquez\b|\bmetadata\b",
]


def run(context: ScanContext, rule: Rule):
    has_actions = has_any_text(context, ACTION_PATTERNS, include_tests=False)
    if not has_actions:
        return []

    if has_any_text(context, TRACE_PATTERNS):
        return []

    return [finding(
        rule,
        "Agent or AI actions were detected, but no obvious audit logging, tracing, metrics, or lineage was found.",
        recommendation="Log tool calls, model calls, retrieved sources, data inputs, caller identity, latency, cost, and failures.",
    )]

