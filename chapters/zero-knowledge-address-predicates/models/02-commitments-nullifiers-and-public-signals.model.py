from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256


FORBIDDEN_PUBLIC_KEYS = {'address_text', 'recipient', 'precise_coordinates', 'private_key', 'witness'}


@dataclass(frozen=True)
class PrivateSubject:
    commitment_seed: str
    regions: tuple[str, ...]
    quality: float
    scopes: tuple[str, ...]
    revoked: bool = False


def commitment(seed: str) -> str:
    return 'cm:' + sha256(seed.encode()).hexdigest()[:24]


def nullifier(commitment_id: str, scope: str) -> str:
    return 'nf:' + sha256(f'{commitment_id}:{scope}'.encode()).hexdigest()[:24]


def prove_region_quality(subject: PrivateSubject, region: str, minimum_quality: float, scope: str) -> dict[str, str | bool | float]:
    accepted = region in subject.regions and subject.quality >= minimum_quality and scope in subject.scopes and not subject.revoked
    signals = {
        'accepted': accepted,
        'commitment': commitment(subject.commitment_seed),
        'nullifier': nullifier(commitment(subject.commitment_seed), scope),
        'predicate': 'region-quality-scope',
        'quality_threshold': minimum_quality,
    }
    leaked = FORBIDDEN_PUBLIC_KEYS & set(signals)
    if leaked:
        raise ValueError(f'unsafe public signals: {sorted(leaked)}')
    return signals


def run_model_checks() -> dict[str, bool]:
    subject = PrivateSubject('demo-secret', ('country:demo', 'zone:delivery'), 0.93, ('delivery',))
    ok = prove_region_quality(subject, 'zone:delivery', 0.9, 'delivery')
    bad = prove_region_quality(subject, 'zone:other', 0.9, 'delivery')
    return {
        'accepted_predicate_true': ok['accepted'] is True,
        'wrong_region_rejected': bad['accepted'] is False,
        'public_signals_hide_subject': not (FORBIDDEN_PUBLIC_KEYS & set(ok)),
        'nullifier_is_scope_bound': ok['nullifier'] != nullifier(ok['commitment'], 'hotel'),
    }


if __name__ == '__main__':
    checks = run_model_checks()
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(', '.join(failed))
    print('chapter model passed')
