from src.analysis.evidence_builder import build_code_evidence
from src.review.local_reviewer import LocalReviewer


def test_local_reviewer_detects_runtime_error():
    code = """x = 10
y = 0
print(x / y)
"""

    evidence = build_code_evidence(code)
    reviewer = LocalReviewer()

    result = reviewer.review(evidence)

    assert len(result.issues) > 0
    assert any(issue.category == "runtime" for issue in result.issues)

    runtime_issue = next(
        issue for issue in result.issues
        if issue.category == "runtime"
    )

    assert runtime_issue.line == 3
    assert "ZeroDivisionError" in runtime_issue.message
    assert "division by zero" in runtime_issue.message


def test_local_reviewer_accepts_working_code():
    code = """x = 10
print(x)
"""

    evidence = build_code_evidence(code)
    reviewer = LocalReviewer()

    result = reviewer.review(evidence)

    assert result.issues == []
    assert "successfully" in result.positive_points[-1]