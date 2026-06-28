const { spawnSync } = require("node:child_process");
const path = require("node:path");
const process = require("node:process");

const ROOT = path.resolve(__dirname, "..");

const STEPS = [
  ["node", ["scripts/verify-repository-layout.cjs"]],
  ["python", ["scripts/verify_publication_safety.py", "--self-test"]],
  ["python", ["scripts/verify_publication_safety.py"]],
  ["python", ["scripts/verify_pdfs.py"]],
];

for (const [command, args] of STEPS) {
  const result = spawnSync(command, args, {
    cwd: ROOT,
    env: process.env,
    stdio: "inherit",
    shell: false,
  });

  if (result.error) {
    console.error(result.error);
    process.exit(1);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

console.log("Address Morphism Theory repository verified.");
