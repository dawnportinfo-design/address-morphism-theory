# Postal Zone Generation Theory Table of Contents

Mathematical model for postal-equivalent zones in reliable, weak, and no-postcode countries.

## Chapters

1. [Postal Equivalence](01-postal-equivalence.md)
   - Defines when an AGID zone can act as a postal-code-equivalent region.
   - Model: [01-postal-equivalence.model.py](models/01-postal-equivalence.model.py)
   - Fixtures: [01-postal-equivalence.model-tests.json](models/01-postal-equivalence.model-tests.json)
2. [Zone Design Objectives](02-zone-design-objectives.md)
   - Defines balance, contiguity, delivery load, area, population, and route cost objectives.
   - Model: [02-zone-design-objectives.model.py](models/02-zone-design-objectives.model.py)
   - Fixtures: [02-zone-design-objectives.model-tests.json](models/02-zone-design-objectives.model-tests.json)
3. [No-Postcode and Weak-Postcode Regions](03-no-postcode-and-weak-postcode-regions.md)
   - Defines behavior for weak postal APIs and AGID-primary no-postcode regions.
   - Model: [03-no-postcode-and-weak-postcode-regions.model.py](models/03-no-postcode-and-weak-postcode-regions.model.py)
   - Fixtures: [03-no-postcode-and-weak-postcode-regions.model-tests.json](models/03-no-postcode-and-weak-postcode-regions.model-tests.json)

## Source Paper

- `verification/universal-postal-code-adoption-theory.md`
