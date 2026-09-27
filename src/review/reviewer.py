from abc import ABC, abstractmethod

from src.schemas.evidence import CodeEvidence
from src.review.review_result import ReviewResult


class Reviewer(ABC):

    @abstractmethod
    def review(self, evidence: CodeEvidence) -> ReviewResult:
        pass