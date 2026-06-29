"""Executable helpers for Address Morphism Theory.

The package intentionally contains small, dependency-free reference models.
They are not production resolvers or audited zero-knowledge circuits.
"""

from .predicate_dsl import (
    AddressPredicateSubject,
    PredicatePolicy,
    PredicateResult,
    evaluate_predicates,
)
from .core import (
    AMTEnvelope,
    Candidate,
    EvidenceArtifact,
    EvidenceBundle,
    EvidenceSafety,
    EvidenceState,
    HistoryEdge,
    HistoryGraph,
    LicenseState,
    QualityState,
    Referent,
    Resolution,
    ResolutionState,
    TransformRecord,
    benchmark_plan_ready,
    build_envelope,
    content_digest,
    equivalence_class,
    example_public_bundle,
    issue_pid,
    resolve_candidates,
    run_core_checks,
)
from .zk_circuit_readiness import (
    CircuitProfile,
    ThreatScenario,
    profile_readiness,
    public_signals_are_safe,
    run_readiness_checks,
)

__all__ = [
    "AMTEnvelope",
    "AddressPredicateSubject",
    "Candidate",
    "CircuitProfile",
    "EvidenceArtifact",
    "EvidenceBundle",
    "EvidenceSafety",
    "EvidenceState",
    "HistoryEdge",
    "HistoryGraph",
    "LicenseState",
    "PredicatePolicy",
    "PredicateResult",
    "QualityState",
    "Referent",
    "Resolution",
    "ResolutionState",
    "ThreatScenario",
    "TransformRecord",
    "benchmark_plan_ready",
    "build_envelope",
    "content_digest",
    "equivalence_class",
    "evaluate_predicates",
    "example_public_bundle",
    "issue_pid",
    "profile_readiness",
    "public_signals_are_safe",
    "resolve_candidates",
    "run_core_checks",
    "run_readiness_checks",
]
