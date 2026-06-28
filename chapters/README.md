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
- `address-machine-translation-theory/` - guarded address machine translation
  with rules, AI assistance, geo evidence, confidence, and abstention.
- `postal-zone-generation-theory/` - postal-code and postal-equivalent zone
  design for countries with missing or weak postal systems.

## Table Of Contents

- `table-of-contents.md` - cross-series table of contents.
- `address-morphism-theory/toc.md` - core Address Morphism Theory chapters.
- `zero-knowledge-address-predicates/toc.md` - ZK address predicate chapters.
- `address-translation-theory/toc.md` - address translation theory chapters.
- `address-machine-translation-theory/toc.md` - address machine translation theory chapters.
- `postal-zone-generation-theory/toc.md` - postal-zone generation theory chapters.

## Chapter Model Layout

Each chapter keeps its prose file in the series directory and its executable
mathematical model under that series' `models/` directory:

```text
chapters/<series>/
  01-example-chapter.md
  models/
    01-example-chapter.model.py
    01-example-chapter.model-tests.json
```

The model is intentionally small and dependency-free. It is not a production
resolver, postal engine, or audited ZK circuit; it is a runnable statement of
the mathematical boundary claimed by the chapter.

## Maintenance Rules

1. Every chapter must be listed in `chapters/index.json`.
2. Every chapter must start with a single `#` heading.
3. Every series must declare its `kind`, `status`, and `sourcePaper`.
4. No chapter may contain raw personal address fixtures, recipients, witnesses,
   private keys, or proof material.
5. Every chapter must declare `modelFile` and `modelTests`.
6. Every chapter model must run locally through `npm run verify:chapters`.
7. Executable claims should point to chapter models, `src/`, or `verification/`,
   not only prose.
