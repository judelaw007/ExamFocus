"""
Quality gates for the content pipeline.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..config import config
from ..models.qa import (
    AccuracyReport,
    ConsistencyReport,
    StructuralReport,
    DiscussionReport,
)


class QualityStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ESCALATE = "escalate"


@dataclass
class QualityCheckResult:
    """Result of a quality check."""

    status: QualityStatus
    agent: str
    message: str
    details: dict = field(default_factory=dict)


class QualityGate:
    """
    Quality gate for verifying agent outputs before proceeding.

    Implements the supervisor checklist from the agents documentation.
    """

    def __init__(self, max_change_percentage: float = 0.20):
        self.max_change_percentage = max_change_percentage

    def check_accuracy(self, report: AccuracyReport, original_word_count: int) -> QualityCheckResult:
        """Check Agent 5a output."""
        checks = []

        # Check if corrections are reasonable
        if report.total_corrections > 20:
            checks.append("High number of corrections - review recommended")

        # Check accuracy rate
        if report.overall_accuracy < 0.80:
            return QualityCheckResult(
                status=QualityStatus.ESCALATE,
                agent="5a",
                message=f"Low accuracy rate: {report.overall_accuracy:.1%}",
                details={"accuracy": report.overall_accuracy},
            )

        # Check for expert review items
        if report.expert_review_items:
            return QualityCheckResult(
                status=QualityStatus.WARNING,
                agent="5a",
                message=f"{len(report.expert_review_items)} items flagged for expert review",
                details={"items": [e.item for e in report.expert_review_items]},
            )

        return QualityCheckResult(
            status=QualityStatus.PASSED,
            agent="5a",
            message=f"{report.total_corrections} corrections made, {report.overall_accuracy:.1%} accuracy",
            details={
                "corrections": report.total_corrections,
                "accuracy": report.overall_accuracy,
            },
        )

    def check_consistency(self, report: ConsistencyReport) -> QualityCheckResult:
        """Check Agent 5b output."""
        # Check if too much content was removed
        total_removed_words = sum(
            len(r.removed_text.split()) for r in report.redundancies_removed
        )
        if total_removed_words > 500:
            return QualityCheckResult(
                status=QualityStatus.WARNING,
                agent="5b",
                message=f"Large amount of content removed: {total_removed_words} words",
                details={"removed_words": total_removed_words},
            )

        return QualityCheckResult(
            status=QualityStatus.PASSED,
            agent="5b",
            message=f"{len(report.terminology_fixes)} terminology fixes, {len(report.redundancies_removed)} redundancies removed",
            details={
                "terminology_fixes": len(report.terminology_fixes),
                "redundancies": len(report.redundancies_removed),
            },
        )

    def check_structural(self, report: StructuralReport) -> QualityCheckResult:
        """Check Agent 5c output."""
        # Verify substantive content preserved
        if not report.substantive_content_preserved:
            return QualityCheckResult(
                status=QualityStatus.ESCALATE,
                agent="5c",
                message="Substantive content may have been removed",
                details={"preserved": False},
            )

        if not report.worked_examples_intact:
            return QualityCheckResult(
                status=QualityStatus.ESCALATE,
                agent="5c",
                message="Worked examples may have been affected",
                details={"examples_intact": False},
            )

        return QualityCheckResult(
            status=QualityStatus.PASSED,
            agent="5c",
            message=f"{len(report.scaffolding_removed)} scaffolding items removed",
            details={"removals": len(report.scaffolding_removed)},
        )

    def check_discussion(self, report: DiscussionReport) -> QualityCheckResult:
        """Check Agent 5d output."""
        # Check discussion percentage
        if report.discussion_percentage < 10:
            return QualityCheckResult(
                status=QualityStatus.WARNING,
                agent="5d",
                message=f"Discussion percentage low: {report.discussion_percentage:.1f}%",
                details={"percentage": report.discussion_percentage},
            )

        if not report.existing_content_preserved:
            return QualityCheckResult(
                status=QualityStatus.ESCALATE,
                agent="5d",
                message="Existing content may have been modified",
                details={"preserved": False},
            )

        if not report.voice_consistent:
            return QualityCheckResult(
                status=QualityStatus.WARNING,
                agent="5d",
                message="Voice consistency issues detected",
                details={"consistent": False},
            )

        return QualityCheckResult(
            status=QualityStatus.PASSED,
            agent="5d",
            message=f"{report.total_words_added} words of discussion added ({report.discussion_percentage:.1f}%)",
            details={
                "words_added": report.total_words_added,
                "percentage": report.discussion_percentage,
            },
        )

    def overall_check(
        self,
        accuracy: Optional[QualityCheckResult] = None,
        consistency: Optional[QualityCheckResult] = None,
        structural: Optional[QualityCheckResult] = None,
        discussion: Optional[QualityCheckResult] = None,
    ) -> QualityCheckResult:
        """Perform overall quality check."""
        results = [r for r in [accuracy, consistency, structural, discussion] if r]

        # Check for any escalations
        escalations = [r for r in results if r.status == QualityStatus.ESCALATE]
        if escalations:
            return QualityCheckResult(
                status=QualityStatus.ESCALATE,
                agent="overall",
                message=f"{len(escalations)} issue(s) require escalation",
                details={"escalations": [e.message for e in escalations]},
            )

        # Check for warnings
        warnings = [r for r in results if r.status == QualityStatus.WARNING]
        if len(warnings) >= 2:
            return QualityCheckResult(
                status=QualityStatus.WARNING,
                agent="overall",
                message=f"{len(warnings)} warnings - review recommended",
                details={"warnings": [w.message for w in warnings]},
            )

        return QualityCheckResult(
            status=QualityStatus.PASSED,
            agent="overall",
            message="All quality checks passed",
            details={"agents_passed": len(results)},
        )
