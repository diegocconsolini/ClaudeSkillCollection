#!/usr/bin/env python3
"""
PDF Smart Extractor - Local extraction with zero LLM involvement
Extracts 100% of PDF content to disk for efficient chunking and caching
"""

import sys
import os
import hashlib
import json
import getpass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import pymupdf  # PyMuPDF


class PDFExtractor:
    """Extract complete PDF content locally without LLM"""

    def __init__(self, cache_dir: str = None):
        """Initialize extractor with cache directory"""
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.claude-pdf-cache")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_pdf_hash(self, pdf_path: str) -> str:
        """Generate unique hash for PDF file"""
        hasher = hashlib.sha256()
        with open(pdf_path, 'rb') as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()[:16]  # Use first 16 chars for filename

    def extract_metadata(self, doc: pymupdf.Document) -> Dict:
        """Extract PDF metadata"""
        metadata = {
            'title': doc.metadata.get('title', 'Unknown'),
            'author': doc.metadata.get('author', 'Unknown'),
            'subject': doc.metadata.get('subject', ''),
            'keywords': doc.metadata.get('keywords', ''),
            'creator': doc.metadata.get('creator', ''),
            'producer': doc.metadata.get('producer', ''),
            'creation_date': doc.metadata.get('creationDate', ''),
            'mod_date': doc.metadata.get('modDate', ''),
            'page_count': len(doc),
            'is_encrypted': doc.is_encrypted,
            'is_pdf': doc.is_pdf
        }
        return metadata

    def extract_page_content(self, page: pymupdf.Page) -> Dict:
        """Extract all content from a single page"""
        page_data = {
            'page_number': page.number + 1,
            'text': page.get_text("text"),  # Plain text only (no binary data)
            'width': page.rect.width,
            'height': page.rect.height
        }
        return page_data

    def extract_toc(self, doc: pymupdf.Document) -> List[Dict]:
        """Extract table of contents if available"""
        toc = doc.get_toc()
        toc_data = []

        for level, title, page_num in toc:
            toc_data.append({
                'level': level,
                'title': title,
                'page': page_num
            })

        return toc_data

    def extract_full_pdf(self, pdf_path: str, force: bool = False, password: str = None) -> Dict:
        """
        Extract complete PDF content to cache

        Args:
            pdf_path: Path to PDF file
            force: Force re-extraction even if cached
            password: Password for encrypted PDFs (if None, will prompt interactively)

        Returns:
            Dictionary with extraction results and cache location
        """
        pdf_path = os.path.abspath(pdf_path)

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Generate cache key
        pdf_hash = self.get_pdf_hash(pdf_path)
        pdf_name = Path(pdf_path).stem
        cache_key = f"{pdf_name}_{pdf_hash}"

        cache_path = self.cache_dir / cache_key
        cache_path.mkdir(parents=True, exist_ok=True)

        # Check if already extracted
        manifest_path = cache_path / "manifest.json"
        if manifest_path.exists() and not force:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)

            return {
                'status': 'cached',
                'cache_key': cache_key,
                'cache_path': str(cache_path),
                'manifest': manifest,
                'message': f'Using cached extraction for {pdf_name}'
            }

        # Extract PDF
        print(f"Extracting PDF: {pdf_name} ({os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB)")

        # Open PDF (may be encrypted)
        doc = pymupdf.open(pdf_path)

        # Handle password-protected PDFs
        if doc.is_encrypted:
            print("🔒 PDF is password protected")

            max_attempts = 3
            attempt = 0

            while attempt < max_attempts:
                # Use provided password or prompt interactively
                if password is None:
                    password_input = getpass.getpass("Enter password: ")
                else:
                    password_input = password

                # Try to authenticate
                auth_result = doc.authenticate(password_input)

                if auth_result:
                    print("✓ Password accepted")
                    break
                else:
                    attempt += 1
                    if password is not None:
                        # If password was provided via CLI, don't retry
                        doc.close()
                        raise PermissionError(f"Invalid password for {pdf_name}")
                    elif attempt < max_attempts:
                        print(f"❌ Invalid password. Attempt {attempt}/{max_attempts}")
                        password = None  # Reset for next attempt
                    else:
                        doc.close()
                        raise PermissionError(f"Failed to unlock {pdf_name} after {max_attempts} attempts")

            # Check if we have access after authentication
            if doc.metadata is None:
                doc.close()
                raise PermissionError(f"PDF is encrypted but could not be unlocked: {pdf_name}")

        # Extract metadata
        metadata = self.extract_metadata(doc)

        # Extract table of contents
        toc = self.extract_toc(doc)

        # Extract all pages
        pages = []
        full_text = []

        for page_num, page in enumerate(doc, start=1):
            print(f"  Processing page {page_num}/{len(doc)}...", end='\r')
            page_data = self.extract_page_content(page)
            pages.append(page_data)
            full_text.append(page_data['text'])

        print()  # New line after progress

        # Combine all text
        complete_text = "\n\n".join(full_text)

        # Calculate statistics
        char_count = len(complete_text)
        word_count = len(complete_text.split())

        # Estimate tokens (rough: 1 token ≈ 4 characters for English)
        estimated_tokens = char_count // 4

        # Save full text to file
        text_path = cache_path / "full_text.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(complete_text)

        # Save structured pages
        pages_path = cache_path / "pages.json"
        with open(pages_path, 'w', encoding='utf-8') as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)

        # Save metadata
        metadata_path = cache_path / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Save TOC
        if toc:
            toc_path = cache_path / "toc.json"
            with open(toc_path, 'w', encoding='utf-8') as f:
                json.dump(toc, f, indent=2, ensure_ascii=False)

        # Create manifest
        manifest = {
            'cache_key': cache_key,
            'original_path': pdf_path,
            'pdf_name': pdf_name,
            'pdf_hash': pdf_hash,
            'extraction_date': str(Path(pdf_path).stat().st_mtime),
            'metadata': metadata,
            'statistics': {
                'page_count': len(pages),
                'char_count': char_count,
                'word_count': word_count,
                'estimated_tokens': estimated_tokens,
                'file_size_mb': os.path.getsize(pdf_path) / 1024 / 1024
            },
            'has_toc': len(toc) > 0,
            'files': {
                'full_text': str(text_path),
                'pages': str(pages_path),
                'metadata': str(metadata_path),
                'toc': str(toc_path) if toc else None
            }
        }

        # Save manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        doc.close()

        print(f"✓ Extraction complete:")
        print(f"  - Pages: {metadata['page_count']}")
        print(f"  - Characters: {char_count:,}")
        print(f"  - Words: {word_count:,}")
        print(f"  - Estimated tokens: {estimated_tokens:,}")
        print(f"  - Cache location: {cache_path}")

        return {
            'status': 'extracted',
            'cache_key': cache_key,
            'cache_path': str(cache_path),
            'manifest': manifest,
            'message': f'Successfully extracted {pdf_name}'
        }


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_path> [--force] [--password PASSWORD]")
        print("\nExtracts complete PDF content to cache for efficient processing")
        print("\nOptions:")
        print("  --force              Force re-extraction even if cached")
        print("  --password PASSWORD  Password for encrypted PDFs (will prompt if not provided)")
        sys.exit(1)

    pdf_path = sys.argv[1]
    force = '--force' in sys.argv

    # Extract password from arguments if provided
    password = None
    if '--password' in sys.argv:
        password_index = sys.argv.index('--password')
        if password_index + 1 < len(sys.argv):
            password = sys.argv[password_index + 1]
        else:
            print("Error: --password requires a value")
            sys.exit(1)

    extractor = PDFExtractor()

    try:
        result = extractor.extract_full_pdf(pdf_path, force=force, password=password)

        print(f"\n{result['message']}")
        print(f"Cache key: {result['cache_key']}")

        if result['status'] == 'cached':
            print("\n💡 Use --force to re-extract")
    except PermissionError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Tip: Use --password <password> to provide password via command line")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
