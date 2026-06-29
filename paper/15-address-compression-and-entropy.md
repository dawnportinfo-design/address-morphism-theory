# 15. Address Compression And Entropy

Address expressions compress information. A good identifier reduces uncertainty
about the referent without leaking more private detail than necessary.

AMT uses entropy as a way to reason about ambiguity reduction, privacy leakage,
and the cost of over-compression.

Model hook: `formal/entropy.ts`, `tests/entropy.test.ts`.
