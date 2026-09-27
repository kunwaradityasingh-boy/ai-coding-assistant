from abc import ABC, abstractmethod

from src.schemas.evidence import CodeEvidence
from src.review.review_result import ReviewResult


class AIReviewer(ABC):

    @abstractmethod
    def review(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> ReviewResult:
        pass