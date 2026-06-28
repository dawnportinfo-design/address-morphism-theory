from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AddressParts:
    country: str
    admin1: str
    locality: str
    area: str
    block: str
    building: str = ''


def transliterate_name(value: str, dictionary: dict[str, str]) -> str:
    return dictionary.get(value, value)


def shipping_lines(parts: AddressParts, dictionary: dict[str, str]) -> list[str]:
    area = transliterate_name(parts.area, dictionary)
    locality = transliterate_name(parts.locality, dictionary)
    admin1 = transliterate_name(parts.admin1, dictionary)
    first = f'{parts.block} {area}'.strip()
    if parts.building:
        first = f'{parts.building}, {first}'
    return [first, f'{locality}, {admin1}', parts.country]


def form_fields(parts: AddressParts, dictionary: dict[str, str]) -> dict[str, str]:
    lines = shipping_lines(parts, dictionary)
    return {'address_line_1': lines[0], 'city': transliterate_name(parts.locality, dictionary), 'state': transliterate_name(parts.admin1, dictionary), 'country': parts.country}


def run_model_checks() -> dict[str, bool]:
    parts = AddressParts('Japan', 'Tokyo', 'Shibuya-ku', 'Jinnan', '1-19-11')
    dictionary = {'神南': 'Jinnan', '渋谷区': 'Shibuya-ku'}
    lines = shipping_lines(parts, dictionary)
    fields = form_fields(parts, dictionary)
    return {
        'shipping_output_preserves_block': lines[0].startswith('1-19-11'),
        'proper_name_not_literal_translated': 'God South' not in ' '.join(lines),
        'form_output_has_city_field': fields['city'] == 'Shibuya-ku',
    }


if __name__ == '__main__':
    checks = run_model_checks()
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(', '.join(failed))
    print('chapter model passed')
