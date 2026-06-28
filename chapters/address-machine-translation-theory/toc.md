# Address Machine Translation Theory Table of Contents

Guarded machine translation model for addresses using rules, gazetteers, postal or AGID evidence, and abstention.

## Chapters

1. [Guarded Address Machine Translation](01-guarded-address-mt.md)
   - Defines why address MT must be guarded by structure, evidence, and non-translation rules.
   - Model: [01-guarded-address-mt.model.py](models/01-guarded-address-mt.model.py)
   - Fixtures: [01-guarded-address-mt.model-tests.json](models/01-guarded-address-mt.model-tests.json)
2. [Rule, AI, and Geo Hybrid Engine](02-rule-ai-geo-hybrid-engine.md)
   - Defines the hybrid pipeline: parser, normalizer, transliterator, geo verifier, and renderer.
   - Model: [02-rule-ai-geo-hybrid-engine.model.py](models/02-rule-ai-geo-hybrid-engine.model.py)
   - Fixtures: [02-rule-ai-geo-hybrid-engine.model-tests.json](models/02-rule-ai-geo-hybrid-engine.model-tests.json)
3. [Quality Feedback and Abstention](03-quality-feedback-and-abstention.md)
   - Defines confidence, warnings, unverified fields, delivery risk, and manual review.
   - Model: [03-quality-feedback-and-abstention.model.py](models/03-quality-feedback-and-abstention.model.py)
   - Fixtures: [03-quality-feedback-and-abstention.model-tests.json](models/03-quality-feedback-and-abstention.model-tests.json)

## Source Paper

- `papers/address-machine-translation-theory-ja-v1.md`
