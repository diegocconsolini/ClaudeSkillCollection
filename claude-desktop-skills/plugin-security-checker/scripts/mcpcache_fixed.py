"""
MCPCache - Fixed Version with Bug Fixes and Agent Integration
Lightweight sharded cache for multi-agent security scanner with learning capabilities

FIXES APPLIED:
1. Thread-safe stats counter (added Lock)
2. Background TTL cleanup task (prevents memory leak)
3. O(log N) eviction using heapq (was O(N))
4. Agent learning integration methods
5. Pattern analysis bounds checking
"""

import asyncio
import hashlib
import heapq
import time
import weakref
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from threading import RLock, Lock
from typing import Any, Dict, List, Optional, Set, Tuple


class EntryType(Enum):
    """Cache entry types for MCP operations"""
    TOOL_RESULT = "tool_result"
    RESOURCE = "resource"
    PROMPT = "prompt"
    CAPABILITY = "capability"
    SESSION = "session"
    AGENT_DETECTION = "agent_detection"  # NEW: For agent learning


@dataclass
class CacheEntry:
    """Individual cache entry with metadata"""
    key: str
    value: Any
    entry_type: EntryType
    size: int
    timestamp: float
    ttl: Optional[float] = None
    access_count: int = 0
    session_id: Optional[str] = None

    def is_expired(self) -> bool:
        """Check if entry has expired"""
        if self.ttl is None:
            return False
        return (time.time() - self.timestamp) > self.ttl

    @property
    def context_score(self) -> float:
        """Calculate priority score for eviction (higher = keep longer)"""
        age = time.time() - self.timestamp

        # Type weights
        type_weight = {
            EntryType.SESSION: 5.0,
            EntryType.AGENT_DETECTION: 4.0,  # Keep learning data longer
            EntryType.CAPABILITY: 3.0,
            EntryType.PROMPT: 2.0,
            EntryType.TOOL_RESULT: 1.5,
            EntryType.RESOURCE: 1.0
        }.get(self.entry_type, 1.0)

        # Recency score (decay over time)
        recency = 1.0 / (1.0 + age / 3600)  # Half-life of 1 hour

        # Frequency score
        frequency = min(self.access_count / 10.0, 2.0)

        # Size penalty (prefer keeping smaller items)
        size_penalty = 1.0 / (1.0 + self.size / 1024)

        return type_weight * (recency + frequency) * size_penalty


class TwoQueueCache:
    """
    2Q cache algorithm implementation
    - Hot queue: Frequently accessed items
    - Cold queue: Recently added items
    - Ghost queue: Recently evicted (for tracking)
    """

    def __init__(self, max_memory_bytes: int, hot_ratio: float = 0.7):
        # FIX: Clarify that max_memory_bytes is BYTES, not entry count
        self.max_memory_bytes = max_memory_bytes
        self.hot_max_bytes = int(max_memory_bytes * hot_ratio)
        self.cold_max_bytes = max_memory_bytes - self.hot_max_bytes

        # Also track entry count limits (reasonable defaults)
        self.hot_max_entries = 10000
        self.cold_max_entries = 10000
        self.ghost_max = 5000

        self.hot_queue: OrderedDict[str, CacheEntry] = OrderedDict()
        self.cold_queue: OrderedDict[str, CacheEntry] = OrderedDict()
        self.ghost_queue: OrderedDict[str, float] = OrderedDict()  # key -> timestamp

        # FIX 1: Thread-safe eviction heap (replaces O(N) scan)
        self.hot_heap: List[Tuple[float, str]] = []  # (score, key)
        self.cold_heap: List[Tuple[float, str]] = []

        self.lock = RLock()
        self.current_size_bytes = 0
        self.hot_size_bytes = 0
        self.cold_size_bytes = 0
        self.eviction_count = 0  # Track total evictions

    def get(self, key: str) -> Optional[CacheEntry]:
        """Get entry and update access patterns"""
        with self.lock:
            # Check hot queue
            if key in self.hot_queue:
                entry = self.hot_queue[key]
                entry.access_count += 1
                self.hot_queue.move_to_end(key)
                return entry

            # Check cold queue (promote to hot on second access)
            if key in self.cold_queue:
                entry = self.cold_queue.pop(key)
                entry.access_count += 1
                self._remove_from_heap(self.cold_heap, key)

                # Remove from cold heap
                self._add_to_hot(key, entry)
                return entry

            # Check ghost queue (recently evicted)
            if key in self.ghost_queue:
                self.ghost_queue.pop(key)

            return None

    def put(self, key: str, entry: CacheEntry) -> None:
        """Add entry to cache"""
        with self.lock:
            # Update if exists
            if key in self.hot_queue:
                old_entry = self.hot_queue[key]
                self.current_size_bytes -= old_entry.size
                self.hot_size_bytes -= old_entry.size
                self.hot_queue[key] = entry
                self.current_size_bytes += entry.size
                self.hot_size_bytes += entry.size
                self._update_heap_score(self.hot_heap, key, entry.context_score)
                return

            if key in self.cold_queue:
                old_entry = self.cold_queue[key]
                self.current_size_bytes -= old_entry.size
                self.cold_size_bytes -= old_entry.size
                self.cold_queue[key] = entry
                self.current_size_bytes += entry.size
                self.cold_size_bytes += entry.size
                self._update_heap_score(self.cold_heap, key, entry.context_score)
                return

            # Add to cold queue (new items start cold)
            self._add_to_cold(key, entry)

    def _add_to_hot(self, key: str, entry: CacheEntry) -> None:
        """Add entry to hot queue with eviction if needed"""
        # Evict if hot queue full OR exceeds memory limit
        while (len(self.hot_queue) >= self.hot_max_entries or
               self.hot_size_bytes + entry.size > self.hot_max_bytes):
            if len(self.hot_queue) == 0:
                break
            if self._evict_from_hot():
                self.eviction_count += 1

        self.hot_queue[key] = entry
        self.current_size_bytes += entry.size
        self.hot_size_bytes += entry.size
        heapq.heappush(self.hot_heap, (entry.context_score, key))

    def _add_to_cold(self, key: str, entry: CacheEntry) -> None:
        """Add entry to cold queue with eviction if needed"""
        # Evict if cold queue full OR exceeds memory limit
        while (len(self.cold_queue) >= self.cold_max_entries or
               self.cold_size_bytes + entry.size > self.cold_max_bytes):
            if len(self.cold_queue) == 0:
                break
            if self._evict_from_cold():
                self.eviction_count += 1

        self.cold_queue[key] = entry
        self.current_size_bytes += entry.size
        self.cold_size_bytes += entry.size
        heapq.heappush(self.cold_heap, (entry.context_score, key))

    def _evict_from_hot(self) -> None:
        """Evict lowest priority item from hot queue - FIX: O(log N) using heap"""
        while self.hot_heap:
            score, key = heapq.heappop(self.hot_heap)

            # Verify key still exists and score matches (lazy deletion)
            if key in self.hot_queue:
                entry = self.hot_queue[key]
                if abs(entry.context_score - score) < 0.01:  # Score hasn't changed
                    # Valid eviction candidate
                    self.hot_queue.pop(key)
                    self.current_size_bytes -= entry.size
                    self.hot_size_bytes -= entry.size

                    # Add to ghost queue
                    if len(self.ghost_queue) >= self.ghost_max:
                        self.ghost_queue.popitem(last=False)
                    self.ghost_queue[key] = time.time()
                    # EVICTION COUNT: Return True to indicate successful eviction
                    return True

        # Fallback: heap empty but queue not (shouldn't happen)
        if self.hot_queue:
            key, entry = self.hot_queue.popitem(last=False)
            self.current_size_bytes -= entry.size
            self.hot_size_bytes -= entry.size
            return True
        return False

    def _evict_from_cold(self) -> bool:
        """Evict lowest priority item from cold queue - FIX: O(log N) using heap"""
        while self.cold_heap:
            score, key = heapq.heappop(self.cold_heap)

            if key in self.cold_queue:
                entry = self.cold_queue[key]
                if abs(entry.context_score - score) < 0.01:
                    self.cold_queue.pop(key)
                    self.current_size_bytes -= entry.size
                    self.cold_size_bytes -= entry.size

                    # Add to ghost queue
                    if len(self.ghost_queue) >= self.ghost_max:
                        self.ghost_queue.popitem(last=False)
                    self.ghost_queue[key] = time.time()
                    return True

        # Fallback
        if self.cold_queue:
            key, entry = self.cold_queue.popitem(last=False)
            self.current_size_bytes -= entry.size
            self.cold_size_bytes -= entry.size
            return True
        return False

    def _remove_from_heap(self, heap: List[Tuple[float, str]], key: str) -> None:
        """Remove key from heap (lazy deletion - actual removal on pop)"""
        # Heap uses lazy deletion - entries removed when popped and validated
        pass

    def _update_heap_score(self, heap: List[Tuple[float, str]], key: str, new_score: float) -> None:
        """Update score in heap (lazy - just add new entry, old one ignored on pop)"""
        heapq.heappush(heap, (new_score, key))

    def remove_expired(self) -> int:
        """Remove all expired entries - FIX 2: Called by background cleanup"""
        removed = 0
        with self.lock:
            # Check hot queue
            expired_hot = [k for k, e in self.hot_queue.items() if e.is_expired()]
            for key in expired_hot:
                entry = self.hot_queue.pop(key)
                self.current_size_bytes -= entry.size
                self.hot_size_bytes -= entry.size
                self._remove_from_heap(self.hot_heap, key)
                removed += 1

            # Check cold queue
            expired_cold = [k for k, e in self.cold_queue.items() if e.is_expired()]
            for key in expired_cold:
                entry = self.cold_queue.pop(key)
                self.current_size_bytes -= entry.size
                self.cold_size_bytes -= entry.size
                self._remove_from_heap(self.cold_heap, key)
                removed += 1

        return removed

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        with self.lock:
            return {
                "hot_size": len(self.hot_queue),
                "cold_size": len(self.cold_queue),
                "ghost_size": len(self.ghost_queue),
                "total_bytes": self.current_size_bytes,
                "hot_bytes": self.hot_size_bytes,
                "cold_bytes": self.cold_size_bytes,
                "hot_max_bytes": self.hot_max_bytes,
                "cold_max_bytes": self.cold_max_bytes,
                "max_memory_bytes": self.max_memory_bytes,
                "evictions": self.eviction_count
            }


class CacheShard:
    """Individual cache shard with dedicated thread pool"""

    def __init__(self, shard_id: int, max_memory: int, pool_size: int = 25):
        self.shard_id = shard_id
        self.cache = TwoQueueCache(max_memory)
        self.executor = ThreadPoolExecutor(max_workers=pool_size, thread_name_prefix=f"shard-{shard_id}")

        # FIX 1: Thread-safe stats
        self.stats_lock = Lock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'evictions': 0,
            'expired': 0
        }

        # Pattern tracking for predictive prefetch
        self.pattern_lock = RLock()
        self.access_patterns: List[str] = []
        self.pattern_transitions: Dict[str, Dict[str, int]] = {}

    async def get(self, key: str) -> Optional[Any]:
        """Async get operation"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._get_sync, key)

    def _get_sync(self, key: str) -> Optional[Any]:
        """Synchronous get with stats"""
        entry = self.cache.get(key)

        # FIX 1: Thread-safe stats update
        with self.stats_lock:
            if entry and not entry.is_expired():
                self.stats['hits'] += 1
                self._track_access(key)
                return entry.value
            else:
                self.stats['misses'] += 1
                if entry and entry.is_expired():
                    self.stats['expired'] += 1
                return None

    async def put(self, key: str, value: Any, entry_type: EntryType,
                  ttl: Optional[float] = None, session_id: Optional[str] = None) -> None:
        """Async put operation"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            self._put_sync,
            key, value, entry_type, ttl, session_id
        )

    def _put_sync(self, key: str, value: Any, entry_type: EntryType,
                  ttl: Optional[float], session_id: Optional[str]) -> None:
        """Synchronous put with stats"""
        # Calculate size
        try:
            import pickle
            size = len(pickle.dumps(value))
        except:
            size = 1024  # Default size if unpicklable

        entry = CacheEntry(
            key=key,
            value=value,
            entry_type=entry_type,
            size=size,
            timestamp=time.time(),
            ttl=ttl,
            session_id=session_id
        )

        self.cache.put(key, entry)

        with self.stats_lock:
            self.stats['sets'] += 1

    def _track_access(self, key: str) -> None:
        """Track access patterns for predictive prefetch"""
        with self.pattern_lock:
            self.access_patterns.append(key)

            # Keep last 100 accesses
            if len(self.access_patterns) > 100:
                self.access_patterns.pop(0)

            # Build transition map
            # FIX 5: Bounds checking for pattern analysis
            if len(self.access_patterns) < 2:
                return

            for i in range(len(self.access_patterns) - 1):
                current = self.access_patterns[i]
                next_key = self.access_patterns[i + 1]

                if current not in self.pattern_transitions:
                    self.pattern_transitions[current] = {}

                self.pattern_transitions[current][next_key] = \
                    self.pattern_transitions[current].get(next_key, 0) + 1

    async def predict_and_prefetch(self, current_key: str) -> None:
        """Predictive prefetch based on Markov chain - FIX: Added error handling"""
        try:
            with self.pattern_lock:
                if current_key not in self.pattern_transitions:
                    return

                transitions = self.pattern_transitions[current_key]
                if not transitions:
                    return

                # Find most likely next key
                next_key = max(transitions.items(), key=lambda x: x[1])[0]

                # Check if already cached
                cached = await self.get(next_key)
                if cached is None:
                    # Fire-and-forget prefetch (would be implemented by caller)
                    pass
        except Exception as e:
            # Don't crash on prefetch errors
            pass

    def get_stats(self) -> Dict:
        """Get shard statistics"""
        with self.stats_lock:
            cache_stats = self.cache.get_stats()
            return {**self.stats, **cache_stats}


class MCPCache:
    """
    Main cache interface with sharding and MCP-specific features
    FIX 2: Added background cleanup task
    """

    def __init__(self, total_memory: int = 100 * 1024 * 1024, num_shards: int = 4):
        self.num_shards = num_shards
        self.shard_memory = total_memory // num_shards

        self.shards = [
            CacheShard(i, self.shard_memory)
            for i in range(num_shards)
        ]

        # FIX 2: Background cleanup task
        self.cleanup_task: Optional[asyncio.Task] = None
        self.cleanup_interval = 60  # seconds

    def _get_shard(self, key: str) -> CacheShard:
        """Get shard for key using consistent hashing"""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        shard_id = hash_value % self.num_shards
        return self.shards[shard_id]

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        shard = self._get_shard(key)
        return await shard.get(key)

    async def put(self, key: str, value: Any, entry_type: EntryType = EntryType.TOOL_RESULT,
                  ttl: Optional[float] = None, session_id: Optional[str] = None) -> None:
        """Put value in cache"""
        shard = self._get_shard(key)
        await shard.put(key, value, entry_type, ttl, session_id)

    async def multi_get(self, keys: List[str]) -> Dict[str, Any]:
        """Batch get operation"""
        tasks = [self.get(key) for key in keys]
        results = await asyncio.gather(*tasks)
        return {k: v for k, v in zip(keys, results) if v is not None}

    async def multi_put(self, items: List[Tuple[str, Any, EntryType]]) -> None:
        """Batch put operation"""
        tasks = [self.put(key, value, entry_type) for key, value, entry_type in items]
        await asyncio.gather(*tasks)

    def get_global_stats(self) -> Dict:
        """Get statistics across all shards"""
        all_stats = [shard.get_stats() for shard in self.shards]

        return {
            'total_hits': sum(s['hits'] for s in all_stats),
            'total_misses': sum(s['misses'] for s in all_stats),
            'total_sets': sum(s['sets'] for s in all_stats),
            'total_evictions': sum(s['evictions'] for s in all_stats),
            'total_expired': sum(s['expired'] for s in all_stats),
            'total_entries': sum(s['hot_size'] + s['cold_size'] for s in all_stats),
            'total_bytes': sum(s['total_bytes'] for s in all_stats),
            'shards': all_stats
        }

    # FIX 2: Background cleanup implementation
    async def start_cleanup_task(self) -> None:
        """Start background cleanup task for expired entries"""
        if self.cleanup_task is None or self.cleanup_task.done():
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _cleanup_loop(self) -> None:
        """Background loop to remove expired entries"""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                total_removed = 0

                for shard in self.shards:
                    removed = shard.cache.remove_expired()
                    total_removed += removed

                    # Update stats
                    with shard.stats_lock:
                        shard.stats['expired'] += removed
                        shard.stats['evictions'] += removed

                if total_removed > 0:
                    print(f"[MCPCache] Cleaned up {total_removed} expired entries")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[MCPCache] Cleanup error: {e}")

    async def stop_cleanup_task(self) -> None:
        """Stop background cleanup task"""
        if self.cleanup_task and not self.cleanup_task.done():
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass

    # ============================================================================
    # AGENT INTEGRATION METHODS
    # ============================================================================

    async def store_detection(
        self,
        agent_id: str,
        file_hash: str,
        result: Dict,
        is_true_positive: Optional[bool] = None
    ) -> None:
        """
        Store agent detection result for learning

        Args:
            agent_id: Identifier for the agent (e.g., "eval-agent")
            file_hash: SHA256 hash of scanned file
            result: Detection result dict with keys: pattern, severity, confidence, context
            is_true_positive: User validation (None = not validated yet)
        """
        detection_key = f"detection:{agent_id}:{file_hash}"

        detection_record = {
            'agent_id': agent_id,
            'file_hash': file_hash,
            'timestamp': time.time(),
            'result': result,
            'is_true_positive': is_true_positive,
            'validated': is_true_positive is not None
        }

        await self.put(
            detection_key,
            detection_record,
            entry_type=EntryType.AGENT_DETECTION,
            ttl=30 * 24 * 3600  # Keep for 30 days
        )

        # Also update agent history index
        history_key = f"agent_history:{agent_id}"
        history = await self.get(history_key) or []
        history.append({
            'file_hash': file_hash,
            'timestamp': time.time(),
            'validated': is_true_positive is not None
        })

        # Keep last 1000 detections per agent
        if len(history) > 1000:
            history = history[-1000:]

        await self.put(
            history_key,
            history,
            entry_type=EntryType.AGENT_DETECTION,
            ttl=None  # No expiry for history index
        )

    async def get_agent_history(
        self,
        agent_id: str,
        limit: int = 100,
        validated_only: bool = False
    ) -> List[Dict]:
        """
        Retrieve agent's detection history for learning

        Args:
            agent_id: Agent identifier
            limit: Max number of records to return
            validated_only: Only return validated detections

        Returns:
            List of detection records sorted by timestamp (newest first)
        """
        history_key = f"agent_history:{agent_id}"
        history = await self.get(history_key) or []

        # Filter and fetch full records
        records = []
        for item in reversed(history[-limit:]):  # Newest first
            if validated_only and not item.get('validated'):
                continue

            detection_key = f"detection:{agent_id}:{item['file_hash']}"
            record = await self.get(detection_key)
            if record:
                records.append(record)

        return records

    async def update_pattern_rules(
        self,
        agent_id: str,
        new_rules: List[Dict]
    ) -> None:
        """
        Store evolved pattern rules for an agent

        Args:
            agent_id: Agent identifier
            new_rules: List of rule dicts with keys: pattern, confidence, context_requirements
        """
        rules_key = f"pattern_rules:{agent_id}"

        rules_record = {
            'agent_id': agent_id,
            'rules': new_rules,
            'updated_at': time.time(),
            'version': int(time.time())  # Version tracking
        }

        await self.put(
            rules_key,
            rules_record,
            entry_type=EntryType.AGENT_DETECTION,
            ttl=None  # No expiry
        )

    async def get_pattern_rules(self, agent_id: str) -> Optional[Dict]:
        """Get current pattern rules for an agent"""
        rules_key = f"pattern_rules:{agent_id}"
        return await self.get(rules_key)

    async def get_agent_performance(self, agent_id: str) -> Dict:
        """
        Calculate agent performance metrics

        Returns:
            Dict with precision, recall, total_detections, validated_count
        """
        history = await self.get_agent_history(agent_id, limit=1000)

        if not history:
            return {
                'precision': 0.0,
                'total_detections': 0,
                'validated_count': 0,
                'true_positives': 0,
                'false_positives': 0
            }

        validated = [h for h in history if h.get('validated')]
        true_positives = len([h for h in validated if h.get('is_true_positive')])
        false_positives = len([h for h in validated if not h.get('is_true_positive')])

        precision = true_positives / len(validated) if validated else 0.0

        return {
            'precision': precision,
            'total_detections': len(history),
            'validated_count': len(validated),
            'true_positives': true_positives,
            'false_positives': false_positives
        }


# Example usage
async def example_usage():
    """Example showing MCPCache with agent integration"""
    cache = MCPCache(total_memory=100 * 1024 * 1024, num_shards=4)

    # Start background cleanup
    await cache.start_cleanup_task()

    try:
        # Basic cache operations
        await cache.put("tool:result:123", {"output": "success"}, EntryType.TOOL_RESULT)
        result = await cache.get("tool:result:123")
        print(f"Cached result: {result}")

        # Agent detection storage
        await cache.store_detection(
            agent_id="eval-agent",
            file_hash="abc123",
            result={
                'pattern': 'eval(',
                'severity': 'CRITICAL',
                'confidence': 0.95,
                'context': 'Direct eval() call with user input'
            },
            is_true_positive=True
        )

        # Retrieve agent history
        history = await cache.get_agent_history("eval-agent", limit=10)
        print(f"Agent history: {len(history)} records")

        # Get performance metrics
        perf = await cache.get_agent_performance("eval-agent")
        print(f"Agent performance: {perf}")

        # Global stats
        stats = cache.get_global_stats()
        print(f"Cache stats: {stats}")

    finally:
        # Cleanup
        await cache.stop_cleanup_task()


if __name__ == "__main__":
    asyncio.run(example_usage())
