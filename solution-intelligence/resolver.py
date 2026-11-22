#!/usr/bin/env python3
"""Deterministic process-to-commercial structural pilot (Python standard library).

Accepts explicit graph JSON. Does not contain authoritative Salesforce license
claims, retrieve vendor data, inspect an org or calculate customer prices.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
from itertools import product
import json
from pathlib import Path
import sys

VERSION = "0.1.0"
EVIDENCE = {"VERIFIED", "INFERRED", "UNKNOWN", "CONFLICTED"}
KINDS = {
    "process", "process_step", "capability", "functional_skill", "delivery_skill",
    "implementation_option", "technical_feature", "product_variant", "surface",
    "integration_component", "access_entitlement", "technical_license",
    "permission_requirement", "commercial_offer", "requirement_group", "pricing_metric",
    "price_observation", "entitlement_allowance", "credit_pool", "source_snapshot",
}
RELS = {
    "HAS_STEP": ({"process"}, {"process_step"}),
    "REQUIRES_CAPABILITY": ({"process_step"}, {"capability"}),
    "DELIVERS": ({"functional_skill"}, {"capability"}),
    "SUPPORTS_BUILD_OF": ({"delivery_skill"}, {"implementation_option"}),
    "REALIZED_BY": ({"capability"}, {"implementation_option"}),
    "USES_SKILL": ({"implementation_option"}, {"functional_skill"}),
    "USES_FEATURE": ({"implementation_option"}, {"technical_feature"}),
    "EXPOSED_ON": ({"implementation_option"}, {"surface"}),
    "PART_OF": ({"technical_feature"}, {"product_variant"}),
    "REQUIRES": (
        {"technical_feature", "implementation_option", "commercial_offer", "access_entitlement"},
        {"requirement_group", "access_entitlement", "technical_license", "permission_requirement", "commercial_offer"},
    ),
    "HAS_MEMBER": (
        {"requirement_group"},
        {"requirement_group", "access_entitlement", "technical_license", "permission_requirement", "commercial_offer"},
    ),
    "PROVISIONED_AS": ({"access_entitlement"}, {"technical_license"}),
    "INCLUDES": ({"commercial_offer"}, {"access_entitlement", "entitlement_allowance", "commercial_offer"}),
    "AVAILABLE_FOR_PURCHASE": ({"commercial_offer"}, {"commercial_offer"}),
    "ELIGIBLE_WITH": ({"commercial_offer", "access_entitlement"}, {"commercial_offer", "access_entitlement"}),
    "BILLED_BY": ({"commercial_offer"}, {"pricing_metric"}),
    "GENERATES_USAGE": ({"implementation_option", "technical_feature"}, {"pricing_metric"}),
    "USES_CREDIT_POOL": ({"pricing_metric"}, {"credit_pool"}),
    "PRICES": ({"price_observation"}, {"pricing_metric"}),
    "OFFSETS": ({"entitlement_allowance"}, {"pricing_metric", "credit_pool"}),
}
REQUIREMENT_KINDS = {"access_entitlement", "technical_license", "permission_requirement", "commercial_offer"}


class GraphError(ValueError):
    """Validation or unsafe/unsupported structural resolution error."""


def unique_sorted(items):
    return sorted(set(items))


class Graph:
    def __init__(self, data):
        if data.get("graph_version") != VERSION:
            raise GraphError("graph_version must be 0.1.0")
        self.meta = data.get("metadata", {})
        self.nodes = {}
        self.claims = {}
        self.edges = []
        self.out = defaultdict(list)
        self.inbound = defaultdict(list)

        for node in data.get("nodes", []):
            node_id, kind = node.get("id"), node.get("kind")
            if not node_id or node_id in self.nodes or kind not in KINDS:
                raise GraphError(f"invalid or duplicate node {node_id!r} ({kind!r})")
            if kind == "requirement_group" and node.get("operator") not in {"ALL_OF", "ANY_OF"}:
                raise GraphError(f"requirement_group {node_id}: expected ALL_OF or ANY_OF")
            self.nodes[node_id] = node

        for claim in data.get("claims", []):
            claim_id, status = claim.get("id"), claim.get("evidence_status")
            if not claim_id or claim_id in self.claims or status not in EVIDENCE:
                raise GraphError(f"invalid or duplicate claim {claim_id!r}")
            if status == "VERIFIED":
                refs = claim.get("evidence_refs") or []
                if not refs or not all(
                    isinstance(x, dict) and x.get("url") and x.get("locator") and x.get("retrieved_at")
                    for x in refs
                ):
                    raise GraphError(f"verified claim {claim_id}: require URL, locator and retrieved_at")
            self.claims[claim_id] = claim

        edge_ids = set()
        for edge in data.get("edges", []):
            eid, src, dst, pred = (edge.get(k) for k in ("id", "source", "target", "predicate"))
            cid = edge.get("claim_id")
            if not eid or eid in edge_ids:
                raise GraphError(f"invalid or duplicate edge id {eid!r}")
            edge_ids.add(eid)
            if src not in self.nodes or dst not in self.nodes:
                raise GraphError(f"dangling edge {eid}: {src} -> {dst}")
            if cid not in self.claims:
                raise GraphError(f"edge {eid}: missing claim {cid}")
            if pred not in RELS:
                raise GraphError(f"edge {eid}: unknown relation {pred}")
            kinds_from, kinds_to = RELS[pred]
            if self.nodes[src]["kind"] not in kinds_from or self.nodes[dst]["kind"] not in kinds_to:
                raise GraphError(f"edge {eid}: invalid endpoint kinds for {pred}")
            self.edges.append(edge)
            self.out[src].append(edge)
            self.inbound[dst].append(edge)

        for key in self.out:
            self.out[key].sort(key=lambda e: e["id"])
        for key in self.inbound:
            self.inbound[key].sort(key=lambda e: e["id"])
        for group_id, node in self.nodes.items():
            if node["kind"] == "requirement_group" and not any(
                e["predicate"] == "HAS_MEMBER" for e in self.out[group_id]
            ):
                raise GraphError(f"requirement_group {group_id} is empty")

    def edges_from(self, source, *preds):
        return [e for e in self.out[source] if e["predicate"] in preds]

    def edges_to(self, target, *preds):
        return [e for e in self.inbound[target] if e["predicate"] in preds]

    def source_readiness(self, edges, context):
        statuses, issues = [], []
        ids = unique_sorted(e["claim_id"] for e in edges)
        for cid in ids:
            claim = self.claims[cid]
            status = claim["evidence_status"]
            statuses.append(status)
            if status != "VERIFIED":
                issues.append(f"{cid}: {status} evidence")
            if claim.get("lifecycle_status") == "RETIRED":
                issues.append(f"{cid}: retired claim")
            if claim.get("freshness_status") in {"STALE", "UNAVAILABLE"}:
                issues.append(f"{cid}: stale/unavailable source")
            if claim.get("effective_from") or claim.get("effective_to"):
                as_of = context.get("as_of")
                if not as_of:
                    issues.append(f"{cid}: missing as_of for dated claim")
                elif ((claim.get("effective_from") and as_of < claim["effective_from"])
                      or (claim.get("effective_to") and as_of > claim["effective_to"])):
                    issues.append(f"{cid}: outside effective period")
            for key, required in (claim.get("applicability") or {}).items():
                if required is None:
                    issues.append(f"{cid}: applicability {key} not established")
                elif key not in context or context[key] is None:
                    issues.append(f"{cid}: missing context {key}")
                elif context[key] != required:
                    issues.append(f"{cid}: inapplicable {key} (requires {required!r})")
        # This pilot loads caller-supplied JSON and NEVER verifies live source content.
        # Even a well-formed VERIFIED claim can be forged in that JSON. A separate,
        # trusted source ingestion/attestation stage is required before promotion.
        if ids:
            issues.append("Independent source validation unavailable in structural pilot")
        return {
            "claim_ids": ids,
            "verified": False,
            "structurally_consistent": bool(ids) and all(
                status == "VERIFIED" for status in statuses
            ) and len(issues) == 1,
            "gaps": unique_sorted(issues),
        }

    def expand_requirement(self, node_id, seen=frozenset()):
        """Return DNF alternatives: [(frozenset(requirements), frozenset(edge IDs))]."""
        if node_id in seen:
            raise GraphError(f"requirement cycle at {node_id}")
        kind = self.nodes[node_id]["kind"]
        if kind in REQUIREMENT_KINDS:
            return [(frozenset({node_id}), frozenset())]
        if kind != "requirement_group":
            raise GraphError(f"node {node_id} is not a requirement")
        members = self.edges_from(node_id, "HAS_MEMBER")
        expanded = []
        for edge in members:
            items = self.expand_requirement(edge["target"], seen | {node_id})
            expanded.append([(req, paths | {edge["id"]}) for req, paths in items])
        result = []
        if self.nodes[node_id]["operator"] == "ANY_OF":
            for branch in expanded:
                result.extend(branch)
                if len(result) > 256:
                    raise GraphError("too many requirement alternatives (>256)")
        else:
            for chosen in product(*expanded):
                req = frozenset().union(*(x[0] for x in chosen))
                paths = frozenset().union(*(x[1] for x in chosen))
                result.append((req, paths))
                if len(result) > 256:
                    raise GraphError("too many requirement alternatives (>256)")
        return sorted(set(result), key=lambda p: (sorted(p[0]), sorted(p[1])))

    def requirements_for(self, option_id):
        features = self.edges_from(option_id, "USES_FEATURE")
        owners = [option_id] + [e["target"] for e in features]
        roots = [e for owner in owners for e in self.edges_from(owner, "REQUIRES")]
        branches = [
            [(req, paths | {edge["id"]}) for req, paths in self.expand_requirement(edge["target"])]
            for edge in roots
        ]
        alternatives = []
        for chosen in product(*branches) if branches else [()]:
            req = frozenset().union(*(x[0] for x in chosen))
            paths = frozenset().union(*(x[1] for x in chosen))
            alternatives.append((req, paths))
            if len(alternatives) > 256:
                raise GraphError("too many combined alternatives (>256)")
        return unique_sorted(e["target"] for e in features), sorted(
            set(alternatives), key=lambda p: (sorted(p[0]), sorted(p[1]))
        )

    def offered_by(self, entitlement_id):
        return [
            e for e in self.edges_to(entitlement_id, "INCLUDES")
            if self.nodes[e["source"]]["kind"] == "commercial_offer"
        ]

    def offer_conditions(self, offer_id, seen=frozenset()):
        """Explain candidate offer dependencies without assuming orderability.

        A relationship edge is not customer eligibility evidence; the caller
        must independently validate its claim, scope and effective period.
        """
        if offer_id in seen:
            raise GraphError(f"commercial offer prerequisite cycle at {offer_id}")
        nodes = self.nodes
        if nodes[offer_id]["kind"] != "commercial_offer":
            raise GraphError(f"{offer_id}: expected commercial_offer")
        requires = self.edges_from(offer_id, "REQUIRES")
        eligibility = self.edges_from(offer_id, "ELIGIBLE_WITH")
        parents = self.edges_to(offer_id, "AVAILABLE_FOR_PURCHASE")
        tracks = []
        edge_ids = {e["id"] for e in requires + eligibility + parents}
        gaps = ["Offer is a candidate only; purchase eligibility and contract applicability unverified"]
        for edge in requires:
            target = edge["target"]
            kind = nodes[target]["kind"]
            if kind == "commercial_offer":
                sub = self.offer_conditions(target, seen | {offer_id})
                edge_ids.update(sub["dependency_edge_ids"])
                tracks.append({"required_offer": target, "alternatives": sub["requirement_routes"]})
                gaps.extend(sub["gaps"])
            elif kind == "requirement_group":
                choices = self.expand_requirement(target)
                tracks.append({
                    "requirement_group_id": target,
                    "alternatives": [sorted(items) for items, _ in choices],
                })
                for _, path_ids in choices:
                    edge_ids.update(path_ids)
            else:
                tracks.append({"required_node": target})
                gaps.append(f"Prerequisite {target} requires independent entitlement mapping")
        for edge in eligibility:
            gaps.append(f"Eligibility constraint {edge['target']} not established for customer")
        if parents:
            gaps.append("Add-on availability requires qualifying base offer; ownership not checked")
        return {
            "offer_id": offer_id,
            "candidate_status": "NOT_CUSTOMER_VALIDATED",
            "requirement_routes": tracks,
            "eligibility_node_ids": unique_sorted(e["target"] for e in eligibility),
            "available_from_offer_ids": unique_sorted(e["source"] for e in parents),
            "dependency_edge_ids": sorted(edge_ids),
            "gaps": unique_sorted(gaps),
        }

    def resolve(self, requested_id, context=None):
        context = context or {}
        node = self.nodes.get(requested_id)
        if node is None or node["kind"] not in {
            "process", "process_step", "capability", "functional_skill"
        }:
            raise GraphError(
                "query ID must identify a known process, process_step, capability or functional_skill"
            )
        scope = []
        if node["kind"] == "process":
            for step_edge in self.edges_from(requested_id, "HAS_STEP"):
                for cap_edge in self.edges_from(step_edge["target"], "REQUIRES_CAPABILITY"):
                    scope.append((step_edge["target"], cap_edge["target"], [step_edge, cap_edge]))
        elif node["kind"] == "process_step":
            for cap_edge in self.edges_from(requested_id, "REQUIRES_CAPABILITY"):
                scope.append((requested_id, cap_edge["target"], [cap_edge]))
        elif node["kind"] == "functional_skill":
            for delivered in self.edges_from(requested_id, "DELIVERS"):
                scope.append((None, delivered["target"], [delivered]))
        else:
            scope.append((None, requested_id, []))

        if not scope:
            return {
                "contract_version": VERSION, "data_class": self.meta.get("data_class", "UNSPECIFIED"),
                "requested_id": requested_id, "route_status": "NO_VERIFIED_ROUTE",
                "coverage": {"requested": [], "mapped": [], "unmapped": []},
                "alternatives": [], "gaps": ["No required capabilities were found for query"],
                "calculation_status": "NOT_RUN", "commercial_total": None,
            }

        alternatives, missing, mapped = [], [], []
        for step, cap, base_edges in scope:
            impl_edges = self.edges_from(cap, "REALIZED_BY")
            if node["kind"] == "functional_skill":
                impl_edges = [
                    e for e in impl_edges
                    if any(x["target"] == requested_id for x in self.edges_from(
                        e["target"], "USES_SKILL"
                    ))
                ]
            if not impl_edges:
                missing.append(cap)
                continue
            mapped.append(cap)
            for impl_edge in impl_edges:
                opt = impl_edge["target"]
                features, routes = self.requirements_for(opt)
                feat_edges = self.edges_from(opt, "USES_FEATURE")
                skill_edges = self.edges_from(opt, "USES_SKILL")
                skills = [e["target"] for e in skill_edges]
                delivery_edges = [
                    e for skill in skills for e in self.edges_from(skill, "DELIVERS") if e["target"] == cap
                ]
                variant_edges = [
                    e for feature in features for e in self.edges_from(feature, "PART_OF")
                ]
                usage_edges = [
                    e for owner in [opt] + features for e in self.edges_from(owner, "GENERATES_USAGE")
                ]
                for reqs, group_edge_ids in routes:
                    path_edges = (
                        list(base_edges) + [impl_edge] + feat_edges + skill_edges
                        + delivery_edges + variant_edges + usage_edges
                    )
                    path_edges += [e for e in self.edges if e["id"] in group_edge_ids]
                    offer_options, gap_notes = {}, []
                    for skill in skills:
                        if not any(e["source"] == skill for e in delivery_edges):
                            gap_notes.append(
                                f"Functional skill {skill} does not have an evidenced DELIVERS edge for {cap}"
                            )
                    for req_id in sorted(reqs):
                        if self.nodes[req_id]["kind"] == "access_entitlement":
                            provides = self.offered_by(req_id)
                            offer_options[req_id] = unique_sorted(e["source"] for e in provides)
                            path_edges.extend(provides)
                            if not provides:
                                gap_notes.append(f"No evidenced commercial offer includes {req_id}")
                        else:
                            gap_notes.append(
                                f"{req_id} is a prerequisite; technical/commercial provision not established"
                            )
                    offer_metrics = {}
                    offer_assessments = {}
                    for offer_id in unique_sorted(
                        offer for offers in offer_options.values() for offer in offers
                    ):
                        assessment = self.offer_conditions(offer_id)
                        offer_assessments[offer_id] = assessment
                        gap_notes.extend(assessment["gaps"])
                        dependency_ids = set(assessment["dependency_edge_ids"])
                        path_edges.extend(e for e in self.edges if e["id"] in dependency_ids)
                        billing_edges = self.edges_from(offer_id, "BILLED_BY")
                        path_edges.extend(billing_edges)
                        offer_metrics[offer_id] = unique_sorted(e["target"] for e in billing_edges)
                        if not billing_edges:
                            gap_notes.append(f"Billing metric for offer {offer_id} is unknown")
                    meters = unique_sorted(e["target"] for e in usage_edges)
                    if meters:
                        gap_notes.extend(
                            f"Usage meter {meter} not priced by this resolver" for meter in meters
                        )
                    evidence = self.source_readiness(path_edges, context)
                    gap_notes.extend(evidence["gaps"])
                    if not reqs:
                        gap_notes.append(
                            "No explicit licensing requirements established (NOT proof of free usage)"
                        )
                    alternatives.append({
                        "process_step_id": step, "capability_id": cap,
                        "implementation_option_id": opt,
                        "functional_skill_ids": unique_sorted(skills),
                        "technical_feature_ids": features,
                        "product_variant_ids": unique_sorted(e["target"] for e in variant_edges),
                        "requirements": sorted(reqs),
                        "providing_offer_candidates": offer_options,
                        "offer_candidate_assessments": offer_assessments,
                        "offer_billing_metric_candidates": offer_metrics,
                        "usage_meter_ids": meters,
                        "trace_edge_ids": unique_sorted(e["id"] for e in path_edges),
                        "trace_claim_ids": evidence["claim_ids"],
                        "evidence_verified": evidence["verified"],
                        "gaps": unique_sorted(gap_notes),
                    })
        alternatives.sort(
            key=lambda a: (
                a["capability_id"], a["implementation_option_id"], a["requirements"]
            )
        )
        all_gaps = unique_sorted(gap for a in alternatives for gap in a["gaps"])
        if missing:
            all_gaps.append("No implementation option for: " + ", ".join(unique_sorted(missing)))
        full = bool(alternatives) and not missing and all(
            any(
                a["evidence_verified"] and not a["gaps"]
                for a in alternatives if a["capability_id"] == cap
            )
            for cap in mapped
        )
        status = "RESOLVED" if full else "PARTIAL" if alternatives else "NO_VERIFIED_ROUTE"
        return {
            "contract_version": VERSION, "data_class": self.meta.get("data_class", "UNSPECIFIED"),
            "requested_id": requested_id, "route_status": status,
            "coverage": {
                "requested": unique_sorted(cap for _, cap, _ in scope),
                "mapped": unique_sorted(mapped), "unmapped": unique_sorted(missing),
            },
            "alternatives": alternatives, "gaps": unique_sorted(all_gaps),
            "calculation_status": "NOT_RUN", "commercial_total": None,
        }

    def impact(self, changed_id):
        """Trace a node, claim or source snapshot into potentially affected processes.

        This is a structural *superset* of impact, not proof of a real vendor
        update. Claim/source links use explicit claim IDs and snapshot IDs.
        """
        changed_is_claim = changed_id in self.claims
        if changed_id not in self.nodes and not changed_is_claim:
            raise GraphError(f"unknown node or claim {changed_id}")
        claim_ids = set()
        if changed_is_claim:
            claim_ids.add(changed_id)
        if changed_id in self.nodes and self.nodes[changed_id]["kind"] == "source_snapshot":
            for cid, claim in self.claims.items():
                snapshots = set(claim.get("source_snapshot_ids") or [])
                snapshots.update(
                    x.get("snapshot_id") for x in (claim.get("evidence_refs") or [])
                    if isinstance(x, dict)
                )
                if changed_id in snapshots:
                    claim_ids.add(cid)
        roots = [changed_id] if changed_id in self.nodes else []
        for e in self.edges:
            if e["claim_id"] in claim_ids:
                roots.extend((e["source"], e["target"]))
        queue, visited = deque(unique_sorted(roots)), set(roots)
        reached = defaultdict(set)
        while queue:
            current = queue.popleft()
            kind = self.nodes[current]["kind"]
            reached[kind].add(current)
            next_ids = []
            if kind == "commercial_offer":
                next_ids.extend(e["target"] for e in self.edges_from(current, "INCLUDES"))
                next_ids.extend(
                    e["source"] for e in self.edges_to(
                        current, "REQUIRES", "ELIGIBLE_WITH", "AVAILABLE_FOR_PURCHASE"
                    )
                )
            if kind == "price_observation":
                next_ids.extend(e["target"] for e in self.edges_from(current, "PRICES"))
            if kind == "pricing_metric":
                next_ids.extend(
                    e["source"] for e in self.edges_to(current, "BILLED_BY", "GENERATES_USAGE")
                )
            if kind in REQUIREMENT_KINDS or kind == "requirement_group":
                next_ids.extend(
                    e["source"] for e in self.edges_to(
                        current, "REQUIRES", "HAS_MEMBER", "ELIGIBLE_WITH", "INCLUDES"
                    )
                )
            if kind == "functional_skill":
                next_ids.extend(e["target"] for e in self.edges_from(current, "DELIVERS"))
                next_ids.extend(e["source"] for e in self.edges_to(current, "USES_SKILL"))
            if kind == "technical_feature":
                next_ids.extend(e["source"] for e in self.edges_to(current, "USES_FEATURE"))
            if kind == "implementation_option":
                next_ids.extend(e["source"] for e in self.edges_to(current, "REALIZED_BY"))
            if kind == "capability":
                next_ids.extend(e["source"] for e in self.edges_to(current, "REQUIRES_CAPABILITY"))
            if kind == "process_step":
                next_ids.extend(e["source"] for e in self.edges_to(current, "HAS_STEP"))
            for nxt in unique_sorted(next_ids):
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        return {
            "contract_version": VERSION, "data_class": self.meta.get("data_class", "UNSPECIFIED"),
            "changed_id": changed_id,
            "affected_claim_ids": sorted(claim_ids),
            "impacted": {kind: sorted(reached[kind]) for kind in sorted(reached)},
        }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--graph", required=True, help="Explicit graph JSON file (read-only)")
    p.add_argument("--resolve", help="Process, step or capability ID")
    p.add_argument("--impact", help="Offer, entitlement, metric or feature ID")
    p.add_argument("--context", help="Optional JSON context object (region, as_of, etc.)")
    opts = p.parse_args(argv)
    if bool(opts.resolve) == bool(opts.impact):
        p.error("specify exactly one of --resolve / --impact")
    try:
        graph = Graph(json.loads(Path(opts.graph).read_text(encoding="utf-8")))
        context = json.loads(opts.context) if opts.context else {}
        if not isinstance(context, dict):
            raise GraphError("context must be an object")
        result = graph.resolve(opts.resolve, context) if opts.resolve else graph.impact(opts.impact)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    except (GraphError, OSError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e), "status": "BLOCKED"}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
