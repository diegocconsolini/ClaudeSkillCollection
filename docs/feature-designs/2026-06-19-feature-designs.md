# Feature designs — issues #34, #36, #37, #38, #40, #43

Status of the 10 open feature issues (2026-06-19):

| Issue | Status |
|---|---|
| #35 HTTP Hooks Collection | ✅ **built** → `security-hooks/` plugin |
| #41 ConfigChange Hook Monitor | ✅ **built** → `security-hooks/` (ConfigChange audit-trail hook + script) |
| #39 Auto-Memory Security Patterns | ✅ **built** → `security-memory-templates/` plugin |
| #42 Wiki Auto-Updater | ✅ **core built** → `scripts/check_doc_drift.py` (derives real counts, flags drift) |
| #34, #36, #37, #38, #40, #43 | 📐 **designed below** (each a concrete, buildable spec) |

All six below target real, currently-supported Claude Code capabilities (verified against
mid-2026 docs). They are designed but not built to avoid half-implementations; each is an
independent unit of work.

---

## #34 — Agent Teams Security Playbook (multi-agent audit swarm)
**Capability:** Agent Teams / parallel subagents (real). **Shape:** a skill that fans out
specialized reviewers (dangerous-functions, supply-chain IOCs, credential-scan, schema,
permissions) over a target plugin in parallel, then an adversarial verifier kills false
positives, then a synthesizer merges. **Reuse:** wraps `scan_plugin.py` + the IOC pack as
the per-lens tools. **Build:** a `Workflow`-style orchestration doc + a `/audit-swarm`
skill that dispatches the lenses and dedupes. **Effort:** M.

## #36 — Compliance Dashboard Generator (interactive MCP Apps UI)
**Capability:** plugin-bundled MCP servers + MCP Apps UI (real). **Shape:** an MCP server
that ingests scan results (`archive_scan_results/*.json`) + SBOMs and serves an interactive
HTML dashboard (risk heatmap, framework coverage, finding drill-down). **Caveat:** the
report generators feeding it must stay escaped (done in this session). **Build:** stdio MCP
server in `compliance-dashboard/` + an HTML template. **Effort:** L.

## #37 — Worktree Parallel Security Scanner
**Capability:** git worktree isolation + parallel agents (real; WorktreeCreate/Remove hooks
exist). **Shape:** scan N plugins/marketplaces concurrently, each in an isolated worktree,
aggregate results. **Reuse:** `scan_plugin.py` per worktree. **Build:** a `/scan-fleet`
skill that lists targets, spawns isolated scans, merges. **Depends on:** scanner imports
cleanly (fixed this session — #44 N3). **Effort:** M.

## #38 — Voice-Driven Security Audit Workflow
**Capability:** voice input in the Claude ecosystem (real, but thin). **Shape:** a UX layer
mapping spoken commands ("scan this plugin", "show critical findings") to the existing scan
+ report skills. **Assessment:** lowest ROI of the set — mostly a command-mapping convenience
over deterministic skills; hardest to test. **Recommendation:** lowest priority. **Effort:** S–M.

## #40 — Batch Security Migration Skill (large-scale fixes)
**Capability:** subagent fan-out + worktree isolation (real). **Shape:** apply a fix across
many files/repos (e.g. add `html.escape` at every report sink, or `encoding='utf-8'` to
every open()) with per-item isolation + verification. **Dogfood target:** this session's
own fixes (cache-path drift across 6 files, encoding flags) were exactly this shape. **Build:**
a `/batch-fix` skill that takes a transform + a file-list and verifies each. **Effort:** M.

## #43 — Update Wiki for New Claude Code Features
**Capability:** documentation task (no new capability). **Shape:** a content pass adding
wiki pages for Agent Teams, ConfigChange/HTTP hooks, output styles, userConfig, channels —
all confirmed real in mid-2026. **Best done after #42** so counts are auto-derived rather
than hand-maintained. **Effort:** S (content), but needs the GitHub wiki checkout.

---

**Sequencing recommendation:** #40 (batch-fix, reusable for everything else) → #34/#37
(the orchestration pair) → #36 (dashboard, the richest) → #43 (wiki content) → #38 (voice,
lowest priority). Each can be built independently; none blocks the others except #43 ⇽ #42.
