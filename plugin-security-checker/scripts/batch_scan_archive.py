#!/usr/bin/env python3
"""
Batch scan all archived plugins efficiently
Minimizes token usage by:
- Scanning only unique plugins (skipping timestamped versions)
- Running scans in parallel
- Saving individual results to files
- Generating summary statistics
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from collections import defaultdict

ARCHIVE_DIR = Path("plugin-security-checker/archive_dev_files/test_data")
OUTPUT_DIR = Path("plugin-security-checker/archive_scan_results")
SCANNER_SCRIPT = Path("plugin-security-checker/scripts/scan_plugin.py")
MAX_WORKERS = 4  # Parallel scans


def find_unique_plugins():
    """Find all unique plugins (exclude timestamped duplicates)"""
    plugins = []
    seen_names = set()

    for plugin_json in ARCHIVE_DIR.rglob("plugin.json"):
        plugin_dir = plugin_json.parent.parent  # .claude-plugin/plugin.json -> plugin_dir
        plugin_name = plugin_dir.name

        # Skip timestamped versions (e.g., plugin_20251019_123456)
        if "_202" in plugin_name and any(c.isdigit() for c in plugin_name.split("_")[-1]):
            continue

        # Skip duplicates
        if plugin_name in seen_names:
            continue

        seen_names.add(plugin_name)
        plugins.append((plugin_name, plugin_dir))

    return sorted(plugins)


def scan_plugin(plugin_name, plugin_dir, output_dir):
    """Scan a single plugin and save results"""
    safe_name = plugin_name.replace("/", "_").replace(" ", "_")
    output_file = output_dir / f"{safe_name}.json"

    # Skip if already scanned
    if output_file.exists():
        return {"status": "skipped", "plugin": plugin_name, "reason": "already_scanned"}

    try:
        # Run scanner
        result = subprocess.run(
            [
                sys.executable,
                str(SCANNER_SCRIPT),
                str(plugin_dir),
                "--output", str(output_file),
                "--format", "json"
            ],
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout per plugin
        )

        if result.returncode == 0:
            return {"status": "success", "plugin": plugin_name, "output": str(output_file)}
        else:
            return {"status": "failed", "plugin": plugin_name, "error": result.stderr[:200]}

    except subprocess.TimeoutExpired:
        return {"status": "timeout", "plugin": plugin_name}
    except Exception as e:
        return {"status": "error", "plugin": plugin_name, "error": str(e)[:200]}


def generate_summary(results, output_dir):
    """Generate summary statistics from scan results"""
    stats = {
        "scan_date": datetime.now().isoformat(),
        "total_plugins": len(results),
        "status_breakdown": defaultdict(int),
        "plugins_by_status": defaultdict(list)
    }

    for result in results:
        status = result["status"]
        stats["status_breakdown"][status] += 1
        stats["plugins_by_status"][status].append(result["plugin"])

    # Convert defaultdicts to regular dicts for JSON serialization
    stats["status_breakdown"] = dict(stats["status_breakdown"])
    stats["plugins_by_status"] = dict(stats["plugins_by_status"])

    summary_file = output_dir / "scan_summary.json"
    with open(summary_file, "w") as f:
        json.dump(stats, f, indent=2)

    return stats


def main():
    """Main batch scanning function"""
    print("=" * 60)
    print("Batch Archive Scanner - Minimal Token Usage")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find unique plugins
    print(f"\n[1/3] Finding unique plugins in {ARCHIVE_DIR}...")
    plugins = find_unique_plugins()
    print(f"Found {len(plugins)} unique plugins (excluding timestamped versions)")

    # Scan plugins in parallel
    print(f"\n[2/3] Scanning plugins (max {MAX_WORKERS} parallel)...")
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(scan_plugin, name, path, OUTPUT_DIR): name
            for name, path in plugins
        }

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)

            # Progress indicator every 50 plugins
            if i % 50 == 0 or i == len(plugins):
                success = sum(1 for r in results if r["status"] == "success")
                skipped = sum(1 for r in results if r["status"] == "skipped")
                failed = sum(1 for r in results if r["status"] in ["failed", "timeout", "error"])
                print(f"Progress: {i}/{len(plugins)} | Success: {success} | Skipped: {skipped} | Failed: {failed}")

    # Generate summary
    print(f"\n[3/3] Generating summary report...")
    stats = generate_summary(results, OUTPUT_DIR)

    # Print final summary
    print("\n" + "=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)
    print(f"Total plugins processed: {stats['total_plugins']}")
    print(f"Results directory: {OUTPUT_DIR}")
    print("\nStatus breakdown:")
    for status, count in stats["status_breakdown"].items():
        print(f"  {status.upper()}: {count}")

    print(f"\nSummary saved to: {OUTPUT_DIR}/scan_summary.json")
    print("Individual results saved as: <plugin-name>.json")


if __name__ == "__main__":
    main()
