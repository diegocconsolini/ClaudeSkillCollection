#!/usr/bin/env python3
"""
Excel Workbook Query Tool - Search and retrieve Excel content efficiently
"""

import json
import sys
from pathlib import Path
import re

def search_chunks(cache_key, query):
    """Search all chunks for query text"""
    cache_base = Path.home() / ".claude-xlsx-cache"
    cache_dir = cache_base / cache_key
    chunks_dir = cache_dir / "chunks"

    if not chunks_dir.exists():
        print(f"Error: Chunks not found. Run chunk_sheets.py first")
        return None

    # Load chunk index
    index_path = chunks_dir / "index.json"
    if not index_path.exists():
        print(f"Error: Chunk index not found")
        return None

    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    query_lower = query.lower()
    results = []

    print(f"Searching {index['total_chunks']} chunks for: '{query}'")

    for chunk_info in index["chunks"]:
        chunk_file = chunks_dir / chunk_info["file"]

        with open(chunk_file, "r", encoding="utf-8") as f:
            chunk = json.load(f)

        # Convert chunk data to searchable text
        chunk_text = json.dumps(chunk["data"], ensure_ascii=False).lower()

        # Search for query
        if query_lower in chunk_text:
            # Count matches
            match_count = chunk_text.count(query_lower)

            # Calculate relevance (simple: match count)
            relevance = min(100, match_count * 10)

            results.append({
                "chunk_id": chunk_info["chunk_id"],
                "sheet": chunk_info["sheet"],
                "type": chunk_info["type"],
                "rows": chunk_info["rows"],
                "columns": chunk_info["columns"],
                "tokens": chunk_info["tokens"],
                "matches": match_count,
                "relevance": relevance,
                "data": chunk["data"]
            })

    # Sort by relevance
    results.sort(key=lambda x: (-x["relevance"], -x["matches"]))

    return results

def get_sheet(cache_key, sheet_name):
    """Get all chunks for a specific sheet"""
    cache_base = Path.home() / ".claude-xlsx-cache"
    cache_dir = cache_base / cache_key
    chunks_dir = cache_dir / "chunks"

    if not chunks_dir.exists():
        print(f"Error: Chunks not found. Run chunk_sheets.py first")
        return None

    # Load chunk index
    index_path = chunks_dir / "index.json"
    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    results = []

    for chunk_info in index["chunks"]:
        if chunk_info["sheet"].lower() == sheet_name.lower():
            chunk_file = chunks_dir / chunk_info["file"]

            with open(chunk_file, "r", encoding="utf-8") as f:
                chunk = json.load(f)

            results.append({
                "chunk_id": chunk_info["chunk_id"],
                "sheet": chunk_info["sheet"],
                "type": chunk_info["type"],
                "rows": chunk_info["rows"],
                "columns": chunk_info["columns"],
                "tokens": chunk_info["tokens"],
                "data": chunk["data"]
            })

    return results

def get_summary(cache_key):
    """Get workbook summary"""
    cache_base = Path.home() / ".claude-xlsx-cache"
    cache_dir = cache_base / cache_key

    # Load manifest
    manifest_path = cache_dir / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Load metadata
    metadata_path = cache_dir / "metadata.json"
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Load chunk index
    chunks_dir = cache_dir / "chunks"
    if (chunks_dir / "index.json").exists():
        with open(chunks_dir / "index.json", "r", encoding="utf-8") as f:
            chunk_index = json.load(f)
    else:
        chunk_index = None

    summary = {
        "workbook": manifest["xlsx_name"],
        "sheets": metadata["sheet_count"],
        "sheet_names": metadata["sheet_names"],
        "total_cells": manifest["total_cells"],
        "formulas": manifest["formula_count"],
        "named_ranges": manifest["named_range_count"],
        "extracted_at": manifest["extracted_at"],
    }

    if chunk_index:
        summary.update({
            "chunks": chunk_index["total_chunks"],
            "total_tokens": chunk_index["total_tokens"],
            "avg_tokens_per_chunk": chunk_index["avg_tokens_per_chunk"],
            "content_preservation": chunk_index["content_preservation"],
        })

    return summary

def format_cell_output(cell_data, max_length=100):
    """Format cell data for display"""
    if cell_data is None:
        return "(empty)"

    value = cell_data.get("value")
    formula = cell_data.get("formula")

    if formula:
        return f"{formula} = {value}" if value else formula

    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length] + "..."

    return str(value) if value is not None else "(empty)"

def print_results(results, max_results=10):
    """Print search results"""
    if not results:
        print("No results found")
        return

    print(f"\nFound {len(results)} result(s):\n")

    for idx, result in enumerate(results[:max_results], 1):
        print(f"{idx}. Chunk {result['chunk_id']} - {result['sheet']}")
        print(f"   Range: {result['columns']}, Rows {result['rows']}")
        print(f"   Type: {result['type']}")

        if "relevance" in result:
            print(f"   Relevance: {result['relevance']}%")
            print(f"   Matches: {result['matches']}")

        print(f"   Tokens: {result['tokens']}")

        # Show sample data (first few non-empty cells)
        data = result["data"]
        cells_shown = 0
        max_cells = 5

        print(f"   Sample data:")

        for row_idx, row in enumerate(data[:10]):  # Show first 10 rows max
            if row and isinstance(row, list):
                for col_idx, cell in enumerate(row):
                    if cell and cells_shown < max_cells:
                        coord = f"{chr(65 + col_idx)}{row_idx + 1}"
                        formatted = format_cell_output(cell)
                        print(f"     {coord}: {formatted}")
                        cells_shown += 1

            if cells_shown >= max_cells:
                break

        print()

    total_tokens = sum(r["tokens"] for r in results[:max_results])
    print(f"Total tokens for displayed results: {total_tokens:,}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python query_xlsx.py search <cache_key> 'query text'")
        print("  python query_xlsx.py sheet <cache_key> 'sheet_name'")
        print("  python query_xlsx.py summary <cache_key>")
        sys.exit(1)

    command = sys.argv[1]
    cache_key = sys.argv[2]

    if command == "search":
        if len(sys.argv) < 4:
            print("Error: Query text required")
            sys.exit(1)

        query = sys.argv[3]
        results = search_chunks(cache_key, query)

        if results:
            print_results(results)

    elif command == "sheet":
        if len(sys.argv) < 4:
            print("Error: Sheet name required")
            sys.exit(1)

        sheet_name = sys.argv[3]
        results = get_sheet(cache_key, sheet_name)

        if results:
            print(f"\nSheet: {sheet_name}")
            print(f"Chunks: {len(results)}\n")
            print_results(results)
        else:
            print(f"Sheet not found: {sheet_name}")

    elif command == "summary":
        summary = get_summary(cache_key)

        if summary:
            print("\n" + "="*60)
            print("Workbook Summary")
            print("="*60)
            print(f"File: {summary['workbook']}")
            print(f"Sheets: {summary['sheets']}")
            print(f"Sheet names: {', '.join(summary['sheet_names'])}")
            print(f"Total cells: {summary['total_cells']:,}")
            print(f"Formulas: {summary['formulas']:,}")
            print(f"Named ranges: {summary['named_ranges']}")

            if "chunks" in summary:
                print(f"\nChunking Statistics:")
                print(f"  Total chunks: {summary['chunks']}")
                print(f"  Total tokens: {summary['total_tokens']:,}")
                print(f"  Avg tokens/chunk: {summary['avg_tokens_per_chunk']}")
                print(f"  Content preservation: {summary['content_preservation']}")

            print(f"\nExtracted: {summary['extracted_at']}")
            print("="*60 + "\n")

    else:
        print(f"Unknown command: {command}")
        print("Available commands: search, sheet, summary")
        sys.exit(1)
