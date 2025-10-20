#!/usr/bin/env python3
"""
Query Engine - Efficiently search and retrieve PDF chunks
Returns only relevant chunks to minimize token usage
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a search result"""
    chunk_id: int
    relevance_score: float
    title: str
    preview: str
    estimated_tokens: int
    match_count: int


class PDFQueryEngine:
    """Search and retrieve PDF chunks efficiently"""

    def __init__(self, cache_dir: str = None):
        """Initialize query engine"""
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.claude-pdf-cache")

        self.cache_dir = Path(cache_dir)

    def list_cached_pdfs(self) -> List[Dict]:
        """List all cached PDFs"""
        if not self.cache_dir.exists():
            return []

        cached_pdfs = []

        for cache_path in self.cache_dir.iterdir():
            if not cache_path.is_dir():
                continue

            manifest_path = cache_path / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)

                cached_pdfs.append({
                    'cache_key': manifest['cache_key'],
                    'pdf_name': manifest['pdf_name'],
                    'page_count': manifest['statistics']['page_count'],
                    'estimated_tokens': manifest['statistics']['estimated_tokens'],
                    'has_chunks': (cache_path / 'chunks.json').exists()
                })

        return cached_pdfs

    def load_chunks_index(self, cache_key: str) -> Optional[Dict]:
        """Load chunks index for a PDF"""
        cache_path = self.cache_dir / cache_key
        chunks_path = cache_path / "chunks.json"

        if not chunks_path.exists():
            return None

        with open(chunks_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search_chunks(self, cache_key: str, query: str,
                      max_results: int = 5, min_relevance: float = 0.1) -> List[SearchResult]:
        """
        Search chunks for relevant content

        Args:
            cache_key: PDF cache key
            query: Search query (keywords or phrase)
            max_results: Maximum number of results to return
            min_relevance: Minimum relevance score (0.0 to 1.0)

        Returns:
            List of search results sorted by relevance
        """
        chunks_index = self.load_chunks_index(cache_key)

        if not chunks_index:
            return []

        results = []
        query_terms = query.lower().split()

        for chunk in chunks_index['chunks']:
            content_lower = chunk['content'].lower()
            title_lower = chunk['title'].lower()

            # Count matches in content and title
            content_matches = sum(content_lower.count(term) for term in query_terms)
            title_matches = sum(title_lower.count(term) for term in query_terms)

            # Calculate relevance score
            # Title matches weighted higher (3x)
            total_matches = content_matches + (title_matches * 3)

            if total_matches == 0:
                continue

            # Normalize by content length
            relevance = total_matches / (len(chunk['content']) / 1000)
            relevance = min(relevance, 1.0)  # Cap at 1.0

            if relevance < min_relevance:
                continue

            # Create preview (first match context)
            preview = self._create_preview(chunk['content'], query_terms)

            results.append(SearchResult(
                chunk_id=chunk['chunk_id'],
                relevance_score=relevance,
                title=chunk['title'],
                preview=preview,
                estimated_tokens=chunk['estimated_tokens'],
                match_count=total_matches
            ))

        # Sort by relevance
        results.sort(key=lambda r: r.relevance_score, reverse=True)

        return results[:max_results]

    def _create_preview(self, content: str, query_terms: List[str], context_chars: int = 200) -> str:
        """Create preview showing first match with context"""
        content_lower = content.lower()

        # Find first match
        first_match_pos = len(content)
        for term in query_terms:
            pos = content_lower.find(term)
            if pos != -1 and pos < first_match_pos:
                first_match_pos = pos

        if first_match_pos == len(content):
            # No match, return beginning
            return content[:context_chars] + "..."

        # Get context around match
        start = max(0, first_match_pos - context_chars // 2)
        end = min(len(content), first_match_pos + context_chars // 2)

        preview = content[start:end]

        # Clean up
        if start > 0:
            preview = "..." + preview
        if end < len(content):
            preview = preview + "..."

        return preview.strip()

    def get_chunk_content(self, cache_key: str, chunk_id: int) -> Optional[str]:
        """Retrieve content of a specific chunk"""
        cache_path = self.cache_dir / cache_key / "chunks" / f"chunk_{chunk_id:04d}.txt"

        if not cache_path.exists():
            return None

        with open(cache_path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_multiple_chunks(self, cache_key: str, chunk_ids: List[int]) -> str:
        """Retrieve and combine multiple chunks"""
        contents = []

        for chunk_id in chunk_ids:
            content = self.get_chunk_content(cache_key, chunk_id)
            if content:
                contents.append(f"=== Chunk {chunk_id} ===\n\n{content}")

        return "\n\n".join(contents)

    def get_chunk_range(self, cache_key: str, start_id: int, end_id: int) -> str:
        """Retrieve a range of consecutive chunks"""
        chunk_ids = list(range(start_id, end_id + 1))
        return self.get_multiple_chunks(cache_key, chunk_ids)

    def get_toc(self, cache_key: str) -> Optional[List[Dict]]:
        """Get table of contents if available"""
        cache_path = self.cache_dir / cache_key
        toc_path = cache_path / "toc.json"

        if not toc_path.exists():
            return None

        with open(toc_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_metadata(self, cache_key: str) -> Optional[Dict]:
        """Get PDF metadata"""
        cache_path = self.cache_dir / cache_key
        metadata_path = cache_path / "metadata.json"

        if not metadata_path.exists():
            return None

        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_statistics(self, cache_key: str) -> Optional[Dict]:
        """Get extraction and chunking statistics"""
        cache_path = self.cache_dir / cache_key
        manifest_path = cache_path / "manifest.json"

        if not manifest_path.exists():
            return None

        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        stats = manifest.get('statistics', {})

        # Add chunking stats if available
        chunks_path = cache_path / "chunks.json"
        if chunks_path.exists():
            with open(chunks_path, 'r', encoding='utf-8') as f:
                chunks_data = json.load(f)
                stats['chunking'] = chunks_data.get('statistics', {})

        return stats


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python query_pdf.py list")
        print("  python query_pdf.py search <cache_key> <query>")
        print("  python query_pdf.py get <cache_key> <chunk_id>")
        print("  python query_pdf.py stats <cache_key>")
        print("  python query_pdf.py toc <cache_key>")
        sys.exit(1)

    command = sys.argv[1]
    engine = PDFQueryEngine()

    if command == 'list':
        pdfs = engine.list_cached_pdfs()
        if not pdfs:
            print("No cached PDFs found")
            sys.exit(0)

        print(f"Found {len(pdfs)} cached PDF(s):\n")
        for pdf in pdfs:
            print(f"Cache Key: {pdf['cache_key']}")
            print(f"  Name: {pdf['pdf_name']}")
            print(f"  Pages: {pdf['page_count']}")
            print(f"  Tokens: {pdf['estimated_tokens']:,}")
            print(f"  Chunked: {'Yes' if pdf['has_chunks'] else 'No'}")
            print()

    elif command == 'search':
        if len(sys.argv) < 4:
            print("Usage: python query_pdf.py search <cache_key> <query>")
            sys.exit(1)

        cache_key = sys.argv[2]
        query = ' '.join(sys.argv[3:])

        results = engine.search_chunks(cache_key, query)

        if not results:
            print(f"No results found for: {query}")
            sys.exit(0)

        print(f"Found {len(results)} result(s) for '{query}':\n")

        total_tokens = 0
        for i, result in enumerate(results, 1):
            print(f"{i}. Chunk {result.chunk_id} - {result.title}")
            print(f"   Relevance: {result.relevance_score:.2%}")
            print(f"   Matches: {result.match_count}")
            print(f"   Tokens: {result.estimated_tokens:,}")
            print(f"   Preview: {result.preview[:150]}...")
            print()
            total_tokens += result.estimated_tokens

        print(f"Total tokens for all results: {total_tokens:,}")

    elif command == 'get':
        if len(sys.argv) < 4:
            print("Usage: python query_pdf.py get <cache_key> <chunk_id>")
            sys.exit(1)

        cache_key = sys.argv[2]
        chunk_id = int(sys.argv[3])

        content = engine.get_chunk_content(cache_key, chunk_id)

        if content:
            print(content)
        else:
            print(f"Chunk {chunk_id} not found")

    elif command == 'stats':
        if len(sys.argv) < 3:
            print("Usage: python query_pdf.py stats <cache_key>")
            sys.exit(1)

        cache_key = sys.argv[2]
        stats = engine.get_statistics(cache_key)

        if stats:
            print("Extraction Statistics:")
            print(f"  Pages: {stats.get('page_count', 'N/A')}")
            print(f"  Characters: {stats.get('char_count', 0):,}")
            print(f"  Words: {stats.get('word_count', 0):,}")
            print(f"  Estimated tokens: {stats.get('estimated_tokens', 0):,}")
            print(f"  File size: {stats.get('file_size_mb', 0):.2f} MB")

            if 'chunking' in stats:
                print("\nChunking Statistics:")
                chunking = stats['chunking']
                print(f"  Total chunks: {chunking.get('total_chunks', 'N/A')}")
                print(f"  Avg tokens/chunk: {chunking.get('avg_tokens_per_chunk', 0):,}")
                print(f"  Content preservation: {chunking.get('preservation_rate', 0):.2f}%")
        else:
            print(f"Statistics not found for {cache_key}")

    elif command == 'toc':
        if len(sys.argv) < 3:
            print("Usage: python query_pdf.py toc <cache_key>")
            sys.exit(1)

        cache_key = sys.argv[2]
        toc = engine.get_toc(cache_key)

        if toc:
            print("Table of Contents:\n")
            for entry in toc:
                indent = "  " * (entry['level'] - 1)
                print(f"{indent}{entry['title']} (page {entry['page']})")
        else:
            print("No table of contents available")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
