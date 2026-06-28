# No-Postcode and Weak-Postcode Regions

No-postcode regions should use AGID or postal-equivalent zones as the primary
identifier. Weak-postcode regions should keep official codes but add candidate
display, confidence, and manual-review paths.

Recommended classes:

- postal code available plus reliable API
- postal code available plus weak API
- no postal code plus strong open geographic data
- no postal code plus weak open geographic data

Each class should have different validation gates and user interface behavior.

## Executable Model

- Model: [03-no-postcode-and-weak-postcode-regions.model.py](models/03-no-postcode-and-weak-postcode-regions.model.py)
- Fixture: [03-no-postcode-and-weak-postcode-regions.model-tests.json](models/03-no-postcode-and-weak-postcode-regions.model-tests.json)

The model is a local mathematical reference for this chapter's claims. It is not a production resolver, postal engine, or audited cryptographic circuit.
