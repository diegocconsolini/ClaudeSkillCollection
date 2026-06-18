---
name: sbom-generator
description: Generates a multi-stack SBOM (CycloneDX + SPDX) for a target project using zero-dependency / ephemeral-runner tooling, with optional quality scoring, vulnerability scan, VEX, and signing.
trigger: When the user wants a Software Bill of Materials, dependency inventory, supply-chain manifest, CycloneDX/SPDX output, or to check/scan/sign a project's dependencies.
tools: [Bash, Read, Write, Grep, Glob]
---

# SBOM Generator — agent procedure

You generate a Software Bill of Materials for a target project **without adding any
dependency to it**. Always consult `references/sbom-knowledge.md` for the verified
facts (formats, per-stack tools, regulatory, VEX, signing). Never improvise a fact that
the knowledge pack covers.

## Guardrails (enforce every time)

- **Confirm the target repo with the user before running anything.** One repo at a time.
- **Never run `npm install`** or any command that modifies the target's manifest/lockfile.
- **Never guess** the stack — detect it from files you actually read.
- Write outputs only into `<target>/sbom/`. Don't commit unless asked.
- `--scan` / `--sign` reach the network — state that and get an explicit OK first.

## Step 1 — Detect the stack (read, don't assume)

Glob/inspect the target root for manifests and lockfiles:

- `package-lock.json` (npm, lockfileVersion ≥ 2) → **npm path** (Step 2a)
- `pnpm-lock.yaml` / `yarn.lock` / `package.json` with no npm lock → **Syft path** (Step 2b)
- `pyproject.toml` / `poetry.lock` / `requirements.txt` → **Python** (Step 2c)
- `go.mod` + `go.sum` → **Go** (Step 2c)
- `Cargo.toml` + `Cargo.lock` → **Rust** (Step 2c, note the spec-1.5 cap)
- `pom.xml` / `build.gradle` → **Java** (Step 2c)
- `*.csproj` / `*.sln` → **.NET** (Step 2c)
- a Dockerfile / image reference, or multiple of the above → **Syft / cdxgen** (Step 2b)

If several stacks are present, say so and generate one SBOM per stack (or use Syft/cdxgen
for a merged polyglot SBOM). Report exactly what you found — do not promise coverage you
can't produce.

## Step 2a — npm (zero-dependency, preferred)

The vendored `scripts/generate-sbom.mjs` reads `package-lock.json` directly (only
`node:` builtins). Point it at any target project with **`--root <target>`** — no need
to copy the script in first:

```bash
# reproducible timestamp = clean re-run diffs; runs from anywhere:
SBOM_TIMESTAMP="$(date -u +%Y-%m-%dT00:00:00Z)" \
  node /path/to/sbom-generator/scripts/generate-sbom.mjs \
  --root <target> --out-dir <target>/sbom
# → <target>/sbom/bom.cdx.json (CycloneDX 1.6) + bom.spdx.json (SPDX 2.3)
# flags: --root DIR (target project), --format cyclonedx|spdx|both (default both),
#        --out-dir DIR, --out FILE (cdx only)
```

Requires `node`. Verified against a real 787-component project (CycloneDX 1.6 + SPDX 2.3,
reproducible bytes). If `lockfileVersion < 2`, the script exits with a clear message —
fall back to `npx -y @cyclonedx/cyclonedx-npm` (ephemeral) or Syft.

## Step 2b — Syft (pnpm/yarn/containers/polyglot)

```bash
# filesystem:
syft dir:<target> -o cyclonedx-json=sbom/bom.cdx.json -o spdx-json=sbom/bom.spdx.json
# container image:
syft <image>@<digest> -o cyclonedx-json=sbom/bom.cdx.json
```

If `syft` isn't installed, offer the ephemeral install
(`curl -sSfL https://get.anchore.io/syft | sh -s -- -b <dir>`) and confirm before running.

## Step 2c — other stacks (ephemeral runners)

Use the exact command for the detected stack from knowledge-pack §4 (Python `pipx run
cyclonedx-bom`, Go `go run …cyclonedx-gomod@latest`, Rust `cargo cyclonedx`, Maven
plugin, .NET `dotnet CycloneDX`). These fetch the tool ephemerally and add nothing to
the project manifest. For Rust, note the spec-1.5 cap and offer a Syft convert to 1.6 if
a consumer needs it.

## Step 3 — Quality score (on `--score`)

```bash
docker run --rm -v "$(pwd)":/app ghcr.io/interlynk-io/sbomqs:latest score /app/sbom/bom.cdx.json
```

Report the 0–10 score; **flag if < 7.0**. Optionally run the NTIA conformance check
(`pipx run ntia-conformance-checker` on the SPDX file). Summarize any missing NTIA-7
fields (supplier, hashes, license, transitive coverage).

## Step 4 — Vulnerability scan (on `--scan`, networked — confirm first)

```bash
grype sbom:sbom/bom.cdx.json          # or: osv-scanner --sbom=sbom/bom.cdx.json
```

If findings exist, offer to draft an **OpenVEX** doc (knowledge-pack §6) marking
non-exploitable items `not_affected` with a justification, linked by purl.

## Step 5 — Sign (on `--sign`, networked — confirm first)

```bash
# standalone SBOM file (blob), cosign v3, keyless/OIDC is default in CI:
cosign attest-blob --predicate sbom/bom.cdx.json --type cyclonedx sbom/bom.cdx.json
```

## Step 6 — Report

Tell the user: which stack(s) were detected, which generator ran, the component counts
(runtime/dev), the output paths, the quality score if requested, any vuln findings, and
**any gap** (a stack you couldn't cover, a tool that wasn't available, transitive deps a
source-SBOM can't see). Never imply completeness you didn't achieve — if the SBOM is
direct-deps-only, label it so (CISA "Known Unknowns").

## Self-SBOM note

This marketplace's own plugins (npm or Python) can be inventoried with this skill — a
good dogfooding/dependency-hygiene step that directly supports the supply-chain currency
goal in `docs/plans/2026-06-18-audit-supplychain-sbom-plan.md`.
