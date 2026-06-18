---
name: security-fp-suppressions
description: Known-safe code patterns the plugin-security-checker should not re-flag in this project
metadata:
  type: reference
---

Patterns confirmed safe in this codebase — do not re-raise as findings:

- `eval()` / `exec()` appearing inside **string literals used as scanner test fixtures**
  (e.g. `test_code = "eval(user_input)"`) — these are detection inputs, not executed code.
- `subprocess` calls with a **fixed argument list** (no `shell=True`, no user-controlled
  string) — safe by construction.
- Base64 in **config/test data** rather than an eval/exec chain.

**Why:** the scanner is regex/AST-based and can over-flag fixtures and benign uses.
**How to apply:** before reporting a finding, check whether it matches one of these; if so,
note it as a confirmed false positive rather than a vulnerability.

Add project-specific confirmed-safe patterns below as they are validated. Each must name
the file/pattern precisely so it can be re-verified — never a blanket suppression.
