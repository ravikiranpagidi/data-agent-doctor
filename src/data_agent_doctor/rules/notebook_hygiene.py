from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    notebooks = [file for file in context.files if file.suffix == ".ipynb"]
    if not notebooks:
        return []

    if len(notebooks) > 5:
        return [finding(
            rule,
            f"{len(notebooks)} notebooks were found. Large notebook-heavy projects can be difficult to review.",
            path=notebooks[0].path,
            recommendation="Move production logic into Python modules and keep notebooks as examples or experiments.",
        )]

    return [finding(
        rule,
        "Notebook files were found. Make sure outputs and secrets are cleaned before sharing.",
        path=notebooks[0].path,
        severity="info",
        recommendation="Clear heavy outputs and move reusable logic into tested Python modules.",
    )]

