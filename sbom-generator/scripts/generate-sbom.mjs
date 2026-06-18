#!/usr/bin/env node
/**
 * generate-sbom.mjs — produce CycloneDX 1.6 + SPDX 2.3 SBOMs from package-lock.json.
 *
 * ┌─ VENDORED COPY ───────────────────────────────────────────────────────────┐
 * │ Canonical source: /_workspace/sbom-toolkit/generate-sbom.mjs (v1.1.0).     │
 * │ This is a self-contained copy bundled into the /sbom skill so the skill is │
 * │ portable. To re-sync after the canonical changes:                          │
 * │   cp ../../../_workspace/sbom-toolkit/generate-sbom.mjs scripts/            │
 * │ then re-add this header AND re-apply the one intentional divergence below.  │
 * │ DIVERGENCE: a `--root <dir>` flag (see below) lets the portable skill target │
 * │ any project. Everything else must stay identical to canonical.              │
 * └────────────────────────────────────────────────────────────────────────────┘
 *
 * Zero new dependencies (reads the lockfile directly), so it respects the
 * project rule against `npm install`. Reusable across npm projects in this
 * workspace. See docs/plans/2026-06-07-sbom-generation.md.
 *
 * Emits two standards-compliant documents from one lockfile read:
 *   - sbom/bom.cdx.json   (CycloneDX 1.6 — security-oriented, native VEX path)
 *   - sbom/bom.spdx.json  (SPDX 2.3 — ISO/IEC 5962 lineage, licensing recognition)
 *
 * Usage:
 *   node scripts/generate-sbom.mjs                 # writes both into sbom/
 *   node scripts/generate-sbom.mjs --format cyclonedx   # only CycloneDX
 *   node scripts/generate-sbom.mjs --format spdx        # only SPDX
 *   node scripts/generate-sbom.mjs --out-dir build/sbom # custom output dir
 *   node scripts/generate-sbom.mjs --out x.json    # (cyclonedx only) explicit path
 *   SBOM_TIMESTAMP=2026-06-07T00:00:00Z node scripts/generate-sbom.mjs   # reproducible
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function argValue(flag) {
  const i = process.argv.indexOf(flag);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : undefined;
}

// VENDORED-SKILL DIVERGENCE from canonical: accept an optional --root <dir> so the
// portable /sbom skill can point the generator at any target project without first
// copying the script into it. Defaults to the script's parent dir (canonical behavior),
// so existing `npm run sbom` usage is unchanged.
const root = argValue("--root")
  ? path.resolve(process.cwd(), argValue("--root"))
  : path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const format = (argValue("--format") ?? "both").toLowerCase();
if (!["both", "cyclonedx", "spdx"].includes(format)) {
  console.error(`Unknown --format "${format}" (expected: both | cyclonedx | spdx).`);
  process.exit(1);
}

const outDir = argValue("--out-dir")
  ? path.resolve(process.cwd(), argValue("--out-dir"))
  : path.join(root, "sbom");

// --out is honoured for the CycloneDX document only (back-compat with v1).
const cdxOutPath = argValue("--out")
  ? path.resolve(process.cwd(), argValue("--out"))
  : path.join(outDir, "bom.cdx.json");
const spdxOutPath = path.join(outDir, "bom.spdx.json");

const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const lock = JSON.parse(
  fs.readFileSync(path.join(root, "package-lock.json"), "utf8"),
);

if (!(lock.lockfileVersion >= 2) || !lock.packages) {
  console.error(
    "Unsupported lockfile: need lockfileVersion >= 2 with a `packages` map.",
  );
  process.exit(1);
}

// Single-package only: this zero-dep reader does NOT expand npm workspaces. If the root
// package.json declares `workspaces`, warn — workspace members will be under-reported and
// the caller should route to Syft/cdxgen instead. (Honors "never imply completeness".)
const rootPkgForWorkspaceCheck = JSON.parse(
  fs.readFileSync(path.join(root, "package.json"), "utf8"),
);
if (rootPkgForWorkspaceCheck.workspaces) {
  console.error(
    "WARNING: package.json declares `workspaces` — this reader inventories the root " +
    "project only and may under-report workspace members. For a complete monorepo SBOM, " +
    "use Syft (`syft dir:.`) or cdxgen instead.",
  );
}

const timestamp = process.env.SBOM_TIMESTAMP ?? new Date().toISOString();

/** Build a Package URL (purl) for an npm component, encoding the scope. */
function purl(name, version) {
  // pkg:npm/@scope%2Fname@version  (slash in scope is %2F per the purl spec)
  const encoded = name.startsWith("@")
    ? "%40" + name.slice(1).replaceAll("/", "%2F")
    : name;
  return `pkg:npm/${encoded}@${version}`;
}

/** Map a lockfile `integrity` (e.g. "sha512-...") to a CycloneDX hash entry. */
function hashes(integrity) {
  if (!integrity || typeof integrity !== "string") return undefined;
  const [algRaw, b64] = integrity.split("-");
  const alg = { sha512: "SHA-512", sha256: "SHA-256", sha1: "SHA-1" }[algRaw];
  if (!alg || !b64) return undefined;
  // CycloneDX expects hex; convert the base64 SRI digest to hex.
  const hex = Buffer.from(b64, "base64").toString("hex");
  return [{ alg, content: hex }];
}

// One normalized pass over the lockfile; both formats are built from `pkgs`.
// A package at the same (name, version) can appear at several install paths in
// the lockfile (e.g. `debug@3.2.7` nested under two parents). For a component
// inventory it is ONE component, so we dedupe by purl — this also keeps the
// CycloneDX `bom-ref` and SPDX `SPDXID` globally unique, which both specs
// require. If the same version is reached on both a prod and a dev path, the
// merged component counts as runtime (needed at runtime anywhere dominates).
const byPurl = new Map();

for (const [key, entry] of Object.entries(lock.packages)) {
  if (key === "" || !key.startsWith("node_modules/")) continue; // skip root + workspaces
  if (!entry.version) continue;
  const name = key.slice(key.lastIndexOf("node_modules/") + "node_modules/".length);
  const isDev = entry.dev === true;
  const p = purl(name, entry.version);
  const existing = byPurl.get(p);
  if (existing) {
    // Seen this exact version before: prefer the runtime classification.
    if (existing.isDev && !isDev) existing.isDev = false;
    continue;
  }
  byPurl.set(p, {
    name,
    version: entry.version,
    isDev,
    purl: p,
    integrity: entry.integrity,
    license: entry.license,
  });
}

const pkgs = [...byPurl.values()];
let prod = 0;
let dev = 0;
for (const p of pkgs) {
  if (p.isDev) dev++;
  else prod++;
}

// Stable ordering so re-runs produce a reviewable diff, not noise.
pkgs.sort((a, b) => (a.purl < b.purl ? -1 : a.purl > b.purl ? 1 : 0));

const rootName = pkg.name ?? "root";
const rootVersion = pkg.version ?? "0.0.0";
const rootPurl = purl(rootName, rootVersion);
const TOOL = "orizon-generate-sbom";
const TOOL_VERSION = "1.1.0";

// Spec versions are pinned for CONSUMER COMPATIBILITY, not because newer specs don't
// exist. As of 2026-06, CycloneDX 1.7 and SPDX 3.0.1 are released but Dependency-Track /
// Trivy / Grype still reject 1.7 and don't reliably ingest SPDX 3.x — so 1.6 / 2.3 are
// the broadest-consumed targets. Revisit when the major consumers accept the newer specs.
const CDX_SPEC_VERSION = "1.6";
const SPDX_SPEC_VERSION = "SPDX-2.3";

/** Normalize a lockfile `license` field into a CycloneDX licenses[] entry.
 *  A bare SPDX id → {license:{id}}; an SPDX expression (e.g. "MIT OR Apache-2.0") →
 *  {expression}; an object/array form is coerced to a string id when possible. */
function cdxLicenses(license) {
  if (!license) return undefined;
  const value = typeof license === "string" ? license : license.type ?? null;
  if (!value || typeof value !== "string") return undefined;
  const isExpression = /\s|\bOR\b|\bAND\b|\bWITH\b|[()]/.test(value);
  return isExpression ? [{ expression: value }] : [{ license: { id: value } }];
}

/* ---------------------------------- CycloneDX 1.6 ---------------------------- */

function buildCycloneDx() {
  const components = pkgs.map((p) => {
    const component = {
      type: "library",
      "bom-ref": p.purl,
      name: p.name,
      version: p.version,
      purl: p.purl,
      // CycloneDX scope: dev deps are not part of the runtime BOM.
      scope: p.isDev ? "excluded" : "required",
    };
    const h = hashes(p.integrity);
    if (h) component.hashes = h;
    const lic = cdxLicenses(p.license);
    if (lic) component.licenses = lic;
    return component;
  });

  return {
    bomFormat: "CycloneDX",
    specVersion: CDX_SPEC_VERSION,
    version: 1,
    metadata: {
      timestamp,
      tools: {
        components: [{ type: "application", name: TOOL, version: TOOL_VERSION }],
      },
      component: {
        type: "application",
        "bom-ref": rootPurl,
        name: rootName,
        version: rootVersion,
        purl: rootPurl,
      },
    },
    components,
  };
}

/* ------------------------------------ SPDX 2.3 ------------------------------- */

/** Make a valid SPDXID fragment: only letters, digits, '.' and '-' are allowed. */
function spdxId(name, version) {
  const safe = `${name}-${version}`.replace(/[^a-zA-Z0-9.-]/g, "-");
  return `SPDXRef-Package-${safe}`;
}

/** Map a lockfile SRI integrity to an SPDX checksum entry (hex digest). */
function spdxChecksums(integrity) {
  if (!integrity || typeof integrity !== "string") return undefined;
  const [algRaw, b64] = integrity.split("-");
  const algorithm = { sha512: "SHA512", sha256: "SHA256", sha1: "SHA1" }[algRaw];
  if (!algorithm || !b64) return undefined;
  return [{ algorithm, checksumValue: Buffer.from(b64, "base64").toString("hex") }];
}

function buildSpdx() {
  const rootSpdxId = spdxId(rootName, rootVersion);

  const packages = [
    {
      SPDXID: rootSpdxId,
      name: rootName,
      versionInfo: rootVersion,
      downloadLocation: "NOASSERTION",
      filesAnalyzed: false,
      licenseConcluded: "NOASSERTION",
      licenseDeclared: pkg.license ?? "NOASSERTION",
      copyrightText: "NOASSERTION",
      externalRefs: [
        {
          referenceCategory: "PACKAGE-MANAGER",
          referenceType: "purl",
          referenceLocator: rootPurl,
        },
      ],
    },
    ...pkgs.map((p) => {
      const entry = {
        SPDXID: spdxId(p.name, p.version),
        name: p.name,
        versionInfo: p.version,
        downloadLocation: `https://registry.npmjs.org/${p.name}/-/${p.name
          .split("/")
          .pop()}-${p.version}.tgz`,
        filesAnalyzed: false,
        licenseConcluded: "NOASSERTION",
        licenseDeclared: p.license ?? "NOASSERTION",
        copyrightText: "NOASSERTION",
        externalRefs: [
          {
            referenceCategory: "PACKAGE-MANAGER",
            referenceType: "purl",
            referenceLocator: p.purl,
          },
        ],
      };
      const sums = spdxChecksums(p.integrity);
      if (sums) entry.checksums = sums;
      return entry;
    }),
  ];

  const relationships = [
    {
      spdxElementId: "SPDXRef-DOCUMENT",
      relationshipType: "DESCRIBES",
      relatedSpdxElement: rootSpdxId,
    },
    ...pkgs.map((p) => ({
      spdxElementId: rootSpdxId,
      relationshipType: "DEPENDS_ON",
      relatedSpdxElement: spdxId(p.name, p.version),
    })),
  ];

  return {
    spdxVersion: SPDX_SPEC_VERSION,
    dataLicense: "CC0-1.0",
    SPDXID: "SPDXRef-DOCUMENT",
    name: `${rootName}@${rootVersion}`,
    // Deterministic, unique namespace — derived from name/version/timestamp so the
    // committed artifact stays reproducible (no random UUID / Date.now()).
    documentNamespace: `https://orizon.sh/spdx/${encodeURIComponent(
      rootName,
    )}-${rootVersion}-${timestamp}`,
    creationInfo: {
      created: timestamp,
      creators: [`Tool: ${TOOL}-${TOOL_VERSION}`],
      licenseListVersion: "3.22",
    },
    packages,
    relationships,
  };
}

/* ------------------------------------ emit ----------------------------------- */

fs.mkdirSync(outDir, { recursive: true });
const wrote = [];

if (format === "both" || format === "cyclonedx") {
  fs.writeFileSync(cdxOutPath, JSON.stringify(buildCycloneDx(), null, 2) + "\n");
  wrote.push(`${path.relative(process.cwd(), cdxOutPath)} (CycloneDX 1.6)`);
}
if (format === "both" || format === "spdx") {
  fs.writeFileSync(spdxOutPath, JSON.stringify(buildSpdx(), null, 2) + "\n");
  wrote.push(`${path.relative(process.cwd(), spdxOutPath)} (SPDX 2.3)`);
}

console.log(
  `Wrote ${wrote.join(" + ")} — ${pkgs.length} components (${prod} runtime, ${dev} dev).`,
);
