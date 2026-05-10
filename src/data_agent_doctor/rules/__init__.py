from data_agent_doctor.models import Rule
from data_agent_doctor.rules.agent_sql_guardrails import run as agent_sql_guardrails
from data_agent_doctor.rules.cost_budget import run as cost_budget
from data_agent_doctor.rules.data_quality_gate import run as data_quality_gate
from data_agent_doctor.rules.framework_metadata import run as framework_metadata
from data_agent_doctor.rules.lineage_audit import run as lineage_audit
from data_agent_doctor.rules.notebook_hygiene import run as notebook_hygiene
from data_agent_doctor.rules.pii_vector_hygiene import run as pii_vector_hygiene
from data_agent_doctor.rules.retry_fallback import run as retry_fallback
from data_agent_doctor.rules.secret_hygiene import run as secret_hygiene
from data_agent_doctor.rules.tests_present import run as tests_present


RULES = [
    Rule(
        id="framework-metadata",
        title="AI and data frameworks are discoverable",
        category="maintainability",
        default_severity="low",
        run=framework_metadata,
    ),
    Rule(
        id="agent-sql-guardrails",
        title="Agent SQL access has guardrails",
        category="security",
        default_severity="high",
        run=agent_sql_guardrails,
    ),
    Rule(
        id="pii-vector-hygiene",
        title="RAG and vector ingestion handles sensitive data",
        category="data-governance",
        default_severity="high",
        run=pii_vector_hygiene,
    ),
    Rule(
        id="data-quality-gate",
        title="AI steps have upstream data quality checks",
        category="data-quality",
        default_severity="medium",
        run=data_quality_gate,
    ),
    Rule(
        id="lineage-audit",
        title="Data and agent actions are traceable",
        category="observability",
        default_severity="medium",
        run=lineage_audit,
    ),
    Rule(
        id="cost-budget",
        title="LLM cost and latency budgets are visible",
        category="operations",
        default_severity="medium",
        run=cost_budget,
    ),
    Rule(
        id="retry-fallback",
        title="Agent workflows define retries or fallbacks",
        category="reliability",
        default_severity="medium",
        run=retry_fallback,
    ),
    Rule(
        id="secret-hygiene",
        title="Secrets are not committed in data or agent files",
        category="security",
        default_severity="high",
        run=secret_hygiene,
    ),
    Rule(
        id="notebook-hygiene",
        title="Notebooks are safe to review",
        category="maintainability",
        default_severity="low",
        run=notebook_hygiene,
    ),
    Rule(
        id="tests-present",
        title="Tests are easy to find",
        category="contributor-experience",
        default_severity="low",
        run=tests_present,
    ),
]

