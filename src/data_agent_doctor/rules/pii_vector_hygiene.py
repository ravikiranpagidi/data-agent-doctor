from __future__ import annotations

from data_agent_doctor.context import ScanContext
from data_agent_doctor.models import Rule, finding
from data_agent_doctor.rules.helpers import first_match_path, has_any_text


RAG_OR_VECTOR = [
    r"\bembedding\b|\bembeddings\b",
    r"\bvectorstore\b|\bvector_store\b",
    r"\bfaiss\b|\bchroma\b|\bchromadb\b|\bmilvus\b|\bpinecone\b|\bweaviate\b|\bqdrant\b",
    r"\bretriever\b|\brag\b",
]

PII_OR_SECRET = [
    r"\bpii\b|\bpersonal data\b|\bemail\b|\bphone\b|\bssn\b|\bpassport\b",
    r"\bsecret\b|\bcredential\b|\btoken\b|\bapi[_-]?key\b",
]

HYGIENE = [
    r"\bredact\b|\bmask\b|\banonymi[sz]e\b",
    r"\bpii[_-]?scan\b|\bpolicy\b|\bclassification\b",
    r"\bmetadata\b|\bsource\b|\bcitation\b|\blineage\b",
]


def run(context: ScanContext, rule: Rule):
    uses_vector = has_any_text(context, RAG_OR_VECTOR, include_tests=False)
    if not uses_vector:
        return []

    mentions_sensitive_data = has_any_text(context, PII_OR_SECRET, include_tests=False)
    has_hygiene = has_any_text(context, HYGIENE)

    if mentions_sensitive_data and not has_hygiene:
        return [finding(
            rule,
            "Vector or RAG ingestion appears near sensitive-data language without obvious redaction, metadata, or policy checks.",
            path=first_match_path(context, RAG_OR_VECTOR, include_tests=False),
            recommendation="Add PII/secret scanning, redaction, source metadata, and retention policy before embedding data.",
        )]

    if not has_hygiene:
        return [finding(
            rule,
            "RAG or vector code was detected, but no obvious metadata, source tracking, or data hygiene checks were found.",
            path=first_match_path(context, RAG_OR_VECTOR, include_tests=False),
            severity="medium",
            recommendation="Track document source, freshness, chunk metadata, and any sensitive-data filtering done before embedding.",
        )]

    return []
