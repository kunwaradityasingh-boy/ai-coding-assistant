from src.review.gemini_reviewer import GeminiReviewer
from src.schemas.evidence import CodeEvidence


class FakeGeminiClient:

    def generate_structured(self, prompt, response_schema):
        return """{
            "summary": "The code contains a division by zero error.",
            "issues": [
                {
                    "severity": "error",
                    "category": "runtime",
                    "message": "You are dividing a number by zero.",
                    "line": 3,
                    "suggestion": "Make sure the divisor is not zero before dividing."
                }
            ],
            "positive_points": [
                "The Python syntax is valid."
            ]
        }"""


def test_gemini_reviewer_returns_structured_feedback():

    reviewer = GeminiReviewer(
        client=FakeGeminiClient()
    )

    evidence = CodeEvidence(
        syntax_valid=True,
        static_issues=[],
        runtime_result=None,
        runtime_error={
            "type": "ZeroDivisionError",
            "message": "division by zero",
            "line": 3,
        },
    )

    result = reviewer.review(
        code="""x = 10
y = 0
print(x / y)
""",
        evidence=evidence,
    )

    assert result.summary == (
        "The code contains a division by zero error."
    )

    assert len(result.issues) == 1

    issue = result.issues[0]

    assert issue.severity == "error"
    assert issue.category == "runtime"
    assert issue.line == 3

    assert "dividing" in issue.message
    assert "divisor" in issue.suggestion

    assert result.positive_points == [
        "The Python syntax is valid."
    ]