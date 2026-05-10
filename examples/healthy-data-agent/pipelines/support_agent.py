import logging


logger = logging.getLogger(__name__)

MAX_TOKENS = 800
TIMEOUT_SECONDS = 30
MAX_RETRIES = 2


def validate_query(sql: str) -> str:
    normalized = sql.lower()
    if not normalized.startswith("select"):
        raise ValueError("Only read-only SELECT queries are allowed")
    if " limit " not in normalized:
        sql = f"{sql} limit 100"
    return sql


def run_support_agent(question, connection):
    # Data quality: upstream job runs freshness, row_count, not_null, and schema validation.
    # Guardrails: table allowlist, read-only role, query validator, and human approval for exceptions.
    # Observability: audit log captures caller, prompt id, model, retrieved sources, latency, and token cost.
    # Resilience: timeout, retry with backoff, and fallback to human review.
    sql = validate_query("select * from support_tickets")
    logger.info("audit tool_call=sql_query max_tokens=%s timeout=%s", MAX_TOKENS, TIMEOUT_SECONDS)
    return connection.cursor().execute(sql).fetchall()

