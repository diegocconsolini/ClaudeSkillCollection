# Next-session prompt — ClaudeSkillCollection

Copy-paste this into the next session.

---

Continue work on the ClaudeSkillCollection marketplace
(/Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection).

Start by reading `docs/plans/2026-06-24-SESSION-SUMMARY.md` for full context. Last session
executed the **C1 git-history scrub** (3 filter-repo passes, removed the 16 spreadsheets +
.pbix + client PDFs + 5 "AOP26 HCL Cost Forecast" slide HTMLs that the original glob missed,
deleted the public `private` branch, hardened .gitignore) and **designed but did not build**
the #40 plugin.

Verify state first before acting: `gh issue list`, `python3 scripts/check_doc_drift.py`, and
that the 12 plugins still load. A local gitwatch daemon auto-commits this repo ~90s but is
**local-only (AUTO_PUSH=false) — NEVER touch it** (my standing instruction). Ground every
claim in real file reads/tests; no success claims without evidence.

## Priority 1 — finish #40 (paused at the spec-approval gate)

The spec is committed + pushed:
`docs/superpowers/specs/2026-06-22-batch-security-migration-design.md`. I still need to approve
it. Two open questions from the brainstorm:
- Recipe tiering OK? (secret-rotation + dependency-CVE-updates are marked 🔴 high-risk-manual.)
- Ship an `agents/*.md`, or skill-only? (spec says skill + script, no agent.)

Once I approve: writing-plans → build the 13th plugin `batch-security-migration`:
`SKILL.md` (7 `/batch` security recipes w/ safety tiers), `scripts/scan_diff.py` (before/after
`plugin-security-checker` diff, blocks on new HIGH+, `--report-only` flag) + its unittest,
`.claude-plugin/plugin.json`, and a `marketplace.json` entry mirroring `security-hooks`. Then
re-run `check_doc_drift.py` (count goes 12 → 13).

## Priority 2 — close already-built GitHub issues

#35, #39, #41, #42 are **built but still OPEN**; #25/#23/#44 fixes shipped. Close/update them on
GitHub so the issue list reflects reality.

## Priority 3 — remaining feature builds (order in docs/feature-designs/2026-06-19-feature-designs.md)

#34/#37 (orchestration pair) → #36 (dashboard) → #43 (wiki) → #38 (voice, lowest priority).

## C1 follow-up (MINE to do — not Claude's, but remind me)

C1 is code-complete but **exposure has not 100% ceased**. The 3 deliverables in `docs/security/`
(gitignored) are waiting on me: (1) file the **GitHub Support GC purge request** — old blobs
are still SHA-retrievable until GitHub garbage-collects; (2) run the **credential-rotation
checklist**; (3) take the **GDPR Art.33/34 assessment** to a DPO. Ask me whether I've done these.
