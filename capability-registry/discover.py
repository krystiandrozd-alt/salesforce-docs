#!/usr/bin/env python3
"""Read-only capability discovery. This module never calls a business action."""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "registry.json"
SCHEMA = ROOT / "schema.sql"
AVAILABILITY = (
    "published",
    "product_available",
    "installed",
    "configured",
    "authorized",
    "executable",
    "entitled",
)
VERIFICATION = {"VERIFIED", "INFERRED", "UNKNOWN", "CONFLICTED", "CANDIDATE"}


def load(path=DATA):
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(document)
    return document


def validate(document):
    ids = set()

    def take(rows, label):
        for row in rows:
            if row["id"] in ids:
                raise ValueError(f"duplicate id {row['id']}")
            ids.add(row["id"])
        return {row["id"]: row for row in rows}

    skills = take(document["skill_definitions"], "skills")
    skill_versions = take(document["skill_versions"], "skill_versions")
    agents = take(document["agent_definitions"], "agents")
    agent_versions = take(document["agent_versions"], "agent_versions")
    capabilities = take(document["business_capabilities"], "capabilities")
    evidence = take(document["evidence_claims"], "evidence")
    claims = take(document["relationship_claims"], "claims")
    take(document["providers"], "providers")
    take(document["processes"], "processes")
    take(document["user_stories"], "stories")
    for version in skill_versions.values():
        if version["skill_id"] not in skills:
            raise ValueError(f"skill version {version['id']} has no skill")
        for field in AVAILABILITY:
            if version[field] not in {"YES", "NO", "UNKNOWN"}:
                raise ValueError(f"bad availability {version['id']}.{field}")
        if version["executable"] == "YES":
            raise ValueError("this slice has no executable skill")
        if version["entitled"] == "YES":
            raise ValueError("published is not entitlement")
    for version in agent_versions.values():
        if version["agent_id"] not in agents:
            raise ValueError(f"agent version {version['id']} has no agent")
        if version["executable"] == "YES" or version["entitled"] == "YES":
            raise ValueError("a named template is not an executable entitled agent")
    for claim in claims.values():
        if claim["verification"] not in VERIFICATION:
            raise ValueError(f"bad verification {claim['id']}")
        if claim["evidence_id"] not in evidence:
            raise ValueError(f"claim {claim['id']} has no evidence")
        if claim["verification"] == "VERIFIED" and evidence[claim["evidence_id"]]["evidence_status"] != "VERIFIED":
            raise ValueError(f"verified claim {claim['id']} lacks verified evidence")
        if claim["relationship_type"] == "EXECUTES":
            raise ValueError("a graph relation must not execute an action")
    for link in document["licensing_links"]:
        if link["relationship_claim_id"] not in claims:
            raise ValueError(f"license link {link['id']} has no claim")
        if link["price_status"] == "UNKNOWN" and link["entitlement_status"] != "UNKNOWN":
            raise ValueError("unknown price cannot become an entitlement")
        if link["commercial_ref"] is not None:
            raise ValueError("this slice must not copy commercial records")
    for story in document["user_stories"]:
        if story["capability_id"] not in capabilities:
            raise ValueError(f"story {story['id']} has no capability")
    if document["schema_version"] != "0.1.0":
        raise ValueError("unexpected schema version")
    return document


def connect(document=None):
    document = document or load()
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    _insert(connection, document)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _insert(connection, document):
    def rows(table, items, columns):
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})"
        connection.executemany(sql, [tuple(item[column] for column in columns) for item in items])

    rows("providers", document["providers"], ("id", "display_name"))
    rows("products", document["products"], ("id", "provider_id", "display_name", "vendor_product_id"))
    rows("surfaces", document["surfaces"], ("id", "provider_id", "display_name"))
    rows("processes", document["processes"], ("id", "display_name", "model_status"))
    rows("process_steps", document["process_steps"], ("id", "process_id", "step_order", "display_name"))
    rows("business_capabilities", document["business_capabilities"], ("id", "display_name"))
    rows("process_step_capabilities", document["process_step_capabilities"], ("id", "process_step_id", "capability_id"))
    rows("skill_definitions", document["skill_definitions"], ("id", "provider_id", "vendor_skill_id", "classification"))
    skill_columns = ("id", "skill_id", "version_label", *AVAILABILITY)
    rows("skill_versions", document["skill_versions"], skill_columns)
    rows("agent_definitions", document["agent_definitions"], ("id", "provider_id", "classification", "display_name"))
    agent_rows = []
    for item in document["agent_versions"]:
        agent_rows.append({**item, "vendor_agent_ids_json": json.dumps(item["vendor_agent_ids"])})
    rows("agent_versions", agent_rows, ("id", "agent_id", "version_label", "vendor_agent_ids_json", *AVAILABILITY))
    rows("source_snapshots", document["source_snapshots"], (
        "id", "repository", "resolved_commit", "path", "original_url", "retrieved_at", "retrieval_status"
    ))
    rows("evidence_claims", document["evidence_claims"], (
        "id", "snapshot_id", "locator", "supported_fact", "evidence_status"
    ))
    rows("relationship_claims", document["relationship_claims"], (
        "id", "source_id", "target_id", "relationship_type", "applicability", "evidence_id", "verification", "observed_at"
    ))
    for claim in document["relationship_claims"]:
        if claim["relationship_type"] == "DELIVERY_SKILL_CONFIGURES":
            connection.execute(
                "INSERT INTO skill_capabilities (id, skill_version_id, capability_id, relationship_claim_id) VALUES (?, ?, ?, ?)",
                (f"sc-{claim['id']}", claim["source_id"], claim["target_id"], claim["id"]),
            )
    rows("licensing_links", document["licensing_links"], (
        "id", "subject_id", "commercial_ref", "price_status", "entitlement_status", "document_statement", "relationship_claim_id"
    ))
    rows("epics", document["epics"], ("id", "process_id", "display_name"))
    rows("user_stories", document["user_stories"], (
        "id", "epic_id", "capability_id", "persona", "statement", "business_outcome"
    ))
    rows("acceptance_criteria", document["acceptance_criteria"], (
        "id", "user_story_id", "given_text", "when_text", "then_text"
    ))
    rows("test_cases", document["test_cases"], ("id", "user_story_id", "kind", "title"))


def account_preparation(document=None):
    """Acceptance query: sales account preparation across Copilotforce and Claudeforce."""
    document = document or load()
    connection = connect(document)
    capability_id = "cap-account-preparation"
    matches = connection.execute(
        """
        SELECT skill_version_id, relationship_claim_id
        FROM skill_capabilities
        WHERE capability_id = ?
        """,
        (capability_id,),
    ).fetchall()
    agent_matches = connection.execute(
        """
        SELECT agent_version_id FROM agent_capabilities WHERE capability_id = ?
        """,
        (capability_id,),
    ).fetchall()
    actions = connection.execute("SELECT COUNT(*) AS n FROM action_definitions").fetchone()["n"]
    stories = connection.execute(
        """
        SELECT id, statement FROM user_stories WHERE capability_id = ?
        """,
        (capability_id,),
    ).fetchall()
    candidates = [
        claim["source_id"]
        for claim in document["relationship_claims"]
        if claim["relationship_type"] == "CATALOG_CANDIDATE"
        and claim["target_id"] == capability_id
        and claim["verification"] == "CANDIDATE"
    ]
    gaps = [
        gap for gap in document["coverage_gaps"]
        if gap["id"] in {
            "gap-claudeforce-catalog",
            "gap-copilotforce-catalog",
            "gap-account-preparation-actions",
            "gap-commercial-not-reverified",
        }
    ]
    return {
        "query": "account preparation on Copilotforce and Claudeforce",
        "capability_id": capability_id,
        "surfaces": ["surface-copilotforce", "surface-claudeforce"],
        "matching_skill_ids": [row["skill_version_id"] for row in matches],
        "candidate_skill_ids": candidates,
        "matching_agent_ids": [row["agent_version_id"] for row in agent_matches],
        "action_count": actions,
        "user_story_ids": [row["id"] for row in stories],
        "commercial_status": "UNKNOWN",
        "price_status": "UNKNOWN",
        "gaps": gaps,
        "execution": "NOT_RUN",
    }


def main():
    print(json.dumps(account_preparation(), indent=2))


if __name__ == "__main__":
    main()
