from __future__ import annotations

from dataclasses import dataclass
import json
import math
import re
from typing import Iterable


@dataclass(frozen=True)
class Entity:
    entity_id: str
    kind: str
    labels: tuple[str, ...]
    has_postal_code: bool
    quality: float
    source_count: int
    hard_errors: int = 0


@dataclass(frozen=True)
class Candidate:
    entity: Entity
    score: float
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class Outcome:
    status: str
    entity_id: str | None
    reason: str


NON_FINAL = {"conditional", "ambiguous", "unresolved", "rejected"}


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def token_set(value: str) -> set[str]:
    return set(normalize(value).split())


def candidate_score(surface: str, entity: Entity) -> float:
    surface_tokens = token_set(surface)
    if not surface_tokens:
        return 0.0

    best_overlap = 0.0
    for label in entity.labels:
        label_tokens = token_set(label)
        if not label_tokens:
            continue
        overlap = len(surface_tokens & label_tokens) / len(surface_tokens | label_tokens)
        best_overlap = max(best_overlap, overlap)

    if best_overlap == 0:
        return 0.0

    evidence_factor = min(1.0, entity.source_count / 2)
    return round((0.65 * best_overlap) + (0.35 * entity.quality * evidence_factor), 4)


def generate_candidates(surface: str, entities: Iterable[Entity]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for entity in entities:
        score = candidate_score(surface, entity)
        if score >= 0.25:
            evidence = ["label-overlap"]
            if not entity.has_postal_code:
                evidence.append("agid-primary-no-postcode")
            candidates.append(Candidate(entity=entity, score=score, evidence=tuple(evidence)))
    return sorted(candidates, key=lambda candidate: candidate.score, reverse=True)


def candidate_entropy(candidates: Iterable[Candidate]) -> float:
    scores = [max(0.0, candidate.score) for candidate in candidates]
    total = sum(scores)
    if total == 0:
        return 0.0
    probabilities = [score / total for score in scores if score > 0]
    return round(-sum(probability * math.log2(probability) for probability in probabilities), 4)


def gate_accepts(candidate: Candidate) -> bool:
    entity = candidate.entity
    return entity.quality >= 0.7 and entity.source_count >= 1 and entity.hard_errors == 0


def resolve(surface: str, entities: Iterable[Entity], tie_margin: float = 0.05) -> Outcome:
    candidates = generate_candidates(surface, entities)
    if not candidates:
        return Outcome(status="unresolved", entity_id=None, reason="candidate-set-empty")

    top = candidates[0]
    if not gate_accepts(top):
        return Outcome(status="rejected", entity_id=None, reason="gate-rejected")

    if len(candidates) > 1 and abs(top.score - candidates[1].score) <= tie_margin:
        return Outcome(status="ambiguous", entity_id=None, reason="near-tie")

    return Outcome(status="resolved", entity_id=top.entity.entity_id, reason="gate-accepted")


def resolve_by_context(
    surface: str,
    entities: Iterable[Entity],
    utilities: dict[str, float],
    tie_margin: float = 0.01,
) -> Outcome:
    candidates = [candidate for candidate in generate_candidates(surface, entities) if gate_accepts(candidate)]
    if not candidates:
        return Outcome(status="unresolved", entity_id=None, reason="candidate-set-empty")

    ranked = sorted(
        ((utilities.get(candidate.entity.entity_id, 0.0), candidate) for candidate in candidates),
        key=lambda item: item[0],
        reverse=True,
    )
    top_score, top_candidate = ranked[0]
    if len(ranked) > 1 and abs(top_score - ranked[1][0]) <= tie_margin:
        return Outcome(status="ambiguous", entity_id=None, reason="context-utility-tie")
    return Outcome(status="resolved", entity_id=top_candidate.entity.entity_id, reason="context-utility-max")


def is_functional_lineage(edges: Iterable[tuple[str, str]]) -> bool:
    successors: dict[str, set[str]] = {}
    for source, target in edges:
        successors.setdefault(source, set()).add(target)
    return all(len(targets) <= 1 for targets in successors.values())


def anonymity_set_size(entities: Iterable[Entity], predicate: str) -> int:
    if predicate == "central-building":
        return sum(1 for entity in entities if any("Central Building" in label for label in entity.labels))
    if predicate.startswith("entity:"):
        expected = predicate.removeprefix("entity:")
        return sum(1 for entity in entities if entity.entity_id == expected)
    raise ValueError(f"unknown predicate: {predicate}")


def run_checks() -> list[dict[str, str | bool]]:
    unit_a = Entity(
        entity_id="unit-501",
        kind="unit",
        labels=("Central Building 5F Room 501", "Central Building"),
        has_postal_code=True,
        quality=0.92,
        source_count=2,
    )
    unit_b = Entity(
        entity_id="unit-502",
        kind="unit",
        labels=("Central Building 5F Room 502", "Central Building"),
        has_postal_code=True,
        quality=0.92,
        source_count=2,
    )
    island_handoff = Entity(
        entity_id="agid-region-barbuda-north-harbor",
        kind="island-handoff-area",
        labels=("North Harbor Barbuda", "Barbuda north handoff"),
        has_postal_code=False,
        quality=0.81,
        source_count=2,
    )
    stale_source = Entity(
        entity_id="stale-building",
        kind="building",
        labels=("Old Market Annex",),
        has_postal_code=True,
        quality=0.41,
        source_count=1,
        hard_errors=0,
    )
    delivery_entrance = Entity(
        entity_id="arena-delivery-dock",
        kind="entrance",
        labels=("Central Arena", "Central Arena loading dock"),
        has_postal_code=True,
        quality=0.9,
        source_count=2,
    )
    emergency_entrance = Entity(
        entity_id="arena-emergency-gate",
        kind="entrance",
        labels=("Central Arena", "Central Arena emergency gate"),
        has_postal_code=True,
        quality=0.9,
        source_count=2,
    )

    ambiguous_candidates = generate_candidates("Central Building", [unit_a, unit_b])
    disambiguated_candidates = generate_candidates("Central Building 5F Room 501", [unit_a, unit_b])
    stale_first = resolve("Old Market Annex", [stale_source])
    stale_second = resolve("Old Market Annex", [stale_source])
    delivery_choice = resolve_by_context(
        "Central Arena",
        [delivery_entrance, emergency_entrance],
        {"arena-delivery-dock": 1.0, "arena-emergency-gate": 0.45},
    )
    emergency_choice = resolve_by_context(
        "Central Arena",
        [delivery_entrance, emergency_entrance],
        {"arena-delivery-dock": 0.45, "arena-emergency-gate": 1.0},
    )

    checks = [
        {
            "id": "collision-produces-ambiguous",
            "passed": resolve("Central Building", [unit_a, unit_b]).status == "ambiguous",
            "claim": "Non-injective surface observation must not emit a false precise identifier.",
        },
        {
            "id": "missing-candidate-produces-unresolved",
            "passed": resolve("Missing Place", [unit_a, unit_b]).status == "unresolved",
            "claim": "Candidate omission is represented as unresolved rather than guessed resolution.",
        },
        {
            "id": "gate-failure-blocks-issuance",
            "passed": resolve("Old Market Annex", [stale_source]).status == "rejected",
            "claim": "Low-quality evidence prevents identifier issuance.",
        },
        {
            "id": "no-postcode-can-resolve-with-agid-primary-evidence",
            "passed": resolve("North Harbor Barbuda", [island_handoff]).status == "resolved",
            "claim": "No-postcode regions can use AGID-first evidence instead of postal-code dependence.",
        },
        {
            "id": "lineage-split-is-not-functional",
            "passed": is_functional_lineage([("old-town", "new-town-east"), ("old-town", "new-town-west")])
            is False,
            "claim": "Address lineage needs a relation for split events.",
        },
        {
            "id": "context-changes-operational-optimum",
            "passed": delivery_choice.entity_id == "arena-delivery-dock"
            and emergency_choice.entity_id == "arena-emergency-gate",
            "claim": "The best address referent can differ by delivery or emergency context.",
        },
        {
            "id": "evidence-reduces-entropy-without-proving-truth",
            "passed": candidate_entropy(ambiguous_candidates) > candidate_entropy(disambiguated_candidates)
            and resolve("Central Building 5F Room 501", [unit_a, unit_b]).entity_id == "unit-501",
            "claim": "More specific evidence reduces candidate entropy but remains scoped to available candidates.",
        },
        {
            "id": "abstention-monotonic-without-new-evidence",
            "passed": stale_first.status in NON_FINAL and stale_first == stale_second,
            "claim": "A rejected or unresolved result must not become resolved without new evidence or policy.",
        },
        {
            "id": "privacy-predicate-needs-anonymity-set",
            "passed": anonymity_set_size([unit_a, unit_b], "central-building") >= 2
            and anonymity_set_size([unit_a, unit_b], "entity:unit-501") == 1,
            "claim": "A predicate with a singleton anonymity set can reveal the referent despite hiding text.",
        },
    ]
    return checks


def main() -> None:
    checks = run_checks()
    failed = [check for check in checks if not check["passed"]]
    report = {
        "schema": "amt-executable-model-report-v1",
        "checks": checks,
        "summary": {
            "total": len(checks),
            "passed": len(checks) - len(failed),
            "failed": len(failed),
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
