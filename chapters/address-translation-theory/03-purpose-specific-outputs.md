# Purpose-Specific Outputs

Address translation should return more than a translated string.

Useful output fields include:

- normalized components
- formatted lines
- confidence
- warnings
- unverified fields
- postal or postal-equivalent match status
- delivery risk
- source consistency
- display language
- privacy disclosure level

This makes translation auditable and compatible with AMT evidence gates.

## Executable Model

- Model: [03-purpose-specific-outputs.model.py](models/03-purpose-specific-outputs.model.py)
- Fixture: [03-purpose-specific-outputs.model-tests.json](models/03-purpose-specific-outputs.model-tests.json)

The model is a local mathematical reference for this chapter's claims. It is not a production resolver, postal engine, or audited cryptographic circuit.
