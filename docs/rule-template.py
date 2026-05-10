from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    has_example = context.file_exists("example.txt")
    if has_example:
        return []

    return [finding(
        rule,
        "Explain the issue in plain language.",
        recommendation="Give the maintainer one clear next step.",
    )]

