import * as esbuild from "esbuild";
import { rmSync, readdirSync, statSync } from "node:fs";

const outdir = "dist/bundle";
const openclawExternals = [
  "openclaw",
  "openclaw/*",
  "openclaw/plugin-sdk/*",
];

rmSync(outdir, { recursive: true, force: true });

await esbuild.build({
  entryPoints: ["index.ts", "setup-entry.ts"],
  outdir,
  bundle: true,
  splitting: true,
  platform: "node",
  target: "node22",
  format: "esm",
  sourcemap: false,
  logLevel: "info",
  external: openclawExternals,
  packages: "bundle",
});

let total = 0;
for (const file of readdirSync(outdir)) {
  const size = statSync(`${outdir}/${file}`).size;
  total += size;
  console.log(`  ${outdir}/${file} ${(size / 1024).toFixed(1)} KiB`);
}
console.log(`bundled ${outdir}/ total ${(total / 1024).toFixed(1)} KiB`);
