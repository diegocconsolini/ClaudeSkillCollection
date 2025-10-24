"""
PatternAgent - Base class for specialized security pattern detection
Each agent is an expert in detecting ONE specific dangerous pattern

63 agents will be auto-generated from dangerous_functions_expanded.json
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from accuracy_cache import AccuracyCache


@dataclass
class DetectionResult:
    """Result from a single agent detection"""
    agent_id: str
    pattern: str
    matched: bool
    confidence: float
    severity: str
    attack_id: Optional[str]
    atlas_id: Optional[str]
    line_number: int
    context: str
    explanation: str


class PatternAgent:
    """
    Base class for pattern detection agents

    Each agent:
    - Detects ONE specific dangerous pattern (e.g., eval, exec, os.system)
    - Learns from validated detections (via cache)
    - Adapts confidence based on historical accuracy
    - Provides context-aware scoring
    """

    def __init__(
        self,
        agent_id: str,
        pattern: str,
        severity: str,
        description: str,
        attack_id: Optional[str] = None,
        atlas_id: Optional[str] = None,
        cwe: Optional[str] = None,
        cvss: Optional[float] = None,
        context_checks: Optional[List[str]] = None,
        cache: Optional[AccuracyCache] = None
    ):
        self.agent_id = agent_id
        self.pattern = pattern
        self.severity = severity
        self.description = description
        self.attack_id = attack_id
        self.atlas_id = atlas_id
        self.cwe = cwe
        self.cvss = cvss
        self.context_checks = context_checks or []
        self.cache = cache

        # Compile regex pattern
        try:
            self.regex = re.compile(pattern, re.MULTILINE)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

        # Base confidence (will adapt based on historical accuracy)
        self.base_confidence = 0.90

    def detect(self, code: str, file_path: str, file_type: str) -> List[DetectionResult]:
        """
        Detect pattern in code with context awareness

        Returns: List of detection results (may be empty)
        """
        results = []

        # Find all matches
        for match in self.regex.finditer(code):
            line_number = code[:match.start()].count('\n') + 1

            # Extract context (3 lines before and after)
            context = self._extract_context(code, match.start(), match.end())

            # Context-aware confidence adjustment (includes file path for security tool detection)
            confidence = self._calculate_confidence(context, file_type, file_path)

            # Check if this pattern+context is known
            if self.cache:
                file_hash = f"{file_path}:{line_number}"
                cached = self.cache.get_detection(self.agent_id, file_hash)

                if cached and cached.is_true_positive is False:
                    # Known false positive - skip or reduce confidence
                    confidence *= 0.1
                elif cached and cached.is_true_positive is True:
                    # Known true positive - boost confidence
                    confidence = min(0.99, confidence * 1.2)

            # Create detection result
            result = DetectionResult(
                agent_id=self.agent_id,
                pattern=self.pattern,
                matched=True,
                confidence=confidence,
                severity=self.severity,
                attack_id=self.attack_id,
                atlas_id=self.atlas_id,
                line_number=line_number,
                context=context,
                explanation=self._generate_explanation(context)
            )

            results.append(result)

        return results

    def _extract_context(self, code: str, start: int, end: int, context_lines: int = 3) -> str:
        """Extract context around match (3 lines before/after)"""
        lines = code.split('\n')

        # Find line number of match
        line_num = code[:start].count('\n')

        # Extract context
        start_line = max(0, line_num - context_lines)
        end_line = min(len(lines), line_num + context_lines + 1)

        context_lines_list = lines[start_line:end_line]
        return '\n'.join(context_lines_list)

    def _calculate_confidence(self, context: str, file_type: str, file_path: str = "") -> float:
        """
        Calculate confidence based on context, file type, and file path

        Adjustments:
        - Context checks (e.g., user_input, request.) reduce confidence
        - File type correlation from cache affects confidence
        - Historical accuracy from cache affects confidence
        - Security tool detection (patterns in detection code = SAFE)
        - File path analysis (test files, reference files, patterns)
        """
        confidence = self.base_confidence

        # FILE PATH FILTERING: Detect if this is a security tool file
        security_tool_paths = [
            '/test',
            '/tests',
            '/test_',
            '/references',
            '/patterns',
            '/dangerous_functions',
            '/generate_agents',
            '/pattern_agent',
            '/scanner',
            '/detector',
            'test.py',
            '_test.py',
            'test_',
        ]

        # If file path indicates security tool code, reduce confidence significantly
        is_security_file = any(
            path_indicator in file_path.lower()
            for path_indicator in security_tool_paths
        )

        if is_security_file:
            # Security scanner test/reference file - drastically reduce confidence
            confidence *= 0.02  # 90% -> 1.8% confidence
            return min(0.99, max(0.01, confidence))

        # CONTEXT FILTERING: Detect if this is pattern matching/detection code (not execution)
        # Security scanners legitimately contain dangerous pattern strings
        security_tool_indicators = [
            r'pattern\s*=\s*r["\']',           # pattern = r"eval\("
            r'regex\s*=\s*r["\']',             # regex = r"exec("
            r'r["\'][^"\']*\\b',               # Raw string with word boundary (r'\beval')
            r'dangerous_pattern',              # Variable name: dangerous_pattern
            r'malicious_code',                 # Variable name: malicious_code
            r'negative_patterns',              # Security pattern lists
            r'positive_patterns',              # Security pattern lists
            r'security_patterns',              # Security pattern lists
            r'test_code\s*=\s*["\']',          # test_code = "eval(...)"
            r'code\s*=\s*"""',                 # Multi-line test code: code = """..."""
            r'example\s*=\s*["\']',            # example = "os.system(...)"
            r'detection_rules',                # detection_rules
            r'scanner_patterns',               # scanner_patterns
            r'audit.*patterns',                # audit patterns
            r'vulnerability.*patterns',        # vulnerability patterns
            r'#.*(?:test|example|pattern|risk|XSS|dangerous)',  # Comments about security
            r'def\s+(?:test_|detect_|scan_|audit_)',  # Function names
            r'\.compile\s*\(',                 # re.compile( - regex compilation
            r'finditer|findall|search|match',  # Regex matching functions
        ]

        # If this looks like security tool detection code, drastically reduce confidence
        is_security_tool_code = any(
            re.search(indicator, context, re.IGNORECASE)
            for indicator in security_tool_indicators
        )

        if is_security_tool_code:
            # This is probably legitimate security scanner code
            # Reduce confidence to near-zero (but not completely to track it)
            confidence *= 0.05  # 90% -> 4.5% confidence
            return min(0.99, max(0.01, confidence))

        # Context checks (reduce confidence if dangerous context detected)
        for check in self.context_checks:
            if re.search(check, context, re.IGNORECASE):
                confidence *= 0.8  # Reduce confidence for dangerous context

        # File type correlation - THE LEARNING MECHANISM
        if self.cache:
            predictions = self.cache.get_file_type_predictions(file_type, min_accuracy=0.0)
            pattern_accuracy = next(
                (acc for pat, acc in predictions if pat == self.agent_id),
                None
            )
            if pattern_accuracy is not None:  # Important: 0.0 is a valid accuracy!
                # Adjust confidence based on historical accuracy for this file type
                # Bayesian updating: average base confidence with historical data
                confidence = (confidence + pattern_accuracy) / 2

        return min(0.99, max(0.1, confidence))

    def _generate_explanation(self, context: str) -> str:
        """Generate human-readable explanation of the detection"""
        return f"{self.description}. Pattern: {self.pattern}"

    def learn_from_validation(
        self,
        file_path: str,
        line_number: int,
        context: str,
        is_true_positive: bool,
        validated_by: str = "human"
    ):
        """
        Update agent knowledge based on validation

        This stores the detection in cache for future learning
        """
        if not self.cache:
            return

        file_hash = f"{file_path}:{line_number}"

        self.cache.store_detection(
            agent_id=self.agent_id,
            pattern=self.pattern,
            file_hash=file_hash,
            file_type=file_path.split('.')[-1] if '.' in file_path else 'unknown',
            confidence=self.base_confidence,
            severity=self.severity,
            context=context,
            attack_id=self.attack_id,
            atlas_id=self.atlas_id,
            is_true_positive=is_true_positive,
            validated_by=validated_by
        )

    def get_performance(self) -> Dict:
        """Get agent's historical performance from cache"""
        if not self.cache or self.agent_id not in self.cache.agent_stats:
            return {
                'precision': 0.0,
                'total_detections': 0,
                'validated_count': 0
            }

        stats = self.cache.agent_stats[self.agent_id]
        return {
            'precision': stats.precision,
            'total_detections': stats.total_detections,
            'validated_count': stats.validated_count,
            'true_positives': stats.true_positives,
            'false_positives': stats.false_positives
        }

    def __repr__(self):
        return f"PatternAgent(id={self.agent_id}, pattern={self.pattern}, severity={self.severity})"


# Example: Create a specialized eval agent
if __name__ == "__main__":
    from accuracy_cache import AccuracyCache

    # Create cache
    cache = AccuracyCache()

    # Create eval agent
    eval_agent = PatternAgent(
        agent_id="eval-agent",
        pattern=r"\beval\s*\(",
        severity="CRITICAL",
        description="Executes arbitrary Python code from string",
        attack_id="T1059.006",
        atlas_id="AML.T0043",
        cwe="CWE-95",
        cvss=9.8,
        context_checks=[
            r"user_input",
            r"request\.",
            r"input\(",
            r"sys\.argv"
        ],
        cache=cache
    )

    # Test detection
    test_code = """
import sys

def process_data(user_input):
    # Dangerous: eval with user input
    result = eval(user_input)
    return result

def safe_function():
    # Safe: eval with literal
    result = eval("2 + 2")
    return result
"""

    results = eval_agent.detect(test_code, "test.py", "py")

    print(f"=== DETECTIONS FROM {eval_agent.agent_id} ===")
    for result in results:
        print(f"Line {result.line_number}: {result.severity} (confidence: {result.confidence:.2%})")
        print(f"Context:\n{result.context}\n")

    # Simulate validation
    if results:
        eval_agent.learn_from_validation(
            file_path="test.py",
            line_number=results[0].line_number,
            context=results[0].context,
            is_true_positive=True,
            validated_by="human"
        )

    # Check performance
    perf = eval_agent.get_performance()
    print(f"\n=== AGENT PERFORMANCE ===")
    for key, value in perf.items():
        print(f"{key}: {value}")
