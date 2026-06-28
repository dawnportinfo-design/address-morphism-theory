from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
MANIFEST_PATH = OUT_DIR / "address-morphism-theory-pdf-manifest.json"

EXPECTED_PDFS = [
    ("address-morphism-theory-full-ja.pdf", 80),
    ("address-morphism-theory-full-en.pdf", 50),
    ("address-morphism-theory-ja.pdf", 10),
    ("address-morphism-theory-en.pdf", 10),
    ("zero-knowledge-address-predicates-en.pdf", 20),
    ("zero-knowledge-address-predicates-ja.pdf", 15),
    ("address-translation-theory-ja.pdf", 12),
    ("address-machine-translation-theory-ja.pdf", 12),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_pdf(file_name: str, min_pages: int) -> dict[str, int | str]:
    path = OUT_DIR / file_name
    if not path.exists():
        raise SystemExit(f"missing PDF: {path}")

    doc = fitz.open(path)
    try:
        page_count = doc.page_count
        if page_count < min_pages:
            raise SystemExit(f"{file_name} has too few pages: {page_count} < {min_pages}")

        sample_text = "".join(page.get_text()[:1200] for page in doc[: min(3, page_count)]).strip()
        if len(sample_text) < 100:
            raise SystemExit(f"{file_name} does not expose enough extractable text")

        size = path.stat().st_size
        if size < 100_000:
            raise SystemExit(f"{file_name} is unexpectedly small: {size} bytes")

        return {
            "fileName": file_name,
            "pages": page_count,
            "bytes": size,
            "textCharsFirstPages": len(sample_text),
            "sha256": sha256_file(path),
        }
    finally:
        doc.close()


def main() -> None:
    results = [verify_pdf(file_name, min_pages) for file_name, min_pages in EXPECTED_PDFS]
    manifest = {
        "schema": "address-morphism-theory-pdf-manifest-v1",
        "pdfs": results,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Address Morphism Theory PDFs verified.")
    for result in results:
        print(
            f"- {result['fileName']}: pages={result['pages']} "
            f"bytes={result['bytes']} text_chars={result['textCharsFirstPages']} "
            f"sha256={str(result['sha256'])[:16]}..."
        )
    print(f"Manifest written: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
