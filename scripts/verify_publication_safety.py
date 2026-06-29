from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [
    "adoption",
    "audit",
    "chapters",
    "circuits",
    "compatibility",
    "demos",
    "formal",
    "grant-readiness",
    "notes",
    "papers",
    "scripts",
    "src",
    "verification",
    "zk",
]
ROOT_TEXT_FILES = ["README.md", "REPOSITORY_SPLIT.md", "package.json", "LICENSE", "LICENSE-PAPERS.md"]
TEXT_SUFFIXES = {".circom", ".cjs", ".json", ".md", ".py", ".tex", ".ts", ".txt"}

DENY_PATTERNS = [
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("stripe-secret-key", re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    ("inline-private-key-field", re.compile(r"(?i)\b(private[_ -]?key|secret[_ -]?key)\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
    ("inline-witness-field", re.compile(r"(?i)\b(witness|proof[_ -]?witness)\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
]


def find_denied_patterns(text: str) -> list[str]:
    return [pattern_id for pattern_id, pattern in DENY_PATTERNS if pattern.search(text)]


def run_self_test() -> None:
    samples = {
        "private-key-block": "-----BEGIN " + "PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----",
        "github-token": "ghp_" + ("A" * 36),
        "aws-access-key": "AKIA" + ("0" * 16),
        "slack-token": "xoxb-" + ("a" * 24),
        "stripe-secret-key": "sk_" + "test_" + ("a" * 24),
        "inline-private-key-field": 'private_key: "' + ("x" * 16) + '"',
        "inline-witness-field": 'witness: "' + ("x" * 16) + '"',
    }

    missing = []
    for pattern_id, sample in samples.items():
        if pattern_id not in find_denied_patterns(sample):
            missing.append(pattern_id)

    safe_text = "Address Morphism Theory discusses proof systems and witness concepts abstractly."
    false_positive = find_denied_patterns(safe_text)

    if missing or false_positive:
        if missing:
            print("Publication safety self-test missed patterns:")
            for pattern_id in missing:
                print(f"- {pattern_id}")
        if false_positive:
            print("Publication safety self-test false positives:")
            for pattern_id in false_positive:
                print(f"- {pattern_id}")
        raise SystemExit(1)

    print(f"Publication safety self-test passed for {len(samples)} denied pattern(s).")


def iter_text_files():
    for file_name in ROOT_TEXT_FILES:
        path = ROOT / file_name
        if path.exists() and path.is_file():
            yield path

    for directory in SCAN_DIRS:
        root = ROOT / directory
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def main() -> None:
    findings: list[str] = []
    scanned = 0
    for path in iter_text_files():
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern_id in find_denied_patterns(text):
            findings.append(f"{path.relative_to(ROOT)}: {pattern_id}")

    if findings:
        print("Publication safety scan failed.")
        for finding in findings:
            print(f"- {finding}")
        raise SystemExit(1)

    print(f"Publication safety scan passed for {scanned} text file(s).")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        run_self_test()
        raise SystemExit(0)
    main()
