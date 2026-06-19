# Session Summary — 2026-06-18/19

Grounded audit → remediation → feature build for the ClaudeSkillCollection marketplace.
Marketplace grew **9 → 12 plugins**. All work verified with real tests; nothing claimed
done without evidence.

## Accomplished

### Audit (issues #25, #23, #44)
- Re-verified #25 (15 findings) and #23 (12 doc findings) — all were still open since March.
- Opened **#44** with 8 newly-found bugs; an ultracode 53-agent adversarial pass confirmed
  40/43 and corrected several severities.

### Bug fixes (all verified)
- **Extractors:** unified cache path (extract↔chunk↔query now share `~/.claude-cache/{type}`);
  vendored `smart_cache.py` into each plugin (no more install-time `ModuleNotFoundError`);
  removed phantom `pandas` dep; fixed xlsx `summary` KeyError. (#44 N1/N2/N4/N5)
- **plugin-security-checker:** `psutil` made optional + listed (#44 N3); report generators
  now use script-relative paths (#44 N7); **XSS fixed** in all report generators —
  `html.escape`/`autoescape=True` (#25 H1/H2/H3, #44 N6); `demo_learning.py` `__main__`
  guard (#25 H5).
- **Misc:** jinja2 `requirements.txt` + guard (#25 C2); SKILL.md frontmatter on 6 files +
  created for 4 root plugins (#25 C5/H4); gdpr encoding (#44 N8); docx version (#25 M1);
  SRB version drift 1.0.1→1.2.0 (#23); CLAUDE.md hardcoded paths + "license required"
  correction (#23).

### Scanner engine reconciliation (#44 / Phase 3)
- `scan_plugin.py` (documented entry) now loads the **canonical** 99-pattern
  `dangerous_functions_expanded.json` (was the 35-pattern basic file) — verified it now
  catches expanded-only patterns. Removed stale `_v2`/`_v3`; generator writes a gitignored
  `.generated.json`.

### Supply-chain currency (npm + PyPI)
- `references/supply_chain_iocs.json` — **10 primary-source-verified incidents** (Shai-Hulud
  v1/v2, Nx s1ngularity, chalk/debug, Axios/plain-crypto-js, litellm/.pth, typosquats, etc.).
- New `_scan_supply_chain_iocs()` (Step 6/6) — verified detection on 5 malicious fixtures +
  **0 false positives** on clean plugins. IR playbook scenario + a new Software Supply Chain
  Security Policy made threat-current.

### New skill + 3 new plugins
- **`/sbom` skill** (`sbom-generator/`, loadable at `.claude/skills/sbom/`) — CycloneDX 1.6 +
  SPDX 2.3 from npm lockfiles, monorepo/license-expression handling, `--score/--scan/--sign`
  flows. Tested end-to-end (sbomqs NTIA 7.1/10). HTML manual at `sbom-generator/MANUAL.html`.
- **`security-memory-templates`** (#39), **`security-hooks`** (#35 + #41 ConfigChange audit
  trail), **`claude-guide`** registered (#23 M3) — all in marketplace.json.
- **`scripts/check_doc_drift.py`** (#42) — derives real counts, fails on drift.
- 6 larger feature issues (#34/#36/#37/#38/#40/#43) **designed** in
  `docs/feature-designs/2026-06-19-feature-designs.md`.

## Still open

1. **C1 — git history scrub (USER-OWNED, security-critical).** 16 sensitive financial/PII
   files were removed from HEAD + gitignored, but **52 blobs remain in git history** and the
   repo is **PUBLIC** (data exposed ~3.5 months → treat as compromised). The history rewrite
   was intentionally **not** done by Claude (irreversible public-history op; reserved for the
   user; the auto-mode classifier blocked it). Backup bundle: `/tmp/ClaudeSkillCollection-backup-20260619.bundle`.
   Run yourself:
   ```bash
   git-filter-repo --force --invert-paths \
     --path-glob 'docs/*.xlsm' --path-glob 'docs/*.xlsx' --path-glob 'docs/*.csv' \
     --path-glob 'docs/CCMv4.0.12+CAIQv4.0.3-Bundle_Generated-at_2024-06-03/*'
   git push origin --force --all
   ```
   Then **rotate any credentials** referenced in those files and make the **GDPR Art.33/34 /
   NDA notification** call (the repo ships a `gdpr-auditor` — optics matter).
2. **6 designed feature issues** (#34/#36/#37/#38/#40/#43) — specs ready, not built.
3. **Phase-4 tail already done** (policy clause); **self-SBOMs** generated for Python plugins
   as source SBOMs.

## Key decisions / context
- **Auto-commit:** a local `gitwatch` daemon (`com.user.gitwatch-manager`) auto-commits this
  repo every ~90s — user chose to leave it on. Work lands committed without a manual `git commit`.
- **CycloneDX 1.6 / SPDX 2.3** kept as defaults (1.7/3.0 rejected by Dependency-Track/Trivy/Grype
  as of 2026-06) — a deliberate consumer-compatibility choice.
- **Supply-chain scope = npm + PyPI** (user decision).
- Full plans: `docs/plans/2026-06-18-NEXT-STEPS.md` (execution), `2026-06-18-REVISION-ultracode.md`
  (corrections), `2026-06-18-audit-supplychain-sbom-plan.md` (original).
