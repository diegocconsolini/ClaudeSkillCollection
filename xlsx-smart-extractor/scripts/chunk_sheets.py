#!/usr/bin/env python3
"""
Excel Workbook Chunker - Split sheets into semantic chunks for efficient querying
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def estimate_tokens(data):
    """Estimate token count (rough approximation: chars / 4)"""
    if isinstance(data, dict):
        char_count = len(json.dumps(data, ensure_ascii=False))
    elif isinstance(data, str):
        char_count = len(data)
    else:
        char_count = len(str(data))
    return char_count // 4

def chunk_sheet(sheet_data, sheet_name, chunk_size_target=2000):
    """
    Chunk a single sheet based on structure

    Strategies:
    - Small sheets (<1000 cells): single chunk
    - Wide tables (>20 columns): split by column groups
    - Long tables (>500 rows): split by row ranges
    """
    chunks = []

    cells = sheet_data.get("cells", [])
    max_row = sheet_data.get("max_row", 0)
    max_column = sheet_data.get("max_column", 0)

    total_cells = max_row * max_column

    # Strategy 1: Small sheets - single chunk
    if total_cells < 1000:
        chunk = {
            "sheet": sheet_name,
            "type": "full_sheet",
            "rows": f"1-{max_row}",
            "columns": f"A-{chr(64 + max_column)}" if max_column <= 26 else f"A-?",
            "data": cells
        }
        chunks.append(chunk)
        return chunks

    # Strategy 2: Long tables - split by rows
    if max_row > 500:
        rows_per_chunk = 250

        for start_row in range(0, max_row, rows_per_chunk):
            end_row = min(start_row + rows_per_chunk, max_row)

            chunk_cells = cells[start_row:end_row]

            # Include header row if not the first chunk
            if start_row > 0 and len(cells) > 0:
                header_row = cells[0]
                chunk_cells = [header_row] + chunk_cells

            chunk = {
                "sheet": sheet_name,
                "type": "row_range",
                "rows": f"{start_row + 1}-{end_row}",
                "columns": f"A-{chr(64 + max_column)}" if max_column <= 26 else f"A-?",
                "data": chunk_cells
            }
            chunks.append(chunk)

        return chunks

    # Strategy 3: Wide tables - split by column groups
    if max_column > 20:
        cols_per_chunk = 10

        for start_col in range(0, max_column, cols_per_chunk):
            end_col = min(start_col + cols_per_chunk, max_column)

            # Extract column slice from each row
            chunk_cells = []
            for row in cells:
                if row:
                    chunk_row = row[start_col:end_col]
                    chunk_cells.append(chunk_row)

            start_letter = chr(65 + start_col) if start_col < 26 else f"Col{start_col + 1}"
            end_letter = chr(65 + end_col - 1) if end_col <= 26 else f"Col{end_col}"

            chunk = {
                "sheet": sheet_name,
                "type": "column_range",
                "rows": f"1-{max_row}",
                "columns": f"{start_letter}-{end_letter}",
                "data": chunk_cells
            }
            chunks.append(chunk)

        return chunks

    # Default: medium-sized sheet - single chunk
    chunk = {
        "sheet": sheet_name,
        "type": "full_sheet",
        "rows": f"1-{max_row}",
        "columns": f"A-{chr(64 + max_column)}" if max_column <= 26 else f"A-?",
        "data": cells
    }
    chunks.append(chunk)

    return chunks

def chunk_workbook(cache_key):
    """Chunk entire workbook"""
    cache_base = Path.home() / ".claude-xlsx-cache"
    cache_dir = cache_base / cache_key

    if not cache_dir.exists():
        print(f"Error: Cache key not found: {cache_key}")
        print(f"Run extract_xlsx.py first")
        return None

    # Load manifest
    manifest_path = cache_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"Error: Manifest not found in cache")
        return None

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"Chunking workbook: {manifest['xlsx_name']}")
    print(f"Sheets: {manifest['sheet_count']}")

    # Load full workbook data
    full_workbook_path = cache_dir / "full_workbook.json"
    with open(full_workbook_path, "r", encoding="utf-8") as f:
        workbook_data = json.load(f)

    all_chunks = []
    chunk_stats = defaultdict(int)

    # Process each sheet
    for sheet_data in workbook_data["sheets"]:
        sheet_name = sheet_data["name"]
        print(f"  Chunking sheet: {sheet_name}")

        sheet_chunks = chunk_sheet(sheet_data, sheet_name)

        for chunk in sheet_chunks:
            chunk["chunk_id"] = len(all_chunks) + 1
            chunk["tokens"] = estimate_tokens(chunk["data"])
            all_chunks.append(chunk)
            chunk_stats[chunk["type"]] += 1

        print(f"    Created {len(sheet_chunks)} chunks")

    # Create chunks directory
    chunks_dir = cache_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)

    # Save individual chunks
    print(f"\nSaving {len(all_chunks)} chunks...")

    for chunk in all_chunks:
        chunk_id = chunk["chunk_id"]
        chunk_filename = f"chunk_{chunk_id:03d}.json"

        with open(chunks_dir / chunk_filename, "w", encoding="utf-8") as f:
            json.dump(chunk, f, indent=2, ensure_ascii=False)

    # Calculate statistics
    total_tokens = sum(chunk["tokens"] for chunk in all_chunks)
    avg_tokens = total_tokens // len(all_chunks) if all_chunks else 0

    # Calculate content preservation
    original_chars = sum(
        len(json.dumps(sheet["cells"], ensure_ascii=False))
        for sheet in workbook_data["sheets"]
    )

    chunked_chars = sum(
        len(json.dumps(chunk["data"], ensure_ascii=False))
        for chunk in all_chunks
    )

    preservation_rate = (chunked_chars / original_chars * 100) if original_chars > 0 else 100

    # Create chunk index
    chunk_index = {
        "cache_key": cache_key,
        "total_chunks": len(all_chunks),
        "total_tokens": total_tokens,
        "avg_tokens_per_chunk": avg_tokens,
        "content_preservation": f"{preservation_rate:.2f}%",
        "chunk_types": dict(chunk_stats),
        "chunks": [
            {
                "chunk_id": chunk["chunk_id"],
                "sheet": chunk["sheet"],
                "type": chunk["type"],
                "rows": chunk["rows"],
                "columns": chunk["columns"],
                "tokens": chunk["tokens"],
                "file": f"chunk_{chunk['chunk_id']:03d}.json"
            }
            for chunk in all_chunks
        ]
    }

    with open(chunks_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(chunk_index, f, indent=2, ensure_ascii=False)

    print(f"\nChunking complete!")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Avg tokens/chunk: {avg_tokens}")
    print(f"Content preservation: {preservation_rate:.2f}%")
    print(f"\nChunk types:")
    for chunk_type, count in chunk_stats.items():
        print(f"  - {chunk_type}: {count}")

    return cache_key

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chunk_sheets.py <cache_key>")
        sys.exit(1)

    cache_key = sys.argv[1]

    result = chunk_workbook(cache_key)

    if result:
        print(f"\nNext step:")
        print(f"Query content: python scripts/query_xlsx.py search {cache_key} 'your query'")
