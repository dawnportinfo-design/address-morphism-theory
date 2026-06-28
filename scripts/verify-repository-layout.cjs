const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');

const requiredFiles = [
  'README.md',
  'LICENSE',
  'package.json',
  'REPOSITORY_SPLIT.md',
  'chapters/README.md',
  'chapters/index.json',
  'papers/address-morphism-theory-formal-core.tex',
  'papers/address-morphism-theory-full-paper-en-v3.md',
  'papers/address-morphism-theory-ja-v1-master.md',
  'papers/address-morphism-theory-ii-zero-knowledge-address-predicates.md',
  'verification/repository-content-gap-audit.md',
  'verification/main5-formal-additions.md',
  'verification/address-morphism-executable-expectations.md',
  'verification/s-priority-verification-feasibility.md',
  'verification/s-priority-verification-plan.json',
  'verification/s-priority-decomposition-gate.json',
  'verification/s-priority-decomposition-verification.md',
  'scripts/verify_amt_executable_model.py',
  'scripts/verify_chapter_index.py',
  'scripts/verify_predicate_dsl.py',
  'scripts/verify_s_priority_plan.py',
  'scripts/verify_s_priority_decomposition.py',
  'scripts/build_address_morphism_full_pdfs.cjs',
];

const forbiddenPatterns = [
  /BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY/i,
  /witness\.wtns/i,
  /rawAddress\s*:/i,
  /recipient\s*:/i,
];

const errors = [];

for (const relativePath of requiredFiles) {
  if (!fs.existsSync(path.join(root, relativePath))) {
    errors.push(`missing required file: ${relativePath}`);
  }
}

for (const topLevel of ['chapters', 'papers', 'notes', 'verification', 'scripts', 'src']) {
  const directory = path.join(root, topLevel);
  if (!fs.existsSync(directory) || !fs.statSync(directory).isDirectory()) {
    errors.push(`missing directory: ${topLevel}`);
  }
}

function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      if (['.git', 'node_modules', 'output'].includes(entry.name)) continue;
      walk(fullPath);
    } else if (entry.isFile() && /\.(md|tex|js|cjs|json|py|ps1)$/i.test(entry.name)) {
      const text = fs.readFileSync(fullPath, 'utf8');
      for (const pattern of forbiddenPatterns) {
        if (pattern.test(text)) {
          errors.push(`forbidden private-material pattern ${pattern} in ${path.relative(root, fullPath)}`);
        }
      }
    }
  }
}

walk(root);

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log('Address Morphism Theory repository layout verified.');
