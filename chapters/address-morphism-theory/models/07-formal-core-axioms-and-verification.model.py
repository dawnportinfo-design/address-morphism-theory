from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Iterable


NON_FINAL_STATES = {
    "unresolved",
    "partial",
    "conditional",
    "ambiguous",
    "manual_required",
    "rejected",
    "blocked",
    "deprecated",
    "successor_required",
    "disputed",
    "policy_dependent",
}

FINAL_QUALITY = {"verified"}


@dataclass(frozen=True)
class EvidenceState:
    source_set_version: str
    gate_version: str
    source_count: int
    quality: str
    hard_errors: int = 0
    stale: bool = False
    disputed: bool = False


@dataclass(frozen=True)
class Candidate:
    referent_id: str
    kind: str
    score: float
    evidence: EvidenceState
    context_utility: dict[str, float]
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class Resolution:
    status: str
    referent_id: str | None
    reason_code: str
    source_set_version: str
    gate_version: str


@dataclass(frozen=True)
class HistoryEdge:
    source: str
    event: str
    target: str
    version: str


@dataclass(frozen=True)
class AMTEnvelope:
    version: str
    referent_commitment: str
    pid_commitment: str | None
    quality_state: str
    resolution_state: str
    lineage_root: str
    freshness_root: str
    revocation_root: str | None
    allowed_predicates: tuple[str, ...]


def entropy(scores: Iterable[float]) -> float:
    cleaned = [max(0.0, score) for score in scores]
    total = sum(cleaned)
    if total <= 0:
        return 0.0
    probabilities = [score / total for score in cleaned if score > 0]
    return round(-sum(p * math.log2(p) for p in probabilities), 6)


def near_tie(rank_values: list[float], tie_margin: float) -> bool:
    if len(rank_values) < 2:
        return False
    return abs(rank_values[0] - rank_values[1]) <= tie_margin


def gate_blocks(candidate: Candidate) -> str | None:
    evidence = candidate.evidence
    if evidence.hard_errors:
        return "hard-error"
    if evidence.stale:
        return "stale-source"
    if evidence.disputed:
        return "disputed-source"
    if evidence.quality not in FINAL_QUALITY:
        return "quality-not-final"
    if evidence.source_count < 1:
        return "source-count-empty"
    return None


def resolve(candidates: Iterable[Candidate], context: str, tie_margin: float = 0.04) -> Resolution:
    ranked_pairs = sorted(
        ((round((0.7 * c.context_utility.get(context, 0.0)) + (0.3 * c.score), 6), c) for c in candidates),
        key=lambda item: item[0],
        reverse=True,
    )
    ranked = [candidate for _, candidate in ranked_pairs]
    rank_values = [value for value, _ in ranked_pairs]
    if not ranked:
        return Resolution("unresolved", None, "candidate-set-empty", "none", "none")

    top = ranked[0]
    blocked = gate_blocks(top)
    if blocked == "disputed-source":
        return Resolution("policy_dependent", None, blocked, top.evidence.source_set_version, top.evidence.gate_version)
    if blocked:
        return Resolution("rejected", None, blocked, top.evidence.source_set_version, top.evidence.gate_version)

    if near_tie(rank_values, tie_margin):
        return Resolution("ambiguous", None, "near-tie", top.evidence.source_set_version, top.evidence.gate_version)

    return Resolution("resolved", top.referent_id, "final", top.evidence.source_set_version, top.evidence.gate_version)


def pid_for(resolution: Resolution, lineage_ok: bool = True) -> str | None:
    if resolution.status != "resolved" or not resolution.referent_id or not lineage_ok:
        return None
    material = f"{resolution.referent_id}|{resolution.source_set_version}|{resolution.gate_version}"
    return "pid_" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def commit(value: str) -> str:
    return "cm_" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:32]


def build_envelope(resolution: Resolution, lineage_edges: Iterable[HistoryEdge]) -> AMTEnvelope:
    pid = pid_for(resolution, lineage_ok=history_graph_valid(lineage_edges))
    referent_commitment = commit(resolution.referent_id or resolution.status)
    lineage_root = history_root(lineage_edges)
    return AMTEnvelope(
        version="amt-envelope-v0.2",
        referent_commitment=referent_commitment,
        pid_commitment=commit(pid) if pid else None,
        quality_state="verified" if resolution.status == "resolved" else "manual_required",
        resolution_state=resolution.status,
        lineage_root=lineage_root,
        freshness_root=commit(resolution.source_set_version),
        revocation_root=None,
        allowed_predicates=("region_membership", "quality_threshold", "freshness", "not_revoked")
        if pid
        else (),
    )


def history_root(edges: Iterable[HistoryEdge]) -> str:
    serialized = "|".join(sorted(f"{e.source}>{e.event}>{e.target}@{e.version}" for e in edges))
    return commit(serialized or "empty-history")


def history_graph_valid(edges: Iterable[HistoryEdge]) -> bool:
    adjacency: dict[str, set[str]] = {}
    for edge in edges:
        if edge.event not in {
            "created",
            "renamed",
            "split_into",
            "merged_into",
            "deprecated_by",
            "transferred_to",
            "source_replaced_by",
            "pid_successor",
        }:
            return False
        adjacency.setdefault(edge.source, set()).add(edge.target)

    visited: set[str] = set()
    active: set[str] = set()

    def visit(node: str) -> bool:
        if node in active:
            return False
        if node in visited:
            return True
        active.add(node)
        for target in adjacency.get(node, set()):
            if not visit(target):
                return False
        active.remove(node)
        visited.add(node)
        return True

    return all(visit(node) for node in adjacency)


def equivalence_class(candidates: Iterable[Candidate], relation: str, context: str = "delivery") -> set[str]:
    if relation == "observational":
        return {candidate.referent_id for candidate in candidates if candidate.score >= 0.5}
    if relation == "operational":
        return {candidate.referent_id for candidate in candidates if candidate.context_utility.get(context, 0.0) >= 0.8}
    if relation == "predicate":
        return {candidate.kind for candidate in candidates}
    raise ValueError(f"unknown relation: {relation}")


def zk_predicate_allowed(envelope: AMTEnvelope, predicate: str, anonymity_set_size: int) -> bool:
    if envelope.resolution_state != "resolved":
        return False
    if predicate not in envelope.allowed_predicates:
        return False
    if envelope.pid_commitment is None:
        return False
    if anonymity_set_size < 2:
        return False
    return True


def benchmark_case_complete(case: dict[str, object]) -> bool:
    required = {
        "region",
        "use_case",
        "source_policy",
        "fixture_type",
        "metrics",
        "failure_behavior",
    }
    if not required.issubset(case):
        return False
    metrics = case.get("metrics")
    if not isinstance(metrics, list):
        return False
    return {"false_pid_issuance_rate", "candidate_recall", "abstention_precision"}.issubset(set(metrics))


def run_model_checks() -> dict[str, bool]:
    verified = EvidenceState("sources-2026-06", "gate-v1", 2, "verified")
    partial = EvidenceState("sources-2026-06", "gate-v1", 1, "partial")
    stale = EvidenceState("sources-2024-01", "gate-v1", 2, "verified", stale=True)
    disputed = EvidenceState("sources-2026-06", "gate-v1", 2, "verified", disputed=True)

    delivery_gate = Candidate("arena-delivery-gate", "entrance", 0.93, verified, {"delivery": 1.0, "emergency": 0.2})
    emergency_gate = Candidate("arena-emergency-gate", "entrance", 0.92, verified, {"delivery": 0.2, "emergency": 1.0})
    alias_a = Candidate("tower-a", "building", 0.91, verified, {"delivery": 0.8}, ("Central Tower",))
    alias_b = Candidate("tower-b", "building", 0.90, verified, {"delivery": 0.8}, ("Central Tower",))
    weak = Candidate("weak-place", "region", 0.88, partial, {"delivery": 0.9})
    old = Candidate("old-annex", "building", 0.95, stale, {"delivery": 1.0})
    contested = Candidate("border-zone", "region", 0.95, disputed, {"delivery": 1.0})

    resolved_delivery = resolve([delivery_gate, emergency_gate], "delivery")
    resolved_emergency = resolve([delivery_gate, emergency_gate], "emergency")
    ambiguous = resolve([alias_a, alias_b], "delivery")
    rejected_partial = resolve([weak], "delivery")
    rejected_stale = resolve([old], "delivery")
    policy_state = resolve([contested], "delivery")
    unresolved = resolve([], "delivery")

    good_history = (
        HistoryEdge("arena", "created", "arena-delivery-gate", "v1"),
        HistoryEdge("arena-delivery-gate", "renamed", "arena-delivery-dock", "v2"),
    )
    cyclic_history = (
        HistoryEdge("a", "renamed", "b", "v1"),
        HistoryEdge("b", "renamed", "a", "v2"),
    )
    envelope = build_envelope(resolved_delivery, good_history)
    bad_envelope = build_envelope(ambiguous, good_history)

    benchmark_case = {
        "region": "synthetic-no-postcode-island",
        "use_case": "delivery",
        "source_policy": "synthetic-public",
        "fixture_type": "synthetic",
        "metrics": ["false_pid_issuance_rate", "candidate_recall", "abstention_precision"],
        "failure_behavior": "manual_required",
    }

    return {
        "partiality_allows_unresolved": unresolved.status == "unresolved",
        "context_relative_selection": resolved_delivery.referent_id == "arena-delivery-gate"
        and resolved_emergency.referent_id == "arena-emergency-gate",
        "near_tie_blocks_pid": ambiguous.status == "ambiguous" and pid_for(ambiguous) is None,
        "quality_gate_blocks_pid": rejected_partial.status == "rejected" and pid_for(rejected_partial) is None,
        "stale_source_blocks_pid": rejected_stale.status == "rejected" and pid_for(rejected_stale) is None,
        "disputed_source_is_policy_dependent": policy_state.status == "policy_dependent",
        "valid_history_graph_allows_envelope_pid_commitment": history_graph_valid(good_history)
        and envelope.pid_commitment is not None,
        "cyclic_history_graph_blocks": history_graph_valid(cyclic_history) is False,
        "equivalence_classes_are_distinct": equivalence_class([alias_a, alias_b], "observational") == {"tower-a", "tower-b"}
        and equivalence_class([delivery_gate, emergency_gate], "operational", "delivery") == {"arena-delivery-gate"}
        and equivalence_class([delivery_gate, emergency_gate], "predicate") == {"entrance"},
        "zk_boundary_requires_resolved_envelope": zk_predicate_allowed(envelope, "region_membership", 3)
        and not zk_predicate_allowed(bad_envelope, "region_membership", 3),
        "zk_boundary_blocks_singleton_anonymity": not zk_predicate_allowed(envelope, "region_membership", 1),
        "entropy_drops_after_disambiguation": entropy([alias_a.score, alias_b.score]) > entropy([alias_a.score]),
        "benchmark_case_names_required_fields": benchmark_case_complete(benchmark_case),
    }


def main() -> None:
    checks = run_model_checks()
    failed = [name for name, passed in checks.items() if not passed]
    print(json.dumps({"schema": "amt-formal-core-model-v1", "checks": checks}, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed))


if __name__ == "__main__":
    main()
