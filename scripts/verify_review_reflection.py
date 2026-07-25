from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "verification" / "review-reflection-map.json"
REQUIRED_CATEGORIES = {
    "formal-core",
    "counterexample",
    "unverified-boundary",
    "zk-compatibility",
    "application-model",
}


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"missing file: {relative_path}")
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> None:
    payload = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    if payload.get("schemaVersion") != "amt-review-reflection-map-v0.1":
        errors.append("unexpected review reflection map schemaVersion")

    items = payload.get("items", [])
    if not isinstance(items, list) or not items:
        errors.append("review reflection map must contain items")

    seen: set[str] = set()
    categories: set[str] = set()

    for item in items:
        item_id = item.get("id")
        if not item_id:
            errors.append("review reflection item missing id")
            continue
        if item_id in seen:
            errors.append(f"{item_id}: duplicate id")
        seen.add(item_id)

        category = item.get("category")
        if category:
            categories.add(category)

        source_review = item.get("sourceReview")
        if not source_review:
            errors.append(f"{item_id}: missing sourceReview")
        elif not (ROOT / source_review).exists():
            errors.append(f"{item_id}: sourceReview does not exist: {source_review}")

        target_files = item.get("targetFiles", [])
        if not target_files:
            errors.append(f"{item_id}: targetFiles must not be empty")
        for target in target_files:
            if not (ROOT / target).exists():
                errors.append(f"{item_id}: target file does not exist: {target}")

        for evidence in item.get("requiredEvidence", []):
            evidence_file = evidence.get("file")
            if not evidence_file:
                errors.append(f"{item_id}: requiredEvidence missing file")
                continue
            text = read_text(evidence_file)
            for fragment in evidence.get("mustContain", []):
                if fragment not in text:
                    errors.append(f"{item_id}: {evidence_file} missing required fragment: {fragment}")

        for executable in item.get("executableChecks", []):
            if not (ROOT / executable).exists():
                errors.append(f"{item_id}: executable check file missing: {executable}")

    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        errors.append(f"missing reflection categories: {', '.join(sorted(missing_categories))}")

    if errors:
        raise SystemExit("\n".join(errors))

    print(f"Review reflection verified: {len(items)} item(s), {len(categories)} category group(s).")


if __name__ == "__main__":
    main()
