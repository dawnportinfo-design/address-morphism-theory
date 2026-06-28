from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ZoneCandidate:
    zone_id: str
    population: int
    delivery_load: int
    area_km2: float
    contiguous: bool
    has_official_postcode: bool


def zone_score(zone: ZoneCandidate, target_population: int, target_load: int) -> float:
    if not zone.contiguous:
        return 0.0
    pop_balance = 1 - min(1, abs(zone.population - target_population) / max(target_population, 1))
    load_balance = 1 - min(1, abs(zone.delivery_load - target_load) / max(target_load, 1))
    official_bonus = 0.1 if zone.has_official_postcode else 0.0
    return round(min(1.0, 0.45 * pop_balance + 0.45 * load_balance + official_bonus), 4)


def postal_mode(has_postcode: bool, api_reliable: bool, geo_oss_strong: bool) -> str:
    if has_postcode and api_reliable:
        return 'postal-code-available-reliable-api'
    if has_postcode:
        return 'postal-code-available-weak-api'
    if geo_oss_strong:
        return 'no-postal-code-strong-geo-oss'
    return 'no-postal-code-weak-geo-oss'


def run_model_checks() -> dict[str, bool]:
    good = ZoneCandidate('zone-a', 2400, 610, 12.4, True, False)
    broken = ZoneCandidate('zone-b', 2400, 610, 12.4, False, False)
    return {
        'contiguous_zone_scores_positive': zone_score(good, 2500, 600) > 0.8,
        'non_contiguous_zone_rejected': zone_score(broken, 2500, 600) == 0.0,
        'no_postcode_strong_geo_mode': postal_mode(False, False, True) == 'no-postal-code-strong-geo-oss',
        'weak_postcode_mode': postal_mode(True, False, False) == 'postal-code-available-weak-api',
    }


if __name__ == '__main__':
    checks = run_model_checks()
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(', '.join(failed))
    print('chapter model passed')
