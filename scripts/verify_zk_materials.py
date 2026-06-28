from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "zk" / "index.json"
EXPECTED_CATEGORIES = {
    "theory",
    "specification",
    "implementation",
    "applications",
    "unverified",
}
ALLOWED_PAPER_ROLES = {
    "canonical",
    "localized",
    "companion",
    "derived",
    "historical-draft",
}
FORBIDDEN_TEXT = [
    "raw" + "Address:",
    "recip" + "ient:",
    "BEGIN " + "PRIVATE KEY",
    "witness" + ".wtns",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    index = read_json(INDEX)

    category_ids = {category.get("id") for category in index.get("categories", [])}
    if category_ids != EXPECTED_CATEGORIES:
        errors.append(f"category mismatch: {sorted(category_ids)}")

    canonical_paper = ROOT / index.get("canonicalPaper", "")
    if not canonical_paper.exists():
        errors.append(f"missing canonical paper: {canonical_paper}")

    canonical_roles = 0
    seen_papers: set[str] = set()
    for role in index.get("paperRoles", []):
        file_name = role.get("file", "")
        role_name = role.get("role")
        if role_name not in ALLOWED_PAPER_ROLES:
            errors.append(f"invalid paper role for {file_name}: {role_name}")
        if file_name in seen_papers:
            errors.append(f"duplicate paper role entry: {file_name}")
        seen_papers.add(file_name)
        if role_name == "canonical":
            canonical_roles += 1
        if not (ROOT / file_name).exists():
            errors.append(f"missing paper role file: {file_name}")

    if canonical_roles != 1:
        errors.append(f"expected exactly one canonical ZK paper, found {canonical_roles}")

    for category in index.get("categories", []):
        readme = ROOT / category.get("readme", "")
        if not readme.exists():
            errors.append(f"missing category readme: {readme}")
            continue
        text = readme.read_text(encoding="utf-8")
        if not text.startswith("# "):
            errors.append(f"{readme}: must start with a heading")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                errors.append(f"{readme}: forbidden publication pattern {forbidden}")

    for model in index.get("executableModels", []):
        if not (ROOT / model.get("file", "")).exists():
            errors.append(f"missing executable model: {model}")
        if not (ROOT / model.get("verification", "")).exists():
            errors.append(f"missing executable verification: {model}")

    dedupe = ROOT / "zk" / "paper-deduplication-map.md"
    if not dedupe.exists():
        errors.append("missing ZK paper deduplication map")
    else:
        text = dedupe.read_text(encoding="utf-8")
        for role in ("Canonical", "Japanese", "Companion", "Historical"):
            if role not in text:
                errors.append(f"dedupe map missing section marker: {role}")

    if errors:
        raise SystemExit("\n".join(errors))

    print("ZK materials verified.")


if __name__ == "__main__":
    main()
