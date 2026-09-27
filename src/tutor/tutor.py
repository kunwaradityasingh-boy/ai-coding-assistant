from abc import ABC, abstractmethod

from src.schemas.evidence import CodeEvidence
from src.tutor.tutor_result import TutorResult


class Tutor(ABC):

    @abstractmethod
    def teach(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> TutorResult:
        pass