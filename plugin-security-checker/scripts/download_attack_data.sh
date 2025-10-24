#!/bin/bash
#
# Download MITRE ATT&CK STIX 2.1 Data
# Downloads the latest enterprise-attack.json from GitHub
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
STIX_DIR="$PLUGIN_DIR/references/stix"

echo "======================================================================"
echo " MITRE ATT&CK STIX 2.1 Data Download"
echo "======================================================================"
echo ""

# Create stix directory
mkdir -p "$STIX_DIR"

# Download enterprise-attack.json
echo "[1/3] Downloading enterprise-attack.json..."
curl -L -o "$STIX_DIR/enterprise-attack.json" \
  https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json

echo "  ✓ Downloaded: $(wc -c < "$STIX_DIR/enterprise-attack.json" | awk '{printf "%.2f MB", $1/1024/1024}')"

# Download mobile-attack.json (optional)
echo "[2/3] Downloading mobile-attack.json..."
curl -L -o "$STIX_DIR/mobile-attack.json" \
  https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json

echo "  ✓ Downloaded: $(wc -c < "$STIX_DIR/mobile-attack.json" | awk '{printf "%.2f MB", $1/1024/1024}')"

# Download ics-attack.json (optional)
echo "[3/3] Downloading ics-attack.json..."
curl -L -o "$STIX_DIR/ics-attack.json" \
  https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json

echo "  ✓ Downloaded: $(wc -c < "$STIX_DIR/ics-attack.json" | awk '{printf "%.2f MB", $1/1024/1024}')"

# Validate JSON
echo ""
echo "Validating JSON..."
for file in "$STIX_DIR"/*.json; do
  if python3 -m json.tool "$file" > /dev/null 2>&1; then
    echo "  ✓ Valid: $(basename "$file")"
  else
    echo "  ✗ Invalid: $(basename "$file")"
    exit 1
  fi
done

echo ""
echo "======================================================================"
echo " Download Complete"
echo "======================================================================"
echo ""
echo "STIX 2.1 data files saved to: $STIX_DIR"
echo ""
echo "Files:"
ls -lh "$STIX_DIR"/*.json
echo ""
echo "Next steps:"
echo "  1. Install dependencies: pip3 install -r requirements.txt"
echo "  2. Run STIX manager test: python3 scripts/stix_manager.py --test"
echo ""
