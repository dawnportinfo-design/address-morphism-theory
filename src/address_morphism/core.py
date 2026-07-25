from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
import math
import re
from typing import Iterable, Mapping, Sequence


class ResolutionState(StrEnum):
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    PARTIAL = "partial"
    CONDITIONAL = "conditional"
    AMBIGUOUS = "ambiguous"
    MANUAL_REQUIRED = "manual_required"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    DEPRECATED = "deprecated"
    SUCCESSOR_REQUIRED = "successor_required"
    DISPUTED = "disputed"
    POLICY_DEPENDENT = "policy_dependent"


class QualityState(StrEnum):
    VERIFIED = "verified"
    PARTIAL = "partial"
    MANUAL_REQUIRED = "manual_required"
    REJECTED = "rejected"


class EvidenceSafety(StrEnum):
    PUBLIC = "public"
    SYNTHETIC = "synthetic"
    REDACTED = "redacted"
    PRIVATE = "private"
    UNSAFE = "unsafe"


class LicenseState(StrEnum):
    COMPATIBLE = "compatible"
    UNKNOWN = "unknown"
    INCOMPATIBLE = "incompatible"


PUBLIC_LICENSES = {"CC-BY-4.0", "ODbL-1.0", "PDDL-1.0", "MIT", "public-domain"}
PUBLIC_EVIDENCE_SAFETY = {EvidenceSafety.PUBLIC, EvidenceSafety.SYNTHETIC, EvidenceSafety.REDACTED}
FINAL_RESOLUTION_STATES = {ResolutionState.RESOLVED}
PID_ALLOWED_QUALITY = {QualityState.VERIFIED}
BLOCKED_FOR_PROOF = {
    ResolutionState.UNRESOLVED,
    ResolutionState.AMBIGUOUS,
    ResolutionState.REJECTED,
    ResolutionState.BLOCKED,
    ResolutionState.DEPRECATED,
    ResolutionState.SUCCESSOR_REQUIRED,
    ResolutionState.POLICY_DEPENDENT,
}


def normalize_surface(value: str) -> str:
    """Normalize a surface expression for search, not for identity."""

    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def token_set(value: str) -> set[str]:
    return {token for token in normalize_surface(value).split(" ") if token}


def canonical_bytes(value: str | bytes | Mapping[str, object] | Sequence[object]) -> bytes:
    """Return canonical bytes for public evidence hashing.

    This helper is intentionally simple and deterministic. It is not a legal
    record canonicalization standard by itself; deployments must document their
    source-specific canonicalization policy.
    """

    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        normalized = value.replace("\r\n", "\n").replace("\r", "\n").strip()
        return normalized.encode("utf-8")
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return encoded.encode("utf-8")


def content_digest(value: str | bytes | Mapping[str, object] | Sequence[object]) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def stable_commitment(*parts: str) -> str:
    return "cm_" + hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:32]


def entropy(weights: Iterable[float]) -> float:
    cleaned = [max(0.0, weight) for weight in weights]
    total = sum(cleaned)
    if total <= 0:
        return 0.0
    probabilities = [weight / total for weight in cleaned if weight > 0]
    return round(-sum(probability * math.log2(probability) for probability in probabilities), 6)


@dataclass(frozen=True)
class EvidenceArtifact:
    source_hint: str
    content: str | bytes | Mapping[str, object] | Sequence[object]
    media_type: str
    license_id: str
    safety: EvidenceSafety
    observed_at: str
    source_class: str = "unspecified"

    @property
    def digest(self) -> str:
        return content_digest(self.content)

    @property
    def byte_length(self) -> int:
        return len(canonical_bytes(self.content))

    @property
    def license_state(self) -> LicenseState:
        if self.license_id in PUBLIC_LICENSES:
            return LicenseState.COMPATIBLE
        if self.license_id in {"proprietary", "restricted", "personal-data"}:
            return LicenseState.INCOMPATIBLE
        return LicenseState.UNKNOWN

    @property
    def publication_safe(self) -> bool:
        return self.safety in PUBLIC_EVIDENCE_SAFETY


@dataclass(frozen=True)
class TransformRecord:
    transform_id: str
    transform_version: str
    parent_digests: tuple[str, ...]
    params_digest: str
    output_digest: str
    lossiness: str
    redaction_class: str

    def valid_against(self, available_digests: set[str]) -> bool:
        if not self.parent_digests:
            return False
        if any(parent not in available_digests for parent in self.parent_digests):
            return False
        return self.lossiness in {"lossless", "lossy"} and self.redaction_class in {
            "none",
            "redacted",
            "aggregated",
        }


@dataclass(frozen=True)
class EvidenceBundle:
    artifacts: tuple[EvidenceArtifact, ...]
    transforms: tuple[TransformRecord, ...] = ()

    @property
    def root(self) -> str:
        return content_digest("|".join(sorted(artifact.digest for artifact in self.artifacts)))

    @property
    def artifact_digests(self) -> tuple[str, ...]:
        return tuple(sorted(artifact.digest for artifact in self.artifacts))

    def transform_chain_valid(self) -> bool:
        available = set(self.artifact_digests)
        for transform in self.transforms:
            if not transform.valid_against(available):
                return False
            available.add(transform.output_digest)
        return True

    def gate(self, require_pid_ready: bool = True) -> tuple[bool, str]:
        if not self.artifacts:
            return False, "empty-evidence-bundle"
        if not self.transform_chain_valid():
            return False, "invalid-transform-chain"
        if any(not artifact.publication_safe for artifact in self.artifacts):
            return False, "publication-unsafe-artifact"
        if require_pid_ready and any(
            artifact.license_state != LicenseState.COMPATIBLE for artifact in self.artifacts
        ):
            return False, "license-not-compatible"
        return True, "accepted"


@dataclass(frozen=True)
class EvidenceState:
    bundle: EvidenceBundle
    gate_version: str
    source_policy: str
    freshness_state: str
    hard_errors: int = 0
    quality_hint: QualityState = QualityState.PARTIAL

    @property
    def bundle_root(self) -> str:
        return self.bundle.root

    def gate_reason(self) -> str:
        bundle_ok, reason = self.bundle.gate()
        if not bundle_ok:
            return reason
        if self.hard_errors:
            return "hard-error"
        if self.freshness_state not in {"fresh", "current", "bounded"}:
            return "stale-evidence"
        return "accepted"


@dataclass(frozen=True)
class Referent:
    referent_id: str
    kind: str
    labels: tuple[str, ...]
    parents: tuple[str, ...] = ()


@dataclass(frozen=True)
class Candidate:
    referent: Referent
    evidence: EvidenceState
    score: float
    context_utility: Mapping[str, float]

    @property
    def referent_id(self) -> str:
        return self.referent.referent_id

    @property
    def quality_state(self) -> QualityState:
        if self.evidence.quality_hint == QualityState.VERIFIED and self.score >= 0.8:
            return QualityState.VERIFIED
        if self.score >= 0.55:
            return QualityState.PARTIAL
        return QualityState.MANUAL_REQUIRED


@dataclass(frozen=True)
class Resolution:
    state: ResolutionState
    reason: str
    evidence_root: str
    gate_version: str
    referent: Referent | None = None
    quality: QualityState = QualityState.MANUAL_REQUIRED

    @property
    def final(self) -> bool:
        return self.state in FINAL_RESOLUTION_STATES and self.referent is not None


def rank_candidates(candidates: Iterable[Candidate], context: str) -> list[tuple[float, Candidate]]:
    ranked = []
    for candidate in candidates:
        rank = (0.55 * candidate.score) + (0.45 * candidate.context_utility.get(context, 0.0))
        ranked.append((round(rank, 6), candidate))
    return sorted(ranked, key=lambda item: item[0], reverse=True)


def resolve_candidates(
    candidates: Iterable[Candidate],
    context: str,
    minimum_rank: float = 0.7,
    tie_margin: float = 0.04,
) -> Resolution:
    ranked = rank_candidates(candidates, context)
    if not ranked:
        return Resolution(ResolutionState.UNRESOLVED, "candidate-set-empty", "none", "none")

    top_rank, top = ranked[0]
    gate_reason = top.evidence.gate_reason()
    if gate_reason != "accepted":
        return Resolution(
            ResolutionState.REJECTED,
            gate_reason,
            top.evidence.bundle_root,
            top.evidence.gate_version,
        )
    if top_rank < minimum_rank:
        return Resolution(
            ResolutionState.MANUAL_REQUIRED,
            "rank-below-threshold",
            top.evidence.bundle_root,
            top.evidence.gate_version,
            quality=top.quality_state,
        )
    if len(ranked) > 1 and abs(top_rank - ranked[1][0]) <= tie_margin:
        return Resolution(
            ResolutionState.AMBIGUOUS,
            "near-tie",
            top.evidence.bundle_root,
            top.evidence.gate_version,
        )

    return Resolution(
        ResolutionState.RESOLVED,
        "accepted",
        top.evidence.bundle_root,
        top.evidence.gate_version,
        referent=top.referent,
        quality=top.quality_state,
    )


@dataclass(frozen=True)
class HistoryEdge:
    source: str
    event: str
    target: str
    version: str


class HistoryGraph:
    ALLOWED_EVENTS = {
        "created",
        "renamed",
        "split_into",
        "merged_into",
        "deprecated_by",
        "transferred_to",
        "source_replaced_by",
        "pid_successor",
    }

    def __init__(self, edges: Iterable[HistoryEdge] = ()) -> None:
        self.edges = tuple(edges)

    @property
    def root(self) -> str:
        serialized = "|".join(
            sorted(f"{edge.source}>{edge.event}>{edge.target}@{edge.version}" for edge in self.edges)
        )
        return content_digest(serialized or "empty-history")

    def valid(self) -> bool:
        if any(edge.event not in self.ALLOWED_EVENTS for edge in self.edges):
            return False
        adjacency: dict[str, set[str]] = {}
        for edge in self.edges:
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

    def successors(self, referent_id: str) -> tuple[str, ...]:
        return tuple(sorted(edge.target for edge in self.edges if edge.source == referent_id))


def issue_pid(resolution: Resolution, history: HistoryGraph) -> str | None:
    if not resolution.final or resolution.quality not in PID_ALLOWED_QUALITY:
        return None
    if not history.valid():
        return None
    material = "|".join(
        [
            resolution.referent.referent_id if resolution.referent else "none",
            resolution.evidence_root,
            resolution.gate_version,
            history.root,
        ]
    )
    return "pid_" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


@dataclass(frozen=True)
class AMTEnvelope:
    version: str
    referent_commitment: str
    pid_commitment: str | None
    resolution_state: ResolutionState
    quality_state: QualityState
    evidence_root: str
    lineage_root: str
    allowed_predicates: tuple[str, ...]

    @property
    def proof_allowed(self) -> bool:
        return (
            self.resolution_state == ResolutionState.RESOLVED
            and self.quality_state == QualityState.VERIFIED
            and self.pid_commitment is not None
        )


def build_envelope(resolution: Resolution, history: HistoryGraph) -> AMTEnvelope:
    pid = issue_pid(resolution, history)
    referent_material = resolution.referent.referent_id if resolution.referent else resolution.state.value
    return AMTEnvelope(
        version="amt-envelope-v0.3",
        referent_commitment=stable_commitment("referent", referent_material),
        pid_commitment=stable_commitment("pid", pid) if pid else None,
        resolution_state=resolution.state,
        quality_state=resolution.quality,
        evidence_root=resolution.evidence_root,
        lineage_root=history.root,
        allowed_predicates=("region_membership", "quality_threshold", "freshness", "not_revoked")
        if pid
        else (),
    )


def equivalence_class(candidates: Iterable[Candidate], relation: str, context: str = "delivery") -> set[str]:
    candidate_tuple = tuple(candidates)
    if relation == "observational":
        return {candidate.referent_id for candidate in candidate_tuple if candidate.score >= 0.5}
    if relation == "operational":
        return {
            candidate.referent_id
            for candidate in candidate_tuple
            if candidate.context_utility.get(context, 0.0) >= 0.8
        }
    if relation == "predicate":
        return {candidate.referent.kind for candidate in candidate_tuple}
    raise ValueError(f"unknown equivalence relation: {relation}")


def benchmark_plan_ready(plan: Mapping[str, object]) -> bool:
    required = {
        "region",
        "use_case",
        "source_policy",
        "fixture_type",
        "metrics",
        "failure_behavior",
        "evidence_root",
    }
    if not required.issubset(plan):
        return False
    metrics = plan.get("metrics")
    if not isinstance(metrics, list):
        return False
    return {"candidate_recall", "false_pid_issuance_rate", "abstention_precision"}.issubset(set(metrics))


def example_public_bundle() -> EvidenceBundle:
    artifacts = (
        EvidenceArtifact(
            source_hint="synthetic-official-register",
            content={"region": "demo", "version": 1},
            media_type="application/json",
            license_id="public-domain",
            safety=EvidenceSafety.SYNTHETIC,
            observed_at="2026-06-29",
            source_class="synthetic",
        ),
        EvidenceArtifact(
            source_hint="synthetic-map-evidence",
            content="id,name\n1,Demo Handoff Area\n",
            media_type="text/csv",
            license_id="CC-BY-4.0",
            safety=EvidenceSafety.SYNTHETIC,
            observed_at="2026-06-29",
            source_class="synthetic",
        ),
    )
    return EvidenceBundle(artifacts)


def run_core_checks() -> dict[str, bool]:
    bundle = example_public_bundle()
    evidence = EvidenceState(
        bundle=bundle,
        gate_version="gate-v1",
        source_policy="synthetic-public",
        freshness_state="fresh",
        quality_hint=QualityState.VERIFIED,
    )
    delivery = Candidate(
        referent=Referent("demo-delivery-gate", "entrance", ("Demo Gate",), ("demo-region",)),
        evidence=evidence,
        score=0.93,
        context_utility={"delivery": 1.0, "emergency": 0.2},
    )
    emergency = Candidate(
        referent=Referent("demo-emergency-gate", "entrance", ("Demo Gate",), ("demo-region",)),
        evidence=evidence,
        score=0.92,
        context_utility={"delivery": 0.2, "emergency": 1.0},
    )
    delivery_resolution = resolve_candidates((delivery, emergency), "delivery")
    emergency_resolution = resolve_candidates((delivery, emergency), "emergency")
    history = HistoryGraph((HistoryEdge("demo-region", "created", "demo-delivery-gate", "v1"),))
    envelope = build_envelope(delivery_resolution, history)
    unsafe_bundle = EvidenceBundle(
        (
            EvidenceArtifact(
                source_hint="unsafe-demo",
                content="synthetic-private-fixture",
                media_type="text/plain",
                license_id="MIT",
                safety=EvidenceSafety.PRIVATE,
                observed_at="2026-06-29",
            ),
        )
    )
    plan = {
        "region": "demo-region",
        "use_case": "delivery",
        "source_policy": "synthetic-public",
        "fixture_type": "synthetic",
        "metrics": ["candidate_recall", "false_pid_issuance_rate", "abstention_precision"],
        "failure_behavior": "manual_required",
        "evidence_root": bundle.root,
    }
    return {
        "content_digest_ignores_location_not_content": bundle.artifacts[0].digest
        == content_digest({"region": "demo", "version": 1}),
        "bundle_gate_accepts_public_synthetic_evidence": bundle.gate() == (True, "accepted"),
        "unsafe_bundle_is_rejected": unsafe_bundle.gate()[1] == "publication-unsafe-artifact",
        "context_changes_selected_referent": delivery_resolution.referent is not None
        and emergency_resolution.referent is not None
        and delivery_resolution.referent.referent_id != emergency_resolution.referent.referent_id,
        "pid_requires_verified_resolved_history": issue_pid(delivery_resolution, history) is not None,
        "amt_envelope_allows_proof_only_after_pid_boundary": envelope.proof_allowed,
        "equivalence_relations_are_distinct": equivalence_class((delivery, emergency), "predicate") == {"entrance"}
        and equivalence_class((delivery, emergency), "operational", "delivery") == {"demo-delivery-gate"},
        "benchmark_plan_requires_evidence_root": benchmark_plan_ready(plan),
    }
