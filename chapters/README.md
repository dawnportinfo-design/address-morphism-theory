# Chapterized Manuscript Sources

This directory is the reader-friendly source map for Address Morphism Theory.
The long files in `papers/` remain the canonical manuscript snapshots, while
these chapter files split the work by research type and chapter.

## Why Split By Type

Address Morphism Theory now spans several different artifacts:

- formal address-reference theory
- zero-knowledge address predicates
- address translation and machine translation
- postal-zone generation and no-postcode regions
- verification boundaries and executable models

Keeping every idea in one long manuscript makes review hard. This directory
separates the work into smaller, maintainable reading paths.

## Series

- `address-morphism-theory/` - the core theory of address reference, evidence,
  abstention, lineage, and reconstruction.
- `zero-knowledge-address-predicates/` - privacy-preserving claims over address
  structures, without publishing raw address material.
- `address-translation-theory/` - purpose-specific restructuring of address
  data across languages, institutions, and forms.
- `postal-zone-generation-theory/` - postal-code and postal-equivalent zone
  design for countries with missing or weak postal systems.

## Maintenance Rules

1. Every chapter must be listed in `chapters/index.json`.
2. Every chapter must start with a single `#` heading.
3. Every series must declare its `kind`, `status`, and `sourcePaper`.
4. No chapter may contain raw personal address fixtures, recipients, witnesses,
   private keys, or proof material.
5. Executable claims should point to `src/` or `verification/`, not only prose.
