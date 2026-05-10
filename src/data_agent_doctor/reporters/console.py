from __future__ import annotations

from data_agent_doctor.models import ScanResult


def print_console_report(result: ScanResult) -> None:
    counts = result.counts
    print("Data Agent Doctor")
    print(f"Path: {result.cwd}")
    print(f"Score: {result.score}/100")
    print(
        "Findings: "
        f"{counts['high']} high, {counts['medium']} medium, "
        f"{counts['low']} low, {counts['info']} info"
    )
    print()

    if not result.findings:
        print("No findings. The project looks production-aware.")
        return

    for item in result.findings:
        location = f" ({item.path})" if item.path else ""
        print(f"[{item.severity.upper()}] {item.rule_id}{location}")
        print(f"  {item.message}")
        if item.recommendation:
            print(f"  Fix: {item.recommendation}")
        print()

