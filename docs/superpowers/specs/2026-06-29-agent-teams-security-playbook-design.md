# Agent Teams Security Playbook — Design / Spec

**Issue:** #34 (the 14th plugin in the ClaudeSkillCollection marketplace)
**Date:** 2026-06-29
**Status:** Design complete — ready to hand to the `superpowers:writing-plans` skill
**Repo:** `/Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection` (public GitHub: `diegocconsolini/ClaudeSkillCollection`)
**Plugin dir name:** `agent-teams-security-playbook` (the manifest `name` field MUST equal this directory name)

> This spec is **self-contained**. A fresh session with no memory of the brainstorm can build the plugin from this document alone. Every "still to specify" item is resolved concretely below — there are no TBDs or placeholders.

---

## 1. Goal

Ship a **knowledge/config skill plus a thin, testable hook core** that lets a Claude Code user run *Agent Teams* (Claude Code's experimental, disabled-by-default multi-agent swarm feature) for three security/compliance workflows **safely and repeatably**:

1. **Security Audit Swarm** — 5 specialist agents auditing a target plugin/repo.
2. **Compliance Audit Swarm** — 4 framework specialists (GDPR, ISO 27001, SOC 2, NIST CSF).
3. **Incident Response Swarm** — 3 agents (triage, containment, documentation).

The plugin delivers:

- A `SKILL.md` containing the **three swarm configurations** as copy-paste-ready prose: per-swarm agent rosters, spawn prompts, coordination/best-practice notes, and an explicit "experimental feature" warning.
- **Two real, working hook scripts** for Agent Teams events:
  - `teammate_idle_gate.sh` — handles the **TeammateIdle** event.
  - `task_completed_gate.py` — handles the **TaskCompleted** event and enforces a **security gate**.
- A **unittest** (`test_task_completed_gate.py`) proving the gate's exit-code logic, with five concrete cases.

The gate ties Agent Teams completion to `plugin-security-checker`: a security-audit task cannot be marked complete (exit 2 blocks it) unless a valid scan artifact exists for the target.

### Why this matters
Agent Teams runs multiple autonomous teammates in parallel. Without guardrails, a teammate can declare a security audit "done" before any scan actually ran, or idle prematurely. This plugin encodes the *configuration knowledge* (so users don't hand-build fragile swarm prompts) and provides *mechanical enforcement* (so "audit complete" provably means "a scan artifact exists").

---

## 2. Why a knowledge skill + testable hook core (NOT an orchestrator)

**Settled architecture decision.** This plugin is deliberately **not** a programmatic team spawner or runtime orchestrator. Reasons:

1. **Agent Teams is experimental and disabled-by-default.** It is enabled only via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and its API surface is unstable. **It cannot be run or exercised in this environment.** Any orchestrator we wrote would be unrunnable here, untestable, and at high risk of breaking when the experimental API changes.
2. **The valuable, durable artifact is the *configuration knowledge*** — which agents, with which prompts, in which order, with which coordination rules. That is exactly what a knowledge skill captures. Swarm configs are **prose, validated by human review**, because they cannot be executed in this environment.
3. **The one piece we *can* make mechanical and testable is the event-hook layer.** Hook scripts read a stdin payload and return an exit code — that contract is stable, pure, and unit-testable **without** running Agent Teams at all. So we invest engineering rigor exactly where it pays off: the hooks.
4. **This mirrors the shipped #40 `batch-security-migration` plugin** (recipe knowledge in `SKILL.md` + a real, tested `scan_diff.py` gate). Same proven shape: *prose recipes + a thin testable enforcement script*. Reusing that shape keeps the marketplace coherent and the review surface small.

**Boundary:** the skill teaches a human how to launch and run the swarms; the hooks mechanically enforce one safety invariant during a run. Neither spawns teammates, schedules work, or talks to the Agent Teams API.

---

## 3. The three settled design decisions (explicit, do not reopen)

These were approved by the user during brainstorming and are **settled**:

- **DECISION 1 — SCOPE (settled):** Ship **all three** swarm configurations:
  - **Security Audit Swarm** = 5 agents: *dependencies scanner, static code analyzer, secrets detector, config reviewer, infrastructure auditor*.
  - **Compliance Audit Swarm** = 4 agents: *GDPR specialist, ISO 27001 specialist, SOC 2 specialist, NIST CSF specialist*.
  - **Incident Response Swarm** = 3 agents: *triage analyst, containment specialist, documentation lead*.
- **DECISION 2 — HOOKS (settled):** Ship **real, working hook scripts plus a unittest** — not inline doc snippets. Two hooks:
  - **TeammateIdle** → `teammate_idle_gate.sh` (exit 2 keeps a teammate working).
  - **TaskCompleted** → `task_completed_gate.py` (exit 2 prevents premature completion).
- **DECISION 3 — GATE LOGIC (settled):** The **TaskCompleted** gate **blocks completion (exit 2) unless a scan artifact is present** — i.e. a `scan_plugin.py --output` JSON exists for the target *and* parses *and* contains a valid `summary.severity_counts`. The check is **file-based and testable**, tying the gate to `plugin-security-checker`.

---

## 4. Components

### 4.1 Directory structure (settled)

```
agent-teams-security-playbook/
├── .claude-plugin/
│   └── plugin.json                  # skill-only manifest, NO agents array
├── SKILL.md                         # 3 swarm configs + spawn prompts + best practices
└── scripts/
    ├── teammate_idle_gate.sh        # TeammateIdle hook (minimal shell; exit 2 = keep working)
    ├── task_completed_gate.py       # TaskCompleted hook (exit 2 unless scan artifact valid; stdlib only)
    └── test_task_completed_gate.py  # unittest for the gate's exit-code logic (5 cases)
```

No `agents/` directory. No `references/`. No third-party dependencies anywhere (stdlib + POSIX shell only).

---

### 4.2 `.claude-plugin/plugin.json`

A **skill-only** manifest. Mirrors the shipped `batch-security-migration` manifest exactly in shape.

**Hard rules (from CLAUDE.md):**
- MUST contain ONLY these keys: `name`, `version`, `description`, `author`, `keywords`.
- MUST NOT contain: `$schema`, `category`, `requirements`, `scripts`, or an `agents` array (this is a skill, not an agent plugin).
- `name` MUST equal the directory name `agent-teams-security-playbook`.
- `author` = `{ "name": "Diego Consolini", "email": "diego@diegocon.nl" }`.

**Exact content to ship:**

```json
{
  "name": "agent-teams-security-playbook",
  "version": "1.0.0",
  "description": "Playbook skill for Claude Code's experimental Agent Teams: three ready-to-run security swarm configurations (5-agent Security Audit, 4-agent Compliance Audit, 3-agent Incident Response) with copy-paste spawn prompts and coordination best practices, plus two real Agent Teams hooks — a TeammateIdle keep-working gate and a TaskCompleted gate that blocks 'audit complete' until a plugin-security-checker scan artifact exists.",
  "author": { "name": "Diego Consolini", "email": "diego@diegocon.nl" },
  "keywords": ["agent-teams", "swarm", "multi-agent", "security-audit", "compliance", "incident-response", "hooks", "teammateidle", "taskcompleted", "experimental"]
}
```

> Note: `version` lives in `plugin.json` (manifest convention used by every plugin here). In `SKILL.md` frontmatter, `version` instead goes under `metadata:` (see §4.3). These are two different files with two different conventions; both are correct.

---

### 4.3 `SKILL.md`

**Frontmatter rules (settled):**
- Only `name` + `description` are *required*. `license: MIT` is a repo convention. All non-standard keys (`version`, `author`) go under `metadata:`.
- `name` MUST equal the plugin directory name: `agent-teams-security-playbook`.
- `description` must be trigger-oriented ("Use when …") so the skill auto-activates correctly.

**Required frontmatter:**

```yaml
---
name: agent-teams-security-playbook
description: Use when running Claude Code's experimental Agent Teams for security work — set up a multi-agent swarm to audit a plugin/repo, run a compliance framework review, or coordinate incident response. Provides three ready-to-run swarm configurations (5-agent Security Audit, 4-agent Compliance Audit, 3-agent Incident Response) with copy-paste spawn prompts, coordination best practices, and two enforcement hooks (TeammateIdle keep-working, TaskCompleted scan-artifact gate).
license: MIT
metadata:
  version: 1.0.0
  author: Diego Consolini
---
```

**Body structure (required sections, in order):**

#### (A) Header + experimental warning (required, first thing after frontmatter)
- One-paragraph overview.
- A prominent warning block stating: Agent Teams is **experimental and disabled by default**; it must be enabled with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; behavior and APIs may change; **the swarm configs in this skill are prose validated by review, not executed in CI** (the build environment cannot run Agent Teams).

#### (B) Quick start (required)
- How to enable the feature (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
- How to pick a swarm.
- How to register the two hooks (point at `scripts/teammate_idle_gate.sh` for `TeammateIdle` and `scripts/task_completed_gate.py` for `TaskCompleted`), and the one env var the gate honors (`SECURITY_SCAN_DIR`, see §5).
- A one-line note: before launching a Security Audit Swarm, run `plugin-security-checker`'s `scan_plugin.py --output "$SECURITY_SCAN_DIR/<target>.json" <target>` so the TaskCompleted gate can pass.

#### (C) Swarm 1 — Security Audit Swarm (5 agents) (required)
For the swarm overall, document: **purpose**, **when to use**, **lead/coordination model** (one lead agent fans out to specialists, collects findings, blocks completion until the gate passes), and **expected output** (a consolidated findings list + a scan artifact at `$SECURITY_SCAN_DIR/<target>.json`).

Then, for **each of the 5 agents**, give a **spawn prompt**. Every spawn prompt MUST contain, concretely:
1. **Role line** — the agent's identity (e.g. "You are the Dependencies Scanner.").
2. **Scope** — exactly what files/areas it owns (so agents don't collide).
3. **Tooling/method** — what it should run or inspect (e.g. dependency manifests; for the lead, `plugin-security-checker`'s `scan_plugin.py`).
4. **Output contract** — the exact shape of findings it returns to the lead (severity + file + description + recommendation).
5. **Boundaries** — what it must NOT do (no fixes, read-only audit; do not mark the task complete itself — only the lead does, and only after the gate passes).
6. **Hand-off** — how/when it reports back to the lead.

The 5 agents and their owned scopes:
- **Dependencies scanner** — third-party dependency manifests (`package-lock.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`); flags known-vuln/abandoned/typosquat-shaped deps. (Recommend it surface SBOM via the workspace `/sbom` skill rather than installing anything.)
- **Static code analyzer** — source files; dangerous patterns (`eval`, `exec`, deserialization, command injection, path traversal).
- **Secrets detector** — all files; hardcoded credentials, tokens, private keys, high-entropy strings.
- **Config reviewer** — `plugin.json` / `marketplace.json` / settings / hooks config; permission overreach, forbidden manifest keys, suspicious hook commands.
- **Infrastructure auditor** — CI/CD, Dockerfiles, IaC, network/transport config; insecure transports, over-broad permissions, exposed services.

**Lead-agent prompt (required, in this swarm):** must instruct the lead to (a) spawn the 5 specialists, (b) collect their findings, (c) **run `scan_plugin.py --output "$SECURITY_SCAN_DIR/<target>.json" <target>` to produce the scan artifact**, and (d) only then attempt to mark the overall task complete — knowing the **TaskCompleted gate** will reject completion if the artifact is missing/invalid.

#### (D) Swarm 2 — Compliance Audit Swarm (4 agents) (required)
Same overall structure (purpose, when-to-use, coordination, output). One spawn prompt per framework specialist, each prompt containing the same six required elements as §C:
- **GDPR specialist** — data-subject rights, lawful basis, retention, DPIA triggers, cross-border transfer.
- **ISO 27001 specialist** — Annex A control coverage, ISMS evidence, risk treatment.
- **SOC 2 specialist** — Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy) evidence.
- **NIST CSF specialist** — Identify/Protect/Detect/Respond/Recover function coverage.

Output contract per agent: a mapped gap list (control/requirement → status → evidence/gap → recommendation). Note that the **TaskCompleted gate also applies** here if the compliance run targets a plugin/repo and `$SECURITY_SCAN_DIR/<target>.json` is the agreed artifact; if a given compliance task is *not* a scannable-target audit, it uses the documented opt-out (§5.4) so it isn't blocked.

#### (E) Swarm 3 — Incident Response Swarm (3 agents) (required)
Same structure. One spawn prompt per agent (six required elements each):
- **Triage analyst** — assess scope/severity, classify the incident, identify affected assets.
- **Containment specialist** — propose and document containment/isolation steps (propose, do not auto-execute destructive actions).
- **Documentation lead** — maintain the running incident timeline and the final report; this agent owns "task complete" and uses the documented opt-out (§5.4) when no scan artifact applies, OR points the gate at an IR evidence artifact if the team chooses to gate on one.

#### (F) Coordination best practices (required)
- Non-overlapping scopes (each agent owns a lane) to avoid duplicate work and write collisions.
- One lead per swarm owns final completion.
- Read-only by default for audit swarms (no fixes).
- How the two hooks change behavior at runtime (idle → keep working; completed → blocked unless artifact valid).
- Cost/parallelism caution: more teammates = more token spend.

#### (G) Hook setup reference (required)
- Exact event→script mapping (`TeammateIdle` → `scripts/teammate_idle_gate.sh`; `TaskCompleted` → `scripts/task_completed_gate.py`).
- That **exit code 2 is the blocking signal** for both events (idle: keep working; completed: reject completion); exit 0 allows.
- The `SECURITY_SCAN_DIR` convention and default (§5).
- The opt-out mechanism (§5.4).

---

### 4.4 `scripts/teammate_idle_gate.sh` — TeammateIdle hook

**Chosen minimal behavior (settled, no ambiguity):**

The script's **default behavior is to exit 0** (allow the teammate to go idle / do not force more work), and it contains **one clearly-commented customization point** where a user can opt in to "keep working" by exiting 2.

Rationale: forcing every idle teammate to keep working by default would create runaway loops and burn tokens — a bad default for a safety plugin. The *capability* (exit 2 keeps a teammate working) is the point of the hook and is fully wired and documented; the *default* is the safe one (exit 0). This is a deliberate, documented default, not a stub.

**Exact contract:**
- POSIX `sh`, executable (`chmod +x`), shebang `#!/usr/bin/env sh`.
- Reads the hook event payload from **stdin** (it may ignore the content in the default path; it must still drain stdin so the producer isn't blocked — e.g. `cat >/dev/null` or read into a var).
- **Default path:** exit `0`.
- **Documented customization point:** a commented block showing how to inspect the payload (e.g. via the `KEEP_TEAMMATES_WORKING` env var, or a grep on the drained payload) and `exit 2` to keep the teammate working, with a one-line message to **stderr** explaining why.
- Honors an env var `KEEP_TEAMMATES_WORKING` (default unset/`0`): when set to `1`, the script exits `2` (keep working) and prints a short reason to stderr. This makes the "keep working" path **real and toggleable** without editing the file, while keeping exit 0 as the default.
- No third-party tools; only POSIX shell builtins / coreutils.

So the behavior table is:

| Condition | Exit | Effect |
|---|---|---|
| `KEEP_TEAMMATES_WORKING` unset or not `1` (default) | 0 | Teammate may idle |
| `KEEP_TEAMMATES_WORKING=1` | 2 | Teammate is kept working; reason on stderr |

---

### 4.5 `scripts/task_completed_gate.py` — TaskCompleted hook (the security gate)

Pure-stdlib Python 3 (`json`, `os`, `sys`, `pathlib` only). Executable, shebang `#!/usr/bin/env python3`. This is the heart of the plugin — its full contract is in §5.

---

### 4.6 `scripts/test_task_completed_gate.py` — unittest

`unittest`, stdlib only. Mirrors the shape of the shipped `batch-security-migration/scripts/test_scan_diff.py`:
- Imports the gate module and/or invokes it as a subprocess (`subprocess.run([sys.executable, SCRIPT, ...], input=<stdin payload>, capture_output=True, text=True)`), asserting on `returncode` and `stderr`.
- Uses `tempfile`/`tmp_path` to create scan-artifact JSON files on disk and points `SECURITY_SCAN_DIR` at the temp dir via the subprocess `env=`.
- Five concrete cases — see §7.

The build must run `python3 -m unittest scripts/test_task_completed_gate.py` (or `python3 scripts/test_task_completed_gate.py`) and show all tests passing as the completion evidence (per `verification-before-completion`).

---

## 5. TaskCompleted gate — full contract (precise)

This section resolves every "still to specify" item. It is the implementation contract for `task_completed_gate.py`.

### 5.1 Input (stdin)

Claude Code delivers hook events as a **JSON object on stdin**. The gate:
1. Reads all of stdin.
2. Parses it as JSON. The fields the gate uses (defensively — treat all as optional):
   - `task` / `task_name` / `description` — a string identifying the task (used for the audit/opt-out classification, §5.4).
   - `target` — the target plugin/repo path or name, if present.
   - `tags` or `labels` — optional list; used for opt-out detection.
3. If stdin is empty or not valid JSON, the gate treats the payload as `{}` (empty dict) and proceeds. (Rationale: a missing/garbage payload must not crash the hook; the artifact check below still governs the decision. See §6.)

The gate must **never** raise an uncaught exception to the runtime — any unexpected error path resolves to a defined exit code (§6), never a traceback that aborts the teammate.

### 5.2 Scan-artifact location convention (defined here)

**The gate reads env var `SECURITY_SCAN_DIR`.**
- **Default (when unset):** `~/.claude-cache/security-scans/` (expand `~` via `pathlib.Path.home()`). This sits under the same `~/.claude-cache/` root the smart-extractors already use, so it's a familiar, writable, per-user location.
- The directory is created on demand by the *producer* (the lead agent running `scan_plugin.py --output ...`), not by the gate. The gate only **reads**.

**Identifying "the target" → the artifact filename:**
1. If the payload provides `target`, derive a **slug** from it: take the basename of the path, lowercase, and replace any character not in `[a-z0-9._-]` with `-`. The expected artifact is `${SECURITY_SCAN_DIR}/${slug}.json`.
2. If `target` is absent, the gate also accepts an env override `SECURITY_SCAN_ARTIFACT` giving an **explicit absolute path** to the artifact JSON (highest precedence — if set, use it directly and skip slug derivation).
3. If neither `target` nor `SECURITY_SCAN_ARTIFACT` is available, the gate falls back to **"any `*.json` in `SECURITY_SCAN_DIR` that parses as a valid scan report"** (newest by mtime). This lets simple single-target runs work without wiring a `target` field. If no such file exists, that is the "artifact missing" case (exit 2).

Precedence (highest first): `SECURITY_SCAN_ARTIFACT` (explicit path) → `target`-derived slug file → newest valid `*.json` in `SECURITY_SCAN_DIR`.

### 5.3 "Valid scan artifact" definition (the decision rule)

A file is a **valid scan artifact** iff ALL of:
1. The file **exists** and is readable.
2. Its contents **parse as JSON** into a dict.
3. The dict has a `summary` object, and `summary["severity_counts"]` exists and **is a dict** (the exact key produced by `scan_plugin.py`, confirmed against `plugin-security-checker/scripts/scan_plugin.py` lines 755–757).
4. `severity_counts` is non-empty (it contains at least the scanner's standard keys). The gate does **not** require zero findings — a scan that found CRITICALs is still a *valid artifact*; the gate only proves a scan **ran**, not that it was clean. (Cleanliness gating is `scan_diff.py`'s job in #40; this gate's contract is "a scan happened.")

### 5.4 Opt-out / non-audit tasks (defined here)

Not every TaskCompleted event is a security-audit task (e.g. an IR documentation task, or a compliance task with no scannable target). The gate must not block those. Opt-out is granted if **any** of:
- Env var `SECURITY_GATE_DISABLE=1` is set (global opt-out for this run), **OR**
- The payload's task/description/tags contain the literal marker `[no-scan-gate]` (case-insensitive), **OR**
- The task is classified as **non-audit**: the gate only *enforces* when the task looks like a security/plugin audit. Heuristic (documented, deterministic): enforce when the task/description/tags string contains any of `audit`, `scan`, `security-audit`, or a `target` field is present; otherwise treat as non-audit and allow. This keeps the gate scoped to audit completions and avoids blocking unrelated work.

When opt-out applies, the gate exits **0** and prints one informational line to stderr stating which opt-out fired.

### 5.5 Exact exit-code decision rule

```
read payload from stdin -> dict (or {} on empty/invalid)

if opt_out_applies(payload, env):            # SECURITY_GATE_DISABLE / [no-scan-gate] / non-audit task
    stderr: "TaskCompleted gate: opt-out (<reason>); completion allowed."
    exit 0

artifact_path = resolve_artifact(payload, env)   # precedence per §5.2

if artifact is a VALID scan artifact (§5.3):
    stderr: "TaskCompleted gate: valid scan artifact found at <path>; completion allowed."
    exit 0
else:
    stderr: "TaskCompleted gate: BLOCKED — no valid plugin-security-checker scan artifact for <target/slug>. "
            "Run: scan_plugin.py --output \"$SECURITY_SCAN_DIR/<slug>.json\" <target>  (looked in <SECURITY_SCAN_DIR>). "
            "Reason: <missing|unparseable|no severity_counts>."
    exit 2
```

- **Exit 0** = allow completion. **Exit 2** = block completion (the documented Agent Teams blocking signal).
- The gate uses **only** exit 0 and exit 2 for its decisions. (Any internal failure also resolves to one of these — see §6; it never returns 1, and never crashes.)
- **All human-facing messages go to stderr**, never stdout, so they don't pollute any payload the runtime reads from stdout.

### 5.6 stderr messages (exact intent)

- **Block (missing artifact):** `TaskCompleted gate: BLOCKED — no valid scan artifact for "<slug>". Run scan_plugin.py --output "$SECURITY_SCAN_DIR/<slug>.json" <target> then retry. (searched: <dir>; reason: missing)`
- **Block (unparseable):** same prefix, `reason: unparseable JSON at <path>`.
- **Block (no severity_counts):** same prefix, `reason: artifact has no summary.severity_counts`.
- **Allow (valid):** `TaskCompleted gate: OK — valid scan artifact at <path> (severity_counts present); completion allowed.`
- **Allow (opt-out):** `TaskCompleted gate: opt-out (<SECURITY_GATE_DISABLE | [no-scan-gate] | non-audit task>); completion allowed.`

The `<reason>` token in block messages is one of exactly: `missing`, `unparseable`, `no-severity-counts`.

---

## 6. Error handling

| Condition | Gate behavior |
|---|---|
| Stdin empty | Treat as `{}`; proceed to artifact/opt-out logic (does NOT auto-allow). |
| Stdin not valid JSON | Treat as `{}`; proceed. Do not crash. |
| `SECURITY_SCAN_DIR` unset | Use default `~/.claude-cache/security-scans/`. |
| `SECURITY_SCAN_DIR` set but dir doesn't exist | Treated as "no artifacts" → if task is an audit and not opted out → **exit 2** (missing). Gate does not create the dir. |
| `SECURITY_SCAN_ARTIFACT` set but file missing | **exit 2** (missing) — explicit path that doesn't exist is a block, not a fallthrough. |
| Artifact file exists but unreadable (permissions) | **exit 2**, reason `unparseable` (treated as not-valid). |
| Artifact exists but is not JSON / not a dict | **exit 2**, reason `unparseable`. |
| Artifact is a dict but lacks `summary.severity_counts` or it isn't a dict | **exit 2**, reason `no-severity-counts`. |
| Any unexpected internal exception | Caught at top level; print `TaskCompleted gate: internal error: <msg>; blocking to be safe.` to stderr and **exit 2** (fail closed — a safety gate must not silently allow on error). |
| `teammate_idle_gate.sh` receives no/garbage stdin | Drains stdin, exits per `KEEP_TEAMMATES_WORKING` (default 0). Never crashes. |

**Fail-closed principle (settled):** when the gate cannot prove the task is safe to complete (and it is an audit task, not opted out), it **blocks (exit 2)**. The only exits to 0 are: explicit opt-out, classified non-audit, or a proven-valid artifact.

---

## 7. Testing — the five concrete gate test cases

All five are implemented in `scripts/test_task_completed_gate.py`, invoking `task_completed_gate.py` as a subprocess with controlled stdin and a temp `SECURITY_SCAN_DIR`. Each asserts the exact `returncode`.

| # | Scenario | Setup | Stdin payload | Expected exit |
|---|---|---|---|---|
| **T1** | **Artifact missing** | `SECURITY_SCAN_DIR` = empty temp dir; no artifact file | `{"task":"security audit of plugin-x","target":"plugin-x"}` | **2** (block; reason `missing`) |
| **T2** | **Artifact present + valid** | Write `<tmp>/plugin-x.json` = `{"summary":{"severity_counts":{"CRITICAL":0,"HIGH":1,"MEDIUM":0,"LOW":2,"INFO":0}}}` | `{"task":"security audit of plugin-x","target":"plugin-x"}` | **0** (allow; valid artifact — note HIGH:1 present, still allowed because gate proves a scan ran, not cleanliness) |
| **T3** | **Artifact present but unparseable** | Write `<tmp>/plugin-x.json` = `not json {{{` | `{"task":"security audit of plugin-x","target":"plugin-x"}` | **2** (block; reason `unparseable`) |
| **T4** | **Artifact present but missing `severity_counts`** | Write `<tmp>/plugin-x.json` = `{"summary":{"categories":{}}}` (valid JSON, valid `summary`, but no `severity_counts`) | `{"task":"security audit of plugin-x","target":"plugin-x"}` | **2** (block; reason `no-severity-counts`) |
| **T5** | **Non-audit task / opt-out** | Empty temp dir (no artifact) | `{"task":"write incident timeline","tags":["[no-scan-gate]"]}` (and a second sub-assert with `SECURITY_GATE_DISABLE=1`, and a third with a plain non-audit task like `{"task":"update the readme"}`) | **0** (allow; opt-out / non-audit) — proves the gate doesn't over-block |

Additional sanity assertions (recommended, not part of the required five): empty stdin on an audit-shaped task with no artifact → exit 2; `SECURITY_SCAN_ARTIFACT` pointing at a valid file → exit 0.

**Completion evidence required (per `verification-before-completion`):** the build must show `python3 -m unittest -v scripts/test_task_completed_gate.py` passing (all cases green) before claiming done. `teammate_idle_gate.sh` is shell — its two-branch behavior (default exit 0, `KEEP_TEAMMATES_WORKING=1` → exit 2) should be demonstrated with two quick `printf '{}' | KEEP_TEAMMATES_WORKING=… sh scripts/teammate_idle_gate.sh; echo $?` invocations as evidence.

---

## 8. Data flow

```
User enables Agent Teams:  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
        │
        ▼
User reads SKILL.md → picks a swarm → spawns lead + specialists (copy-paste prompts)
        │
        ▼  (Security Audit Swarm)
Lead fans out to 5 specialists → collects findings
Lead runs:  scan_plugin.py --output "$SECURITY_SCAN_DIR/<slug>.json" <target>
        │                                  │
        │                                  └── writes the scan ARTIFACT to disk
        ▼
Lead attempts "task complete"
        │
        ▼  Claude Code fires TaskCompleted event → stdin JSON → task_completed_gate.py
        │
        ├─ opt-out?  ─yes→ exit 0 (allow)
        ├─ resolve artifact (SECURITY_SCAN_ARTIFACT | target slug | newest valid)
        ├─ artifact valid (parses + summary.severity_counts dict)? ─yes→ exit 0 (allow)
        └─ else → exit 2 (BLOCK) + stderr remediation message → completion prevented
        ▲
        │  Meanwhile, when a teammate goes idle:
        └─ TeammateIdle event → stdin → teammate_idle_gate.sh
              ├─ KEEP_TEAMMATES_WORKING=1 → exit 2 (keep working) + stderr reason
              └─ default → exit 0 (allow idle)
```

The hooks are the only executable, runtime-active components; everything else is human-driven prose. The single shared piece of state is the **scan artifact file** at `$SECURITY_SCAN_DIR/<slug>.json`, which the lead *produces* and the gate *consumes*.

---

## 9. Out of scope (YAGNI)

Explicitly **not** built:
- **No programmatic team spawner / orchestrator.** The plugin never starts, schedules, or manages teammates.
- **No execution of Agent Teams.** The feature is experimental/disabled and unrunnable in this environment; swarm configs are prose validated by review, not run in CI.
- **No agents/ directory or sub-agent definitions** in this plugin (it's skill-only; the swarm "agents" are spawn-prompt prose, not Claude Code agent files).
- **No new scanner.** The gate *reuses* `plugin-security-checker`'s `scan_plugin.py` output; it does not re-scan or re-implement detection.
- **No cleanliness/regression gating.** Whether the scan found HIGH/CRITICAL is out of scope — that is `batch-security-migration`'s `scan_diff.py` (#40). This gate only proves a scan *ran*.
- **No HTML/report output** (so no `html.escape()` concerns apply here).
- **No third-party dependencies** (stdlib Python + POSIX shell only).
- **No auto-creation of `SECURITY_SCAN_DIR`** by the gate (the producer/lead owns directory creation).
- **No remediation/auto-fix.** Audit swarms are read-only by design.

---

## 10. Repo conventions checklist (must all hold at ship)

- [ ] Dir name `agent-teams-security-playbook`; `plugin.json.name` == dir name; `SKILL.md` frontmatter `name` == dir name.
- [ ] `plugin.json` keys ⊆ {`name`,`version`,`description`,`author`,`keywords`}; NO `$schema`/`category`/`requirements`/`scripts`/`agents`.
- [ ] `SKILL.md` frontmatter has `name`+`description` (required); `license: MIT` (convention); `version`/`author` under `metadata:`.
- [ ] Zero third-party deps; stdlib Python + POSIX shell only. No `npm install`, no `pip install`.
- [ ] No hardcoded plugin counts anywhere in shipped docs (let `scripts/check_doc_drift.py` derive them).
- [ ] `task_completed_gate.py` and `teammate_idle_gate.sh` are executable (`chmod +x`), correct shebangs.
- [ ] Gate reads stdin, decides, exits 0/2 only, all human messages to stderr, fail-closed on error.
- [ ] `test_task_completed_gate.py` passes all five cases; output captured as completion evidence.

---

## 11. marketplace.json entry (added at ship, mirrors the `security-hooks` entry)

When the plugin ships, add this object to `.claude-plugin/marketplace.json`'s `plugins` array (taking the count from 13 → 14). The marketplace **entry** MAY use `category`/`keywords`/`homepage`/`repository`/`license` (these are allowed in marketplace entries even though forbidden in `plugin.json`).

```json
{
  "name": "agent-teams-security-playbook",
  "description": "Playbook skill for Claude Code's experimental Agent Teams: three ready-to-run security swarm configurations (5-agent Security Audit, 4-agent Compliance Audit, 3-agent Incident Response) with copy-paste spawn prompts and coordination best practices, plus two real Agent Teams hooks — a TeammateIdle keep-working gate and a TaskCompleted gate that blocks 'audit complete' until a plugin-security-checker scan artifact exists.",
  "source": "./agent-teams-security-playbook",
  "version": "1.0.0",
  "author": { "name": "Diego Consolini", "email": "diego@diegocon.nl" },
  "category": "security",
  "keywords": ["agent-teams", "swarm", "multi-agent", "security-audit", "compliance", "incident-response", "hooks", "teammateidle", "taskcompleted", "experimental"],
  "homepage": "https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/agent-teams-security-playbook",
  "repository": "https://github.com/diegocconsolini/ClaudeSkillCollection",
  "license": "MIT"
}
```

---

## 12. Doc-drift impact (13 → 14)

- Adding this plugin moves the marketplace plugin count **13 → 14**.
- `scripts/check_doc_drift.py` **derives** counts from the repo (it must not be fed a hardcoded number); after adding the plugin dir + the `marketplace.json` entry, run `python3 scripts/check_doc_drift.py` and confirm it passes (the derived count updates to 14 automatically).
- Do **not** hardcode "14" anywhere in shipped docs. If any doc references the count, it must derive it or the drift check will fail.
- The root `CLAUDE.md` "Security & Compliance Marketplace … 12/13 plugins" narrative prose is informational; update it only if the drift check or its own logic requires, and never with a hardcoded magic number that the drift checker would later flag. (The drift checker is the source of truth; reconcile to it.)

---

## 13. Acceptance criteria (definition of done for #34)

1. `agent-teams-security-playbook/` exists with the four files in §4.1, correct permissions/shebangs.
2. `plugin.json` validates as JSON, contains only the allowed keys, `name` == dir name.
3. `SKILL.md` contains all three swarms with per-agent spawn prompts (5 + 4 + 3 agents, each prompt covering the six required elements in §4.3C), the experimental warning, hook-setup reference, and best practices.
4. `task_completed_gate.py` implements the §5 contract exactly (stdin → decide → exit 0/2; `SECURITY_SCAN_DIR` default `~/.claude-cache/security-scans/`; precedence per §5.2; valid-artifact per §5.3; opt-out per §5.4; fail-closed per §6).
5. `teammate_idle_gate.sh` implements §4.4 (default exit 0; `KEEP_TEAMMATES_WORKING=1` → exit 2; drains stdin; never crashes).
6. `test_task_completed_gate.py` passes all five §7 cases; passing output captured as evidence.
7. `marketplace.json` entry added (§11); `python3 scripts/check_doc_drift.py` passes with count at 14.
8. Built via `superpowers:subagent-driven-development` (mirroring #40); committed straight to `main`; #34 closed with evidence (test output + drift-clean).

---

*End of spec. Hand to `superpowers:writing-plans`.*
