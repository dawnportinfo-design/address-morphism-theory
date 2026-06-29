const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');

const required = [
  'SUMMARY.md',
  'paper/00-frontmatter.md',
  'paper/01-introduction-registration-difficulty.md',
  'paper/02-address-basics-reference-compression-communication-history.md',
  'paper/03-registrable-entities.md',
  'paper/04-surface-address-expressions.md',
  'paper/05-formal-preliminaries.md',
  'paper/06-address-unresolvability-decision.md',
  'paper/07-amt-morphism-chain.md',
  'paper/08-candidate-generation-and-source-policy.md',
  'paper/09-clusters-and-address-equivalence-classes.md',
  'paper/10-unresolved-country-theory.md',
  'paper/11-safe-resolution-and-pid-issuance.md',
  'paper/12-history-graph-and-address-conservation.md',
  'paper/13-social-continuity.md',
  'paper/14-conflict-relative-optimality.md',
  'paper/15-address-compression-and-entropy.md',
  'paper/16-natural-cultural-geography-and-vertical-reference.md',
  'paper/17-evaluation-quality-and-reputation.md',
  'paper/18-amt-cryptographic-extension-boundary.md',
  'paper/19-pid-and-application-identifier-boundary.md',
  'paper/20-communication-registration-and-audit-model.md',
  'paper/21-verification-and-reproducibility.md',
  'paper/22-security-abuse-and-governance.md',
  'paper/23-benchmarks-and-comparison.md',
  'paper/24-case-studies.md',
  'paper/25-limitations.md',
  'paper/26-conclusion.md',
  'appendices/A-core-notation.md',
  'appendices/B-definitions-propositions-lemmas-theorems-corollaries.md',
  'appendices/C-counterexamples.md',
  'appendices/D-verification-map.md',
  'appendices/E-glossary.md',
  'appendices/F-japanese-international-paper-conversion-rules.md',
  'appendices/G-commutative-diagram-insertion-plan.md',
  'appendices/H-proof-appendix-basic-propositions.md',
  'formal/definitions.ts',
  'formal/morphism-chain.ts',
  'formal/equivalence-classes.ts',
  'formal/entropy.ts',
  'formal/history-graph.ts',
  'formal/unresolvability.ts',
  'formal/verification-map.ts',
  'diagrams/amt-chain.mmd',
  'diagrams/history-graph.mmd',
  'diagrams/pid-boundary.mmd',
  'diagrams/zk-boundary.mmd',
  'tests/morphism-chain.test.ts',
  'tests/equivalence-classes.test.ts',
  'tests/entropy.test.ts',
  'tests/unresolvability.test.ts',
];

const errors = [];

for (const relativePath of required) {
  const fullPath = path.join(root, relativePath);
  if (!fs.existsSync(fullPath)) {
    errors.push(`missing ${relativePath}`);
  }
}

const summary = fs.readFileSync(path.join(root, 'SUMMARY.md'), 'utf8');
for (const relativePath of required.filter(file => file.startsWith('paper/') || file.startsWith('appendices/') || file.startsWith('formal/'))) {
  if (!summary.includes(relativePath)) {
    errors.push(`SUMMARY.md does not link ${relativePath}`);
  }
}

for (const file of required.filter(file => file.startsWith('paper/') && file !== 'paper/00-frontmatter.md')) {
  const text = fs.readFileSync(path.join(root, file), 'utf8');
  if (!/Model hook:|Limitations|Conclusion/.test(text)) {
    errors.push(`${file} should declare a model hook or terminal chapter role`);
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`Formal AMT tree verified: ${required.length} required files.`);
