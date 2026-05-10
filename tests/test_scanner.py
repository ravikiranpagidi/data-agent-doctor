import json
import tempfile
import unittest
from pathlib import Path

from data_agent_doctor.scanner import scan_project


class DataAgentDoctorTest(unittest.TestCase):
    def test_missing_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = scan_project(tmp, only_rules=["framework-metadata"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].rule_id, "framework-metadata")

    def test_agent_sql_without_guardrails_is_high(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "agent.py").write_text(
                "agent = 'demo'\n"
                "def tool(connection):\n"
                "    return connection.cursor().execute('select * from customers').fetchall()\n",
                encoding="utf-8",
            )

            result = scan_project(root, only_rules=["agent-sql-guardrails"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].severity, "high")

    def test_vector_ingestion_without_metadata_is_medium(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "rag.py").write_text(
                "from chromadb import Client\n"
                "def ingest(docs):\n"
                "    collection.add(documents=docs, ids=['1'])\n",
                encoding="utf-8",
            )

            result = scan_project(root, only_rules=["pii-vector-hygiene"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].severity, "medium")

    def test_env_file_is_reported_but_example_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env").write_text("TOKEN=real-secret-value", encoding="utf-8")
            (root / ".env.example").write_text("TOKEN=placeholder", encoding="utf-8")

            result = scan_project(root, only_rules=["secret-hygiene"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].path, ".env")

    def test_config_can_skip_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            (root / ".data-agent-doctor.json").write_text(
                json.dumps({"skip_rules": ["tests-present"]}),
                encoding="utf-8",
            )

            result = scan_project(root)

        self.assertFalse(any(item.rule_id == "tests-present" for item in result.findings))


if __name__ == "__main__":
    unittest.main()

