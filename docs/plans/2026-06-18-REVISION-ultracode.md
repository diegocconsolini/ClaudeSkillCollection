# REVISION (ultracode re-plan) — supersedes parts of `2026-06-18-audit-supplychain-sbom-plan.md`

**Date:** 2026-06-18 · **Status:** decision-ready · **Method:** 53-agent adversarial workflow (40/43 findings red-team-confirmed against actual files) + 4 primary-source research threads + a dedicated read of the **current Claude skills docs**.
**Supersedes:** original plan §2.1, §2.2, §3.2–§3.7, §4, and the "no code was edited" framing.

> Two facts I missed in v1, both **independently re-verified by me** (not just agent-asserted):
> 1. **A `gitwatch` daemon auto-commits this repo (`com.user.gitwatch-manager`, PID 9462; repo listed in `~/.gitwatch/repos.list`).** Every recent commit is `Auto-commit: …`. → My `sbom-generator/` skill **and** the v1 plan/issue edits were **auto-committed to the PUBLIC repo, unreviewed** (`2fc895b`, `5017865`). I did not run `git commit`; the daemon did.
> 2. **The built skill does NOT load as-is** — per current Claude docs (verified §A below), wrong filename case, wrong location, and `invocation:` is a no-op.

---

## A. Claude skills docs — the built skill is non-loadable (NEW, highest-impact correction)

Read against current docs (`code.claude.com/docs/en/skills.md`):

| Issue | Current state | Required fix |
|---|---|---|
| **Filename case** | `sbom-generator/Skill.md` | Docs mandate **`SKILL.md`** (all caps), casing enforced. Rename. *(Note: `claude-guide/Skill.md` — the template I copied — is itself non-loadable for the same reason.)* |
| **Location** | dir at repo root | Standalone skills auto-load only from `~/.claude/skills/<name>/` or `.claude/skills/<name>/`. A repo-root dir **never loads**. Move it (or ship it inside a plugin's `skills/`). |
| **`/sbom` command** | `invocation: /sbom [path]` in frontmatter | `invocation` is **not a real field** (no-op). Command name = **directory name** in a recognized location → would be `/sbom-generator`, not `/sbom`. Rename dir to `sbom/` or accept `/sbom-generator`. |
| **Frontmatter** | `version`/`author`/`license`/`invocation` | Not recognized fields (silently ignored). Only `description` matters (+ optional `name`, `allowed-tools`, `disable-model-invocation`, `paths`, `context: fork`). Trim. *(Confirms #23 item 4: `license` is NOT required — repo CLAUDE.md is wrong.)* |
| **`agents/` subdir** | `agents/sbom-generator.md` | Inside a skill, `agents/` is **not special** — it's just a file that must be referenced from `SKILL.md`. The agent procedure should be linked, not assumed auto-loaded. |

**Decision needed (B-variants):** (B1) move to `~/.claude/skills/sbom/` (personal, all projects, not in this repo); (B2) `.claude/skills/sbom/` in this repo (project-scoped, loads + version-controlled); (B3) keep it as a plugin `skills/` dir (→ marketplace, namespaced `/sbom-generator:sbom`). **Recommend B2** — it actually loads, stays in the repo, and is the closest to what "a /sbom skill in this project" implied.

---

## B. Corrected facts (research overturned / sharpened)

1. **CycloneDX → STAY ON 1.6 (as built is correct).** 1.7 (ECMA-424, Oct 2025) is the current spec, but as of 2026-06 **Dependency-Track / Trivy / Grype reject 1.7** (`invalid specification version`). 1.6 = broadest consumption. Fix: state the *rationale* in the knowledge pack and make `"1.6"` a named constant (`generate-sbom.mjs:168` is a bare literal). Revisit Q4'26.
2. **SPDX → STAY ON 2.3 (as built is correct).** 3.0.1 finalized but not production-ingestible (Dependency-Track declined 3.x; Grype/Trivy ingestion immature). Keep with dated caveat.
3. **npm v12 wording — fix the polarity.** Confirmed (GitHub changelog 2026-06-09, July-2026 release) but the mechanism is **`allowScripts` defaulting OFF** (blocks pre/install/post scripts unless approved) — *effect* ≈ auto-`--ignore-scripts`. v1 plan §2.1 said "ignore-scripts default-on" (right effect, inverted flag). Still a **future date** → gate behind build-time re-verify.
4. **2026 incidents now PRIMARY-SOURCE CONFIRMED** (upgrade the v1 "research-reported" caveat): Axios RAT **GHSA-fw8c-xr5c-95f9** / `plain-crypto-js@4.2.1` (2026-03-31, Critical); **Shai-Hulud 2.0** preinstall worm (2025-11-24/26, 25k+ repos); **Miasma** — name is *Miasma*, not "Red Hat Miasma" (2026-06-01, 32 `@redhat-cloud-services` pkgs, `binding.gyp` preinstall); **chalk/debug** clipper (2025-09-08, `npmjs.help` phish, ~2.6B wk dl); **Trusted Publishing/OIDC GA** 2025-07-31. Nothing came back UNVERIFIED; drop the placeholder "Mini Shai-Hulud".
5. **Per-stack command corrections:** Python entrypoint is **`cyclonedx-py`** (pkg `cyclonedx-bom`); `--schema-version`→`--spec-version`, `--outfile`→`--output-file`; **unpinned deps are excluded-with-warnings** (this is the self-SBOM hole). Go `cyclonedx-gomod` defaults XML → pass `-json`, caps 1.6. Rust `cargo cyclonedx` caps 1.5/defaults 1.3 — **verify emitted `specVersion`, don't hardcode**. Syft normalize command (was named, never given): `syft convert bom.cdx.json -o cyclonedx-json@1.6=bom.cdx.json`. pnpm has **native `pnpm sbom`** (pnpm ≥11) — prefer over Syft. `.NET dotnet CycloneDX` needs networked `dotnet restore`.

---

## C. Audit-finding corrections (#44 / #25 re-grading)

- **N4** "phantom hard dep" → reword **"enforced-but-unused"** (import is guarded; the kill is `check_dependencies()` `sys.exit(1)`).
- **N6** keep distinct from H3, but **Med < High because WeasyPrint runs no JS** → markup/link/CSS injection, not live XSS.
- **N7** first half (cwd-relative paths) REAL; **second half ("stray plugin.json counted") NOT grounded → drop or re-verify.**
- **N8** "UnicodeDecodeError on binary inputs" **overstated** — it's caught (`analyze_database_schema.py:220-222`, clean exit). Reword to "inconsistent encoding"; fold in `generate_audit_report.py:30` + `sync_versions.py`.
- **N2** scope to the **Desktop ZIPs** (in-repo Claude Code plugins resolve `shared/` fine).
- **C2** attribute explicitly to **incident-response-playbook-creator** (not cyber-policy); cyber-policy H6 deps are guarded.
- **§4 "central html.escape, one report path" is impossible** — it spans **2 plugins, 4 sites, 3 mechanisms** (incl. a jinja `autoescape=True` path that `html.escape` can't fix). Split it.
- **§2 detector track targets the wrong engine** — `scan_plugin.py` (the real entrypoint) loads `dangerous_functions.json`; the orchestrator (loads `…_expanded.json`) is **never called by scan_plugin**. IOCs must land in the file scan_plugin actually reads, or they're dead code. **Reconcile the two engines first.**
- **§2 item 3 (lockfile/provenance posture) exceeds the regex engine** → net-new code in `scan_plugin.py`, not an IOC pack entry.
- **§2 is npm-only; PyPI is a real gap** (scanner already AST-scans Python; STIX encodes PyPI attacks). Decide: add a PyPI track OR explicitly declare "v1 = npm-only, Python deferred."

---

## D. Revised `/sbom` skill action list (ordered; supersedes §3.7 "next")

0. **[blocking] Make it loadable** — rename `Skill.md`→`SKILL.md`; move to `.claude/skills/sbom/`; drop off-schema frontmatter; reconcile the command name (`/sbom` needs dir `sbom/`). Without this the skill does nothing. *(§A)*
1. **[High] Monorepo silent drop** — vendored generator drops npm `workspaces` members (`generate-sbom.mjs:109`, reproduced: 2 dropped, no warning). Agent Step 1: detect `workspaces` → route to Syft/cdxgen or emit-and-warn. Violates the skill's own "never imply completeness."
2. **[High] Self-SBOM target wrong for THIS repo** — zero npm; plugins ship **unpinned `requirements.txt`** the vendored generator can't read. Agent:116 "npm or Python" → "Python (unpinned)". Make **dependency pinning a prerequisite** (also fixes #44 N3/N4); smoke-test `cyclonedx-py` before claiming the milestone.
3. **[Med] Container auth** — Syft image pull is networked + may need registry creds; agent confirms user is logged in (doesn't run `docker login`); keep `@digest`, warn bare tag = `latest`.
4. **[Med] Rust spec drift** — knowledge pack: keep ⚠, reword to "verify emitted specVersion & normalize"; add the literal `syft convert` command to both pack and agent.
5. **[Low] Upstream `--root`** into canonical `_workspace/sbom-toolkit/generate-sbom.mjs`, then re-vendor (canonical = superset; CLAUDE.md warns against drift).
6. **[Low] purl `.replace`→`.replaceAll`** (`:83`); **CycloneDX license `id` vs `expression`** (`:162`, detect SPDX expressions); **SPDX `DEPENDS_ON` includes dev deps** contradicting CycloneDX `excluded` (`:257-261`) — filter or document.
7. **[nit]** spec versions → named constants + WHY-1.6 rationale; explicit `lockfileVersion >= 2` guard (`:70`); optional SRI byte-length validation.

---

## E. Revised priority sequence (supersedes §4)

0. **STOP-THE-LINE (no approval gate):** **0a.** neutralize the gitwatch agent (`launchctl bootout gui/$(id -u)/com.user.gitwatch-manager`; remove this repo from `~/.gitwatch/repos.list`) so remediation isn't re-undone every ~90s. **0b.** make the repo **private**, then start the C1 incident.
1. **#25 C1 = data-breach incident, not a backlog item.** 16 files still tracked, public since 2026-03-04. History scrub (`git filter-repo`/BFG) + **secret/credential rotation** + `.gitignore docs/` + **legal/privacy track** (GDPR Art.33/34 on the employee `ABM-ActivityLog…csv`; HCLTech/NDA third-party data; **history rewrite ≠ remediation** — assume already cloned/cached).
2. **#44 N1/N2/N3** — unbreak extractors + scanner on install (N2 = Desktop-ZIP-scoped).
3. **XSS — split per plugin/mechanism:** (3a) plugin-security-checker f-strings; (3b) SRB `html_generator.py` → `autoescape=True` + f-string fallback; (3c) SRB `pdf_generator.py` f-strings (Med, WeasyPrint no-JS).
4. **Reconcile `scan_plugin.py` vs `intelligent_orchestrator.py`** (must precede §2, or detectors are dead code).
5. **Supply-chain content** — IOC pack (primary-source incidents from §B.4), promoted detectors, posture code in `scan_plugin.py`, IR scenario, policy clauses. **Decide npm-only vs +PyPI.**
6. **SBOM skill** — make loadable (D.0) + apply D-list; gate self-SBOM behind plugin pinning.
7. **Docs/feature issues** (#23, #42/#39/#41).

---

## F. Residual decisions for you (human-only)

1. **The auto-commit situation.** A daemon committed my skill + plan edits to the public repo unreviewed. Do you want gitwatch left on, or paused for this repo while we work? (It also makes any C1 fix futile until paused — F-blocking.)
2. **Git history rewrite on a public repo is irreversible + currently futile** (data public ~3.5 months → treat as compromised regardless). Accept exposure-happened and prioritize rotation+notification over rewrite optics? Coordinate with forks? Contact GitHub Support to purge cached views?
3. **Employee-data + third-party-NDA legal exposure** (not an engineering fix): does `ABM-ActivityLog…csv` trip a GDPR clock? Are HCLTech pricing / contracting disclosures NDA breaches? The repo ships a `gdpr-auditor` — optics matter.
4. **Sanction the already-built `sbom-generator/`** (it's committed + non-loadable): ratify + fix to load (D.0), or revert the commit and treat as draft?
5. **§2 scope:** npm-only vs +PyPI detector track — commit to a decision so it's not a silent gap.
6. **CLI/regulatory specifics drift** — npm v12 polarity/date, Rust caps, `cyclonedx-py` flags, `cosign v3` flow, `sbomqs ≥7.0` gate: keep behind the knowledge-pack `last-verified: 2026-06-18` line; re-confirm before quoting in any audit deliverable.
