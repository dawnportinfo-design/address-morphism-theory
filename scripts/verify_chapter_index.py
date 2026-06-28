from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "chapters" / "index.json"
ALLOWED_KINDS = {
    "core-theory",
    "machine-translation-theory",
    "privacy-proof-theory",
    "translation-theory",
    "postal-zone-theory",
}
FORBIDDEN_TEXT = [
    "raw" + "Address:",
    "recip" + "ient:",
    "BEGIN " + "PRIVATE KEY",
    "witness" + ".wtns",
]


def main() -> None:
    errors: list[str] = []
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    seen_files: set[str] = set()
    root_toc = ROOT / index.get("rootToc", "")
    if not root_toc.exists():
        errors.append(f"missing rootToc {root_toc}")

    for series in index.get("series", []):
        series_id = series.get("id")
        if series.get("kind") not in ALLOWED_KINDS:
            errors.append(f"{series_id}: invalid kind {series.get('kind')!r}")
        source_paper = ROOT / series.get("sourcePaper", "")
        if not source_paper.exists():
            errors.append(f"{series_id}: missing sourcePaper {source_paper}")
        toc_file = ROOT / series.get("tocFile", "")
        if not toc_file.exists():
            errors.append(f"{series_id}: missing tocFile {toc_file}")

        orders: list[int] = []
        for chapter in series.get("chapters", []):
            relative_file = chapter.get("file", "")
            orders.append(chapter.get("order"))
            if relative_file in seen_files:
                errors.append(f"duplicate chapter file: {relative_file}")
            seen_files.add(relative_file)

            path = ROOT / relative_file
            if not path.exists():
                errors.append(f"missing chapter file: {relative_file}")
                continue

            text = path.read_text(encoding="utf-8")
            if not text.startswith("# "):
                errors.append(f"{relative_file}: chapter must start with '# ' heading")
            expected_title = chapter.get("title", "")
            if expected_title and f"# {expected_title}" not in text.splitlines()[0]:
                errors.append(f"{relative_file}: heading does not match index title")
            for forbidden in FORBIDDEN_TEXT:
                if forbidden in text:
                    errors.append(f"{relative_file}: forbidden publication pattern {forbidden}")

            model_file = ROOT / chapter.get("modelFile", "")
            model_tests = ROOT / chapter.get("modelTests", "")
            if not model_file.exists():
                errors.append(f"{relative_file}: missing modelFile {model_file}")
            elif not str(model_file).endswith(".model.py"):
                errors.append(f"{relative_file}: modelFile must end with .model.py")
            else:
                result = subprocess.run(
                    [sys.executable, str(model_file)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                if result.returncode != 0:
                    errors.append(
                        f"{relative_file}: modelFile failed: {result.stderr.strip() or result.stdout.strip()}"
                    )

            if not model_tests.exists():
                errors.append(f"{relative_file}: missing modelTests {model_tests}")
            elif not str(model_tests).endswith(".model-tests.json"):
                errors.append(f"{relative_file}: modelTests must end with .model-tests.json")
            else:
                fixture = json.loads(model_tests.read_text(encoding="utf-8"))
                if fixture.get("model") != chapter.get("modelFile"):
                    errors.append(f"{relative_file}: modelTests model path mismatch")
                if fixture.get("chapter") != Path(relative_file).name:
                    errors.append(f"{relative_file}: modelTests chapter mismatch")

        expected = list(range(1, len(orders) + 1))
        if orders != expected:
            errors.append(f"{series_id}: chapter orders must be contiguous from 1")

    if errors:
        raise SystemExit("\n".join(errors))

    print("Chapter index verified.")


if __name__ == "__main__":
    main()
