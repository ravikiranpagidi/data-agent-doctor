from __future__ import annotations

import re

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding


SECRET_FILE_PATTERN = re.compile(r"(^|/)\.env($|\.)", re.IGNORECASE)
SECRET_TEXT_PATTERN = re.compile(
    r"(api[_-]?key|secret|password|token)\s*=\s*['\"]?[A-Za-z0-9_\-]{12,}",
    re.IGNORECASE,
)


def run(context: ScanContext, rule: Rule):
    findings = []
    for file in context.files:
        lowered = file.name.lower()
        if SECRET_FILE_PATTERN.search(file.path) and not any(
            marker in lowered for marker in ["example", "sample", "template"]
        ):
            findings.append(finding(
                rule,
                "A real .env-style file appears to be committed.",
                path=file.path,
                recommendation="Remove secrets and commit only .env.example with placeholder values.",
            ))

    for match in context.grep(SECRET_TEXT_PATTERN, include_tests=False):
        findings.append(finding(
            rule,
            "A hard-coded secret-like value appears in source or configuration.",
            path=f"{match.path}:{match.line}",
            recommendation="Move secrets into a secret manager or environment variable and rotate exposed values.",
        ))
        break

    return findings

