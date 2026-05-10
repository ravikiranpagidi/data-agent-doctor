from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding
from data_agent_doctor.rules.helpers import has_any_text


AGENT_OR_LLM = [
    r"\bagent\b|\btool\b|\bllm\b|\bopenai\b|\banthropic\b",
    r"\bchain\b|\bgraph\b|\bretriever\b|\bembedding\b",
]

RESILIENCE = [
    r"\bretry\b|\bbackoff\b|\bfallback\b|\btimeout\b|\bcircuit breaker\b",
    r"\bexcept\b|\btry\b|\bon_failure\b|\bon_retry\b",
]


def run(context: ScanContext, rule: Rule):
    if not has_any_text(context, AGENT_OR_LLM, include_tests=False):
        return []

    if has_any_text(context, RESILIENCE, include_tests=False):
        return []

    return [finding(
        rule,
        "Agent or LLM workflow code was detected without obvious retry, timeout, or fallback handling.",
        recommendation="Add timeouts, retries with backoff, fallback paths, and clear user-facing failure behavior.",
    )]

