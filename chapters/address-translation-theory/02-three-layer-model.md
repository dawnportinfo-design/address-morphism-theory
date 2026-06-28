# Three-Layer Model

Address translation can be organized into three layers.

## Semantic Layer

Parse the address into structural elements: country, region, municipality,
locality, street, building, unit, postal code, landmark, or handoff point.

## Institutional Layer

Map those elements into the destination institution's expected fields. A
Japanese ward, a US city, a Gulf locality, and a no-postcode island region do
not share the same field semantics.

## Output Layer

Format the result for the purpose. A shipping label, identity form, and map
query may each require a different ordering and disclosure level.
