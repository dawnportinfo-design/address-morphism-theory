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

## Executable Model

- Model: [02-three-layer-model.model.py](models/02-three-layer-model.model.py)
- Fixture: [02-three-layer-model.model-tests.json](models/02-three-layer-model.model-tests.json)

The model is a local mathematical reference for this chapter's claims. It is not a production resolver, postal engine, or audited cryptographic circuit.
