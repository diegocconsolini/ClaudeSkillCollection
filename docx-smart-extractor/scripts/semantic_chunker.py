#!/usr/bin/env python3
"""
DOCX Smart Extractor - semantic_chunker.py

Intelligently chunks Word document content into semantically meaningful pieces:
- By heading hierarchy (H1, H2, H3 sections)
- By paragraph groups (10-20 paragraphs per chunk)
- By tables (each table as separate chunk)
- Target chunk size: 500-2000 tokens

Chunking strategies:
1. Small documents (<50 paragraphs): Single chunk
2. Well-structured documents: Chunk by heading sections
3. Large documents: Chunk by paragraph ranges
4. Tables: Always separate chunks

No BS metrics - just efficient, queryable chunks.
"""

import sys
import json
from pathlib import Path


def get_cache_dir():
    """Get cache directory"""
    cache_dir = Path.home() / ".claude-docx-cache"
    if not cache_dir.exists():
        print(f"Error: Cache directory not found: {cache_dir}")
        print("Run extract_docx.py first")
        sys.exit(1)
    return cache_dir


def estimate_tokens(text):
    """Rough token estimation: chars / 4"""
    return len(text) // 4


def chunk_by_headings(content, metadata):
    """Chunk document by heading hierarchy"""
    chunks = []
    current_chunk = {
        "paragraphs": [],
        "heading": None,
        "level": 0
    }

    heading_styles = ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Title']

    for para in content["paragraphs"]:
        style = para.get("style", "")

        # Check if this is a heading
        if style in heading_styles:
            # Save previous chunk if it has content
            if current_chunk["paragraphs"]:
                chunks.append(current_chunk)

            # Start new chunk
            current_chunk = {
                "paragraphs": [para],
                "heading": para["text"],
                "level": int(style.split()[-1]) if "Heading" in style else 0
            }
        else:
            # Add to current chunk
            current_chunk["paragraphs"].append(para)

    # Add final chunk
    if current_chunk["paragraphs"]:
        chunks.append(current_chunk)

    return chunks


def chunk_by_paragraphs(content, paragraphs_per_chunk=15):
    """Chunk document by paragraph ranges"""
    chunks = []
    paragraphs = content["paragraphs"]

    for i in range(0, len(paragraphs), paragraphs_per_chunk):
        chunk_paras = paragraphs[i:i + paragraphs_per_chunk]
        chunks.append({
            "paragraphs": chunk_paras,
            "heading": f"Paragraphs {i+1}-{i+len(chunk_paras)}",
            "level": 0
        })

    return chunks


def chunk_tables(content):
    """Extract tables as separate chunks"""
    table_chunks = []

    for table in content["tables"]:
        # Calculate table text
        table_text = ""
        for row in table["data"]["cells"]:
            for cell in row:
                table_text += cell["text"] + " "

        table_chunks.append({
            "type": "table",
            "index": table["index"],
            "table_data": table["data"],
            "text": table_text.strip(),
            "tokens": estimate_tokens(table_text)
        })

    return table_chunks


def chunk_document(cache_key):
    """
    Chunk Word document content into semantically meaningful pieces

    Args:
        cache_key: Cache key from extract_docx.py

    Returns:
        cache_key: Same cache key
    """
    cache_dir = get_cache_dir() / cache_key

    if not cache_dir.exists():
        print(f"Error: Cache not found: {cache_key}")
        print(f"Run: python scripts/extract_docx.py <file> first")
        sys.exit(1)

    # Load metadata and content
    with open(cache_dir / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    with open(cache_dir / "content.json", "r", encoding="utf-8") as f:
        content = json.load(f)

    print(f"Chunking document: {metadata['filename']}")
    print(f"Paragraphs: {len(content['paragraphs'])}")
    print(f"Tables: {len(content['tables'])}")

    # Determine chunking strategy
    total_paragraphs = len(content["paragraphs"])

    # Check if document has heading structure
    heading_count = sum(1 for p in content["paragraphs"]
                       if p.get("style", "").startswith("Heading"))

    if total_paragraphs < 50:
        print("  Strategy: Single chunk (small document)")
        para_chunks = [{
            "paragraphs": content["paragraphs"],
            "heading": "Full Document",
            "level": 0
        }]
    elif heading_count > 3:
        print(f"  Strategy: Chunk by headings ({heading_count} headings)")
        para_chunks = chunk_by_headings(content, metadata)
    else:
        print("  Strategy: Chunk by paragraph ranges")
        para_chunks = chunk_by_paragraphs(content)

    # Extract table chunks
    table_chunks = chunk_tables(content)

    # Create final chunks
    all_chunks = []
    chunk_id = 1

    # Add paragraph chunks
    for chunk_data in para_chunks:
        # Calculate chunk text and tokens
        chunk_text = "\n\n".join(p["text"] for p in chunk_data["paragraphs"])
        chunk_tokens = estimate_tokens(chunk_text)

        chunk = {
            "chunk_id": chunk_id,
            "type": "paragraphs",
            "heading": chunk_data["heading"],
            "level": chunk_data["level"],
            "paragraph_count": len(chunk_data["paragraphs"]),
            "text": chunk_text,
            "tokens": chunk_tokens,
            "paragraphs": chunk_data["paragraphs"]
        }

        all_chunks.append(chunk)
        chunk_id += 1

        heading_display = (chunk_data['heading'] or "Untitled")[:50]
        print(f"  Created chunk {chunk_id-1}: {heading_display}... ({chunk_tokens} tokens)")

    # Add table chunks
    for table_chunk in table_chunks:
        table_chunk["chunk_id"] = chunk_id
        all_chunks.append(table_chunk)
        chunk_id += 1

        print(f"  Created chunk {chunk_id-1}: Table {table_chunk['index']+1} ({table_chunk['tokens']} tokens)")

    # Save chunks
    chunks_dir = cache_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)

    for chunk in all_chunks:
        chunk_filename = f"chunk_{chunk['chunk_id']:03d}.json"
        with open(chunks_dir / chunk_filename, "w", encoding="utf-8") as f:
            json.dump(chunk, f, indent=2, ensure_ascii=False)

    # Calculate statistics
    total_tokens = sum(chunk["tokens"] for chunk in all_chunks)
    avg_tokens = total_tokens // len(all_chunks) if all_chunks else 0

    # Count chunk types
    chunk_types = {}
    for chunk in all_chunks:
        chunk_type = chunk["type"]
        chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1

    # Create chunk index
    chunk_index = {
        "cache_key": cache_key,
        "total_chunks": len(all_chunks),
        "total_tokens": total_tokens,
        "avg_tokens_per_chunk": avg_tokens,
        "chunk_types": chunk_types,
        "chunks": [
            {
                "chunk_id": chunk["chunk_id"],
                "type": chunk["type"],
                "heading": chunk.get("heading", f"Table {chunk.get('index', 0)+1}"),
                "tokens": chunk["tokens"]
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
    print(f"\nChunk types:")
    for chunk_type, count in chunk_types.items():
        print(f"  - {chunk_type}: {count}")

    print(f"\nNext step:")
    print(f"Query content: python scripts/query_docx.py search {cache_key} 'your query'")

    return cache_key


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python semantic_chunker.py <cache_key>")
        print("\nExample:")
        print("  python semantic_chunker.py document_name_a8f9e2c1")
        sys.exit(1)

    cache_key = sys.argv[1]
    chunk_document(cache_key)
