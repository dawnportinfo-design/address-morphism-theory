from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Evidence:
    source: str
    score: float
    hard_errors: int = 0


@dataclass(frozen=True)
class Candidate:
    referent_id: str
    kind: str
    evidence: tuple[Evidence, ...]
    parent_ids: tuple[str, ...] = ()


def evidence_score(candidate: Candidate) -> float:
    if not candidate.evidence:
        return 0.0
    if any(item.hard_errors for item in candidate.evidence):
        return 0.0
    return round(sum(item.score for item in candidate.evidence) / len(candidate.evidence), 4)


def resolve_candidates(candidates: Iterable[Candidate], minimum_score: float = 0.7, tie_margin: float = 0.04) -> str:
    ranked = sorted(((evidence_score(c), c) for c in candidates), key=lambda item: item[0], reverse=True)
    if not ranked:
        return 'unresolved'
    if ranked[0][0] < minimum_score:
        return 'rejected'
    if len(ranked) > 1 and ranked[0][0] - ranked[1][0] <= tie_margin:
        return 'ambiguous'
    return f'resolved:{ranked[0][1].referent_id}'


def reconstruct_breadcrumb(candidate: Candidate) -> list[str]:
    return [*candidate.parent_ids, candidate.referent_id]


def run_model_checks() -> dict[str, bool]:
    strong = Candidate('unit-demo', 'unit', (Evidence('official', 0.95), Evidence('map', 0.9)), ('country:demo', 'city:demo'))
    weak = Candidate('unit-weak', 'unit', (Evidence('single-source', 0.42),), ('country:demo', 'city:demo'))
    twin_a = Candidate('tower-a', 'building', (Evidence('map', 0.84),), ('country:demo',))
    twin_b = Candidate('tower-b', 'building', (Evidence('map', 0.82),), ('country:demo',))
    return {
        'strong_candidate_resolves': resolve_candidates([strong]) == 'resolved:unit-demo',
        'weak_candidate_rejected': resolve_candidates([weak]) == 'rejected',
        'near_tie_abstains': resolve_candidates([twin_a, twin_b]) == 'ambiguous',
        'breadcrumb_restores_parent_chain': reconstruct_breadcrumb(strong) == ['country:demo', 'city:demo', 'unit-demo'],
    }


if __name__ == '__main__':
    checks = run_model_checks()
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(', '.join(failed))
    print('chapter model passed')
