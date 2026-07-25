from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from address_morphism.zk_circuit_readiness import run_readiness_checks


def main() -> None:
    checks = run_readiness_checks()
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise SystemExit("failed ZK circuit-readiness checks: " + ", ".join(failed))
    print("ZK circuit-readiness verified.")


if __name__ == "__main__":
    main()
