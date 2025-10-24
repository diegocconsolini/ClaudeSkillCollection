#!/bin/bash
#
# Scan All Marketplace Plugins - Comprehensive security analysis across 15 repositories
# Version: 1.0.0
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
REPOS_BASE="$PLUGIN_DIR/test_plugins_full"
OUTPUT_DIR="$PLUGIN_DIR/full_marketplace_scan_results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "======================================================================"
echo " Plugin Security Checker - FULL MARKETPLACE SCAN"
echo " Scanning ALL plugins from 15 Claude Code repositories"
echo "======================================================================"
echo ""
echo "Base Directory: $REPOS_BASE"
echo "Output Directory: $OUTPUT_DIR"
echo "Scan Start Time: $(date)"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/scans"
mkdir -p "$OUTPUT_DIR/reports"

# Function to get repository name from repo ID
get_repo_name() {
    local repo_id="$1"
    case "$repo_id" in
        "repo-01-jeremylongshore") echo "jeremylongshore/claude-code-plugins-plus" ;;
        "repo-02-wshobson") echo "wshobson/agents" ;;
        "repo-03-brennercruvinel") echo "brennercruvinel/CCPlugins" ;;
        "repo-04-ananddtyagi") echo "ananddtyagi/claude-code-marketplace" ;;
        "repo-05-everyinc") echo "EveryInc/every-marketplace" ;;
        "repo-06-ccplugins") echo "ccplugins/marketplace" ;;
        "repo-07-devgom") echo "Dev-GOM/claude-code-marketplace" ;;
        "repo-08-jmanhype") echo "jmanhype/claude-code-plugin-marketplace" ;;
        "repo-09-hugoduncan") echo "hugoduncan/claude-marketplace" ;;
        "repo-10-dhofheinz") echo "dhofheinz/open-plugins" ;;
        "repo-11-awesome-ccplugins") echo "ccplugins/awesome-claude-code-plugins" ;;
        "repo-12-yanmxa") echo "yanmxa/cc-plugins" ;;
        "repo-13-pchalasani") echo "pchalasani/claude-code-tools" ;;
        "repo-14-curiouslearner") echo "CuriousLearner/devkit" ;;
        "repo-15-hesreallyhim") echo "hesreallyhim/awesome-claude-code" ;;
        *) echo "unknown" ;;
    esac
}

# Initialize counters
total_repos=0
total_plugins=0
scanned_plugins=0
failed_scans=0

# Function to find plugins in a directory
find_plugins() {
    local repo_path="$1"
    local plugins=()

    # Look for directories with .claude-plugin/plugin.json
    while IFS= read -r -d '' plugin_json; do
        plugin_dir=$(dirname "$(dirname "$plugin_json")")
        plugins+=("$plugin_dir")
    done < <(find "$repo_path" -name "plugin.json" -path "*/.claude-plugin/plugin.json" -print0 2>/dev/null)

    printf '%s\n' "${plugins[@]}"
}

# Function to get plugin name from path
get_plugin_name() {
    basename "$1"
}

# Function to scan a single plugin
scan_plugin() {
    local plugin_path="$1"
    local plugin_name="$2"
    local repo_name="$3"
    local scan_num="$4"

    local safe_name="${repo_name//\//_}_${plugin_name}"
    local output_json="$OUTPUT_DIR/scans/${safe_name}_scan.json"

    echo "  [$scan_num] Scanning: $plugin_name"

    if python3 "$SCRIPT_DIR/scan_plugin.py" "$plugin_path" \
        --output "$output_json" \
        --format json 2>&1 | grep -E "\\[.*\\]|Risk Level|Verdict" | head -3; then

        scanned_plugins=$((scanned_plugins + 1))

        # Generate markdown report
        if [ -f "$output_json" ]; then
            python3 "$SCRIPT_DIR/generate_report.py" "$output_json" \
                --format markdown \
                --output "$OUTPUT_DIR/reports/${safe_name}_report.md" 2>/dev/null || true
        fi

        return 0
    else
        echo "    ERROR: Scan failed for $plugin_name"
        failed_scans=$((failed_scans + 1))
        return 1
    fi
}

echo "======================================================================"
echo " PHASE 1: Repository Discovery"
echo "======================================================================"
echo ""

# Process each repository
for repo_dir in "$REPOS_BASE"/repo-*; do
    if [ ! -d "$repo_dir" ]; then
        continue
    fi

    total_repos=$((total_repos + 1))
    repo_id=$(basename "$repo_dir")
    repo_name="$(get_repo_name "$repo_id")"

    echo "[$total_repos/15] Repository: $repo_name"
    echo "  Path: $repo_dir"

    # Find all plugins in this repository
    plugins_found=()
    while IFS= read -r plugin_path; do
        [ -n "$plugin_path" ] && plugins_found+=("$plugin_path")
    done < <(find_plugins "$repo_dir")

    plugin_count=${#plugins_found[@]}
    total_plugins=$((total_plugins + plugin_count))

    echo "  Plugins found: $plugin_count"
    echo ""
done

echo "======================================================================"
echo " PHASE 2: Security Scanning"
echo "======================================================================"
echo ""
echo "Total repositories: $total_repos"
echo "Total plugins discovered: $total_plugins"
echo ""
echo "Starting comprehensive scan..."
echo ""

scan_counter=0

# Scan all plugins
for repo_dir in "$REPOS_BASE"/repo-*; do
    if [ ! -d "$repo_dir" ]; then
        continue
    fi

    repo_id=$(basename "$repo_dir")
    repo_name="$(get_repo_name "$repo_id")"

    # Count plugins in this repository
    plugin_count=0
    while IFS= read -r plugin_path; do
        [ -n "$plugin_path" ] && plugin_count=$((plugin_count + 1))
    done < <(find_plugins "$repo_dir")

    if [ "$plugin_count" -eq 0 ]; then
        echo "[$repo_id] No plugins to scan"
        echo ""
        continue
    fi

    echo "[$repo_id] Scanning $plugin_count plugins from $repo_name"
    echo "----------------------------------------------------------------------"

    # Find and scan each plugin
    while IFS= read -r plugin_path; do
        if [ -n "$plugin_path" ]; then
            scan_counter=$((scan_counter + 1))
            plugin_name=$(get_plugin_name "$plugin_path")
            scan_plugin "$plugin_path" "$plugin_name" "$repo_name" "$scan_counter"
        fi
    done < <(find_plugins "$repo_dir")

    echo ""
done

echo "======================================================================"
echo " PHASE 3: Results Analysis"
echo "======================================================================"
echo ""

# Risk distribution counters
critical_count=0
high_count=0
medium_count=0
low_count=0
error_count=0

# Verdict counters
pass_count=0
review_count=0
fail_count=0

# Generate comprehensive summary
echo "Processing scan results..."
echo ""

for scan_file in "$OUTPUT_DIR"/scans/*_scan.json; do
    if [ -f "$scan_file" ]; then
        risk_level=$(python3 -c "import json; print(json.load(open('$scan_file'))['metadata']['risk_level'])" 2>/dev/null || echo "ERROR")
        verdict=$(python3 -c "import json; print(json.load(open('$scan_file'))['metadata']['verdict'])" 2>/dev/null || echo "ERROR")

        # Count by risk level
        case "$risk_level" in
            CRITICAL) critical_count=$((critical_count + 1)) ;;
            HIGH) high_count=$((high_count + 1)) ;;
            MEDIUM) medium_count=$((medium_count + 1)) ;;
            LOW) low_count=$((low_count + 1)) ;;
            ERROR) error_count=$((error_count + 1)) ;;
        esac

        # Count by verdict
        case "$verdict" in
            PASS) pass_count=$((pass_count + 1)) ;;
            REVIEW) review_count=$((review_count + 1)) ;;
            FAIL) fail_count=$((fail_count + 1)) ;;
        esac
    fi
done

# Generate final summary report
SUMMARY_FILE="$OUTPUT_DIR/SCAN_SUMMARY_${TIMESTAMP}.md"

cat > "$SUMMARY_FILE" <<EOF
# Plugin Security Checker - Full Marketplace Scan Results

**Scan Date:** $(date)
**Scanner Version:** 1.0.0
**Repositories Scanned:** $total_repos

---

## Executive Summary

### Scan Coverage
- **Total Repositories:** $total_repos
- **Total Plugins Discovered:** $total_plugins
- **Successfully Scanned:** $scanned_plugins
- **Failed Scans:** $failed_scans
- **Scan Success Rate:** $(awk "BEGIN {printf \"%.1f\", ($scanned_plugins / $total_plugins) * 100}")%

### Risk Distribution
| Risk Level | Count | Percentage |
|------------|-------|------------|
| CRITICAL   | $critical_count | $(awk "BEGIN {printf \"%.1f\", ($critical_count / $scanned_plugins) * 100}")% |
| HIGH       | $high_count | $(awk "BEGIN {printf \"%.1f\", ($high_count / $scanned_plugins) * 100}")% |
| MEDIUM     | $medium_count | $(awk "BEGIN {printf \"%.1f\", ($medium_count / $scanned_plugins) * 100}")% |
| LOW        | $low_count | $(awk "BEGIN {printf \"%.1f\", ($low_count / $scanned_plugins) * 100}")% |

### Verdict Distribution
| Verdict | Count | Percentage |
|---------|-------|------------|
| PASS    | $pass_count | $(awk "BEGIN {printf \"%.1f\", ($pass_count / $scanned_plugins) * 100}")% |
| REVIEW  | $review_count | $(awk "BEGIN {printf \"%.1f\", ($review_count / $scanned_plugins) * 100}")% |
| FAIL    | $fail_count | $(awk "BEGIN {printf \"%.1f\", ($fail_count / $scanned_plugins) * 100}")% |

---

## Repository Breakdown

EOF

# Add per-repository statistics
for repo_dir in "$REPOS_BASE"/repo-*; do
    if [ ! -d "$repo_dir" ]; then
        continue
    fi

    repo_id=$(basename "$repo_dir")
    repo_name="$(get_repo_name "$repo_id")"

    # Count plugins in this repository
    plugin_count=0
    while IFS= read -r plugin_path; do
        [ -n "$plugin_path" ] && plugin_count=$((plugin_count + 1))
    done < <(find_plugins "$repo_dir")

    cat >> "$SUMMARY_FILE" <<EOF
### $repo_name
- **Plugins Found:** $plugin_count
- **Repository:** https://github.com/${repo_name}

EOF
done

cat >> "$SUMMARY_FILE" <<EOF

---

## Detailed Results

All scan results are available in:
- **JSON Scans:** \`scans/\` directory
- **Markdown Reports:** \`reports/\` directory

### High/Critical Findings

EOF

# List all CRITICAL and HIGH risk plugins
echo "Identifying high-priority findings..."

for scan_file in "$OUTPUT_DIR"/scans/*_scan.json; do
    if [ -f "$scan_file" ]; then
        risk_level=$(python3 -c "import json; print(json.load(open('$scan_file'))['metadata']['risk_level'])" 2>/dev/null || echo "ERROR")

        if [ "$risk_level" = "CRITICAL" ] || [ "$risk_level" = "HIGH" ]; then
            plugin_name=$(basename "$scan_file" "_scan.json")
            total_findings=$(python3 -c "import json; print(json.load(open('$scan_file'))['metadata']['total_findings'])" 2>/dev/null || echo "0")

            cat >> "$SUMMARY_FILE" <<EOF
- **$plugin_name** - Risk: $risk_level, Findings: $total_findings
EOF
        fi
    fi
done

cat >> "$SUMMARY_FILE" <<EOF

---

## Scanner Disclaimer

⚠️ **IMPORTANT SECURITY DISCLAIMER**

This is a SUPPORTING TOOL for preliminary security checks.

**What this tool DOES:**
✓ Detects common code obfuscation patterns
✓ Identifies dangerous function usage
✓ Validates plugin.json structure
✓ Flags suspicious code patterns
✓ Provides security recommendations

**What this tool does NOT do:**
✗ Guarantee plugin safety or security
✗ Detect all possible vulnerabilities
✗ Replace manual security code review
✗ Provide legal or compliance advice
✗ Detect zero-day vulnerabilities
✗ Analyze runtime behavior

**YOUR RESPONSIBILITY:**
🔒 YOU are ultimately responsible for plugins you install and use
📖 ALWAYS review plugin source code manually before installation
🛡️ ONLY install plugins from sources you trust
🔍 VERIFY the plugin author's identity and reputation
💻 RUN untrusted plugins in sandboxed environments only
⚠️ USE this tool at your own risk

EOF

echo ""
echo "======================================================================"
echo " SCAN COMPLETE"
echo "======================================================================"
echo ""
echo "Scan Duration: Started at $TIMESTAMP, Completed at $(date +%Y%m%d_%H%M%S)"
echo ""
echo "Final Statistics:"
echo "  Total Repositories: $total_repos"
echo "  Total Plugins Discovered: $total_plugins"
echo "  Successfully Scanned: $scanned_plugins"
echo "  Failed Scans: $failed_scans"
echo ""
echo "Risk Distribution:"
echo "  CRITICAL: $critical_count"
echo "  HIGH: $high_count"
echo "  MEDIUM: $medium_count"
echo "  LOW: $low_count"
echo ""
echo "Verdict Distribution:"
echo "  PASS: $pass_count"
echo "  REVIEW: $review_count"
echo "  FAIL: $fail_count"
echo ""
echo "Results saved to:"
echo "  Summary: $SUMMARY_FILE"
echo "  Scans: $OUTPUT_DIR/scans/"
echo "  Reports: $OUTPUT_DIR/reports/"
echo ""
echo "======================================================================"
