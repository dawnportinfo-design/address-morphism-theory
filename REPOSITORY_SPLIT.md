# Repository Split Notes

This repository was split from the AGID workspace as the independent home for
Address Morphism Theory.

## Canonical Ownership

| Area | Canonical repository |
| --- | --- |
| Address Morphism Theory papers | `address-morphism-theory` |
| AMT verification notes and claim maps | `address-morphism-theory` |
| AGID/AOID resolver implementation | `AGID` |
| SDKs and conformance vectors | `AGID` until generated from `agid-spec` |
| Product UI, POS, QR, maps, field workflows | `AGID` |

## Migration Policy

1. Copy first, do not delete from AGID until links and release scripts are updated.
2. Publish this repository as the canonical source for future AMT edits.
3. Replace AGID research-page links with links to this repository.
4. Move PDF build automation here after the repository is pushed.

## Do Not Move Here

- Raw address fixtures.
- Private recipients or witness material.
- Runtime AGID code.
- Country packs or postal datasets.
