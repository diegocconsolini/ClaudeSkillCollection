# Next Session Prompt

Copy and paste this as your first message in a new Claude Code session:

---

Execute the implementation plan at `docs/plans/2026-03-05-audit-fixes-plan.md` using the `superpowers:executing-plans` skill.

This plan fixes 15 verified audit issues from GitHub Issue #25 (https://github.com/diegocconsolini/ClaudeSkillCollection/issues/25). All issues were independently verified with direct file inspection - no assumptions.

**Summary of 18 tasks:**
- Task 1: Create branch `fix/audit-issues-25`
- Task 2: Remove sensitive business data from public repo (C1) - **CRITICAL**
- Task 3: Add requirements.txt for incident-response-playbook-creator (C2)
- Task 4: Add missing files to desktop security-report-builder (C3)
- Task 5: Add missing requirements.txt to desktop pdf-smart-extractor (C4)
- Task 6: Add YAML frontmatter to 3 root SKILL.md files (C5)
- Task 7: Fix XSS in generate_complete_report.py (H1)
- Task 8: Fix XSS in generate_html_report.py (H2)
- Task 9: Fix XSS in html_generator.py (H3)
- Task 10: Create missing SKILL.md for 4 root plugins (H4)
- Task 11: Add __main__ guard to demo_learning.py (H5)
- Task 12: Add requirements.txt for cybersecurity-policy-generator (H6)
- Task 13: No-op (resolved by Tasks 4+5) (H7)
- Task 14: Fix docx-smart-extractor version mismatch (M1)
- Task 15: Fix stale version comment (M2)
- Task 16: Add claude-guide to marketplace.json (M3)
- Task 17: Create PR
- Task 18: Update plugin counts in CLAUDE.md and README.md

Execute in batches of 3. Report after each batch. Do NOT skip any verification steps.
