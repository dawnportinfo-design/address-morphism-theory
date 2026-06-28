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
