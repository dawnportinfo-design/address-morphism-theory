# 7. AMT Morphism Chain

AMT represents address resolution as a chain:

```text
surface -> normalized -> candidates -> evidence -> referent -> PID -> view
```

Each edge is typed, context-indexed, and reversible only when the evidence and
privacy policy allow it. The chain makes it possible to audit where information
was gained, lost, compressed, or blocked.

Model hook: `formal/morphism-chain.ts`, `diagrams/amt-chain.mmd`.
