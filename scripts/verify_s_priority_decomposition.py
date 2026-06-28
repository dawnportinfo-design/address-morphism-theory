from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "verification" / "s-priority-decomposition-gate.json"

EXPECTED_IDS = {
    "candidate-generation-world-coverage",
    "multilingual-search-recall",
    "natural-cultural-feature-world-coverage",
    "strict-gis-validation",
    "commercial-address-api-comparison",
    "zk-circuit-security",
    "agid-aoid-production-security",
}

REQUIRED_ITEM_FIELDS = {
    "id",
    "claim",
    "regions",
    "useCases",
    "dataSources",
    "metrics",
    "failureBehaviors",
    "safeWording",
    "forbiddenClaim",
}

EXTERNAL_APPROVAL_MARKERS = {
    "external-approval-required",
    "terms-review-required",
}

OVERCLAIM_MARKERS = [
    "every addressable object",
    "proves worldwide",
    "beats all",
    "complete zero-knowledge",
    "production secure because",
]


def load_gate() -> dict:
    return json.loads(GATE_PATH.read_text(encoding="utf-8"))


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    gate = load_gate()

    require(gate.get("schema") == "amt-s-priority-decomposition-gate-v1", errors, "invalid schema")
    items = gate.get("items", [])
    require(isinstance(items, list), errors, "items must be a list")

    ids = {item.get("id") for item in items if isinstance(item, dict)}
    require(ids == EXPECTED_IDS, errors, f"unexpected S-priority ids: {sorted(ids ^ EXPECTED_IDS)}")

    for item in items:
        if not isinstance(item, dict):
            errors.append("each item must be an object")
            continue

        item_id = item.get("id", "<unknown>")
        missing = REQUIRED_ITEM_FIELDS - set(item)
        require(not missing, errors, f"{item_id}: missing fields {sorted(missing)}")
        require(len(item.get("regions", [])) >= 3, errors, f"{item_id}: requires at least 3 region slices")
        require(len(item.get("useCases", [])) >= 3, errors, f"{item_id}: requires at least 3 use-case slices")
        require(len(item.get("dataSources", [])) >= 3, errors, f"{item_id}: requires at least 3 data-source slices")
        require(len(item.get("metrics", [])) >= 3, errors, f"{item_id}: requires at least 3 metrics")
        require(len(item.get("failureBehaviors", [])) >= 2, errors, f"{item_id}: requires at least 2 failure behaviors")

        for source in item.get("dataSources", []):
            approval = str(source.get("approval", ""))
            if approval in EXTERNAL_APPROVAL_MARKERS:
                require(
                    approval.endswith("required"),
                    errors,
                    f"{item_id}: external source approval must remain explicit",
                )

        for behavior in item.get("failureBehaviors", []):
            require(
                behavior.get("blocksVerifiedIssuance") is True,
                errors,
                f"{item_id}: failure behavior must block verified issuance",
            )

        safe = str(item.get("safeWording", "")).lower()
        for marker in OVERCLAIM_MARKERS:
            require(marker not in safe, errors, f"{item_id}: safe wording contains overclaim marker '{marker}'")

        forbidden = str(item.get("forbiddenClaim", "")).strip()
        require(bool(forbidden), errors, f"{item_id}: forbiddenClaim must be non-empty")

    candidate = next((item for item in items if item.get("id") == "candidate-generation-world-coverage"), {})
    require("recall@k" in candidate.get("metrics", []), errors, "candidate generation must track recall@k")
    require(
        any(behavior.get("action") == "unresolved" for behavior in candidate.get("failureBehaviors", [])),
        errors,
        "candidate generation must have unresolved fallback",
    )

    multilingual = next((item for item in items if item.get("id") == "multilingual-search-recall"), {})
    require("false-merge-rate" in multilingual.get("metrics", []), errors, "multilingual recall must track false-merge-rate")

    commercial = next((item for item in items if item.get("id") == "commercial-address-api-comparison"), {})
    require(
        any(source.get("approval") in EXTERNAL_APPROVAL_MARKERS for source in commercial.get("dataSources", [])),
        errors,
        "commercial comparison must require terms or external approval",
    )

    zk = next((item for item in items if item.get("id") == "zk-circuit-security"), {})
    require(
        any(behavior.get("action") == "zk-ready-only" for behavior in zk.get("failureBehaviors", [])),
        errors,
        "ZK item must remain ZK-ready only without an audited circuit",
    )

    if errors:
        print("S-priority decomposition gate failed.")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"S-priority decomposition gate verified: {len(items)} item(s).")


if __name__ == "__main__":
    main()
