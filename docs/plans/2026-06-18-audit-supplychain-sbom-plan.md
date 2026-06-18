# ClaudeSkillCollection — Grounded Audit, Supply-Chain Currency & SBOM Skill Plan

**Date:** 2026-06-18
**Phase:** Exploratory / planning only — **no plugin code was edited.**
**Method:** Direct file reads + `grep`/`git`/`gh`; 5 parallel deep-audits; 2 research streams (SBOM deep-research workflow, recent-incident search). Every claim below was independently reproduced. Items I could **not** verify are explicitly flagged.

---

## 0. TL;DR

1. **Audit:** GitHub issues #25 (15 findings) and #23 (12 doc findings) are **all still unfixed** since March. I re-verified each and opened **#44** for **8 new bugs** the old audits missed. Most urgent is **not** code — it's **#25 C1: 16 sensitive financial files still git-tracked in a PUBLIC repo**.
2. **Supply-chain currency (new user requirement):** the security plugins are **out of date** on the 2024–2026 supply-chain/npm threat wave. `plugin-security-checker` lists 200+ generic CVEs but references **none** of xz-utils, Shai-Hulud, s1ngularity/Nx, chalk/debug, Trusted Publishing, sigstore, or npm v12 script-blocking. Per-skill update plan in §2.
3. **SBOM skill:** plan-only this turn. It should **wrap the existing zero-dep toolkit** at `_workspace/sbom-toolkit/`, not reinvent it, and add the orchestration/quality/scan/sign layers the toolkit itself names as gaps. Design in §3. **Location decision deferred to you** (§3.6).

---

## 1. Audit status (grounded re-verification)

### 1.1 Issues #25 / #23 — all findings reproduce
Posted dated re-verification comments to both. Summary:

- **#25 (5 Critical / 7 High / 3 Medium):** every one still present on `main`.
  - **C1 — live data exposure (highest priority of the whole engagement).** `gh repo view` → `visibility: PUBLIC`; `git ls-files 'docs/*.xlsm' 'docs/*.xlsx' 'docs/*.csv'` → **16 files** (AOP24/25/26 IT financials, HCLTech pricing sheet, CONTRACTING TRACKER, ABM employee activity log, AOP2024 Cyber details). Open since 2026-03-04. Needs history scrub (`git filter-repo`/BFG) + secret rotation + `.gitignore`, and **the repo arguably should go private** while that happens.
  - C2 jinja2 hard import + no requirements.txt; C3/C4 desktop skills declare missing files; C5 three SKILL.md lack frontmatter; H1/H2/H3 XSS in report generators; H4 missing SKILL.md; H5 demo no `__main__` guard; H6 cyber-policy deps; H7 "8 of 9" overclaim; M1 docx version mismatch; M2 stale version comment; M3 claude-guide unregistered.
- **#23 (docs):** hardcoded `/home/diegocc` ×3 in CLAUDE.md, SRB version split (plugin.json 1.0.1 vs version.json/marketplace 1.2.0), README missing a desktop-skills section, empty `wiki/`, and the `license`-is-required misconception (confirmed false against current docs).

### 1.2 New bugs — issue #44 (8, all independently verified)
| # | Sev | Where | Bug |
|---|-----|-------|-----|
| N1 | High | all 3 extractors | extract writes `~/.claude-cache/{type}/` but chunk/query read legacy `~/.claude-{type}-cache/` (6 files) → pipeline severed |
| N2 | High | extractors | `shared/smart_cache.py` never bundled (`parent.parent.parent/shared` import hack) → ModuleNotFoundError on install |
| N3 | High | plugin-security-checker | `psutil` imported in core orchestrator, not in requirements.txt |
| N4 | Med | xlsx | phantom `pandas` hard dep (required, never used) |
| N5 | Med | xlsx | `summary` command KeyError on `content_preservation` (read, never written) |
| N6 | Med | security-report-builder | XSS also in the PDF generator (widens #25 H3; **no** `_escape_html` exists anywhere in SRB) |
| N7 | Med | plugin-security-checker | aggregate report generators use cwd-relative paths + count stray `plugin.json` as a scanned plugin |
| N8 | Low | gdpr-auditor | inconsistent file-read encoding → UnicodeDecodeError on binary inputs |

### 1.3 Feature issues #34–#43 — triaged
Commented on each with grounded feasibility. All ten target **real, currently-supported** Claude Code capabilities (Agent Teams, `http`/`ConfigChange` hooks, MCP-in-plugins, worktree isolation, userConfig, output styles, channels). Recommendation: **sequence them after #44 + #25 C1** — most would orchestrate plugins that don't currently run clean. Best early wins: **#39** (memory templates, self-contained), **#41** (ConfigChange audit trail, real event), **#42** (wiki auto-updater — directly kills the doc-drift class in #23).

### 1.4 Format/staleness verdict
Checked against **current (June 2026)** Claude Code docs: **no breaking spec drift.** `SKILL.md` naming, `agents` array, `.claude-plugin/` location all valid. `license` is **not** a required skill-frontmatter field. So the audit items are genuine bugs, not version rot. (One forward note: plugin-bundled **agents** may not declare `hooks`/`mcpServers`/`permissionMode` in v2.1.150+ — relevant to feature issues #35/#41, which must ship those as **plugin-level** config.)

---

## 2. Supply-chain currency — per-skill update plan

> **User requirement:** "all the skills need to be up to date with recent issues on supply chain and npm vulns."

### 2.1 The grounded gap
`plugin-security-checker` references CVEs from **CVE-2001-0507 → CVE-2025-9377** (200+), but a name search shows **zero** coverage of the incidents that define the current npm threat model:

| Recent threat (verified) | In repo? |
|---|---|
| xz-utils backdoor **CVE-2024-3094** (liblzma/sshd, "Jia Tan") | ❌ none |
| **Shai-Hulud** self-replicating npm worm (Sept 2025, `@ctrl/tinycolor`, 500+ pkgs) | ❌ none |
| **s1ngularity / Nx** CI-token theft (Aug 2025, GHSA-cxm3-wv7p-598c) | ❌ none |
| **chalk/debug/ansi-styles** maintainer-phish crypto-clipper (Sept 2025, ~2.6B wk dl) | ❌ none |
| Trusted Publishing / OIDC, npm provenance + **Sigstore** | ❌ none |
| npm v12 **`ignore-scripts` default-on** (July 2026), `min-release-age` | ❌ none |

It *does* already have generic `postinstall`/`preinstall`/`typosquat`/`wallet`/`clipper` patterns (good base) — they're just not tied to the named 2024–2026 campaigns or their IOCs.

> ⚠️ **Verification caveat:** the incident research returned several items dated **2026** (Axios RAT "GHSA-fw8c-xr5c-95f9", npm v12 July-2026 deadline, "Red Hat Miasma", "Mini Shai-Hulud"). Treat dates/IDs as **research-reported, not first-party-confirmed** until checked against GitHub Advisory DB / CISA directly before they're written into any plugin. The pre-2026 incidents (xz, Shai-Hulud Sept-2025, chalk/debug, s1ngularity) are well-corroborated.

### 2.2 What to update, per skill
- **plugin-security-checker (primary):**
  1. Add a **named-incident knowledge pack** (`references/supply_chain_incidents_2024_2026.json`) keyed by incident → packages, IOCs (the Shai-Hulud SHA256s, `support@npmjs.help` phish domain, `plain-crypto-js`), GHSA/CVE, detection signal. Verify each IOC against a primary source first.
  2. Promote the existing generic patterns into **scored detectors** for: postinstall/preinstall credential exfil, `eval()`/Function-constructor obfuscation, clipboard/Web3 wallet hooks, base64+HTTP-POST exfil, token-harvest env reads (`NPM_TOKEN`/`GH_TOKEN`).
  3. Add **lockfile/provenance posture checks**: missing `package-lock.json` integrity, no npm provenance/Sigstore attestation, no `ignore-scripts`, no `min-release-age`/cooldown.
  4. Refresh the CVE table top-end and the stale `# Version: 2.0.0` comment (#44 N3 / #25 M2).
- **incident-response-playbook-creator:** add a **"Dependency / Supply-Chain Compromise" scenario** (worm-style npm token theft, maintainer account takeover, CI-token exfil) — it currently has a generic "Supply Chain Attack" scenario; make it concrete with the Shai-Hulud/s1ngularity playbook (rotate npm+GH+cloud tokens from a clean machine, audit published versions, revoke OIDC).
- **cybersecurity-policy-generator:** add policy clauses for **npm/registry hardening** (mandatory 2FA/passkeys, Trusted Publishing/OIDC, `ignore-scripts`, dependency cooldown, SBOM-on-release) mapped to existing frameworks.
- **gdpr-auditor / extractors / chrome-optimizer:** not supply-chain scanners — but each should **ship its own SBOM** (dogfooding, §3) and pin/declare deps honestly (fixes #44 N3/N4, #25 M1).
- **The marketplace itself:** scope clarification — `plugin-security-checker` scans **Claude Code plugins**, not arbitrary npm trees. The supply-chain content should frame plugins as a *delivery vector* for these npm-style payloads (a plugin can ship a malicious `postinstall`), which is exactly its lane.

These updates are **content/detector work, plannable now, build later** — none require the deferred SBOM skill.

---

## 3. SBOM skill — design (plan only)

### 3.1 Hard constraint (grounded, non-negotiable)
A **zero-dependency, multi-stack SBOM toolkit already exists** at `/Users/diegocavalariconsolini/ClaudeCode/_workspace/sbom-toolkit/` (read in full):
- `generate-sbom.mjs` v1.1.0 — reads npm `package-lock.json` v2/v3 → **CycloneDX 1.6 + SPDX 2.3**, `node:`-only imports, purl encoding, SRI→hex hashes, dedup-by-purl, dev/runtime scope, reproducible `SBOM_TIMESTAMP`, diff-stable sort.
- `ROLLOUT-PLAYBOOK.md` — per-stack ephemeral-runner commands, verified repo inventory, CI drift-guard, per-repo checklist.
- **Workspace CLAUDE.md rule:** start at the toolkit README; never copy SBOM docs into a project; **never `npm install` to make an SBOM.**

→ The skill is an **orchestration wrapper**, not new SBOM logic.

### 3.2 What the deep-research adds (22/25 claims verified)
- **Formats:** emit **both** CycloneDX + SPDX (both NTIA- and CISA-endorsed). CycloneDX is now **v1.7** (ECMA-424, Oct 2025); **1.6 is fine** and what the toolkit emits. Mandatory CycloneDX top-level fields: `bomFormat`, `specVersion`. SPDX 2.3 vs 3.0 default is an **open question** (§3.5).
- **Minimum elements:** satisfy **NTIA's 7 per-component fields** (Supplier, Name, Version, Other IDs, Dependency Relationship, Author, Timestamp). CISA-2025 (**draft**, not binding) renames Depth→**Coverage** (all transitive, no min depth) and formalizes **Known Unknowns** — treat as forward-looking best practice.
- **Regulatory (verified):** US **OMB M-26-05 (Jan 23 2026) rescinded M-22-18/M-23-16** → SBOM is now an *optional* "on-request" contractual term, **not** a federal mandate. **EU CRA** in force Dec 10 2024; reporting obligations **Sep 11 2026**, main **Dec 11 2027**. (Refuted/❌: a specific "CISA-2025 11-field list", and "M-26-05 points to CISA-2025" — do **not** encode those.)
- **Per-stack canonical tools (ephemeral):** npm=`cyclonedx-npm` (wraps `npm-ls`, adds nothing); Python=`cyclonedx-py`/`cyclonedx-bom` (pipx); Go=`cyclonedx-gomod`; Rust=`cargo-cyclonedx` (**caps at spec 1.5, defaults 1.3** → normalize); Java=CycloneDX Maven/Gradle plugin; polyglot=`cdxgen`/ORT; containers/filesystem=**Syft** (also converts formats).
- **Quality / scan / sign:** score with **sbomqs** / SPDX **ntia-conformance-checker**; scan via **Grype/Trivy/OSV-Scanner**; layer **VEX** (OpenVEX or CSAF); sign/attest with **cosign**/in-toto/SLSA. (VEX-internals and signing command specifics were **not fully verified** — §3.5.)

### 3.3 Skill shape (proposed)
A guardrail-respecting orchestrator that, per target repo:
1. **Detect** stack(s) + lockfile type from the manifest (never guess — read it).
2. **Route** to the right generator: npm → the existing `generate-sbom.mjs`; other stacks → the playbook's ephemeral runner; pnpm/yarn/container → Syft/cdxgen (gap the toolkit names).
3. **Emit** CycloneDX + SPDX into `sbom/`, normalizing spec version (e.g. via Syft convert for Rust's 1.3).
4. **Score** with sbomqs and report against NTIA's 7 fields + Coverage/Known-Unknowns.
5. **(Optional) Scan** the SBOM (Grype/OSV) and **(optional) sign** (cosign) — opt-in, networked, asked first.
6. **Report** what ran, the component counts, gaps, and which artifact is authoritative.

**Honors the hard rules:** ask before touching a repo; one repo at a time; no `npm install`; ephemeral runners only; SBOMs live in `sbom/`.

### 3.4 Tie-in to the supply-chain requirement (§2)
The SBOM skill is the natural feeder for the supply-chain detectors: SBOM → Grype/OSV scan → VEX → (for this repo's own plugins) a **self-SBOM** of each plugin so the marketplace can prove its own dependency hygiene. This is the strongest answer to "be up to date": don't just *describe* supply-chain risk, **measure** it.

### 3.5 Open questions (must verify before building)
- SPDX **2.3 vs 3.0** default for a 2026 skill (deep-research left this open).
- VEX: **OpenVEX vs CSAF** interop + how a VEX statement links to SBOM components by purl.
- Signing: exact canonical `cosign attest --predicate sbom.json --type cyclonedx …` flow + SLSA level targeting.
- Re-confirm the **2026-dated incidents/GHSAs** from §2 against first-party advisories.
- sbomqs scoring methodology + a sensible **minimum score** to gate on.

### 3.6 Location — **decision deferred to you**
Three viable homes (you asked to decide after reviewing current skill docs; here are the grounded options):
- **(A) Marketplace plugin** `./sbom-generator/` registered in `marketplace.json` — fits the security/compliance theme; gets versioning + distribution; heavier.
- **(B) Standalone skill** (`SKILL.md`) like `claude-guide/` — lightest; invokable as `/sbom`; not distributed via the marketplace.
- **(C) Workspace-level** beside the existing toolkit in `_workspace/` — matches the "SBOM tooling is workspace-shared, lives outside any one repo" rule in the workspace CLAUDE.md, but then it's not part of *this* product.

My recommendation: **(B) now → (A) later.** Build it as a standalone skill that drives the existing toolkit (fast, low-risk, respects the no-reinvent rule), and promote it to a marketplace plugin once the core bugs (#44) are fixed and it has a self-SBOM story. But this is your call.

---

## 4. Suggested sequence (when the build phase starts)
1. **#25 C1** — scrub history, rotate secrets, `.gitignore docs/`, consider private. *(Before anything public-facing.)*
2. **#44 N1/N2/N3** — unbreak the extractors + scanner on install.
3. **XSS** (#25 H1/H2/H3 + #44 N6) — central `html.escape`, one report path.
4. **Supply-chain content** (§2) — incident knowledge pack + detectors + IR scenario + policy clauses.
5. **SBOM skill** (§3) — standalone, wrapping the toolkit; then self-SBOM every plugin.
6. **Docs/feature issues** (#23, #42/#39/#41) — auto-derive doc numbers; close the drift class.

*No code was changed in this phase. This document is the plan; each numbered item above is a separately approvable unit of work.*
