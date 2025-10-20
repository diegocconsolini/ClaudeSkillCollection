#!/usr/bin/env python3
"""
Semantic Chunker - Split text at intelligent boundaries without losing content
Preserves 100% of content while organizing for efficient token usage
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class SemanticBoundary:
    """Represents a detected semantic boundary in text"""
    position: int
    type: str  # 'section', 'chapter', 'appendix', 'paragraph'
    title: str
    confidence: float  # 0.0 to 1.0


@dataclass
class TextChunk:
    """Represents a semantic chunk of text"""
    chunk_id: int
    start_pos: int
    end_pos: int
    content: str
    boundary_type: str
    title: str
    char_count: int
    word_count: int
    estimated_tokens: int
    page_range: Optional[Tuple[int, int]] = None


class SemanticChunker:
    """Split text at semantic boundaries while preserving all content"""

    def __init__(self, target_chunk_size: int = 2000):
        """
        Initialize chunker

        Args:
            target_chunk_size: Target tokens per chunk (will respect boundaries)
        """
        self.target_chunk_size = target_chunk_size

        # Patterns for detecting semantic boundaries
        self.patterns = {
            'chapter': [
                r'\n\n(Chapter\s+\d+[\s:\.][^\n]+)',
                r'\n\n(CHAPTER\s+\d+[\s:\.][^\n]+)',
            ],
            'section': [
                r'\n\n(\d+\.\d+[\s\.][^\n]+)',  # 1.1 Section Title
                r'\n\n(\d+\.\d+\.\d+[\s\.][^\n]+)',  # 1.1.1 Subsection
                r'\n\n([A-Z][^\n]{3,80})\n',  # ALL CAPS SECTION
            ],
            'appendix': [
                r'\n\n(Appendix\s+[A-Z][\s:\.][^\n]+)',
                r'\n\n(APPENDIX\s+[A-Z][\s:\.][^\n]+)',
            ],
            'paragraph': [
                r'\n\n+',  # Double line break = paragraph boundary
            ]
        }

    def detect_boundaries(self, text: str) -> List[SemanticBoundary]:
        """
        Detect all semantic boundaries in text

        Args:
            text: Full text content

        Returns:
            List of detected boundaries, sorted by position
        """
        boundaries = []

        # Detect chapters
        for pattern in self.patterns['chapter']:
            for match in re.finditer(pattern, text, re.MULTILINE):
                boundaries.append(SemanticBoundary(
                    position=match.start(),
                    type='chapter',
                    title=match.group(1).strip(),
                    confidence=0.95
                ))

        # Detect appendices
        for pattern in self.patterns['appendix']:
            for match in re.finditer(pattern, text, re.MULTILINE):
                boundaries.append(SemanticBoundary(
                    position=match.start(),
                    type='appendix',
                    title=match.group(1).strip(),
                    confidence=0.95
                ))

        # Detect sections
        for pattern in self.patterns['section']:
            for match in re.finditer(pattern, text, re.MULTILINE):
                # Skip if too close to chapter/appendix boundary
                if not any(abs(b.position - match.start()) < 20
                           for b in boundaries if b.type in ['chapter', 'appendix']):
                    title = match.group(1).strip() if match.groups() else ''
                    boundaries.append(SemanticBoundary(
                        position=match.start(),
                        type='section',
                        title=title,
                        confidence=0.85
                    ))

        # Detect paragraphs (lower priority)
        for match in re.finditer(self.patterns['paragraph'][0], text):
            # Only add if not near other boundaries
            if not any(abs(b.position - match.start()) < 50 for b in boundaries):
                boundaries.append(SemanticBoundary(
                    position=match.start(),
                    type='paragraph',
                    title='',
                    confidence=0.60
                ))

        # Sort by position
        boundaries.sort(key=lambda b: b.position)

        # Remove duplicates (keep highest confidence)
        filtered_boundaries = []
        for boundary in boundaries:
            if not any(abs(b.position - boundary.position) < 10
                       for b in filtered_boundaries):
                filtered_boundaries.append(boundary)

        return filtered_boundaries

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters for English)"""
        return len(text) // 4

    def split_at_boundaries(self, text: str, boundaries: List[SemanticBoundary]) -> List[TextChunk]:
        """
        Split text into chunks at semantic boundaries

        Args:
            text: Full text content
            boundaries: List of detected boundaries

        Returns:
            List of text chunks
        """
        if not boundaries:
            # No boundaries found, create single chunk
            return [TextChunk(
                chunk_id=0,
                start_pos=0,
                end_pos=len(text),
                content=text,
                boundary_type='full_document',
                title='Complete Document',
                char_count=len(text),
                word_count=len(text.split()),
                estimated_tokens=self.estimate_tokens(text)
            )]

        chunks = []
        chunk_id = 0

        # Add start boundary if text doesn't start at 0
        if boundaries[0].position > 100:
            boundaries.insert(0, SemanticBoundary(
                position=0,
                type='preamble',
                title='Document Preamble',
                confidence=1.0
            ))

        # Create chunks between boundaries
        for i in range(len(boundaries)):
            start_pos = boundaries[i].position
            end_pos = boundaries[i + 1].position if i + 1 < len(boundaries) else len(text)

            chunk_content = text[start_pos:end_pos].strip()

            if not chunk_content:
                continue  # Skip empty chunks

            chunk_tokens = self.estimate_tokens(chunk_content)

            # If chunk is too large, split it further by paragraphs
            if chunk_tokens > self.target_chunk_size * 1.5:
                sub_chunks = self._split_large_chunk(
                    chunk_content, start_pos, boundaries[i], chunk_id
                )
                chunks.extend(sub_chunks)
                chunk_id += len(sub_chunks)
            else:
                chunks.append(TextChunk(
                    chunk_id=chunk_id,
                    start_pos=start_pos,
                    end_pos=end_pos,
                    content=chunk_content,
                    boundary_type=boundaries[i].type,
                    title=boundaries[i].title or f'Chunk {chunk_id}',
                    char_count=len(chunk_content),
                    word_count=len(chunk_content.split()),
                    estimated_tokens=chunk_tokens
                ))
                chunk_id += 1

        return chunks

    def _split_large_chunk(self, content: str, start_pos: int,
                           boundary: SemanticBoundary, chunk_id: int) -> List[TextChunk]:
        """Split a large chunk into smaller pieces at paragraph boundaries"""
        paragraphs = re.split(r'\n\n+', content)
        sub_chunks = []
        current_chunk = []
        current_tokens = 0
        sub_id = chunk_id

        for para in paragraphs:
            para_tokens = self.estimate_tokens(para)

            if current_tokens + para_tokens > self.target_chunk_size and current_chunk:
                # Create chunk from accumulated paragraphs
                chunk_content = '\n\n'.join(current_chunk)
                sub_chunks.append(TextChunk(
                    chunk_id=sub_id,
                    start_pos=start_pos,
                    end_pos=start_pos + len(chunk_content),
                    content=chunk_content,
                    boundary_type=boundary.type,
                    title=f"{boundary.title} (part {len(sub_chunks) + 1})",
                    char_count=len(chunk_content),
                    word_count=len(chunk_content.split()),
                    estimated_tokens=current_tokens
                ))
                sub_id += 1
                current_chunk = []
                current_tokens = 0

            current_chunk.append(para)
            current_tokens += para_tokens

        # Add remaining content
        if current_chunk:
            chunk_content = '\n\n'.join(current_chunk)
            sub_chunks.append(TextChunk(
                chunk_id=sub_id,
                start_pos=start_pos,
                end_pos=start_pos + len(chunk_content),
                content=chunk_content,
                boundary_type=boundary.type,
                title=f"{boundary.title} (part {len(sub_chunks) + 1})",
                char_count=len(chunk_content),
                word_count=len(chunk_content.split()),
                estimated_tokens=current_tokens
            ))

        return sub_chunks

    def chunk_text(self, text: str) -> Dict:
        """
        Main chunking function - preserves 100% of content

        Args:
            text: Full text content

        Returns:
            Dictionary with chunks and statistics
        """
        print(f"Analyzing text ({len(text):,} characters)...")

        # Detect semantic boundaries
        boundaries = self.detect_boundaries(text)
        print(f"Found {len(boundaries)} semantic boundaries:")
        for btype in ['chapter', 'appendix', 'section', 'paragraph']:
            count = sum(1 for b in boundaries if b.type == btype)
            if count > 0:
                print(f"  - {btype}: {count}")

        # Split into chunks
        chunks = self.split_at_boundaries(text, boundaries)
        print(f"\nCreated {len(chunks)} chunks")

        # Calculate statistics
        total_chars = sum(c.char_count for c in chunks)
        total_tokens = sum(c.estimated_tokens for c in chunks)

        # Verify content preservation
        original_chars = len(text)
        preservation_rate = (total_chars / original_chars * 100) if original_chars > 0 else 0

        statistics = {
            'total_chunks': len(chunks),
            'total_characters': total_chars,
            'total_tokens': total_tokens,
            'original_characters': original_chars,
            'preservation_rate': preservation_rate,
            'avg_tokens_per_chunk': total_tokens // len(chunks) if chunks else 0,
            'min_tokens': min(c.estimated_tokens for c in chunks) if chunks else 0,
            'max_tokens': max(c.estimated_tokens for c in chunks) if chunks else 0
        }

        print(f"\nStatistics:")
        print(f"  - Total chunks: {statistics['total_chunks']}")
        print(f"  - Total tokens: {statistics['total_tokens']:,}")
        print(f"  - Avg tokens/chunk: {statistics['avg_tokens_per_chunk']:,}")
        print(f"  - Content preservation: {preservation_rate:.2f}%")

        return {
            'chunks': [asdict(c) for c in chunks],
            'statistics': statistics,
            'boundaries_detected': len(boundaries)
        }


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python semantic_chunker.py <cache_key> [--target-size TOKENS]")
        print("\nChunks cached PDF text at semantic boundaries")
        print("\nOptions:")
        print("  --target-size TOKENS    Target tokens per chunk (default: 2000)")
        sys.exit(1)

    cache_key = sys.argv[1]
    target_size = 2000

    if '--target-size' in sys.argv:
        idx = sys.argv.index('--target-size')
        target_size = int(sys.argv[idx + 1])

    # Load from cache
    cache_dir = Path.home() / ".claude-pdf-cache" / cache_key
    text_path = cache_dir / "full_text.txt"

    if not text_path.exists():
        print(f"Error: Cache not found for key '{cache_key}'")
        print(f"Run extract_pdf.py first")
        sys.exit(1)

    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Chunk text
    chunker = SemanticChunker(target_chunk_size=target_size)
    result = chunker.chunk_text(text)

    # Save chunks
    chunks_path = cache_dir / "chunks.json"
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Save individual chunk files for easy access
    chunks_dir = cache_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)

    for chunk_data in result['chunks']:
        chunk_file = chunks_dir / f"chunk_{chunk_data['chunk_id']:04d}.txt"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk_data['content'])

    print(f"\n✓ Chunks saved to: {cache_dir}")
    print(f"  - Index: chunks.json")
    print(f"  - Individual chunks: chunks/")


if __name__ == "__main__":
    main()
