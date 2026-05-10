from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding
from data_agent_doctor.rules.helpers import first_match_path, has_any_text


AI_STEP = [
    r"\bopenai\b|\banthropic\b|\bbedrock\b|\bazure[_-]?openai\b",
    r"\bllm\b|\bchat_model\b|\bgenerate\b",
    r"\bagent\b|\bchain\b|\brag\b",
]

PIPELINE = [
    r"\bairflow\b|\bDAG\b|\bdagster\b|\basset\b|\bdbt\b|\bpyspark\b|\bspark\b",
]

QUALITY = [
    r"\bgreat_expectations\b|\bgx\b",
    r"\bsoda\b|\bdeequ\b",
    r"\bdbt test\b|\bnot_null\b|\bunique\b",
    r"\bquality\b|\bvalidation\b|\bschema check\b|\brow_count\b|\bfreshness\b",
]


def run(context: ScanContext, rule: Rule):
    has_ai_step = has_any_text(context, AI_STEP, include_tests=False)
    has_pipeline = has_any_text(context, PIPELINE, include_tests=False)
    if not has_ai_step or not has_pipeline:
        return []

    if has_any_text(context, QUALITY):
        return []

    return [finding(
        rule,
        "A data pipeline appears to include an AI step, but no obvious data quality gate was found.",
        path=first_match_path(context, AI_STEP, include_tests=False),
        recommendation="Add freshness, schema, row-count, null, uniqueness, or business-rule checks before AI/agent execution.",
    )]

