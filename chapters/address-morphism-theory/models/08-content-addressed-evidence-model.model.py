from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Iterable


PUBLIC_LICENSES = {"CC-BY-4.0", "ODbL-1.0", "PDDL-1.0", "MIT", "public-domain"}
PUBLIC_SAFETY_CLASSES = {"public", "synthetic", "redacted"}
PID_ALLOWED_LICENSE_STATES = {"compatible"}


def canonical_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    normalized = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    return normalized.encode("utf-8")


def digest(value: str | bytes) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_json(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return digest(encoded)


@dataclass(frozen=True)
class EvidenceArtifact:
    source_hint: str
    content: str | bytes
    media_type: str
    license_id: str
    safety_class: str
    observed_at: str

    @property
    def digest(self) -> str:
        return digest(self.content)

    @property
    def byte_length(self) -> int:
        return len(canonical_bytes(self.content))

    @property
    def license_state(self) -> str:
        return "compatible" if self.license_id in PUBLIC_LICENSES else "unknown"

    @property
    def publication_safe(self) -> bool:
        return self.safety_class in PUBLIC_SAFETY_CLASSES


@dataclass(frozen=True)
class TransformRecord:
    transform_id: str
    transform_version: str
    parent_digests: tuple[str, ...]
    params_digest: str
    output_digest: str
    lossiness: str
    redaction_class: str


@dataclass(frozen=True)
class EvidenceBundle:
    artifacts: tuple[EvidenceArtifact, ...]
    transforms: tuple[TransformRecord, ...] = ()

    @property
    def root(self) -> str:
        return bundle_root(artifact.digest for artifact in self.artifacts)


@dataclass(frozen=True)
class EvidenceGateResult:
    accepted: bool
    reason: str
    bundle_root: str


def bundle_root(digests: Iterable[str]) -> str:
    joined = "|".join(sorted(digests))
    return digest(joined)


def transform_valid(transform: TransformRecord, available_digests: set[str]) -> bool:
    if not transform.parent_digests:
        return False
    if any(parent not in available_digests for parent in transform.parent_digests):
        return False
    if transform.lossiness not in {"lossless", "lossy"}:
        return False
    if transform.redaction_class not in {"none", "redacted", "aggregated"}:
        return False
    return True


def bundle_transform_chain_valid(bundle: EvidenceBundle) -> bool:
    available = {artifact.digest for artifact in bundle.artifacts}
    for transform in bundle.transforms:
        if not transform_valid(transform, available):
            return False
        available.add(transform.output_digest)
    return True


def evidence_gate(bundle: EvidenceBundle, require_pid_ready: bool = True) -> EvidenceGateResult:
    if not bundle.artifacts:
        return EvidenceGateResult(False, "empty-bundle", bundle.root)
    if not bundle_transform_chain_valid(bundle):
        return EvidenceGateResult(False, "invalid-transform-chain", bundle.root)
    if any(not artifact.publication_safe for artifact in bundle.artifacts):
        return EvidenceGateResult(False, "publication-unsafe-artifact", bundle.root)
    if require_pid_ready and any(artifact.license_state not in PID_ALLOWED_LICENSE_STATES for artifact in bundle.artifacts):
        return EvidenceGateResult(False, "license-not-compatible", bundle.root)
    return EvidenceGateResult(True, "accepted", bundle.root)


def evidence_envelope(bundle: EvidenceBundle, gate_version: str = "evidence-gate-v1") -> dict[str, object]:
    gate = evidence_gate(bundle)
    return {
        "schema": "amt-content-addressed-evidence-envelope-v1",
        "bundleRoot": bundle.root,
        "gateVersion": gate_version,
        "artifactCount": len(bundle.artifacts),
        "accepted": gate.accepted,
        "reason": gate.reason,
        "artifactDigests": sorted(artifact.digest for artifact in bundle.artifacts),
    }


def run_model_checks() -> dict[str, bool]:
    public_a = EvidenceArtifact(
        source_hint="https://example.invalid/source-a.csv",
        content="id,name\n1,synthetic-place\n",
        media_type="text/csv",
        license_id="CC-BY-4.0",
        safety_class="synthetic",
        observed_at="2026-06-29",
    )
    same_content_new_location = EvidenceArtifact(
        source_hint="file://mirror/source-a.csv",
        content="id,name\r\n1,synthetic-place\r\n",
        media_type="text/csv",
        license_id="CC-BY-4.0",
        safety_class="synthetic",
        observed_at="2026-06-29",
    )
    tampered = EvidenceArtifact(
        source_hint="https://example.invalid/source-a.csv",
        content="id,name\n1,changed-place\n",
        media_type="text/csv",
        license_id="CC-BY-4.0",
        safety_class="synthetic",
        observed_at="2026-06-29",
    )
    public_b = EvidenceArtifact(
        source_hint="official-register-demo",
        content=json.dumps({"region": "demo", "version": 1}, sort_keys=True),
        media_type="application/json",
        license_id="public-domain",
        safety_class="public",
        observed_at="2026-06-29",
    )
    unknown_license = EvidenceArtifact(
        source_hint="unknown-license-demo",
        content="demo",
        media_type="text/plain",
        license_id="unknown",
        safety_class="public",
        observed_at="2026-06-29",
    )
    unsafe = EvidenceArtifact(
        source_hint="private-fixture-demo",
        content="synthetic-private-fixture",
        media_type="text/plain",
        license_id="MIT",
        safety_class="private",
        observed_at="2026-06-29",
    )

    bundle_one = EvidenceBundle((public_a, public_b))
    bundle_reordered = EvidenceBundle((public_b, public_a))
    transform = TransformRecord(
        transform_id="normalize-json",
        transform_version="1",
        parent_digests=(public_b.digest,),
        params_digest=digest_json({"sort_keys": True}),
        output_digest=digest_json({"normalized": True, "source": public_b.digest}),
        lossiness="lossless",
        redaction_class="none",
    )
    missing_parent_transform = TransformRecord(
        transform_id="orphan-transform",
        transform_version="1",
        parent_digests=("sha256:" + "0" * 64,),
        params_digest=digest_json({}),
        output_digest=digest("orphan"),
        lossiness="lossless",
        redaction_class="none",
    )

    accepted_bundle = EvidenceBundle((public_a, public_b), (transform,))
    missing_parent_bundle = EvidenceBundle((public_a,), (missing_parent_transform,))

    envelope = evidence_envelope(accepted_bundle)

    return {
        "same_content_same_digest_across_location_and_line_endings": public_a.digest == same_content_new_location.digest,
        "tampered_content_changes_digest": public_a.digest != tampered.digest,
        "bundle_root_order_independent": bundle_one.root == bundle_reordered.root,
        "valid_transform_chain_accepts": bundle_transform_chain_valid(accepted_bundle),
        "missing_transform_parent_rejects": not bundle_transform_chain_valid(missing_parent_bundle),
        "unsafe_artifact_blocks_publication": evidence_gate(EvidenceBundle((unsafe,))).reason == "publication-unsafe-artifact",
        "unknown_license_blocks_pid_ready_gate": evidence_gate(EvidenceBundle((unknown_license,))).reason == "license-not-compatible",
        "accepted_bundle_has_root_in_envelope": envelope["accepted"] is True and envelope["bundleRoot"] == accepted_bundle.root,
        "artifact_digest_list_is_sorted": envelope["artifactDigests"] == sorted(envelope["artifactDigests"]),
    }


def main() -> None:
    checks = run_model_checks()
    failed = [name for name, passed in checks.items() if not passed]
    print(json.dumps({"schema": "amt-content-addressed-evidence-model-v1", "checks": checks}, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed))


if __name__ == "__main__":
    main()
