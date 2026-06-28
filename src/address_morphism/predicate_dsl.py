from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


FORBIDDEN_PUBLIC_SIGNAL_KEYS = {
    "raw_address",
    "rawAddress",
    "recipient",
    "private_key",
    "privateKey",
    "witness",
    "precise_coordinates",
    "preciseCoordinates",
}


@dataclass(frozen=True)
class AddressPredicateSubject:
    """Private-side subject summary for a ZK-ready predicate model.

    This object is a local executable abstraction. In a real ZK circuit, most of
    these fields would be witness material or committed values, not public data.
    """

    commitment_id: str
    region_ids: tuple[str, ...]
    quality_score: float
    credential_issued_at: datetime
    revoked: bool
    consent_scopes: tuple[str, ...]
    anonymity_set_size: int


@dataclass(frozen=True)
class PredicatePolicy:
    predicate_id: str
    required_region: str | None = None
    minimum_quality: float = 0.0
    maximum_age_days: int | None = None
    required_scope: str | None = None
    minimum_anonymity_set: int = 2
    nullifier_scope: str = "default"


@dataclass(frozen=True)
class PredicateResult:
    accepted: bool
    reason: str
    public_signals: dict[str, Any]


def _age_days(now: datetime, issued_at: datetime) -> int:
    return max(0, (now - issued_at).days)


def _make_nullifier(subject: AddressPredicateSubject, policy: PredicatePolicy) -> str:
    seed = f"{subject.commitment_id}:{policy.predicate_id}:{policy.nullifier_scope}"
    # This is a deterministic local model, not a cryptographic hash.
    return f"model-nullifier-{abs(hash(seed)) % 10**12:012d}"


def _safe_public_signals(signals: dict[str, Any]) -> dict[str, Any]:
    leaked = sorted(FORBIDDEN_PUBLIC_SIGNAL_KEYS & set(signals))
    if leaked:
        raise ValueError(f"forbidden public signal keys: {', '.join(leaked)}")
    return signals


def evaluate_predicates(
    subject: AddressPredicateSubject,
    policy: PredicatePolicy,
    now: datetime | None = None,
) -> PredicateResult:
    """Evaluate a ZK-ready address predicate policy.

    The result exposes only public verifier signals. It deliberately omits raw
    address fields, recipients, precise coordinates, witnesses, and keys.
    """

    current_time = now or datetime.now(UTC)
    age = _age_days(current_time, subject.credential_issued_at)

    checks = [
        (
            policy.required_region is None or policy.required_region in subject.region_ids,
            "region-membership-failed",
        ),
        (subject.quality_score >= policy.minimum_quality, "quality-threshold-failed"),
        (
            policy.maximum_age_days is None or age <= policy.maximum_age_days,
            "freshness-window-failed",
        ),
        (not subject.revoked, "credential-revoked"),
        (
            policy.required_scope is None or policy.required_scope in subject.consent_scopes,
            "consent-scope-failed",
        ),
        (
            subject.anonymity_set_size >= policy.minimum_anonymity_set,
            "anonymity-set-too-small",
        ),
    ]

    for accepted, reason in checks:
        if not accepted:
            return PredicateResult(
                accepted=False,
                reason=reason,
                public_signals=_safe_public_signals(
                    {
                        "predicateId": policy.predicate_id,
                        "commitmentId": subject.commitment_id,
                        "result": "rejected",
                        "reason": reason,
                        "nullifier": _make_nullifier(subject, policy),
                    }
                ),
            )

    return PredicateResult(
        accepted=True,
        reason="accepted",
        public_signals=_safe_public_signals(
            {
                "predicateId": policy.predicate_id,
                "commitmentId": subject.commitment_id,
                "result": "accepted",
                "nullifier": _make_nullifier(subject, policy),
                "qualityClass": "verified" if subject.quality_score >= 0.9 else "partial",
                "freshnessDays": age,
                "anonymitySetLowerBound": subject.anonymity_set_size,
            }
        ),
    )
