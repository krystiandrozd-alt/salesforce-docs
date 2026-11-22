#!/usr/bin/env python3
"""Compare independently graded A/B agent responses; never runs a model itself.

Input must be supplied after two real, comparable executions. A JSON document
with grades written by the same tested agent is NOT independent evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

VERSION = "0.1.0"
CRITERIA = (
    "routing_correct",
    "source_trace_complete",
    "license_semantics_correct",
    "no_unsupported_claims",
    "execution_truth",
    "applicability_correct",
)
CRITICAL = {"no_unsupported_claims", "execution_truth"}


class BenchmarkError(ValueError):
    pass


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_run(run, case_ids, label):
    if not run.get("reviewed_by") or run.get("reviewed_by") == "tested_agent":
        raise BenchmarkError(f"{label}: independent reviewer required")
    if not run.get("model") or not run.get("source_snapshot_id") or not run.get("tool_profile"):
        raise BenchmarkError(f"{label}: missing model/source_snapshot_id/tool_profile")
    responses = run.get("responses")
    if not isinstance(responses, list):
        raise BenchmarkError(f"{label}: expected response list")
    found = {}
    for row in responses:
        cid = row.get("case_id")
        if cid not in case_ids or cid in found:
            raise BenchmarkError(f"{label}: unexpected or duplicate case {cid}")
        score = row.get("review")
        if not isinstance(score, dict) or any(type(score.get(k)) is not bool for k in CRITERIA):
            raise BenchmarkError(f"{label} {cid}: reviewed Boolean values required for each criterion")
        if not isinstance(row.get("artifact_ref"), str) or not row["artifact_ref"]:
            raise BenchmarkError(f"{label} {cid}: recorded response artifact reference required")
        found[cid] = row
    missing = case_ids - set(found)
    if missing:
        raise BenchmarkError(f"{label}: missing cases {sorted(missing)}")
    return found


def compare(case_suite, baseline, candidate):
    if case_suite.get("status") != "NOT_EXECUTED":
        raise BenchmarkError("holdout suite unexpectedly contains pre-claimed execution")
    cases = case_suite.get("cases") or []
    case_ids = {c["case_id"] for c in cases}
    if len(case_ids) != len(cases) or not cases:
        raise BenchmarkError("invalid case IDs")
    if baseline.get("source_snapshot_id") != candidate.get("source_snapshot_id"):
        raise BenchmarkError("baseline and candidate used different source snapshots")
    if baseline.get("model") != candidate.get("model"):
        raise BenchmarkError("baseline and candidate used different models")
    if baseline.get("tool_profile") != candidate.get("tool_profile"):
        raise BenchmarkError("baseline and candidate used different tool permissions")
    b = validate_run(baseline, case_ids, "baseline")
    c = validate_run(candidate, case_ids, "candidate")
    results = []
    for cid in sorted(case_ids):
        old = sum(b[cid]["review"][key] for key in CRITERIA)
        new = sum(c[cid]["review"][key] for key in CRITERIA)
        results.append({
            "case_id": cid,
            "baseline_pass": old,
            "candidate_pass": new,
            "delta": new - old,
            "candidate_critical_failures": [
                key for key in sorted(CRITICAL) if not c[cid]["review"][key]
            ],
        })
    return {
        "suite_id": case_suite["suite_id"], "tool_profile": baseline["tool_profile"],
        "model": baseline["model"], "source_snapshot_id": baseline["source_snapshot_id"],
        "criteria_per_case": len(CRITERIA),
        "case_count": len(case_ids),
        "baseline_total_pass": sum(x["baseline_pass"] for x in results),
        "candidate_total_pass": sum(x["candidate_pass"] for x in results),
        "candidate_blocked": any(x["candidate_critical_failures"] for x in results),
        "cases": results,
        "meaning": "Independent graded A/B ONLY; not Salesforce billing validation",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases", required=True)
    p.add_argument("--baseline", required=True)
    p.add_argument("--candidate", required=True)
    opts = p.parse_args(argv)
    try:
        result = compare(_read(opts.cases), _read(opts.baseline), _read(opts.candidate))
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not result["candidate_blocked"] else 3
    except (BenchmarkError, KeyError, OSError, ValueError) as err:
        print(json.dumps({"status": "BLOCKED", "error": str(err)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
