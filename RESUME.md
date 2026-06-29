# Address Morphism Theory Resume

Address Morphism Theory (AMT) is a research program for treating addresses as
resolvable, auditable references rather than as plain text labels.

Most address systems assume that an address can eventually be normalized into a
single correct string, postal-code row, coordinate, or delivery label. That
assumption breaks in many ordinary cases: countries without reliable postal
codes, informal settlements, islands, ports, hotels, large buildings, shared
entrances, renamed streets, disputed regions, temporary shelters, natural
features, and privacy-preserving delivery flows.

AMT asks a different question:

> When a person, machine, institution, or delivery network receives an address
> expression, what is it allowed to resolve, what must remain uncertain, and
> what evidence is required before issuing a persistent identifier?

## Why This Theory Is Needed

Addresses are not only written text. They are references to entities that may be
physical, social, legal, virtual, temporary, or operational. A string such as a
street address, postal code, QR alias, room reference, port handoff point, or
region name is only a surface expression. The resolver must decide what entity
the expression refers to, which context it is valid in, and whether the evidence
is strong enough for the requested use.

This matters because address failure is often not a formatting problem. It is a
reference problem.

- The true target may not be in the candidate set.
- Multiple targets may share the same visible expression.
- A postal code may be absent, stale, or too coarse.
- A coordinate may be precise but socially or legally wrong.
- A building name may be useful locally but invisible to a global form.
- A delivery actor may need proof of deliverability without seeing the full
  address.
- A system may need to refuse precise issuance when evidence is weak.

AMT gives names, states, and tests to these failure modes instead of hiding them
inside ad hoc resolver behavior.

## Core Innovation

AMT models address resolution as a chain of partial morphisms:

```text
surface expression
  -> normalized expression
  -> candidate set
  -> evidence-bound referent
  -> persistent identifier
  -> application-specific view
```

Each step is context-indexed and may fail safely. This makes unresolved,
ambiguous, rejected, deprecated, and privacy-limited states part of the model
rather than exceptions.

The main innovation is not a new geocoder or a new postal database. It is a
general theory for deciding when address information can be transformed without
losing reference integrity.

## What AMT Does Better Than Common Approaches

| Common approach | Limitation | AMT advantage |
| --- | --- | --- |
| String normalization | Improves format but may preserve wrong reference | Separates expression cleanup from referent resolution |
| Postal-code lookup | Fails where postal codes are absent, weak, or stale | Allows AGID-first and postal-equivalent regions |
| Geocoding | Coordinates may not encode delivery, consent, or institution context | Treats coordinates as evidence, not final truth |
| Address validation API | Often returns pass/fail without explaining unresolved states | Makes abstention, ambiguity, and evidence gaps explicit |
| Blockchain identity | Risks putting sensitive address material in public systems | Keeps address data off-chain; only commitments or roots are optional |
| Machine translation | Translates words but may damage address structure | Preserves hierarchy, purpose, and country-specific form rules |

## Competitive Position

AMT is strongest where ordinary address products are weakest:

- countries with incomplete or no postal-code systems
- cross-border delivery and international checkout
- local-first address wallets and private QR sharing
- hotel, POS, locker, field handoff, port, island, and drone/robot handoff flows
- multilingual address search where alias, transliteration, and local names
  must not collapse distinct places
- public datasets that need versioned lineage and source confidence
- zero-knowledge-ready systems that prove address predicates without exposing
  the full address

The competitive advantage is the ability to combine formal abstention,
evidence-based candidate generation, lineage, quality scoring, and
privacy-preserving predicate boundaries in one framework.

## How To Use AMT

### For Researchers

Use AMT as a formal language for address reference. Start with:

1. What is the referent?
2. What is the surface expression?
3. Which context makes the expression meaningful?
4. Which evidence sources generate candidates?
5. When must the resolver abstain?
6. Which identifier can be issued without overclaiming?

The theory is designed to support definitions, propositions, counterexamples,
commutative diagrams, and executable reference models.

### For Developers

Use AMT as a design checklist for resolvers:

- normalize input without assuming it is correct
- generate candidates with source provenance
- score evidence and record unresolved states
- issue persistent IDs only after safety gates
- keep lineage and deprecation history
- expose purpose-specific views instead of raw address material

Run:

```bash
npm run verify:model
npm run verify:predicate-dsl
npm run verify:chapters
```

### For Standards And Public-Sector Readers

Use AMT to separate policy-sensitive address questions:

- Does this expression identify a legal place, a delivery point, a social
  settlement, or a temporary operational point?
- Which source is authoritative for this context?
- Can a public system show a useful identifier without exposing private address
  material?
- Can disputed or unresolved regions be represented without taking a political
  position?

### For AGID Implementers

AMT should be treated as the research layer beneath AGID. AGID can implement
resolvers, QR, SDKs, postal-zone generation, address wallets, and machine
handoff protocols while AMT defines the theory of reference, abstention,
lineage, and safe identifier issuance.

## What AMT Does Not Claim Yet

AMT is intentionally conservative. This repository does not claim:

- complete global candidate generation for every building, natural feature, or
  indoor unit
- production-grade zero-knowledge circuit security
- superiority over every commercial address validation provider under all
  benchmarks
- resolved sovereignty for disputed regions
- that coordinates alone are enough for delivery
- that postal codes can be replaced everywhere without local review

Those are empirical, operational, or cryptographic claims that require separate
benchmarks, audits, and source-specific validation.

## Research Questions AMT Opens

- What is the minimal evidence needed to issue a persistent address identifier?
- When are two address expressions equivalent across language, time, and
  institutions?
- How much information can be compressed out of an address before it loses
  delivery or legal meaning?
- Can a resolver prove deliverability without disclosing the full address?
- How should unresolved countries, informal settlements, ports, islands,
  natural features, and vertical spaces be represented?
- What is the correct failure state when a resolver cannot responsibly identify
  a referent?

## One-Sentence Summary

Address Morphism Theory is a formal and executable framework for transforming
address expressions into safe, evidence-bound identifiers while preserving
uncertainty, lineage, privacy, and context.
