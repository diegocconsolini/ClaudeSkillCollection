# Next-Steps Plan — addressing all remaining work

**Date:** 2026-06-18 · **Status:** active execution plan · **Basis:** `2026-06-18-REVISION-ultracode.md` (corrections) + the audit issues (#25/#23/#44) + user decisions this session.

> **Decisions locked (2026-06-18):** XSS first · supply-chain scope = **npm + PyPI together** · C1 scrub/rotation/legal = **user handles outside this session** · gitwatch left running.

---

## Status legend
✅ done · 🔵 in progress · ⬜ queued · 🧍 user-owned (non-engineering)

---

## Phase 0 — already complete this session ✅
- ✅ **C1 working-tree remediation** — 16 sensitive `docs/` files `git rm --cached` + `.gitignore`'d.
- ✅ **`/sbom` skill** — built, made loadable (`.claude/skills/sbom/`, `SKILL.md`, valid frontmatter), hardened (license expressions, monorepo warning, `--root`), **tested end-to-end** (sbomqs NTIA 7.1/10), HTML manual.
- ✅ **#44 N1/N2/N3** — extractor cache pipeline unified, `smart_cache.py` vendored ×3, `psutil` optional + listed. All verified.

---

## Phase 1 — XSS remediation 🔵 (current)
Three independent sites, three mechanisms — **not** one shared fix (the revision corrected the v1 "central html.escape" oversimplification). User-controlled finding fields (`description`, `code_snippet`, `category`, `impact`, `recommendation`) from *scanned* plugins flow unescaped into reports.

| Site | File | Sinks | Fix | Grade |
|---|---|---|---|---|
| **A** | `plugin-security-checker/scripts/generate_complete_report.py` | L645/651/663/667/675 (`description`, `category/subcategory`, `impact`, `recommendation`, `code_snippet`) | Reuse `_escape_html()` — **already exists** at `generate_report.py:562` — wrap each sink | High |
| **A** | `plugin-security-checker/scripts/generate_html_report.py` | L474/477/498/501 (`name`, `verdict`) | Same helper | High |
| **B** | `security-report-builder/scripts/generators/html_generator.py` | `Environment(...)` L37 (no `autoescape`) + inline fallback L495/530/531/534 | `autoescape=True` on the Jinja env **and** escape the f-string fallback | High |
| **C** | `security-report-builder/scripts/generators/pdf_generator.py` (#44 N6) | L401/402 (`plugin`, `desc`) | Add an escape helper to SRB (none exists) + apply | Med* |

*\*Med: WeasyPrint executes no JS → impact is markup/link/CSS injection, not live script execution. Still real (broken layout, phishing links).*

**Approach:** centralize one `escape_html()` per codebase (PSC already has one; SRB needs one), apply at every user-controlled sink, leave numeric/enum fields alone.
**Verify:** feed a finding containing `<script>alert(1)</script>` and `<img src=x onerror=...>` through each generator; assert the output contains `&lt;script&gt;` not `<script>`.

---

## Phase 2 — remaining #44 / #25 small bugs ✅ DONE (2026-06-18)
All fixed + verified (compile + behavioral tests for N5/C2); posted to #44/#25.
- **#44 N4** — drop phantom `pandas` from `xlsx-smart-extractor` (`requirements.txt` + `check_dependencies()` `sys.exit`). *Reword: "enforced-but-unused", import is guarded.*
- **#44 N5** — `xlsx query_xlsx.py` `summary` `KeyError` on `content_preservation`: write it in `chunk_sheets.py` or `.get()` on read.
- **#44 N8** — `gdpr-auditor` encoding: add `encoding='utf-8', errors='ignore'` to `analyze_database_schema.py:~197`, `generate_audit_report.py:30`, `sync_versions.py`.
- **#25 C2** — add `incident-response-playbook-creator/requirements.txt` (`jinja2>=3.1`) + guard the import.
- **#25 C5** — add YAML frontmatter to the 3 `SKILL.md` lacking it (incident-response, pdf-smart-extractor, security-report-builder). *(Same class as the `/sbom` SKILL.md fix.)*
- **#25 M1/M2** — docx `python-docx` version match (M2 already fixed via the psutil requirements pass); align docx `requirements.txt` ≥1.1.0.

---

## Phase 3 — scanner-engine reconciliation ✅ DONE (2026-06-18)
**Resolved:** `scan_plugin.py` (documented entry) now loads `dangerous_functions_expanded.json`
(verified strict superset — 63 python patterns vs 14, + obfuscation/credentials sections), with a
graceful fallback to the basic file. Stale `_v2`/`_v3` removed (untracked; `_v3` was byte-identical
to canonical); `expand_patterns.py` now writes a gitignored `.generated.json` build artifact.
Verified: documented entry now catches expanded-only patterns (e.g. `ctypes.CDLL`) it previously
missed. **New IOCs now land in ONE canonical file** → Phase 4 unblocked.

### Original finding (for reference)
**Critical finding from the ultracode re-audit:** the real entrypoint `scan_plugin.py` loads `dangerous_functions.json`; the `IntelligentOrchestrator` loads `dangerous_functions_expanded.json` and is **never called by scan_plugin**. Any new detectors added to the orchestrator are **dead code**.
- **Decide the canonical engine** (likely wire `scan_plugin.py` → the orchestrator/expanded set, or land everything in `dangerous_functions.json`).
- Add a smoke test that runs `scan_plugin.py` on a known-malicious fixture and asserts the new patterns fire.

---

## Phase 4 — supply-chain currency (npm + PyPI) ✅ MOSTLY DONE (2026-06-19)
- ✅ **IOC knowledge pack** `references/supply_chain_iocs.json` — 10 incidents (6 npm + 4 PyPI), all primary-source-verified, regex detection signals, GHSA/CVE, severity.
- ✅ **Detectors wired** into `scan_plugin.py` (`_scan_supply_chain_iocs()`, Step 6/6) — matches package.json scripts/deps, file names, source content. Verified: 5 malicious fixtures detect with correct campaign + severity; clean plugin = 0 false positives; legit postinstall doesn't over-trigger.
- ✅ **IR scenario** enriched — "Supply Chain Attack" now has 13 technical / 6 behavioral indicators citing Shai-Hulud, Nx, chalk/debug, axios, litellm + a threat-intel-references block.
- ⬜ **Remaining:** cybersecurity-policy-generator clauses (npm/registry hardening: 2FA/passkeys, Trusted Publishing/OIDC, ignore-scripts, cooldown, SBOM-on-release) — scoped as a follow-up (new policy templates).

### Original scope notes
- **IOC knowledge pack** (`references/supply_chain_incidents_2024_2026.json`): primary-source-verified incidents — xz-utils CVE-2024-3094, Shai-Hulud 1.0/2.0, s1ngularity/Nx (GHSA-cxm3-wv7p-598c), chalk/debug clipper, Axios RAT (GHSA-fw8c-xr5c-95f9), Miasma — keyed by packages, IOCs (Shai-Hulud SHA256s, `npmjs.help` phish, `plain-crypto-js`), GHSA/CVE, detection signal.
- **npm detectors:** postinstall/preinstall credential-exfil, `eval`/Function-constructor obfuscation, clipboard/Web3 wallet hooks, base64+HTTP-POST exfil, token-harvest env reads.
- **PyPI/pip detectors:** `setup.py`/`pyproject` build-hook exec, sdist exec, `requirements.txt` typosquats, `pip-audit`/OSV.
- **Posture checks** (net-new code, not regex): missing lockfile integrity, no provenance/Sigstore, no `ignore-scripts`, no dependency cooldown.
- **IR scenario** in incident-response-playbook-creator: concrete "Dependency/Supply-Chain Compromise" (token theft, account takeover, CI exfil → rotate npm+GH+cloud from a clean machine).
- **Policy clauses** in cybersecurity-policy-generator: 2FA/passkeys, Trusted Publishing/OIDC, `ignore-scripts`, cooldown, SBOM-on-release.
- **Re-verify** the 2026-dated incident IDs against GitHub Advisory DB / CISA before writing them in.

---

## Phase 5 — SBOM skill follow-through ✅ PARTIAL (2026-06-19)
- ✅ Upstreamed `--root` into canonical `_workspace/sbom-toolkit/generate-sbom.mjs` (canonical now superset; vendored header updated — divergence resolved).
- ⬜ Self-SBOM the marketplace plugins (needs plugin `requirements.txt` pinning first) — deferred.

### Original notes
- **Self-SBOM the marketplace plugins** — but the plugins are Python with **unpinned** `requirements.txt`; pin first (also closes N3/N4), then smoke-test the `cyclonedx-py` path before claiming the milestone.
- **Upstream `--root`** into the canonical `_workspace/sbom-toolkit/generate-sbom.mjs`, then re-vendor (canonical = superset).
- Remaining low/nit script hardening from revision §D.6–D.7 (SPDX dev-dep filter, SRI length validation).

---

## Phase 6 — docs & feature issues ✅ DONE (#23) (2026-06-19)
Fixed: 3 `/home/diegocc` paths in CLAUDE.md → relative; SRB plugin.json 1.0.1 → 1.2.0 (drift
resolved); "`license` required" claim corrected + SKILL.md filename/location note added; README
gained a Claude Desktop Skills section; stale "53 pages" hardcodes removed; `wiki/README.md`
pointer added. Feature issues #34–#43 remain valid, sequenced later.
Also: added a threat-informed **Software Supply Chain Security Policy** to the policy generator
(52 policies now) — the Phase-4 policy-clause tail.

### Original notes
- **#23** doc fixes: remove `/home/diegocc` paths from CLAUDE.md, fix SRB version drift (plugin.json 1.0.1 → 1.2.0), correct "`license` required" claim, stale counts (53 pages / "8 of 9" / 425 KB), add the desktop-skills README section.
- **#42** (wiki auto-updater) would *derive* those numbers at build time → prevents the whole drift class. Good candidate.
- Triaged feature issues **#34–#43** remain valid; sequence after the bug/supply-chain work.

---

## 🧍 User-owned (outside this session)
- **C1 history scrub** — `git filter-repo`/BFG to purge the 16 files from history. *(Irreversible; coordinate with forks; GitHub Support to purge cached views.)*
- **C1 credential rotation** — assume the data was public ~3.5 months → rotate anything referenced.
- **C1 legal/privacy** — GDPR Art.33/34 assessment for the exposed employee `ABM-ActivityLog…csv`; HCLTech/NDA third-party exposure. *(Optics: the repo ships a `gdpr-auditor`.)*
- **Repo visibility** — decide whether to take the repo private while remediating.

---

## Execution order (this & next sessions)
1. 🔵 **Phase 1 — XSS** (3 sites, verified by payload test) ← now
2. ⬜ **Phase 2 — small bugs** (batch)
3. ⬜ **Phase 3 — engine reconcile** (unblocks 4)
4. ⬜ **Phase 4 — supply-chain npm + PyPI**
5. ⬜ **Phase 5 — SBOM follow-through**
6. ⬜ **Phase 6 — docs**

Each phase: ground in real files → edit → **verify with a concrete test** → update the relevant GH issue. No success claim without evidence.
