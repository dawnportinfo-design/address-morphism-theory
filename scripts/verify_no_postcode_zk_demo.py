from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = ROOT / "demos" / "no-postcode-private-proof-demo.json"
CIRCUIT_PATH = ROOT / "circuits" / "no-postcode-postal-equivalent.circom"

SAFE_PUBLIC_SIGNAL_KEYS = {
    "predicateId",
    "commitmentId",
    "result",
    "nullifier",
    "qualityClass",
    "freshnessDays",
    "anonymitySetLowerBound",
}

FORBIDDEN_KEY_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"rawAddress$",
        r"raw_address$",
        r"recipient$",
        r"privateKey$",
        r"private_key$",
        r"proofSecret$",
        r"preciseCoordinates$",
        r"precise_coordinates$",
    ]
]

ROOT_PATTERN = re.compile(r"^(0x[0-9a-fA-F]{64}|sha256:[0-9a-fA-F]{64}|bafy[a-z2-7]{20,})$")


def walk_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    if isinstance(value, dict):
        findings: list[str] = []
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if any(pattern.search(key) for pattern in FORBIDDEN_KEY_PATTERNS):
                findings.append(child_path)
            findings.extend(walk_forbidden_keys(child, child_path))
        return findings
    if isinstance(value, list):
        findings = []
        for index, child in enumerate(value):
            findings.extend(walk_forbidden_keys(child, f"{path}[{index}]"))
        return findings
    return []


def load_demo() -> dict[str, Any]:
    return json.loads(DEMO_PATH.read_text(encoding="utf-8"))


def freshness_days(issued_at: str, now: datetime) -> int:
    issued = datetime.fromisoformat(issued_at.replace("Z", "+00:00"))
    return max(0, (now - issued).days)


def evaluate_demo(demo: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    envelope = demo["amtEnvelope"]
    request = demo["predicateRequest"]
    subject = demo["privateSubjectSummary"]

    age = freshness_days(subject["credentialIssuedAt"], datetime(2026, 6, 29, tzinfo=UTC))
    accepted = all(
        [
            demo["region"]["postalStatus"] == "no_official_postcode",
            demo["region"]["postalEquivalent"] is True,
            envelope["resolutionState"] == "resolved",
            envelope["qualityState"] == "verified",
            request["predicateId"] in envelope["allowedPredicates"],
            request["requiredRegion"] in subject["regionIds"],
            subject["qualityScore"] >= request["minimumQuality"],
            age <= request["maximumAgeDays"],
            subject["revoked"] is False,
            request["requiredScope"] in subject["consentScopes"],
            subject["anonymitySetSize"] >= request["minimumAnonymitySet"],
        ]
    )

    signals = {
        "predicateId": request["predicateId"],
        "commitmentId": subject["commitmentId"],
        "result": "accepted" if accepted else "rejected",
        "nullifier": "model-nullifier-demo-no-postcode",
        "qualityClass": envelope["qualityState"],
        "freshnessDays": age,
        "anonymitySetLowerBound": subject["anonymitySetSize"],
    }
    return accepted, signals


def ethereum_anchor_is_safe(anchor: dict[str, Any]) -> bool:
    root_fields = [
        "evidenceRoot",
        "issuerRegistryRoot",
        "freshnessRoot",
        "revocationRoot",
        "schemaHash",
    ]
    return all(ROOT_PATTERN.match(str(anchor.get(field, ""))) for field in root_fields)


def circuit_is_safe() -> list[str]:
    text = CIRCUIT_PATH.read_text(encoding="utf-8")
    errors = []
    required_terms = [
        "template NoPostcodePostalEquivalent",
        "public [",
        "commitmentHash",
        "regionRoot",
        "freshnessRoot",
        "revocationRoot",
        "policyHash",
        "nullifier",
        "amtResolved === 1",
        "revoked === 0",
        "consentScopeOk === 1",
    ]
    for term in required_terms:
        if term not in text:
            errors.append(f"circuit missing {term}")

    forbidden_public_terms = ["rawAddress", "recipient", "privateKey", "preciseCoordinates"]
    public_section = text.split("public [", 1)[-1].split("]", 1)[0]
    for term in forbidden_public_terms:
        if term in public_section:
            errors.append(f"forbidden public signal {term}")
    return errors


def main() -> None:
    demo = load_demo()
    errors: list[str] = []

    forbidden_paths = walk_forbidden_keys(demo)
    if forbidden_paths:
        errors.append("forbidden fixture keys: " + ", ".join(forbidden_paths))

    accepted, public_signals = evaluate_demo(demo)
    if accepted is not True:
        errors.append("expected no-postcode demo to be accepted")

    if set(public_signals) - SAFE_PUBLIC_SIGNAL_KEYS:
        errors.append("unsafe public signals: " + ", ".join(sorted(set(public_signals) - SAFE_PUBLIC_SIGNAL_KEYS)))

    if demo["expectedDecision"]["rawAddressReturned"] is not False:
        errors.append("demo must not return raw address")

    if demo["expectedDecision"]["proofIsProductionAudited"] is not False:
        errors.append("demo must not claim production audit")

    if not ethereum_anchor_is_safe(demo["ethereumAnchor"]):
        errors.append("ethereum anchor must use roots or digests only")

    refusal_case_ids = {case["caseId"] for case in demo["refusalCases"]}
    required_refusals = {
        "unresolved-amt-state",
        "revoked-credential",
        "stale-credential",
        "singleton-anonymity",
    }
    if not required_refusals <= refusal_case_ids:
        errors.append("missing refusal cases: " + ", ".join(sorted(required_refusals - refusal_case_ids)))

    errors.extend(circuit_is_safe())

    if errors:
        raise SystemExit("\n".join(errors))

    print(
        json.dumps(
            {
                "schema": "no-postcode-zk-demo-verification-v0.1",
                "accepted": accepted,
                "publicSignals": public_signals,
                "auditStatus": demo["circuitProfile"]["auditStatus"],
                "productionReady": demo["circuitProfile"]["productionReady"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

