from __future__ import annotations

from dataclasses import dataclass


ALLOWED_PUBLIC_SIGNALS = {
    "predicateId",
    "commitmentId",
    "result",
    "reason",
    "nullifier",
    "qualityClass",
    "freshnessDays",
    "anonymitySetLowerBound",
    "regionRoot",
    "freshnessRoot",
    "revocationRoot",
    "policyVersion",
    "scopeId",
    "epoch",
    "threshold",
    "maxAgeDays",
}

FORBIDDEN_PUBLIC_SIGNALS = {
    "address",
    "raw_address",
    "rawAddress",
    "recipient",
    "private_key",
    "privateKey",
    "witness",
    "precise_coordinates",
    "preciseCoordinates",
    "proofInternals",
}

ALLOWED_AMT_STATES = {"resolved"}
BLOCKED_AMT_STATES = {"unresolved", "ambiguous", "rejected", "deprecated", "successor_required"}


@dataclass(frozen=True)
class CircuitProfile:
    relation_id: str
    status: str
    amt_states: tuple[str, ...]
    private_inputs: tuple[str, ...]
    public_signals: tuple[str, ...]
    constraints: tuple[str, ...]
    test_vector_classes: tuple[str, ...]
    audit_status: str
    minimum_anonymity_set: int = 2


@dataclass(frozen=True)
class ThreatScenario:
    threat_id: str
    asset: str
    attack_path: str
    required_control: str
    covered_by: tuple[str, ...]
    residual_status: str


REQUIRED_TEST_VECTOR_CLASSES = {
    "accepted",
    "wrong-region-rejection",
    "threshold-rejection",
    "stale-rejection",
    "revoked-rejection",
    "consent-rejection",
    "singleton-anonymity-rejection",
    "malformed-envelope-rejection",
    "public-signal-redaction",
}


def public_signals_are_safe(signals: tuple[str, ...]) -> bool:
    signal_set = set(signals)
    return signal_set <= ALLOWED_PUBLIC_SIGNALS and not (signal_set & FORBIDDEN_PUBLIC_SIGNALS)


def amt_state_guard_is_safe(states: tuple[str, ...]) -> bool:
    state_set = set(states)
    return bool(state_set) and state_set <= ALLOWED_AMT_STATES and not (state_set & BLOCKED_AMT_STATES)


def profile_readiness(profile: CircuitProfile) -> str:
    if not public_signals_are_safe(profile.public_signals):
        return "blocked:public-signal-leakage"
    if not amt_state_guard_is_safe(profile.amt_states):
        return "blocked:amt-state-guard"
    if profile.minimum_anonymity_set < 2:
        return "blocked:singleton-anonymity"
    if not REQUIRED_TEST_VECTOR_CLASSES.issubset(set(profile.test_vector_classes)):
        return "test-vector-incomplete"
    if profile.audit_status != "external-audit-complete":
        return "audit-required"
    return "production-ready"


def threat_controls_are_covered(threats: tuple[ThreatScenario, ...], profiles: tuple[CircuitProfile, ...]) -> bool:
    controls = {constraint for profile in profiles for constraint in profile.constraints}
    return all(threat.required_control in controls or threat.residual_status == "research-target" for threat in threats)


def sample_profiles() -> tuple[CircuitProfile, ...]:
    common_vectors = tuple(sorted(REQUIRED_TEST_VECTOR_CLASSES))
    return (
        CircuitProfile(
            relation_id="region-membership-v0",
            status="constraint-ready",
            amt_states=("resolved",),
            private_inputs=("committed-referent-path", "amt-envelope", "region-path"),
            public_signals=("predicateId", "commitmentId", "regionRoot", "result", "nullifier"),
            constraints=("amt-state-guard", "merkle-membership", "public-signal-allowlist", "anonymity-set-minimum"),
            test_vector_classes=common_vectors,
            audit_status="audit-required",
            minimum_anonymity_set=16,
        ),
        CircuitProfile(
            relation_id="delivery-zone-eligibility-v0",
            status="test-vector-ready",
            amt_states=("resolved",),
            private_inputs=("amt-envelope", "consent-path", "freshness-path", "revocation-path"),
            public_signals=(
                "predicateId",
                "commitmentId",
                "result",
                "nullifier",
                "freshnessRoot",
                "revocationRoot",
                "policyVersion",
                "anonymitySetLowerBound",
            ),
            constraints=(
                "amt-state-guard",
                "purpose-bound-consent",
                "freshness-window",
                "revocation-check",
                "public-signal-allowlist",
                "anonymity-set-minimum",
                "scoped-nullifier",
            ),
            test_vector_classes=common_vectors,
            audit_status="audit-required",
            minimum_anonymity_set=32,
        ),
    )


def sample_threats() -> tuple[ThreatScenario, ...]:
    return (
        ThreatScenario(
            threat_id="public-signal-leakage",
            asset="public-signals",
            attack_path="unsafe verifier metadata",
            required_control="public-signal-allowlist",
            covered_by=("region-membership-v0", "delivery-zone-eligibility-v0"),
            residual_status="covered",
        ),
        ThreatScenario(
            threat_id="ambiguous-state-proven",
            asset="amt-envelope",
            attack_path="non-final envelope accepted",
            required_control="amt-state-guard",
            covered_by=("region-membership-v0", "delivery-zone-eligibility-v0"),
            residual_status="covered",
        ),
        ThreatScenario(
            threat_id="cross-scope-linkability",
            asset="nullifier",
            attack_path="same nullifier reused across verifier scopes",
            required_control="scoped-nullifier",
            covered_by=("delivery-zone-eligibility-v0",),
            residual_status="covered",
        ),
        ThreatScenario(
            threat_id="side-channel-timing",
            asset="proof-request-metadata",
            attack_path="timing correlation",
            required_control="batching-and-delay",
            covered_by=(),
            residual_status="research-target",
        ),
    )


def run_readiness_checks() -> dict[str, bool]:
    profiles = sample_profiles()
    threats = sample_threats()
    readiness = {profile.relation_id: profile_readiness(profile) for profile in profiles}
    unsafe_profile = CircuitProfile(
        relation_id="unsafe-public-signal-demo",
        status="blocked",
        amt_states=("resolved",),
        private_inputs=("amt-envelope",),
        public_signals=("predicateId", "rawAddress"),
        constraints=("public-signal-allowlist",),
        test_vector_classes=tuple(sorted(REQUIRED_TEST_VECTOR_CLASSES)),
        audit_status="audit-required",
    )
    ambiguous_profile = CircuitProfile(
        relation_id="ambiguous-state-demo",
        status="blocked",
        amt_states=("ambiguous",),
        private_inputs=("amt-envelope",),
        public_signals=("predicateId", "result"),
        constraints=("amt-state-guard",),
        test_vector_classes=tuple(sorted(REQUIRED_TEST_VECTOR_CLASSES)),
        audit_status="audit-required",
    )
    return {
        "safe_profiles_are_audit_required_not_production_ready": all(
            value == "audit-required" for value in readiness.values()
        ),
        "unsafe_public_signal_blocks_profile": profile_readiness(unsafe_profile)
        == "blocked:public-signal-leakage",
        "ambiguous_amt_state_blocks_profile": profile_readiness(ambiguous_profile)
        == "blocked:amt-state-guard",
        "threat_controls_covered_or_marked_research": threat_controls_are_covered(threats, profiles),
    }
