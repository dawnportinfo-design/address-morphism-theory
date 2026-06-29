from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from address_morphism import run_core_checks


def main() -> None:
    checks = run_core_checks()
    failed = [name for name, passed in checks.items() if not passed]
    print(json.dumps({"schema": "amt-core-library-checks-v1", "checks": checks}, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed AMT core checks: " + ", ".join(failed))


if __name__ == "__main__":
    main()
