#!/bin/bash
#
# Scan Marketplace Plugins - Security analysis of marketplace plugins
# Version: 1.0.0
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PLUGIN_DIR/marketplace_scan_results"
MARKETPLACE_BASE="$PLUGIN_DIR/test_plugins"

echo "=== Plugin Security Checker - Marketplace Scan ==="
echo ""
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Select 15 diverse plugins to scan
PLUGINS=(
    "claude-code-plugins-plus/plugins/examples/hello-world"
    "claude-code-plugins-plus/plugins/examples/security-agent"
    "claude-code-plugins-plus/plugins/examples/skills-powerkit"
    "claude-code-plugins-plus/plugins/devops/docker-compose-generator"
    "claude-code-plugins-plus/plugins/devops/kubernetes-deployment-creator"
    "claude-code-plugins-plus/plugins/devops/terraform-module-builder"
    "claude-code-plugins-plus/plugins/devops/ci-cd-pipeline-builder"
    "claude-code-plugins-plus/plugins/devops/container-security-scanner"
    "claude-code-plugins-plus/plugins/ai-ml/ai-sdk-agents"
    "claude-code-plugins-plus/plugins/ai-ml/anomaly-detection-system"
    "claude-code-plugins-plus/plugins/backend/fastapi-app-builder"
    "claude-code-plugins-plus/plugins/backend/graphql-schema-designer"
    "claude-code-plugins-plus/plugins/frontend/react-component-generator"
    "claude-code-plugins-plus/plugins/frontend/vue-app-scaffolder"
    "claude-code-plugins-plus/plugins/security/penetration-test-planner"
)

echo "Plugins to scan: ${#PLUGINS[@]}"
echo ""

total=0
scanned=0
failed=0

# Scan each plugin
for plugin_rel in "${PLUGINS[@]}"; do
    total=$((total + 1))
    plugin_path="$MARKETPLACE_BASE/$plugin_rel"
    plugin_name=$(basename "$plugin_rel")

    if [ ! -d "$plugin_path" ]; then
        echo "[$total/${#PLUGINS[@]}] SKIP - $plugin_name (not found)"
        failed=$((failed + 1))
        continue
    fi

    echo "[$total/${#PLUGINS[@]}] SCAN - $plugin_name..."

    # JSON output
    if python3 "$SCRIPT_DIR/scan_plugin.py" "$plugin_path" \
        --output "$OUTPUT_DIR/${plugin_name}_scan.json" \
        --format json 2>&1 | grep -E "\[.*\]|Risk Level|Verdict|Total Findings"; then

        scanned=$((scanned + 1))

        # Markdown report
        if [ -f "$OUTPUT_DIR/${plugin_name}_scan.json" ]; then
            python3 "$SCRIPT_DIR/generate_report.py" "$OUTPUT_DIR/${plugin_name}_scan.json" \
                --format markdown \
                --output "$OUTPUT_DIR/${plugin_name}_report.md" 2>&1 | grep "Report written" || true
        fi
    else
        echo "  ERROR: Scan failed"
        failed=$((failed + 1))
    fi

    echo ""
done

echo "=== Scan Complete ==="
echo ""
echo "Total plugins: $total"
echo "Successfully scanned: $scanned"
echo "Failed: $failed"
echo ""
echo "Results saved to: $OUTPUT_DIR"
echo ""

# Generate summary
echo "=== Security Summary ==="
echo ""
printf "%-50s %-10s %-8s %-10s\n" "Plugin" "Risk" "Verdict" "Findings"
printf "%-50s %-10s %-8s %-10s\n" "------" "----" "-------" "--------"

critical_count=0
high_count=0
medium_count=0
low_count=0

for plugin_rel in "${PLUGINS[@]}"; do
    plugin_name=$(basename "$plugin_rel")
    json_file="$OUTPUT_DIR/${plugin_name}_scan.json"

    if [ -f "$json_file" ]; then
        risk_level=$(python3 -c "import json; print(json.load(open('$json_file'))['metadata']['risk_level'])" 2>/dev/null || echo "ERROR")
        verdict=$(python3 -c "import json; print(json.load(open('$json_file'))['metadata']['verdict'])" 2>/dev/null || echo "ERROR")
        total=$(python3 -c "import json; print(json.load(open('$json_file'))['metadata']['total_findings'])" 2>/dev/null || echo "0")

        printf "%-50s %-10s %-8s %-10s\n" "$plugin_name" "$risk_level" "$verdict" "$total"

        # Count by risk level
        case "$risk_level" in
            CRITICAL) critical_count=$((critical_count + 1)) ;;
            HIGH) high_count=$((high_count + 1)) ;;
            MEDIUM) medium_count=$((medium_count + 1)) ;;
            LOW) low_count=$((low_count + 1)) ;;
        esac
    fi
done

echo ""
echo "=== Risk Distribution ==="
echo "CRITICAL: $critical_count"
echo "HIGH: $high_count"
echo "MEDIUM: $medium_count"
echo "LOW: $low_count"
echo ""
echo "Done!"
