from src.review.gemini_reviewer import GeminiReviewer
from src.review.local_reviewer import LocalReviewer
from src.review.review_result import ReviewResult
from src.schemas.evidence import CodeEvidence


class ReviewService:

    def __init__(
        self,
        local_reviewer=None,
        ai_reviewer=None,
    ):
        self.local_reviewer = local_reviewer or LocalReviewer()
        self.ai_reviewer = ai_reviewer or GeminiReviewer()

    def review(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> ReviewResult:

        local_result = self.local_reviewer.review(evidence)

        try:
            ai_result = self.ai_reviewer.review(
                code,
                evidence,
            )

            return ai_result

        except Exception:
            local_result.source = "local-fallback"
            return local_result
