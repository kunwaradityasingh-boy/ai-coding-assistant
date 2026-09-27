from src.review.review_service import ReviewService
from src.review.review_result import ReviewResult
from src.schemas.evidence import CodeEvidence


class FakeLocalReviewer:

    def review(self, evidence):
        return ReviewResult(
            summary="Local review",
            issues=[],
            positive_points=["Local check passed."],
        )


class FakeAIReviewer:

    def review(self, code, evidence):
        return ReviewResult(
            summary="AI review",
            issues=[],
            positive_points=["AI review completed."],
        )


class FailingAIReviewer:

    def review(self, code, evidence):
        raise RuntimeError("Gemini unavailable")


def test_review_service_returns_ai_result():

    service = ReviewService(
        local_reviewer=FakeLocalReviewer(),
        ai_reviewer=FakeAIReviewer(),
    )

    evidence = CodeEvidence(
        syntax_valid=True,
        static_issues=[],
        runtime_result=None,
        runtime_error=None,
    )

    result = service.review(
        "print('hello')",
        evidence,
    )

    assert result.summary == "AI review"
    assert result.positive_points == [
        "AI review completed."
    ]


def test_review_service_falls_back_to_local_review():

    service = ReviewService(
        local_reviewer=FakeLocalReviewer(),
        ai_reviewer=FailingAIReviewer(),
    )

    evidence = CodeEvidence(
        syntax_valid=True,
        static_issues=[],
        runtime_result=None,
        runtime_error=None,
    )

    result = service.review(
        "print('hello')",
        evidence,
    )

    assert result.summary == "Local review"
    assert result.positive_points == [
        "Local check passed."
    ]