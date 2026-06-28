# Addressless private delivery protocol model check

Date: 2026-06-27

Question reviewed:

Can Address Morphism Theory support delivery without entering a conventional
address, keep the counterparty from learning the address, work internationally,
and replace paper forms or human-readable labels with protocol-level
information?

## Verdict

Address Morphism Theory is strong enough as the semantic foundation, but it is
not enough by itself as the full delivery protocol.

AMT currently gives the right mathematical language for:

- addressable entities, not only postal strings;
- context-dependent reference;
- unresolved safety;
- evidence, lineage, and quality gates;
- AGID/AOID/PID boundary concepts;
- address-derived predicates and privacy proof boundaries;
- natural, vertical, and delivery handoff points.

However, addressless private delivery requires additional protocol mathematics:

- role-based views;
- staged disclosure;
- encrypted delivery objects;
- delivery predicates;
- international compliance predicates;
- paperless machine-readable label tokens;
- signed handoff receipts;
- revocation and replay prevention;
- leakage and anonymity-set analysis.

The correct claim is therefore:

> AMT can define the semantic object being delivered to. A companion AGID/AOID
> delivery protocol can let a merchant or counterparty ship to that object
> without seeing the raw address, while authorized carriers receive only the
> minimum view needed for routing, customs, and final handoff.

It should not claim:

> No actor ever needs any address-like information in every country.

For international delivery, customs, sanctions screening, tax, restricted goods,
and carrier rules may legally require specific information. The protocol can
keep that information away from the merchant and most intermediaries, but it
must support scoped disclosure to authorized parties when required.

## Adequacy by layer

| Layer | Current AMT adequacy | Gap |
| --- | --- | --- |
| Address semantics | Strong | Keep in AMT core. |
| Address quality and unresolved states | Strong | Add delivery-specific non-answer states. |
| Private predicates | Partial | ZK paper handles proof details; AMT should only define attributes. |
| AOID ownership and delegation | Conceptual | Needs protocol paper/spec. |
| Addressless checkout | Partial | Needs merchant view, carrier view, and receipt model. |
| Paperless handoff | Weak | Needs label token and signed state machine. |
| International shipping | Weak | Needs compliance predicate and scoped customs disclosure. |
| "No raw address by default" | Conceptual | Needs invariant and testable interface rule. |

## Required model extension

### 1. Private Delivery Object

Define a private delivery object:

\[
\mathsf{PDO}
=
(\mathsf{pid},
\mathsf{agid},
\mathsf{aoidCommit},
\mathsf{policy},
\mathsf{routeHints},
\mathsf{credentialRefs},
\mathsf{expiry},
\mathsf{revocation})
\]

The public part is not a raw address. It is a commitment, alias, policy, and
delivery capability descriptor. Hidden routing fields are encrypted or otherwise
restricted to authorized roles.

This makes "no address input" practical in two ways:

1. the user can select or scan an AOID/PDO instead of typing an address;
2. the merchant receives only a deliverability result, alias, and receipt.

### 2. Role-based view lattice

Define a role-indexed disclosure function:

\[
\operatorname{Disclose}_{r,\sigma}:\mathsf{PDO}\to\mathsf{View}_{r}
\]

where \(r\) is a role and \(\sigma\) is an authorization token, consent grant,
credential, or policy proof.

Useful roles include:

\[
r\in\{\mathsf{buyer},\mathsf{merchant},\mathsf{platform},
\mathsf{carrier},\mathsf{customs},\mathsf{lastMile},
\mathsf{locker},\mathsf{recipient}\}.
\]

Views should be a lattice, not a single total order. Customs, carrier, locker,
and last-mile views may need different fields.

Safety invariant:

\[
\mathsf{rawAddress}\notin\mathsf{View}_{\mathsf{merchant}}
\]

unless the user explicitly chooses a raw-address sharing mode.

### 3. Delivery predicate

Define a delivery eligibility predicate:

\[
P_{\mathrm{deliver}}(q,\rho,\chi,t)=1
\]

where \(q\) is an AMT-resolved referent, \(\rho\) is carrier or service policy,
\(\chi\) is the delivery context, and \(t\) is time.

The predicate should distinguish:

- deliverable to door;
- deliverable to building entrance;
- deliverable to locker or PUDO;
- deliverable to port, shore, station, gate, or access point;
- manual review required;
- not currently deliverable.

This prevents the system from pretending that a coordinate or place name is
automatically a delivery endpoint.

### 4. International compliance predicate

International delivery needs a separate predicate:

\[
P_{\mathrm{intl}}(o,d,i,\rho,t)=1
\]

where \(o\) is origin, \(d\) is destination jurisdiction or route zone, \(i\) is
the item class, \(\rho\) is carrier/customs policy, and \(t\) is time.

This predicate should not expose the raw destination to the merchant. It should
return a capability result such as:

- accepted;
- accepted with customs disclosure to authorized party;
- restricted item;
- service unavailable;
- manual review required.

This is the mathematical layer needed for "overseas does not matter" to become
"the protocol can decide overseas deliverability without revealing the raw
address to the counterparty."

### 5. Paperless label token

Replace human-readable labels with a machine-readable token:

\[
\mathsf{LabelToken}
=H(\mathsf{deliveryId}\,\|\,\mathsf{carrier}\,\|\,\mathsf{epoch}\,\|\,n)
\]

The token may be represented as QR, NFC, barcode, or API receipt. It should not
contain the raw address. Carrier systems resolve it to the authorized view.

The safer claim is:

> Paperless by default means no human-readable raw address is printed or shared;
> physical parcels may still carry a machine-readable token where carriers
> support tokenized routing.

### 6. Handoff state machine

Define the delivery lifecycle:

\[
\mathsf{quote}
\to
\mathsf{reserved}
\to
\mathsf{accepted}
\to
\mathsf{inTransit}
\to
\mathsf{handoffReady}
\to
\mathsf{delivered}
\]

with failure and privacy states:

\[
\mathsf{manualRequired},\quad
\mathsf{carrierOnlyDisclosureRequired},\quad
\mathsf{cannotReach},\quad
\mathsf{revoked},\quad
\mathsf{expired}.
\]

Each transition should produce a signed receipt:

\[
s_i \xrightarrow{\tau_i,\operatorname{sig}_i} s_{i+1}
\]

where \(\tau_i\) records only the minimum non-raw facts needed for audit.

### 7. Leakage and anonymity-set constraint

Hiding the address string is not enough. If a predicate identifies a tiny
region, the address may leak by inference.

Add an anonymity constraint:

\[
|\{q\in Q_t : P(q)=1\}|\ge k_{\min}
\]

or, for sparse areas, require a coarser predicate or carrier-only disclosure.

This should apply to delivery zone, customs region, last-mile depot, and
building-level claims.

### 8. Resolver and disclosure commutative diagram

The protocol should commute across merchant, carrier, and last-mile views:

\[
\begin{tikzcd}
\mathsf{PDO} \arrow[r,"\operatorname{Pred}"] \arrow[d,"\operatorname{Disclose}_{carrier}"']
& \pi_{\mathrm{deliver}} \arrow[r]
& \mathsf{MerchantReceipt} \\
\mathsf{CarrierView} \arrow[r,"\operatorname{route}"']
& \mathsf{LastMileView} \arrow[r,"\operatorname{handoff}"']
& \mathsf{DeliveryReceipt}
\end{tikzcd}
\]

The merchant receipt and carrier route must refer to the same delivery object
without requiring the merchant to learn the raw address.

### 9. Consent and revocation predicate

Define:

\[
\operatorname{Allowed}(r,p,t,s)=1
\]

where \(r\) is role, \(p\) is purpose, \(t\) is time, and \(s\) is scope.

Disclosure is valid only if:

\[
\operatorname{Allowed}(r,p,t,s)=1
\quad\land\quad
\operatorname{Revoked}(\mathsf{PDO},t)=0.
\]

This is essential for paperless, private, and reusable address objects.

## Recommended paper/spec split

AMT core should keep only a short section:

- addressless delivery is an application of AMT;
- AMT defines addressable referents, attributes, context, quality, and
  unresolved safety;
- AGID/AOID delivery protocol handles encrypted objects, scoped disclosure,
  receipt states, and carrier handoff;
- ZK Address Predicates handles cryptographic proofs and predicate leakage.

Create or reserve a companion document:

> Addressless Private Delivery Protocol over AMT

Suggested sections:

1. Private Delivery Object;
2. role/view lattice;
3. delivery eligibility predicates;
4. international compliance predicates;
5. paperless token and receipts;
6. carrier and customs scoped disclosure;
7. locker/PUDO/agent handoff;
8. non-deliverable and manual review states;
9. privacy leakage and anonymity sets;
10. conformance tests and no-raw-address gates.

## Final judgment

AMT is enough to make the idea academically plausible. It is not enough to make
the product/protocol claim complete.

The missing bridge is not more address formatting. The missing bridge is a
formal private delivery protocol:

\[
\text{AMT semantics}
\quad+\quad
\text{AOID/PDO scoped disclosure}
\quad+\quad
\text{ZK predicates}
\quad+\quad
\text{carrier handoff receipts}.
\]

With that bridge, the strongest safe claim becomes:

> A user can send a private delivery object instead of typing a raw address.
> The counterparty can verify deliverability and receive a receipt without
> learning the address. Authorized logistics actors receive only the scoped
> information needed to route, comply, and hand off the parcel.

