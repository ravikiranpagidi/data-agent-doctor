from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding
from data_agent_doctor.rules.helpers import has_any_text


LLM_PATTERNS = [
    r"\bopenai\b|\banthropic\b|\bbedrock\b|\bgemini\b|\bazure[_-]?openai\b",
    r"\bllm\b|\bchatcompletion\b|\bresponses\.create\b",
]

BUDGET_PATTERNS = [
    r"\bcost\b|\bbudget\b|\btoken\b|\brate limit\b|\brate_limit\b",
    r"\btimeout\b|\blatency\b|\bmax_tokens\b|\bmax[_-]?retries\b",
]


def run(context: ScanContext, rule: Rule):
    if not has_any_text(context, LLM_PATTERNS, include_tests=False):
        return []

    if has_any_text(context, BUDGET_PATTERNS):
        return []

    return [finding(
        rule,
        "LLM usage was detected without obvious token, cost, timeout, or latency budget controls.",
        recommendation="Define max tokens, timeouts, retries, rate limits, and expected cost per run or workflow.",
    )]

