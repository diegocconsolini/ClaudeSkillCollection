#!/usr/bin/env python3
"""
Smart Cache - Unified caching for smart-extractor series

SHAKE256 hashing (SHA-3 family), optional Bloom filter,
automatic SHA-256 migration, zero dependencies.

Version: 2.0.0
License: MIT
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Optional, Tuple


# ============================================================================
# SHAKE256 Hashing (SHA-3 Family)
# ============================================================================

class PostQuantumHash:
    """
    SHAKE256-based hashing (SHA-3 family, NIST FIPS 202)

    Modern hash function with flexible output length.
    Used for generating unique cache keys.
    """

    @staticmethod
    def hash_file(file_path: str, digest_size: int = 32) -> str:
        """
        Generate SHAKE256 hash of file

        Args:
            file_path: Path to file to hash
            digest_size: Output size in bytes (default 32)

        Returns:
            Hex string of first 16 characters (cache key suffix)
        """
        hasher = hashlib.shake_256()

        with open(file_path, 'rb') as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)

        # Return first 16 hex chars for cache key
        return hasher.hexdigest(digest_size)[:16]

    @staticmethod
    def hash_sha256(file_path: str) -> str:
        """
        Generate SHA-256 hash (for migration detection)

        Args:
            file_path: Path to file to hash

        Returns:
            Hex string of first 16 characters
        """
        hasher = hashlib.sha256()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)

        return hasher.hexdigest()[:16]


# ============================================================================
# Bloom Filter (Optional)
# ============================================================================

class BloomFilter:
    """
    Lightweight Bloom filter for fast cache existence checks

    Uses SHAKE256 for hash functions. Zero external dependencies.
    False positive rate: ~1% (configurable)
    Memory: ~9.6 bits per element
    """

    def __init__(self, size: int = 1000000, hash_count: int = 7):
        """
        Initialize Bloom filter

        Args:
            size: Bit array size (default 1M = ~1.2MB memory)
            hash_count: Number of hash functions (default 7 for ~1% FP rate)
        """
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        """Generate k hash values using SHAKE256 with different seeds"""
        for i in range(self.hash_count):
            hasher = hashlib.shake_256(f"{item}:{i}".encode())
            hash_bytes = hasher.digest(4)  # 4 bytes = 32 bits
            yield int.from_bytes(hash_bytes, 'big') % self.size

    def add(self, item: str):
        """Add item to Bloom filter"""
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1

    def contains(self, item: str) -> bool:
        """
        Check if item might be in set

        Returns:
            True if item might be in set (may have false positives)
            False if item is definitely not in set (no false negatives)
        """
        return all(self.bit_array[h] for h in self._hashes(item))

    def save(self, path: Path):
        """Save Bloom filter to disk"""
        data = {
            'size': self.size,
            'hash_count': self.hash_count,
            'bit_array': self.bit_array
        }
        with open(path, 'w') as f:
            json.dump(data, f)

    @classmethod
    def load(cls, path: Path) -> 'BloomFilter':
        """Load Bloom filter from disk"""
        with open(path, 'r') as f:
            data = json.load(f)

        bloom = cls(size=data['size'], hash_count=data['hash_count'])
        bloom.bit_array = data['bit_array']
        return bloom


# ============================================================================
# Smart Cache - Main API
# ============================================================================

class SmartCache:
    """
    Unified caching API for smart-extractor series

    Features:
    - SHAKE256 hashing (SHA-3 family)
    - Auto-migration from SHA-256 caches
    - Optional Bloom filter for fast lookups
    - Zero external dependencies

    Usage:
        cache = SmartCache(doc_type='pdf')
        cache_key, cache_path = cache.get_cache_key(file_path)

        if cache.exists(cache_key):
            # Use cached extraction
            pass
        else:
            # Extract and cache
            cache.mark_cached(cache_key)
    """

    def __init__(self,
                 doc_type: str,
                 cache_dir: Optional[Path] = None,
                 enable_bloom: bool = False):
        """
        Initialize SmartCache

        Args:
            doc_type: Document type ('pdf', 'xlsx', 'docx')
            cache_dir: Cache directory (default ~/.claude-cache/{doc_type})
            enable_bloom: Enable Bloom filter for fast lookups
        """
        self.doc_type = doc_type

        # Set cache directory
        if cache_dir is None:
            cache_dir = Path.home() / '.claude-cache' / doc_type

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Bloom filter if enabled
        self.bloom = None
        if enable_bloom:
            bloom_path = self.cache_dir.parent / '.bloom.json'
            if bloom_path.exists():
                try:
                    self.bloom = BloomFilter.load(bloom_path)
                except:
                    # If load fails, create new Bloom filter
                    self.bloom = BloomFilter()
            else:
                self.bloom = BloomFilter()

        # Track old cache directory for migration
        self.old_cache_dir = Path.home() / f'.claude-{doc_type}-cache'

    def get_cache_key(self, file_path: str) -> Tuple[str, Path]:
        """
        Generate cache key with SHAKE256 and check for migration

        Args:
            file_path: Path to document file

        Returns:
            Tuple of (cache_key, cache_path)

        Note:
            Automatically migrates from SHA-256 cache if found
        """
        file_path = os.path.abspath(file_path)
        doc_name = Path(file_path).stem

        # Generate new SHAKE256 hash
        shake_hash = PostQuantumHash.hash_file(file_path)
        new_cache_key = f"{doc_name}_{shake_hash}"
        new_cache_path = self.cache_dir / new_cache_key

        # Check if new cache exists
        if new_cache_path.exists():
            return new_cache_key, new_cache_path

        # Check for old SHA-256 cache and migrate
        sha_hash = PostQuantumHash.hash_sha256(file_path)
        old_cache_key = f"{doc_name}_{sha_hash}"
        old_cache_path = self.old_cache_dir / old_cache_key

        if old_cache_path.exists():
            # Migrate old cache to new location
            print(f"🔄 Migrating cache from SHA-256 to SHAKE256...")
            new_cache_path.parent.mkdir(parents=True, exist_ok=True)

            # Move old cache directory to new location
            import shutil
            shutil.move(str(old_cache_path), str(new_cache_path))

            # Add to Bloom filter if enabled
            if self.bloom:
                self.bloom.add(new_cache_key)
                self._save_bloom()

            print(f"✓ Migration complete: {new_cache_key}")
            return new_cache_key, new_cache_path

        # No existing cache
        return new_cache_key, new_cache_path

    def exists(self, cache_key: str) -> bool:
        """
        Check if cache exists

        Args:
            cache_key: Cache key to check

        Returns:
            True if cache exists, False otherwise
        """
        # Fast check with Bloom filter if enabled
        if self.bloom and not self.bloom.contains(cache_key):
            return False

        # Verify with filesystem
        cache_path = self.cache_dir / cache_key
        manifest_path = cache_path / 'manifest.json'
        return manifest_path.exists()

    def mark_cached(self, cache_key: str):
        """
        Mark cache key as cached (for Bloom filter)

        Args:
            cache_key: Cache key to mark
        """
        if self.bloom:
            self.bloom.add(cache_key)
            self._save_bloom()

    def _save_bloom(self):
        """Save Bloom filter to disk"""
        if self.bloom:
            bloom_path = self.cache_dir.parent / '.bloom.json'
            self.bloom.save(bloom_path)

    def get_cache_path(self, cache_key: str) -> Path:
        """
        Get cache directory path for cache key

        Args:
            cache_key: Cache key

        Returns:
            Path to cache directory
        """
        return self.cache_dir / cache_key


# ============================================================================
# Convenience Functions
# ============================================================================

def get_cache_for_extractor(doc_type: str, enable_bloom: bool = False) -> SmartCache:
    """
    Convenience function to get SmartCache instance

    Args:
        doc_type: Document type ('pdf', 'xlsx', 'docx')
        enable_bloom: Enable Bloom filter

    Returns:
        SmartCache instance
    """
    return SmartCache(doc_type=doc_type, enable_bloom=enable_bloom)
