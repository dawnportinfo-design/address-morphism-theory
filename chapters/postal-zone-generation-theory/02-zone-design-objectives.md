# Zone Design Objectives

Postal-zone generation should optimize several objectives at once:

- delivery reachability
- administrative consistency
- population and parcel balance
- route continuity
- code stability
- low collision risk
- human readability
- compatibility with existing national formats
- ability to deprecate and redirect zones

No single objective is enough. A compact geometric zone can be operationally
bad if it cuts through roads, ports, rivers, or administrative boundaries.

## Executable Model

- Model: [02-zone-design-objectives.model.py](models/02-zone-design-objectives.model.py)
- Fixture: [02-zone-design-objectives.model-tests.json](models/02-zone-design-objectives.model-tests.json)

The model is a local mathematical reference for this chapter's claims. It is not a production resolver, postal engine, or audited cryptographic circuit.
