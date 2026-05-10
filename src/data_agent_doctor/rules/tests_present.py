from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    has_tests = any(
        file.path.startswith(("tests/", "test/"))
        or file.name.endswith(("_test.py", "_spec.py"))
        or file.name.startswith("test_")
        for file in context.files
    )
    if has_tests:
        return []

    return [finding(
        rule,
        "No tests were found.",
        recommendation="Add at least one smoke test so contributors can verify rule and scanner changes.",
    )]

