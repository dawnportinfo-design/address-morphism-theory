# Address Translation Theory and Address Machine Translation Theory

Date: 2026-06-27

## Purpose

Address translation should not be treated as ordinary sentence translation.
An address is a reference object, a routing object, and sometimes a legal or
postal object. Translating it incorrectly can change the destination, not merely
change wording.

This memo proposes two related but separate theories:

1. Address Translation Theory: the semantic theory of what must be preserved
   when an address is rendered across language, script, postal convention, and
   delivery context.
2. Address Machine Translation Theory: the operational theory of how software,
   gazetteers, romanization standards, postal data, large language models, and
   validation gates produce safe address renderings.

## Core distinction

Address Morphism Theory answers:

> What addressable object is being referred to?

Address Translation Theory answers:

> Which representation of that same object is appropriate for a target
> language, script, jurisdiction, and use context?

Address Machine Translation Theory answers:

> How can a system generate that representation while detecting when it should
> not answer?

## Address Translation Theory

### 1. Address expression and referent

Let \(S_{L,\Sigma,\chi,t}\) be the space of address surface expressions in
language \(L\), script \(\Sigma\), context \(\chi\), and time \(t\).

Let \(Q_t\) be the AMT referent space. A parser/resolver maps a surface
expression to a candidate referent:

\[
\rho_{L,\Sigma,\chi,t}:S_{L,\Sigma,\chi,t}\to \mathcal{P}(Q_t).
\]

An address translation from source locale \(u\) to target locale \(v\) is not
only a string map:

\[
\tau_{u\to v}:S_u\to S_v.
\]

It is valid only when it preserves the intended referent under the target
resolver:

\[
q\in \rho_u(s)
\quad\Rightarrow\quad
q\in \rho_v(\tau_{u\to v}(s)).
\]

If this cannot be established above a declared confidence threshold, the system
must return `manual_required`, `ambiguous`, or `source_gap`.

### 2. Preservation law

The central law is referent preservation:

\[
\operatorname{Ref}_t(s)
=
\operatorname{Ref}_t(\tau_{u\to v}(s))
\]

whenever the translation is emitted as a resolved address.

This is weaker than saying every token has a perfect translation. Proper nouns,
building names, road names, historic names, and dialect-derived names may be:

- retained;
- transliterated;
- romanized;
- rendered by official alias;
- rendered by carrier-preferred alias;
- left in original script with a structured English routing layer.

### 3. Component-preserving translation

Let an address be decomposed into components:

\[
c=(c_{\mathrm{name}},c_{\mathrm{building}},c_{\mathrm{unit}},
c_{\mathrm{street}},c_{\mathrm{locality}},c_{\mathrm{region}},
c_{\mathrm{postal}},c_{\mathrm{country}},c_{\mathrm{route}})
\]

Translation is a pair:

\[
\tau=(\tau_{\mathrm{lex}},\tau_{\mathrm{order}})
\]

where \(\tau_{\mathrm{lex}}\) transforms component labels or names, and
\(\tau_{\mathrm{order}}\) renders components in the target address order.

This prevents a common failure:

> translating words but keeping the wrong country order.

For international English, the target order should usually be delivery-oriented
and country-specific, not a literal mirror of the source string.

### 4. Translation modes

Address translation must declare its mode:

| Mode | Meaning | Example use |
| --- | --- | --- |
| native | Local postal or administrative language | Domestic delivery |
| international-English | English rendering for cross-border logistics | Overseas shipping |
| official-alias | Official multilingual name or government alias | Switzerland, Belgium, Hong Kong |
| romanization | Script-to-Latin conversion under a named standard | Japanese Hepburn, Korean Revised Romanization |
| carrier | Carrier-preferred logistics rendering | DHL, postal operators, last-mile routing |
| search-expansion | Recall-oriented aliases for search only | User search, not label output |

Search-expansion output must not be treated as a deliverable label without
validation.

### 5. Non-equivalence cases

Translation is not identity preserving when:

- two different places share one romanized form;
- a local proper noun is mistranslated as a common noun;
- an old name and a current name are both valid for different scopes;
- a dialect form and standard form refer to different administrative objects;
- a building name has a local commercial alias not present in postal data;
- the target country does not accept the target-language format for delivery.

Therefore multilingual expansion is a recall layer, while translation for
delivery is a gated rendering layer.

## Address Machine Translation Theory

### 1. Machine translation pipeline

Address machine translation should be a constrained pipeline:

\[
s
\xrightarrow{\pi}
T
\xrightarrow{\varepsilon_t}
C
\xrightarrow{\kappa}
q
\xrightarrow{R_{v,\chi}}
\hat{s}_v
\xrightarrow{V}
\{\mathrm{emit},\mathrm{manual},\mathrm{reject}\}.
\]

Where:

- \(\pi\): parse into typed tokens;
- \(\varepsilon_t\): expand aliases, old names, romanization, official names;
- \(C\): candidate set;
- \(\kappa\): cluster or select the intended referent;
- \(R_{v,\chi}\): render for target locale and context;
- \(V\): verify with postal, geographic, source, and component gates.

The important point:

> The model should translate from resolved structure, not directly from raw
> source string to target string.

### 2. Source hierarchy

Machine translation should prioritize sources by authority:

1. official local address or postal data;
2. government multilingual gazetteer;
3. carrier or postal operator convention;
4. open geographic data with language tags;
5. community gazetteer or OSM aliases;
6. romanization standard;
7. statistical or neural model suggestion;
8. human correction.

Neural or LLM output should be treated as a proposal, not as authority.

### 3. Quality score

Define:

\[
Q_{\mathrm{tr}}(\hat{s}_v,q,v,\chi,t)
=
w_1R+w_2O+w_3P+w_4G+w_5C-w_6H-w_7A
\]

where:

- \(R\): referent preservation score;
- \(O\): correct target order score;
- \(P\): postal compatibility score;
- \(G\): geographic consistency score;
- \(C\): source confidence score;
- \(H\): homograph or romanization collision risk;
- \(A\): alias ambiguity risk.

Emit rules:

\[
Q_{\mathrm{tr}}\ge \theta_{\mathrm{emit}}
\Rightarrow \mathrm{emit}
\]

\[
\theta_{\mathrm{manual}}\le Q_{\mathrm{tr}}<\theta_{\mathrm{emit}}
\Rightarrow \mathrm{manualRequired}
\]

\[
Q_{\mathrm{tr}}<\theta_{\mathrm{manual}}
\Rightarrow \mathrm{rejectOrSearchOnly}
\]

### 4. Round-trip is useful but insufficient

Back-translation can detect some errors:

\[
s \to \hat{s}_v \to \hat{s}_u
\]

But exact string equality is too strict and can be misleading. The better test
is referent round-trip:

\[
\operatorname{Ref}_t(s)=\operatorname{Ref}_t(\hat{s}_u).
\]

This keeps the focus on address identity, not surface text.

### 5. Region-specific translation policies

Address machine translation must use country and region policies:

- Japan: Japanese official form plus Hepburn romanization for international
  English; do not translate proper nouns as common words.
- Mainland China: simplified Chinese plus Hanyu Pinyin and administrative
  division data; preserve common English aliases where logistics still uses
  them.
- Taiwan: traditional Chinese plus Taiwan conventional English names; retain
  Hanyu Pinyin as alias, not primary where conventional form dominates.
- Hong Kong: traditional Chinese plus Hong Kong English and Cantonese-derived
  place names.
- Macao: traditional Chinese, Portuguese, Cantonese-derived names, and English
  support.
- Korea: Korean plus Revised Romanization, with known exceptions and official
  English aliases.
- Arabic-script countries: Arabic local form plus country-specific French,
  English, or romanized delivery rendering where appropriate.
- Multilingual Europe: render only address-relevant official languages for the
  place, not every application language.

### 6. Machine translation failure states

The system should expose concise failure states:

| State | Meaning |
| --- | --- |
| `language_gap` | Missing reliable source for language/script. |
| `alias_conflict` | Multiple referents share the target alias. |
| `romanization_collision` | Romanization collapses different names. |
| `postal_order_uncertain` | Target address order is not verified. |
| `carrier_format_unknown` | Carrier-accepted international format is unknown. |
| `proper_name_risk` | Proper noun may be mistranslated. |
| `manual_required` | Human or authoritative source required. |

### 7. Human correction as governed evidence

Human correction should be stored as evidence, not silently overwrite official
data:

\[
h=(\hat{s}_v,q,\mathrm{source},\mathrm{scope},t,\mathrm{reviewStatus})
\]

Accepted corrections can improve aliases and rendering rules, but must remain
scoped by country, language, source, and time.

## Relationship to AMT

Address Translation Theory is an application layer of AMT:

\[
\text{AMT referent}
\to
\text{localized rendering}
\to
\text{delivery/display/search use}.
\]

It should not redefine address identity. It should preserve and render it.

Address Machine Translation Theory is an implementation and verification layer:

\[
\text{sources + models + policies + gates}
\to
\text{safe translated address output}.
\]

It should be tested with:

- referent preservation;
- component order correctness;
- postal/carrier compatibility;
- romanization collision detection;
- alias conflict detection;
- multilingual round-trip by referent;
- manual-required behavior under weak sources.

## Recommended paper split

AMT core should include a short section:

> Address translation is valid only when it preserves the resolved referent
> under the target locale and context. Multilingual expansion improves recall
> but is not itself a proof of identity.

Then create a companion paper or chapter:

> Address Translation Theory and Address Machine Translation over AMT

Suggested structure:

1. Address translation is not sentence translation.
2. Referent preservation law.
3. Component order and postal rendering.
4. Romanization, transliteration, alias, and official name layers.
5. Translation modes: native, international English, carrier, search.
6. Machine translation pipeline.
7. Quality score and failure states.
8. Regional policies and examples.
9. Human correction and governance.
10. Conformance tests.

## Final judgment

The strongest design is:

\[
\text{resolve first, translate second, validate before emitting}.
\]

This makes address translation compatible with AMT and avoids the dangerous
pattern:

\[
\text{raw string} \to \text{neural translation} \to \text{shipping label}.
\]

For AGID, this is especially important because the goal is not pretty language
conversion. The goal is preserving the destination, respecting local and
international address order, and knowing when a translation is too risky to use.

