"""
AccuracyCache - Bloom Filter + Trie with Learning for Zero False Positives
Optimized for ACCURACY (not speed/memory) with shareable knowledge export

INNOVATION:
1. Bloom + Trie eliminates false positives from probabilistic filter
2. Shared learning across agents (TP/FP tracking, file type correlations)
3. Export to MITRE ATLAS/ATT&CK format for human consumption
4. Evolving detection rules from validated findings
5. Adaptive eviction by agent accuracy (low-precision agents evicted first)

TARGET: Reduce false positive rate to <1% across all agents
"""

import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Detection:
    """Detection record with full context for learning"""
    agent_id: str
    pattern: str
    file_hash: str
    file_type: str              # e.g., "py", "js", "ts"
    confidence: float
    severity: str               # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    attack_id: Optional[str]    # MITRE ATT&CK technique (e.g., "T1059.006")
    atlas_id: Optional[str]     # MITRE ATLAS technique (e.g., "AML.T0043")
    context: str                # Code context around detection
    timestamp: float
    is_true_positive: Optional[bool]  # Validation status
    validated_by: Optional[str]       # "human" or "consensus"


@dataclass
class AgentStats:
    """Agent performance statistics for adaptive eviction"""
    agent_id: str
    total_detections: int = 0
    true_positives: int = 0
    false_positives: int = 0
    validated_count: int = 0

    @property
    def precision(self) -> float:
        """Calculate precision (TP / (TP + FP))"""
        total = self.true_positives + self.false_positives
        return self.true_positives / total if total > 0 else 0.0

    @property
    def validation_rate(self) -> float:
        """Percentage of detections that have been validated"""
        return self.validated_count / self.total_detections if self.total_detections > 0 else 0.0


@dataclass
class FileTypeCorrelation:
    """File type to pattern correlation for smart prefetching"""
    pattern: str
    file_type: str
    detection_count: int = 0
    true_positive_count: int = 0

    @property
    def accuracy(self) -> float:
        """Accuracy for this pattern+filetype combination"""
        return self.true_positive_count / self.detection_count if self.detection_count > 0 else 0.0


@dataclass
class EvolvedRule:
    """Auto-generated detection rule from validated findings"""
    pattern: str
    confidence: float
    derived_from: List[str]     # List of file_hashes that led to this rule
    validated_detections: int
    created_at: float
    attack_id: Optional[str]
    atlas_id: Optional[str]


class BloomFilter:
    """Probabilistic filter for fast negative lookups"""

    def __init__(self, size: int = 100000, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = bytearray(size // 8)

    def _hashes(self, key: str) -> List[int]:
        """Generate k hash values"""
        h1 = int(hashlib.md5(key.encode()).hexdigest(), 16) % self.size
        h2 = int(hashlib.sha1(key.encode()).hexdigest(), 16) % self.size
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]

    def add(self, key: str):
        """Add key to bloom filter"""
        for h in self._hashes(key):
            byte_idx, bit_idx = h // 8, h % 8
            self.bits[byte_idx] |= (1 << bit_idx)

    def contains(self, key: str) -> bool:
        """Check if key MIGHT be in set (may have false positives)"""
        for h in self._hashes(key):
            byte_idx, bit_idx = h // 8, h % 8
            if not (self.bits[byte_idx] & (1 << bit_idx)):
                return False
        return True


class TrieNode:
    """Trie node for deterministic storage (eliminates bloom false positives)"""
    __slots__ = ['children', 'detection']

    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.detection: Optional[Detection] = None


class AccuracyCache:
    """
    Accuracy-focused cache with learning and ATLAS/ATT&CK export

    Key Features:
    1. Zero false positives (Bloom filter + Trie validation)
    2. Shared learning across agents
    3. File type correlation learning
    4. Rule evolution from validated findings
    5. Export to MITRE ATLAS/ATT&CK format
    """

    def __init__(self, max_detections: int = 10000):
        # Primary storage
        self.bloom = BloomFilter(size=100000)
        self.trie_root = TrieNode()
        self.detections: List[Detection] = []
        self.max_detections = max_detections

        # Learning systems
        self.agent_stats: Dict[str, AgentStats] = {}
        self.file_type_correlations: Dict[Tuple[str, str], FileTypeCorrelation] = {}
        self.evolved_rules: List[EvolvedRule] = []

        # Pattern frequency tracking for rule evolution
        self.pattern_contexts: Dict[str, List[str]] = defaultdict(list)  # pattern -> contexts

    def store_detection(
        self,
        agent_id: str,
        pattern: str,
        file_hash: str,
        file_type: str,
        confidence: float,
        severity: str,
        context: str,
        attack_id: Optional[str] = None,
        atlas_id: Optional[str] = None,
        is_true_positive: Optional[bool] = None,
        validated_by: Optional[str] = None
    ):
        """
        Store detection with full learning

        This updates:
        - Agent statistics (for adaptive eviction)
        - File type correlations (for smart prefetching)
        - Pattern contexts (for rule evolution)
        """

        # Create detection record
        detection = Detection(
            agent_id=agent_id,
            pattern=pattern,
            file_hash=file_hash,
            file_type=file_type,
            confidence=confidence,
            severity=severity,
            attack_id=attack_id,
            atlas_id=atlas_id,
            context=context,
            timestamp=time.time(),
            is_true_positive=is_true_positive,
            validated_by=validated_by
        )

        # Add to Bloom filter
        key = f"{agent_id}:{file_hash}"
        self.bloom.add(key)

        # Add to Trie (eliminates bloom false positives)
        node = self.trie_root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.detection = detection

        # Update agent statistics
        if agent_id not in self.agent_stats:
            self.agent_stats[agent_id] = AgentStats(agent_id=agent_id)

        stats = self.agent_stats[agent_id]
        stats.total_detections += 1

        if is_true_positive is not None:
            stats.validated_count += 1
            if is_true_positive:
                stats.true_positives += 1
            else:
                stats.false_positives += 1

        # Update file type correlations
        correlation_key = (pattern, file_type)
        if correlation_key not in self.file_type_correlations:
            self.file_type_correlations[correlation_key] = FileTypeCorrelation(
                pattern=pattern,
                file_type=file_type
            )

        corr = self.file_type_correlations[correlation_key]
        corr.detection_count += 1
        if is_true_positive:
            corr.true_positive_count += 1

        # Track pattern context for rule evolution
        if is_true_positive and context:
            self.pattern_contexts[pattern].append(context)

            # Try to evolve rules if we have enough validated data
            if len(self.pattern_contexts[pattern]) >= 10:
                self._try_evolve_rule(pattern, attack_id, atlas_id)

        # Store detection
        self.detections.append(detection)

        # Adaptive eviction (low-accuracy agents first)
        if len(self.detections) > self.max_detections:
            self._evict_by_accuracy()

    def get_detection(self, agent_id: str, file_hash: str) -> Optional[Detection]:
        """
        Retrieve detection with ZERO false positives

        1. Bloom filter: Fast negative check (if not in bloom, definitely not in cache)
        2. Trie: Deterministic confirmation (eliminates bloom false positives)
        """
        key = f"{agent_id}:{file_hash}"

        # Fast negative check
        if not self.bloom.contains(key):
            return None  # Definitely not in cache

        # Trie confirmation (eliminates false positives)
        node = self.trie_root
        for char in key:
            if char not in node.children:
                return None  # Bloom false positive!
            node = node.children[char]

        return node.detection

    def get_file_type_predictions(self, file_type: str, min_accuracy: float = 0.7) -> List[Tuple[str, float]]:
        """
        Get patterns likely to match for a file type (for smart prefetching)

        Returns: List of (pattern, accuracy) tuples sorted by accuracy
        """
        predictions = []

        for (pattern, ftype), corr in self.file_type_correlations.items():
            if ftype == file_type and corr.accuracy >= min_accuracy:
                predictions.append((pattern, corr.accuracy))

        return sorted(predictions, key=lambda x: x[1], reverse=True)

    def _try_evolve_rule(self, pattern: str, attack_id: Optional[str], atlas_id: Optional[str]):
        """
        Evolve new detection rules from validated findings

        Looks for common patterns in code contexts to generate new regex
        """
        contexts = self.pattern_contexts[pattern]

        # Simple rule evolution: if >80% of contexts contain a common substring,
        # create a more specific rule
        # (This is a placeholder - real implementation would use NLP/ML)

        if len(contexts) >= 10:
            # Count common substrings (simplified)
            common_contexts = [ctx for ctx in contexts if "user_input" in ctx or "request." in ctx]

            if len(common_contexts) / len(contexts) > 0.8:
                evolved_pattern = f"{pattern}.*(?:user_input|request\\.)"

                # Check if this evolved rule already exists
                if not any(rule.pattern == evolved_pattern for rule in self.evolved_rules):
                    rule = EvolvedRule(
                        pattern=evolved_pattern,
                        confidence=0.95,  # Higher confidence for evolved rules
                        derived_from=[ctx[:50] for ctx in common_contexts[:5]],
                        validated_detections=len(common_contexts),
                        created_at=time.time(),
                        attack_id=attack_id,
                        atlas_id=atlas_id
                    )
                    self.evolved_rules.append(rule)

    def _evict_by_accuracy(self):
        """
        Adaptive eviction: Remove detections from low-accuracy agents first

        Eviction priority (lowest to highest):
        1. Unvalidated detections from low-precision agents
        2. False positives from any agent
        3. Old true positives from high-precision agents
        """
        if not self.detections:
            return

        # Score each detection
        scored = []
        for detection in self.detections:
            stats = self.agent_stats.get(detection.agent_id)
            if not stats:
                score = 0.0  # Unknown agent = lowest priority
            else:
                # Score = precision × validation_rate × recency × severity
                age_days = (time.time() - detection.timestamp) / 86400
                recency = max(0.1, 1.0 - (age_days / 30))

                severity_map = {'LOW': 0.25, 'MEDIUM': 0.5, 'HIGH': 0.75, 'CRITICAL': 1.0}
                severity_score = severity_map.get(detection.severity, 0.5)

                score = stats.precision * stats.validation_rate * recency * severity_score

                # Penalty for false positives
                if detection.is_true_positive is False:
                    score *= 0.1

            scored.append((score, detection))

        # Sort by score (lowest first)
        scored.sort(key=lambda x: x[0])

        # Evict lowest 10%
        evict_count = max(1, len(scored) // 10)
        self.detections = [d for _, d in scored[evict_count:]]

    def export_to_atlas(self, output_file: str):
        """
        Export validated findings to MITRE ATLAS format for human consumption

        ATLAS Tactic/Technique JSON format:
        {
            "technique_id": "AML.T0043",
            "detections": [...],
            "agent_accuracy": 0.95,
            "file_type_correlations": {...}
        }
        """
        atlas_export = defaultdict(lambda: {
            'technique_id': None,
            'technique_name': None,
            'detections': [],
            'agent_stats': {},
            'file_type_correlations': {},
            'evolved_rules': []
        })

        # Group detections by ATLAS ID
        for detection in self.detections:
            if detection.atlas_id and detection.is_true_positive:
                atlas_export[detection.atlas_id]['technique_id'] = detection.atlas_id
                atlas_export[detection.atlas_id]['detections'].append({
                    'agent_id': detection.agent_id,
                    'pattern': detection.pattern,
                    'file_type': detection.file_type,
                    'confidence': detection.confidence,
                    'severity': detection.severity,
                    'timestamp': detection.timestamp
                })

        # Add agent statistics
        for agent_id, stats in self.agent_stats.items():
            for atlas_id in atlas_export.keys():
                relevant_detections = [
                    d for d in self.detections
                    if d.agent_id == agent_id and d.atlas_id == atlas_id
                ]
                if relevant_detections:
                    atlas_export[atlas_id]['agent_stats'][agent_id] = {
                        'precision': stats.precision,
                        'total_detections': len(relevant_detections),
                        'validation_rate': stats.validation_rate
                    }

        # Add file type correlations
        for (pattern, file_type), corr in self.file_type_correlations.items():
            for atlas_id in atlas_export.keys():
                if any(d.pattern == pattern and d.atlas_id == atlas_id for d in self.detections):
                    if file_type not in atlas_export[atlas_id]['file_type_correlations']:
                        atlas_export[atlas_id]['file_type_correlations'][file_type] = []
                    atlas_export[atlas_id]['file_type_correlations'][file_type].append({
                        'pattern': pattern,
                        'accuracy': corr.accuracy,
                        'detection_count': corr.detection_count
                    })

        # Add evolved rules
        for rule in self.evolved_rules:
            if rule.atlas_id in atlas_export:
                atlas_export[rule.atlas_id]['evolved_rules'].append(asdict(rule))

        # Write to file
        with open(output_file, 'w') as f:
            json.dump(dict(atlas_export), f, indent=2, default=str)

    def get_stats(self) -> Dict:
        """Get comprehensive cache statistics"""
        return {
            'total_detections': len(self.detections),
            'bloom_size_bytes': len(self.bloom.bits),
            'total_agents': len(self.agent_stats),
            'agent_avg_precision': sum(s.precision for s in self.agent_stats.values()) / len(self.agent_stats) if self.agent_stats else 0.0,
            'file_type_correlations': len(self.file_type_correlations),
            'evolved_rules': len(self.evolved_rules),
            'validated_rate': sum(s.validated_count for s in self.agent_stats.values()) / sum(s.total_detections for s in self.agent_stats.values()) if self.agent_stats else 0.0
        }

    def save_to_disk(self, cache_file: str):
        """
        Save cache to disk for persistence across runs

        Saves:
        - Agent statistics (TP/FP counts, accuracy)
        - File type correlations
        - Evolved rules
        - Detections (limited to keep file size manageable)
        - Pattern contexts
        """
        import os

        # Create directory if it doesn't exist
        cache_dir = os.path.dirname(cache_file)
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Prepare serializable data
        cache_data = {
            'version': '3.0.0',
            'saved_at': time.time(),
            'agent_stats': {
                agent_id: asdict(stats)
                for agent_id, stats in self.agent_stats.items()
            },
            'file_type_correlations': {
                f"{pattern}::{file_type}": asdict(corr)
                for (pattern, file_type), corr in self.file_type_correlations.items()
            },
            'evolved_rules': [asdict(rule) for rule in self.evolved_rules],
            'detections': [asdict(det) for det in self.detections[-1000:]],  # Keep last 1000
            'pattern_contexts': {
                pattern: contexts[-100:]  # Keep last 100 contexts per pattern
                for pattern, contexts in self.pattern_contexts.items()
            }
        }

        # Write to file
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)

    def load_from_disk(self, cache_file: str) -> bool:
        """
        Load cache from disk to restore previous learning

        Returns: True if loaded successfully, False otherwise
        """
        import os

        if not os.path.exists(cache_file):
            return False

        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)

            # Restore agent statistics
            for agent_id, stats_dict in cache_data.get('agent_stats', {}).items():
                self.agent_stats[agent_id] = AgentStats(**stats_dict)

            # Restore file type correlations
            for key, corr_dict in cache_data.get('file_type_correlations', {}).items():
                pattern, file_type = key.split('::', 1)
                self.file_type_correlations[(pattern, file_type)] = FileTypeCorrelation(**corr_dict)

            # Restore evolved rules
            for rule_dict in cache_data.get('evolved_rules', []):
                self.evolved_rules.append(EvolvedRule(**rule_dict))

            # Restore detections (rebuild Bloom + Trie)
            for det_dict in cache_data.get('detections', []):
                detection = Detection(**det_dict)
                self.detections.append(detection)

                # Rebuild Bloom and Trie
                key = f"{detection.agent_id}:{detection.file_hash}"
                self.bloom.add(key)

                node = self.trie_root
                for char in key:
                    if char not in node.children:
                        node.children[char] = TrieNode()
                    node = node.children[char]
                node.detection = detection

            # Restore pattern contexts
            for pattern, contexts in cache_data.get('pattern_contexts', {}).items():
                self.pattern_contexts[pattern] = contexts

            return True

        except Exception as e:
            print(f"Warning: Could not load cache from {cache_file}: {e}")
            return False


# Example usage
if __name__ == "__main__":
    cache = AccuracyCache(max_detections=10000)

    # Simulate detections from eval-agent
    for i in range(50):
        cache.store_detection(
            agent_id="eval-agent",
            pattern=r"\beval\s*\(",
            file_hash=f"file-{i}.py",
            file_type="py",
            confidence=0.95,
            severity="CRITICAL",
            context=f"eval(user_input) # line {i}",
            attack_id="T1059.006",
            atlas_id="AML.T0043",
            is_true_positive=(i % 5 != 0),  # 80% accuracy
            validated_by="human"
        )

    # Simulate detections from exec-agent
    for i in range(30):
        cache.store_detection(
            agent_id="exec-agent",
            pattern=r"\bexec\s*\(",
            file_hash=f"file-{i}.js",
            file_type="js",
            confidence=0.85,
            severity="HIGH",
            context=f"exec(code) // line {i}",
            attack_id="T1059.007",
            is_true_positive=(i % 2 == 0),  # 50% accuracy
            validated_by="consensus"
        )

    # Get stats
    stats = cache.get_stats()
    print("=== CACHE STATISTICS ===")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # File type predictions
    print("\n=== FILE TYPE PREDICTIONS (.py) ===")
    predictions = cache.get_file_type_predictions("py", min_accuracy=0.7)
    for pattern, accuracy in predictions:
        print(f"  {pattern}: {accuracy:.2%} accuracy")

    # Export to ATLAS
    cache.export_to_atlas("atlas_findings.json")
    print("\n✓ Exported to atlas_findings.json")
