# Next-session prompt — ClaudeSkillCollection (2026-06-29)

Copy-paste this verbatim into a fresh session.

---

Continue work on the ClaudeSkillCollection marketplace.
Repo: `/Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection`
GitHub: `diegocconsolini/ClaudeSkillCollection`
Commit straight to main (standing choice). A local gitwatch daemon auto-commits ~90s but is **local-only (AUTO_PUSH=false) — NEVER touch it**.

## Step 0 — verify state before acting

Run all four; do not claim success without evidence:

```
gh issue list --state open
python3 scripts/check_doc_drift.py
git status && git log --oneline -5
```

Also confirm 13 plugins are present (one dir per plugin, each with `.claude-plugin/plugin.json`). If anything diverges from the state below, stop and reconcile before building.

**Expected state:** main in sync with origin (HEAD 8162c35). 13 marketplace plugins. doc-drift clean. Issues closed this past session: #40, #41, #35, #39.

## Priority 1 — BUILD #34 "Agent Teams Security Playbook" (14th plugin)

Design is **fully committed** at:
`docs/superpowers/specs/2026-06-29-agent-teams-security-playbook-design.md`

Three design decisions are **settled — do not reopen**:

1. **SCOPE:** ship all 3 swarm configurations — Security Audit Swarm (5 agents: dependencies scanner, static code analyzer, secrets detector, config reviewer, infrastructure auditor), Compliance Audit Swarm (4 agents: GDPR, ISO 27001, SOC 2, NIST CSF), Incident Response Swarm (3 agents: triage analyst, containment specialist, documentation lead).
2. **HOOKS:** ship real working hook scripts + a unittest (not inline doc snippets). Two hooks: `TeammateIdle` (exit 2 keeps a teammate working) and `TaskCompleted` (exit 2 prevents premature completion).
3. **GATE LOGIC:** `TaskCompleted` gate blocks (exit 2) unless a `scan_plugin.py --output JSON` scan artifact exists for the target, parses cleanly, and contains `summary.severity_counts`. File-based, testable, ties the gate to `plugin-security-checker`.

**Approved file structure:**

```
agent-teams-security-playbook/
  .claude-plugin/plugin.json            # skill-only manifest; name must equal dir name; author: Diego Consolini <diego@diegocon.nl>; NO $schema/category/requirements/scripts keys
  SKILL.md                              # 3 swarm configs + spawn prompts + best practices; frontmatter: name + description required
  scripts/
    teammate_idle_gate.sh               # TeammateIdle hook — exits 0 by default with a documented customization point (comment block); stdlib shell only
    task_completed_gate.py              # TaskCompleted hook — reads event payload from stdin; looks for scan artifact via SECURITY_SCAN_DIR env var (default: ~/.claude-cache/security-scans/); exits 0 (allow) or exit 2 (block) with message to stderr; stdlib only
    test_task_completed_gate.py         # 5 unittest cases: artifact missing→exit 2; artifact+valid→exit 0; artifact+unparseable→exit 2; artifact missing severity_counts→exit 2; opt-out env var set→exit 0
```

**Build sequence:**

1. Run `/writing-plans` skill on the spec file above to produce a concrete task list.
2. Run `/subagent-driven-development` to build the plugin (SKILL.md, 2 hook scripts + test, plugin.json).
3. Add marketplace entry in `.claude-plugin/marketplace.json` mirroring the `security-hooks` entry (may use `category`/`keywords`/`homepage`/`repository`/`license`).
4. Re-run `python3 scripts/check_doc_drift.py` — count must go 13 → 14 cleanly.
5. Close #34 on GitHub with evidence (link to commit + drift check output).

**Repo conventions that must hold:**
- `plugin.json` must NOT have keys: `$schema`, `category`, `requirements`, `scripts`.
- SKILL.md frontmatter: only `name` + `description` required; non-standard keys under `metadata:`.
- Zero third-party deps; stdlib only throughout.
- Do not hardcode plugin counts in any docs — `check_doc_drift.py` owns that.
- Agent Teams is experimental (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`); cannot be executed in this environment. Swarm configs are prose-validated by review; only hook scripts are executable + tested.

## Priority 2 — remaining feature builds (in order)

After #34 ships, work through:

- **#37** — worktree parallel scanner
- **#36** — compliance dashboard MCP
- **#43** — wiki content (needs #42 first)
- **#38** — voice integration (lowest priority)

**Note on #42 Wiki Auto-Updater:** it is **NOT built**. The feature-designs doc may label it as partially done via `check_doc_drift.py` — that is a stretch; a real wiki-updater skill does not exist. `./wiki` is just a README stub. Build #42 before #43.

## C1 follow-up (user's own tasks — remind them)

Three deliverables are waiting in `docs/security/` (gitignored):

1. **File the GitHub Support GC purge request** — old blobs are still SHA-retrievable until GitHub garbage-collects the history post-filter-repo.
2. **Run the credential-rotation checklist** — any secrets that may have been in the purged files.
3. **Take the GDPR Art.33/34 assessment to a DPO** — data was in a public repo; breach timeline and notification obligations need a qualified assessment.

Ask the user whether any of these have been completed before moving on.
