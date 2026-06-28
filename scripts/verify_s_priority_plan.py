from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "verification" / "s-priority-verification-plan.json"

EXPECTED_IDS = {
    "candidate-generation-world-coverage",
    "multilingual-search-recall",
    "natural-cultural-feature-world-coverage",
    "strict-gis-validation",
    "commercial-address-api-comparison",
    "zk-circuit-security",
    "agid-aoid-production-security",
}

REQUIRED_FIELDS = {
    "id",
    "priority",
    "claim",
    "feasibility",
    "canVerifyNow",
    "requiresExternalData",
    "requiresContractsAudit",
    "requiresExternalSecurityAudit",
    "localVerificationCommand",
    "minimumDataset",
    "metrics",
    "passCriterion",
    "safeWording",
    "unsafeWording",
    "firstExperiment",
}

FORBIDDEN_SAFE_WORDING = [
    "worldwide complete",
    "globally complete",
    "fully solved",
    "complete zero-knowledge",
    "production secure",
    "beats all",
]


def load_plan() -> dict:
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    plan = load_plan()
    if plan.get("schema") != "amt-s-priority-verification-plan-v1":
        errors.append("invalid or missing schema")

    items = plan.get("items")
    if not isinstance(items, list):
        errors.append("items must be a list")
        items = []

    ids = {item.get("id") for item in items if isinstance(item, dict)}
    missing = EXPECTED_IDS - ids
    extra = ids - EXPECTED_IDS
    if missing:
        errors.append(f"missing S-priority ids: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"unexpected S-priority ids: {', '.join(sorted(extra))}")

    for item in items:
        if not isinstance(item, dict):
            errors.append("each item must be an object")
            continue
        item_id = str(item.get("id", "<unknown>"))
        missing_fields = REQUIRED_FIELDS - set(item)
        if missing_fields:
            errors.append(f"{item_id}: missing fields {', '.join(sorted(missing_fields))}")
        if item.get("priority") != "S":
            errors.append(f"{item_id}: priority must be S")
        if not isinstance(item.get("metrics"), list) or not item["metrics"]:
            errors.append(f"{item_id}: metrics must be a non-empty list")
        for field in ["minimumDataset", "passCriterion", "safeWording", "unsafeWording", "firstExperiment"]:
            if not str(item.get(field, "")).strip():
                errors.append(f"{item_id}: {field} must be non-empty")

        safe_wording = str(item.get("safeWording", "")).lower()
        for phrase in FORBIDDEN_SAFE_WORDING:
            if phrase in safe_wording:
                errors.append(f"{item_id}: safe wording contains overclaim phrase: {phrase}")

    commercial = next((item for item in items if item.get("id") == "commercial-address-api-comparison"), None)
    if commercial and not commercial.get("requiresContractsAudit"):
        errors.append("commercial-address-api-comparison must require contracts audit")

    for security_id in ["zk-circuit-security", "agid-aoid-production-security"]:
        item = next((candidate for candidate in items if candidate.get("id") == security_id), None)
        if item and not item.get("requiresExternalSecurityAudit"):
            errors.append(f"{security_id} must require external security audit")

    if errors:
        print("S-priority verification plan failed.")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"S-priority verification plan verified: {len(items)} item(s).")


if __name__ == "__main__":
    main()
