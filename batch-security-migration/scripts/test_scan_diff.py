import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "scan_diff.py"

# Real scanner finding shape (verified against plugin-security-checker v3.2.0).
def make_finding(severity, category="Cat", subcategory="Sub", file="f.py",
                 line=1, description="desc", fid="FINDING-001"):
    return {
        "id": fid, "severity": severity, "category": category,
        "subcategory": subcategory, "file": file, "line": line, "column": 0,
        "code_snippet": "x", "description": description, "explanation": "e",
        "impact": "i", "recommendation": "r", "cvss_score": 9.8,
        "cve_reference": None, "owasp_reference": None,
        "remediation_effort": "HIGH", "false_positive_likelihood": "LOW",
    }

def write_scan(findings):
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    for f in findings:
        counts[f["severity"]] += 1
    data = {"metadata": {}, "summary": {"severity_counts": counts, "categories": {}},
            "findings": findings, "disclaimer": "x"}
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(data, fh)
    fh.close()
    return fh.name


class TestCore(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import scan_diff
        self.m = scan_diff

    def test_finding_key_excludes_id(self):
        a = make_finding("HIGH", fid="FINDING-001")
        b = make_finding("HIGH", fid="FINDING-999")
        self.assertEqual(self.m.finding_key(a), self.m.finding_key(b))

    def test_diff_new_fixed_unchanged(self):
        before = [make_finding("LOW", description="stays"),
                  make_finding("CRITICAL", description="gets-fixed")]
        after = [make_finding("LOW", description="stays"),
                 make_finding("HIGH", description="brand-new")]
        d = self.m.diff_findings(before, after)
        self.assertEqual([f["description"] for f in d["new"]], ["brand-new"])
        self.assertEqual([f["description"] for f in d["fixed"]], ["gets-fixed"])
        self.assertEqual([f["description"] for f in d["unchanged"]], ["stays"])

    def test_has_blocking_true_on_high(self):
        self.assertTrue(self.m.has_blocking([make_finding("HIGH")]))
        self.assertTrue(self.m.has_blocking([make_finding("CRITICAL")]))

    def test_has_blocking_false_on_medium_and_below(self):
        self.assertFalse(self.m.has_blocking([make_finding("MEDIUM"),
                                              make_finding("LOW"),
                                              make_finding("INFO")]))

    def test_load_findings_bad_file_exits(self):
        with self.assertRaises(SystemExit):
            self.m.load_findings("/no/such/file.json")


class TestCLI(unittest.TestCase):
    def run_cli(self, args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              capture_output=True, text=True)

    def test_new_high_exits_1(self):
        before = write_scan([])
        after = write_scan([make_finding("HIGH", description="brand-new")])
        r = self.run_cli([before, after])
        self.assertEqual(r.returncode, 1)
        self.assertIn("brand-new", r.stdout)

    def test_fixed_finding_exits_0(self):
        before = write_scan([make_finding("CRITICAL", description="was-here")])
        after = write_scan([])
        r = self.run_cli([before, after])
        self.assertEqual(r.returncode, 0)
        self.assertIn("was-here", r.stdout)  # listed under FIXED

    def test_report_only_suppresses_exit_1(self):
        before = write_scan([])
        after = write_scan([make_finding("HIGH", description="brand-new")])
        r = self.run_cli([before, after, "--report-only"])
        self.assertEqual(r.returncode, 0)

    def test_identity_keying_same_finding_diff_id_is_unchanged(self):
        before = write_scan([make_finding("HIGH", description="same", fid="FINDING-001")])
        after = write_scan([make_finding("HIGH", description="same", fid="FINDING-777")])
        r = self.run_cli([before, after])
        self.assertEqual(r.returncode, 0)  # not new -> no block

    def test_scan_mode_end_to_end(self):
        # Smoke test: --scan over two real plugin dirs runs the real scanner.
        # gdpr-auditor has 0 findings both sides -> no new HIGH -> exit 0.
        repo = SCRIPT.resolve().parent.parent.parent
        target = str(repo / "gdpr-auditor")
        r = self.run_cli(["--scan", target, target])
        self.assertEqual(r.returncode, 0, msg=r.stderr)


if __name__ == "__main__":
    unittest.main()
