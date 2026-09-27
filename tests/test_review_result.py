from src.review.review_result import ReviewIssue, ReviewResult


def test_review_result_creation():
    issue = ReviewIssue(
        severity="error",
        category="runtime",
        message="Division by zero.",
        line=3,
        suggestion="Check that the denominator is not zero.",
    )

    result = ReviewResult(
        summary="The code contains a runtime problem.",
        issues=[issue],
        positive_points=["The code is syntactically valid."],
    )

    assert result.summary == "The code contains a runtime problem."
    assert len(result.issues) == 1
    assert result.issues[0].line == 3
    assert result.positive_points[0] == "The code is syntactically valid."