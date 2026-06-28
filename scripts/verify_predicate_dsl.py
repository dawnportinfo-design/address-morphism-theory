from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from address_morphism import AddressPredicateSubject, PredicatePolicy, evaluate_predicates


def assert_true(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def main() -> None:
    subject = AddressPredicateSubject(
        commitment_id="commitment-demo-001",
        region_ids=("country:jp", "region:tokyo", "delivery-zone:demo"),
        quality_score=0.94,
        credential_issued_at=datetime(2026, 6, 1, tzinfo=UTC),
        revoked=False,
        consent_scopes=("delivery", "hotel-checkin"),
        anonymity_set_size=128,
    )
    policy = PredicatePolicy(
        predicate_id="delivery-region-eligibility-v0",
        required_region="delivery-zone:demo",
        minimum_quality=0.9,
        maximum_age_days=45,
        required_scope="delivery",
        minimum_anonymity_set=16,
        nullifier_scope="merchant:demo",
    )
    accepted = evaluate_predicates(subject, policy, now=datetime(2026, 6, 29, tzinfo=UTC))
    assert_true(accepted.accepted, "expected accepted delivery predicate")
    assert_true("nullifier" in accepted.public_signals, "accepted proof needs nullifier")
    assert_true("rawAddress" not in accepted.public_signals, "public signals must not leak raw address")
    assert_true("recipient" not in accepted.public_signals, "public signals must not leak recipient")

    rejected = evaluate_predicates(
        subject,
        PredicatePolicy(
            predicate_id="delivery-region-eligibility-v0",
            required_region="delivery-zone:other",
            minimum_quality=0.9,
            required_scope="delivery",
            minimum_anonymity_set=16,
        ),
        now=datetime(2026, 6, 29, tzinfo=UTC),
    )
    assert_true(not rejected.accepted, "wrong region must reject")
    assert_true(rejected.reason == "region-membership-failed", "wrong rejection reason")
    assert_true(set(rejected.public_signals) <= {"predicateId", "commitmentId", "result", "reason", "nullifier"}, "rejected signal set is too broad")

    small_set = evaluate_predicates(
        AddressPredicateSubject(
            commitment_id="commitment-demo-002",
            region_ids=("delivery-zone:demo",),
            quality_score=0.94,
            credential_issued_at=datetime(2026, 6, 1, tzinfo=UTC),
            revoked=False,
            consent_scopes=("delivery",),
            anonymity_set_size=1,
        ),
        policy,
        now=datetime(2026, 6, 29, tzinfo=UTC),
    )
    assert_true(not small_set.accepted, "small anonymity set must reject")
    assert_true(small_set.reason == "anonymity-set-too-small", "expected anonymity-set rejection")

    print("Predicate DSL verified.")


if __name__ == "__main__":
    main()
