from abc import ABC, abstractmethod

from src.fixer.fix_result import FixResult
from src.schemas.evidence import CodeEvidence


class Fixer(ABC):

    @abstractmethod
    def fix(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> FixResult:
        pass