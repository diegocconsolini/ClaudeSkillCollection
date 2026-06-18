---
name: sbom
description: Generate standards-compliant SBOMs (CycloneDX 1.6 + SPDX 2.3) for a project across stacks (npm, Python, Go, Rust, Java, containers), with optional quality scoring, vulnerability scan, VEX, and signing. Adds zero dependencies to the target project. Use when the user asks for a software bill of materials, dependency inventory, supply-chain manifest, or CycloneDX/SPDX output.
argument-hint: "[path-to-project]"
metadata:
  skill-version: 0.2.0
  author: ClaudeSkillCollection
  license: MIT
---

# SBOM Generator Skill

Produce a **Software Bill of Materials** for a project without adding any dependency
to it. Wraps the workspace's zero-dependency generator (vendored at
`scripts/generate-sbom.mjs`) and the per-stack ephemeral-runner approach, and adds the
optional quality / scan / VEX / sign layers.

Grounded reference: [`references/sbom-knowledge.md`](references/sbom-knowledge.md).
Detailed agent procedure: [`agents/sbom-generator.md`](agents/sbom-generator.md).

## Usage

```
/sbom                 # SBOM for the current directory (auto-detect stack)
/sbom ./path/to/repo  # SBOM for a specific project
/sbom --score         # also run sbomqs quality scoring (gate ≥ 7.0)
/sbom --scan          # also run a vulnerability scan over the SBOM (Grype/OSV)
/sbom --sign          # also create a cosign attestation (asks first; networked)
```

## Hard rules (non-negotiable)

1. **Ask before touching a repo.** One repo at a time; show the plan first.
2. **Never `npm install`** (or any manifest-modifying install) to make an SBOM. Use the
   vendored lockfile reader for npm; **ephemeral runners** (`npx -y`, `pipx run`,
   `go run …@latest`, Docker) for everything else.
3. **Never guess** a project's stack/lockfile/scripts — read its manifest first.
4. SBOMs are written to the project's **`sbom/`** directory and kept out of its bundle.
5. `--scan` and `--sign` are **networked and opt-in** — confirm before running.

## What it emits

- `sbom/bom.cdx.json` — **CycloneDX 1.6**
- `sbom/bom.spdx.json` — **SPDX 2.3** (3.0 only on explicit request — breaking JSON-LD)

Both satisfy the **NTIA 7 minimum fields**. See the knowledge pack for formats,
per-stack tools, regulatory facts (US M-26-05 / EU CRA), VEX (OpenVEX), and signing
(cosign v3) — all verified 2026-06-18.

## Quick decision: which generator?

| Detected | Generator |
|---|---|
| npm `package-lock.json` (v2/v3) | vendored `scripts/generate-sbom.mjs` (zero-dep) |
| pnpm / yarn / no npm lockfile | Syft (`syft dir:.`) |
| Python / Go / Rust / Maven / .NET | per-stack ephemeral runner (knowledge pack §4) |
| container image / mixed repo | Syft / cdxgen |

Status: v0.2.0 — standalone skill (Option B), **made loadable** (2026-06-18).
- **Install:** the loadable copy lives at `.claude/skills/sbom/` (recognized location →
  invocable as `/sbom`). This directory (`sbom-generator/`) is the **tracked canonical
  source**; `.claude/` is gitignored, so re-copy after edits:
  `cp -r sbom-generator/{SKILL.md,agents,references,scripts} .claude/skills/sbom/`.
- **Format fixed:** `SKILL.md` (all caps), valid frontmatter (off-schema
  `invocation`/`version`/`author`/`license` removed; `name: sbom` drives `/sbom`).
- **npm path verified** against a real 787-component project (valid CycloneDX 1.6 + SPDX
  2.3, reproducible bytes); license **expressions** emit as `{expression}`; npm
  **workspaces** monorepos trigger an explicit under-report warning → route to Syft.
- Non-npm stacks rely on ephemeral tools that must be available/fetchable. Not in
  `marketplace.json` (standalone skill); promote to a plugin later if desired.
