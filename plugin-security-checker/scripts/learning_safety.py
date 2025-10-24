"""
Learning Safety System - Prevents Wrong Knowledge from Poisoning the Cache

CRITICAL SAFETY FEATURES:
1. Validation confidence threshold (require multiple confirmations)
2. Rollback mechanism (undo bad learning)
3. Audit trail (track who/what validated each detection)
4. Decay old knowledge (reduce confidence over time)
5. Human override (always trust human > consensus)
6. Conflict detection (flag contradictory validations)
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class ValidationEvent:
    """Audit trail for all validation events"""
    detection_id: str
    timestamp: float
    validated_by: str          # "human", "consensus", "admin"
    is_true_positive: bool
    confidence: float
    agent_id: str
    pattern: str
    file_hash: str
    reason: Optional[str] = None


class LearningSafetyGuard:
    """
    Prevents bad knowledge from poisoning the learning system

    Safety Mechanisms:
    1. Multi-confirmation requirement
    2. Decay old knowledge
    3. Human override always wins
    4. Audit trail for all changes
    5. Rollback capabilities
    6. Conflict detection
    """

    def __init__(self, audit_log_path: str = "audit_log.json"):
        self.audit_log_path = audit_log_path
        self.validation_history: List[ValidationEvent] = []
        self.conflicts: List[Dict] = []

        # Safety thresholds
        self.min_consensus_votes = 3           # Require 3+ confirmations for auto-validation
        self.human_override_always = True      # Human validation overrides consensus
        self.knowledge_decay_days = 90         # Reduce confidence after 90 days
        self.conflict_threshold = 2            # Flag if 2+ contradictory validations

        self.load_audit_log()

    def load_audit_log(self):
        """Load validation history from disk"""
        if Path(self.audit_log_path).exists():
            with open(self.audit_log_path, 'r') as f:
                data = json.load(f)
                self.validation_history = [
                    ValidationEvent(**event) for event in data.get('events', [])
                ]
                self.conflicts = data.get('conflicts', [])

    def save_audit_log(self):
        """Save validation history to disk"""
        data = {
            'events': [asdict(event) for event in self.validation_history],
            'conflicts': self.conflicts,
            'last_updated': time.time()
        }
        with open(self.audit_log_path, 'w') as f:
            json.dump(data, f, indent=2)

    def validate_detection(
        self,
        detection_id: str,
        agent_id: str,
        pattern: str,
        file_hash: str,
        is_true_positive: bool,
        validated_by: str,
        confidence: float = 0.90,
        reason: Optional[str] = None
    ) -> Dict:
        """
        Safely validate a detection with multiple safeguards

        Returns: {
            "approved": bool,
            "confidence": float,
            "warnings": List[str],
            "conflicts": List[str]
        }
        """
        warnings = []
        conflicts_found = []

        # Create validation event
        event = ValidationEvent(
            detection_id=detection_id,
            timestamp=time.time(),
            validated_by=validated_by,
            is_true_positive=is_true_positive,
            confidence=confidence,
            agent_id=agent_id,
            pattern=pattern,
            file_hash=file_hash,
            reason=reason
        )

        # CHECK 1: Detect conflicts with previous validations
        previous_validations = [
            e for e in self.validation_history
            if e.file_hash == file_hash and e.pattern == pattern
        ]

        for prev in previous_validations:
            if prev.is_true_positive != is_true_positive:
                # CONFLICT DETECTED
                conflict = {
                    "detection_id": detection_id,
                    "previous_validation": {
                        "by": prev.validated_by,
                        "result": prev.is_true_positive,
                        "timestamp": prev.timestamp
                    },
                    "new_validation": {
                        "by": validated_by,
                        "result": is_true_positive,
                        "timestamp": event.timestamp
                    }
                }
                conflicts_found.append(conflict)
                self.conflicts.append(conflict)

                # HUMAN OVERRIDE: If current is human and previous was consensus
                if validated_by == "human" and prev.validated_by == "consensus":
                    warnings.append(f"Overriding consensus validation with human judgment")
                elif validated_by == "consensus" and prev.validated_by == "human":
                    # DON'T OVERRIDE HUMAN VALIDATION
                    warnings.append(f"REJECTED: Cannot override human validation with consensus")
                    self.save_audit_log()
                    return {
                        "approved": False,
                        "confidence": 0.0,
                        "warnings": warnings,
                        "conflicts": conflicts_found,
                        "reason": "Human validation takes precedence"
                    }

        # CHECK 2: Require multiple confirmations for consensus
        if validated_by == "consensus":
            consensus_confirmations = [
                e for e in previous_validations
                if e.validated_by == "consensus" and e.is_true_positive == is_true_positive
            ]

            if len(consensus_confirmations) < (self.min_consensus_votes - 1):
                # Not enough confirmations yet
                warnings.append(
                    f"Need {self.min_consensus_votes - len(consensus_confirmations) - 1} "
                    f"more confirmations before accepting consensus validation"
                )
                # Store but don't apply yet
                self.validation_history.append(event)
                self.save_audit_log()
                return {
                    "approved": False,
                    "confidence": confidence * 0.5,  # Reduced confidence
                    "warnings": warnings,
                    "conflicts": conflicts_found,
                    "reason": "Awaiting more confirmations"
                }

        # CHECK 3: Apply knowledge decay
        age_days = 0
        if previous_validations:
            latest = max(previous_validations, key=lambda x: x.timestamp)
            age_days = (time.time() - latest.timestamp) / (24 * 3600)

            if age_days > self.knowledge_decay_days:
                decay_factor = max(0.5, 1.0 - (age_days - self.knowledge_decay_days) / 365)
                confidence *= decay_factor
                warnings.append(
                    f"Knowledge is {age_days:.0f} days old - "
                    f"confidence reduced by {(1 - decay_factor) * 100:.0f}%"
                )

        # APPROVED - Add to validation history
        self.validation_history.append(event)
        self.save_audit_log()

        return {
            "approved": True,
            "confidence": confidence,
            "warnings": warnings,
            "conflicts": conflicts_found,
            "validation_count": len([e for e in self.validation_history if e.file_hash == file_hash])
        }

    def rollback_validation(self, detection_id: str, reason: str):
        """
        Rollback a bad validation

        This removes the validation from history and flags it as incorrect
        """
        # Find the validation
        validation = next(
            (e for e in self.validation_history if e.detection_id == detection_id),
            None
        )

        if not validation:
            return {"success": False, "reason": "Validation not found"}

        # Remove from history
        self.validation_history = [
            e for e in self.validation_history if e.detection_id != detection_id
        ]

        # Add rollback event
        rollback_event = ValidationEvent(
            detection_id=detection_id,
            timestamp=time.time(),
            validated_by="admin",
            is_true_positive=not validation.is_true_positive,  # Flip it
            confidence=0.0,
            agent_id=validation.agent_id,
            pattern=validation.pattern,
            file_hash=validation.file_hash,
            reason=f"ROLLBACK: {reason}"
        )
        self.validation_history.append(rollback_event)

        self.save_audit_log()

        return {
            "success": True,
            "rolled_back": asdict(validation),
            "reason": reason
        }

    def get_validation_confidence(self, file_hash: str, pattern: str) -> float:
        """
        Get confidence for a detection based on validation history

        Returns:
        - 0.99 if validated as TP by human
        - 0.90 if validated as TP by consensus (3+ votes)
        - 0.10 if validated as FP by human
        - 0.50 if conflicting validations
        - 0.90 if no validation yet (default)
        """
        validations = [
            e for e in self.validation_history
            if e.file_hash == file_hash and e.pattern == pattern
        ]

        if not validations:
            return 0.90  # Default confidence

        # Check for human validation (highest priority)
        human_validations = [e for e in validations if e.validated_by == "human"]
        if human_validations:
            latest_human = max(human_validations, key=lambda x: x.timestamp)
            return 0.99 if latest_human.is_true_positive else 0.10

        # Check for consensus (require 3+ votes)
        consensus_tp = [e for e in validations if e.validated_by == "consensus" and e.is_true_positive]
        consensus_fp = [e for e in validations if e.validated_by == "consensus" and not e.is_true_positive]

        if len(consensus_tp) >= 3:
            return 0.90  # High confidence TP
        elif len(consensus_fp) >= 3:
            return 0.10  # High confidence FP
        elif len(consensus_tp) > 0 and len(consensus_fp) > 0:
            return 0.50  # Conflicting - medium confidence

        return 0.90  # Default

    def get_conflicts_report(self) -> str:
        """Generate human-readable conflict report"""
        if not self.conflicts:
            return "No conflicts detected."

        report = "VALIDATION CONFLICTS DETECTED\n"
        report += "=" * 80 + "\n\n"

        for i, conflict in enumerate(self.conflicts, 1):
            report += f"Conflict #{i}:\n"
            report += f"  Detection ID: {conflict['detection_id']}\n"
            report += f"  Previous: {conflict['previous_validation']['by']} "
            report += f"→ {'TP' if conflict['previous_validation']['result'] else 'FP'}\n"
            report += f"  New: {conflict['new_validation']['by']} "
            report += f"→ {'TP' if conflict['new_validation']['result'] else 'FP'}\n"
            report += f"  Resolution: "
            if conflict['new_validation']['by'] == 'human':
                report += "Human validation accepted\n"
            elif conflict['previous_validation']['by'] == 'human':
                report += "Previous human validation preserved\n"
            else:
                report += "MANUAL REVIEW REQUIRED\n"
            report += "\n"

        return report

    def audit_trail(self, file_hash: Optional[str] = None) -> str:
        """Generate audit trail for validations"""
        events = self.validation_history
        if file_hash:
            events = [e for e in events if e.file_hash == file_hash]

        if not events:
            return "No validation events found."

        report = "VALIDATION AUDIT TRAIL\n"
        report += "=" * 80 + "\n\n"

        for event in sorted(events, key=lambda x: x.timestamp, reverse=True):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event.timestamp))
            result = "TRUE POSITIVE" if event.is_true_positive else "FALSE POSITIVE"
            report += f"[{timestamp}] {event.validated_by} → {result}\n"
            report += f"  Detection: {event.detection_id}\n"
            report += f"  Agent: {event.agent_id}\n"
            report += f"  Pattern: {event.pattern}\n"
            report += f"  Confidence: {event.confidence:.0%}\n"
            if event.reason:
                report += f"  Reason: {event.reason}\n"
            report += "\n"

        return report


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("LEARNING SAFETY SYSTEM DEMO")
    print("=" * 80)
    print()

    safety = LearningSafetyGuard(audit_log_path="demo_audit_log.json")

    # Scenario 1: Consensus validation (needs 3 confirmations)
    print("Scenario 1: Consensus Validation")
    print("-" * 80)

    result1 = safety.validate_detection(
        detection_id="det_001",
        agent_id="eval-agent",
        pattern=r"\beval\s*\(",
        file_hash="plugin.py:42",
        is_true_positive=True,
        validated_by="consensus",
        reason="First consensus vote"
    )
    print(f"Vote 1: {result1}")
    print()

    result2 = safety.validate_detection(
        detection_id="det_002",
        agent_id="eval-agent",
        pattern=r"\beval\s*\(",
        file_hash="plugin.py:42",
        is_true_positive=True,
        validated_by="consensus",
        reason="Second consensus vote"
    )
    print(f"Vote 2: {result2}")
    print()

    result3 = safety.validate_detection(
        detection_id="det_003",
        agent_id="eval-agent",
        pattern=r"\beval\s*\(",
        file_hash="plugin.py:42",
        is_true_positive=True,
        validated_by="consensus",
        reason="Third consensus vote - APPROVED!"
    )
    print(f"Vote 3: {result3}")
    print()

    # Scenario 2: Human override
    print("Scenario 2: Human Override")
    print("-" * 80)

    result4 = safety.validate_detection(
        detection_id="det_004",
        agent_id="eval-agent",
        pattern=r"\beval\s*\(",
        file_hash="plugin.py:42",
        is_true_positive=False,  # Human says: Actually FALSE POSITIVE!
        validated_by="human",
        reason="This is test code, not a real threat"
    )
    print(f"Human override: {result4}")
    print()

    # Scenario 3: Try to override human with consensus (should fail)
    print("Scenario 3: Attempt to Override Human (Should Fail)")
    print("-" * 80)

    result5 = safety.validate_detection(
        detection_id="det_005",
        agent_id="eval-agent",
        pattern=r"\beval\s*\(",
        file_hash="plugin.py:42",
        is_true_positive=True,
        validated_by="consensus",
        reason="Trying to override human validation"
    )
    print(f"Consensus override attempt: {result5}")
    print()

    # Show conflicts
    print("Conflicts Report:")
    print(safety.get_conflicts_report())

    # Show audit trail
    print("Audit Trail:")
    print(safety.audit_trail(file_hash="plugin.py:42"))

    # Rollback example
    print("Scenario 4: Rollback Bad Validation")
    print("-" * 80)
    rollback_result = safety.rollback_validation(
        detection_id="det_001",
        reason="Incorrectly auto-validated - was actually FP"
    )
    print(f"Rollback result: {rollback_result}")
    print()

    print("Final Audit Trail:")
    print(safety.audit_trail(file_hash="plugin.py:42"))
