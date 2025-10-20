#!/usr/bin/env python3
"""
DOCX Smart Extractor - query_docx.py

Query extracted and chunked Word document content:
- search: Keyword search across all chunks
- heading: Get specific section by heading
- table: Get specific table
- summary: Get document metadata and statistics

Relevance scoring: Simple keyword match count.
No fancy algorithms - just fast, effective search.
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


def search_chunks(cache_key, query):
    """Search for keyword across all chunks"""
    cache_dir = get_cache_dir() / cache_key
    chunks_dir = cache_dir / "chunks"

    if not chunks_dir.exists():
        print(f"Error: Chunks not found. Run semantic_chunker.py first")
        sys.exit(1)

    # Load chunk index
    with open(chunks_dir / "index.json", "r", encoding="utf-8") as f:
        index = json.load(f)

    query_lower = query.lower()
    results = []

    print(f"Searching {index['total_chunks']} chunks for: '{query}'")
    print()

    # Search each chunk
    for chunk_info in index["chunks"]:
        chunk_file = chunks_dir / f"chunk_{chunk_info['chunk_id']:03d}.json"

        with open(chunk_file, "r", encoding="utf-8") as f:
            chunk = json.load(f)

        # Count matches in chunk text
        chunk_text_lower = chunk["text"].lower()
        match_count = chunk_text_lower.count(query_lower)

        if match_count > 0:
            # Calculate relevance (simple: match count * 10, capped at 100)
            relevance = min(match_count * 10, 100)

            results.append({
                "chunk": chunk,
                "match_count": match_count,
                "relevance": relevance
            })

    # Sort by relevance and match count
    results.sort(key=lambda x: (x["relevance"], x["match_count"]), reverse=True)

    if not results:
        print(f"No results found for: '{query}'")
        return

    print(f"Found {len(results)} result(s):\n")

    for idx, result in enumerate(results, 1):
        chunk = result["chunk"]
        heading = chunk.get("heading", f"Table {chunk.get('index', 0)+1}")

        print(f"{idx}. Chunk {chunk['chunk_id']} - {heading}")
        print(f"   Type: {chunk['type']}")
        print(f"   Relevance: {result['relevance']}%")
        print(f"   Matches: {result['match_count']}")
        print(f"   Tokens: {chunk['tokens']}")

        # Show sample text (first 200 chars)
        sample_text = chunk["text"][:200].replace("\n", " ")
        print(f"   Sample: {sample_text}...")
        print()

    total_tokens = sum(r["chunk"]["tokens"] for r in results)
    print(f"Total tokens for displayed results: {total_tokens:,}")


def get_heading(cache_key, heading_query):
    """Get specific section by heading"""
    cache_dir = get_cache_dir() / cache_key
    chunks_dir = cache_dir / "chunks"

    if not chunks_dir.exists():
        print(f"Error: Chunks not found. Run semantic_chunker.py first")
        sys.exit(1)

    # Load chunk index
    with open(chunks_dir / "index.json", "r", encoding="utf-8") as f:
        index = json.load(f)

    heading_lower = heading_query.lower()
    found = False

    for chunk_info in index["chunks"]:
        chunk_heading = chunk_info.get("heading", "")

        if heading_lower in chunk_heading.lower():
            chunk_file = chunks_dir / f"chunk_{chunk_info['chunk_id']:03d}.json"

            with open(chunk_file, "r", encoding="utf-8") as f:
                chunk = json.load(f)

            print(f"Heading: {chunk_heading}")
            print(f"Type: {chunk['type']}")
            print(f"Tokens: {chunk['tokens']}")
            print()
            print(chunk["text"])
            print()

            found = True
            break

    if not found:
        print(f"Heading not found: '{heading_query}'")
        print("\nAvailable headings:")
        for chunk_info in index["chunks"]:
            if chunk_info["type"] == "paragraphs":
                print(f"  - {chunk_info['heading']}")


def get_summary(cache_key):
    """Get document summary"""
    cache_dir = get_cache_dir() / cache_key

    # Load metadata
    with open(cache_dir / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Load manifest
    with open(cache_dir / "manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Load chunk index if available
    chunks_dir = cache_dir / "chunks"
    if chunks_dir.exists():
        with open(chunks_dir / "index.json", "r", encoding="utf-8") as f:
            chunk_index = json.load(f)
    else:
        chunk_index = None

    print("=" * 60)
    print("Document Summary")
    print("=" * 60)
    print(f"Filename: {metadata['filename']}")
    print(f"File size: {metadata['file_size'] / 1024 / 1024:.2f} MB")
    print(f"Author: {metadata.get('author', 'N/A')}")
    print(f"Title: {metadata.get('title', 'N/A')}")
    print(f"Created: {metadata.get('created', 'N/A')}")
    print(f"Modified: {metadata.get('modified', 'N/A')}")
    print()
    print(f"Total paragraphs: {manifest['total_paragraphs']}")
    print(f"Total tables: {manifest['total_tables']}")
    print(f"Total sections: {manifest['total_sections']}")
    print(f"Total characters: {manifest['total_characters']:,}")
    print()

    if chunk_index:
        print("Chunking Statistics:")
        print(f"  Total chunks: {chunk_index['total_chunks']}")
        print(f"  Total tokens: {chunk_index['total_tokens']:,}")
        print(f"  Avg tokens/chunk: {chunk_index['avg_tokens_per_chunk']}")
        print()
        print("Chunk types:")
        for chunk_type, count in chunk_index['chunk_types'].items():
            print(f"  - {chunk_type}: {count}")
    else:
        print("Document not chunked yet. Run semantic_chunker.py")

    print()
    print(f"Extracted: {metadata['extracted_at']}")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python query_docx.py <command> <cache_key> [query]")
        print("\nCommands:")
        print("  search <cache_key> <query>   - Search for keyword")
        print("  heading <cache_key> <query>  - Get section by heading")
        print("  summary <cache_key>          - Get document metadata")
        print("\nExamples:")
        print("  python query_docx.py search document_a8f9e2 'security policy'")
        print("  python query_docx.py heading document_a8f9e2 'Introduction'")
        print("  python query_docx.py summary document_a8f9e2")
        sys.exit(1)

    command = sys.argv[1]
    cache_key = sys.argv[2]

    if command == "search":
        if len(sys.argv) < 4:
            print("Error: Missing search query")
            sys.exit(1)
        query = " ".join(sys.argv[3:])
        search_chunks(cache_key, query)

    elif command == "heading":
        if len(sys.argv) < 4:
            print("Error: Missing heading query")
            sys.exit(1)
        heading_query = " ".join(sys.argv[3:])
        get_heading(cache_key, heading_query)

    elif command == "summary":
        get_summary(cache_key)

    else:
        print(f"Error: Unknown command: {command}")
        print("Valid commands: search, heading, summary")
        sys.exit(1)
