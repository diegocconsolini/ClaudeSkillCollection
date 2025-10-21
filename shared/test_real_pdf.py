#!/usr/bin/env python3
"""Test smart_cache with a real PDF file"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from smart_cache import SmartCache, PostQuantumHash

# Test with real PDF
pdf_file = Path(__file__).parent.parent / "docs" / "NIST.IR.8228.pdf"

if not pdf_file.exists():
    print(f"❌ Test PDF not found: {pdf_file}")
    sys.exit(1)

print(f"Testing with real PDF: {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")
print()

# Test hashing performance
print("1. Testing SHAKE256 hash performance...")
shake_hash = PostQuantumHash.hash_file(str(pdf_file))
print(f"   SHAKE256: {shake_hash}")

print("\n2. Testing SHA-256 hash (for comparison)...")
sha_hash = PostQuantumHash.hash_sha256(str(pdf_file))
print(f"   SHA-256: {sha_hash}")

# Test cache key generation
print("\n3. Testing cache key generation...")
cache = SmartCache(doc_type='pdf', cache_dir=Path("/tmp/test_real_cache"))
cache_key, cache_path = cache.get_cache_key(str(pdf_file))
print(f"   Cache key: {cache_key}")
print(f"   Cache path: {cache_path}")

# Test exists (should be False)
print("\n4. Testing cache.exists() (should be False)...")
exists = cache.exists(cache_key)
print(f"   Exists: {exists}")
assert not exists, "Cache should not exist yet"

# Create fake cache
print("\n5. Creating fake cache manifest...")
cache_path.mkdir(parents=True, exist_ok=True)
manifest_path = cache_path / "manifest.json"
manifest_path.write_text('{"test": "real pdf cache"}')
cache.mark_cached(cache_key)

# Test exists (should be True now)
print("\n6. Testing cache.exists() (should be True now)...")
exists = cache.exists(cache_key)
print(f"   Exists: {exists}")
assert exists, "Cache should exist now"

# Cleanup
import shutil
if cache.cache_dir.exists():
    shutil.rmtree(cache.cache_dir)

print("\n✓ All real PDF tests passed!")
