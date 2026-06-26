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


if __name__ == "__main__":
    unittest.main()
