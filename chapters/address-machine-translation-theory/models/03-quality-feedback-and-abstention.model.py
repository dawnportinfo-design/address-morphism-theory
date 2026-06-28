from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TranslationCandidate:
    structured_fields: dict[str, str]
    language: str
    confidence: float
    warnings: tuple[str, ...] = ()


def guarded_translate(fields: dict[str, str], target_language: str, evidence_score: float) -> TranslationCandidate:
    warnings: list[str] = []
    if evidence_score < 0.7:
        warnings.append('manual-review-required')
    if 'block' not in fields and 'postal_code' not in fields:
        warnings.append('weak-location-anchor')
    output = dict(fields)
    output['target_language'] = target_language
    confidence = min(0.99, max(0.0, evidence_score - 0.08 * len(warnings)))
    return TranslationCandidate(output, target_language, round(confidence, 3), tuple(warnings))


def should_emit(candidate: TranslationCandidate, minimum_confidence: float = 0.75) -> bool:
    return candidate.confidence >= minimum_confidence and 'manual-review-required' not in candidate.warnings


def run_model_checks() -> dict[str, bool]:
    strong = guarded_translate({'country': 'JP', 'city': 'demo', 'block': 'demo-block'}, 'en', 0.93)
    weak = guarded_translate({'country': 'XX', 'city': 'demo'}, 'en', 0.55)
    return {
        'strong_candidate_emits': should_emit(strong),
        'weak_candidate_abstains': not should_emit(weak),
        'warning_added_for_weak_anchor': 'weak-location-anchor' in weak.warnings,
        'output_keeps_structure': 'target_language' in strong.structured_fields and 'city' in strong.structured_fields,
    }


if __name__ == '__main__':
    checks = run_model_checks()
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(', '.join(failed))
    print('chapter model passed')
