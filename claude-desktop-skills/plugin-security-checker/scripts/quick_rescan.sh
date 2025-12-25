#!/bin/bash
# Quick rescan of marketplace plugins with integrated_scanner.py v2.0.0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$SCRIPT_DIR/../test_plugins_full"
SCANNER="$SCRIPT_DIR/integrated_scanner.py"
OUTPUT_DIR="$SCRIPT_DIR/../v2_scan_results"

mkdir -p "$OUTPUT_DIR"

echo "======================================================================"
echo " Plugin Security Checker v2.0.0 - Marketplace Rescan"
echo " MITRE ATT&CK + ATLAS + 70+ Patterns"
echo "======================================================================"
echo ""
echo "Plugin Directory: $PLUGIN_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Find all plugin directories
plugins=$(find "$PLUGIN_DIR" -name "plugin.json" -type f)
total=$(echo "$plugins" | wc -l | tr -d ' ')

echo "Found: $total plugins"
echo ""

# Counters
count=0
critical=0
high=0
medium=0
low=0
clean=0

# Scan each plugin
while IFS= read -r plugin_json; do
    ((count++))
    plugin_dir=$(dirname "$plugin_json")
    plugin_name=$(basename "$plugin_dir")

    echo -n "[$count/$total] Scanning $plugin_name... "

    # Run scanner
    output=$(python3 "$SCANNER" "$plugin_dir" --no-stix 2>&1)

    # Extract risk score
    risk_score=$(echo "$output" | grep "Risk Score:" | head -1 | awk '{print $3}')
    findings=$(echo "$output" | grep "Security Findings:" | head -1 | awk '{print $3}')

    if [ -z "$risk_score" ]; then
        risk_score=0
    fi

    # Classify
    if [ "$risk_score" -ge 1000 ]; then
        echo "CRITICAL (Score: $risk_score, Findings: $findings)"
        ((critical++))
        # Save report
        echo "$output" > "$OUTPUT_DIR/${plugin_name}_CRITICAL.txt"
    elif [ "$risk_score" -ge 500 ]; then
        echo "HIGH (Score: $risk_score, Findings: $findings)"
        ((high++))
        echo "$output" > "$OUTPUT_DIR/${plugin_name}_HIGH.txt"
    elif [ "$risk_score" -ge 200 ]; then
        echo "MEDIUM (Score: $risk_score, Findings: $findings)"
        ((medium++))
    elif [ "$risk_score" -gt 0 ]; then
        echo "LOW (Score: $risk_score, Findings: $findings)"
        ((low++))
    else
        echo "CLEAN"
        ((clean++))
    fi

done <<< "$plugins"

echo ""
echo "======================================================================"
echo " SCAN COMPLETE"
echo "======================================================================"
echo ""
echo "Risk Distribution:"
echo "  CRITICAL: $critical"
echo "  HIGH:     $high"
echo "  MEDIUM:   $medium"
echo "  LOW:      $low"
echo "  CLEAN:    $clean"
echo ""
echo "High-risk reports saved to: $OUTPUT_DIR"
