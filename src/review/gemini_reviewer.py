import json

from src.review.ai_reviewer import AIReviewer
from src.review.ai_response import AIReviewIssue, AIReviewResponse
from src.review.gemini_client import GeminiClient
from src.review.review_result import ReviewIssue, ReviewResult
from src.schemas.evidence import CodeEvidence


GEMINI_REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string"
        },
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string"
                    },
                    "category": {
                        "type": "string"
                    },
                    "message": {
                        "type": "string"
                    },
                    "line": {
                        "type": "integer"
                    },
                    "suggestion": {
                        "type": "string"
                    }
                },
                "required": [
                    "severity",
                    "category",
                    "message",
                    "line",
                    "suggestion"
                ]
            }
        },
        "positive_points": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "summary",
        "issues",
        "positive_points"
    ]
}


class GeminiReviewer(AIReviewer):

    def __init__(self, client=None):
        self.client = client or GeminiClient()

    def review(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> ReviewResult:

        prompt = self._build_prompt(code, evidence)

        response = self.client.generate_structured(
            prompt,
            GEMINI_REVIEW_SCHEMA,
        )

        ai_response = self._parse_response(response)

        return ReviewResult(
            summary=ai_response.summary,
            issues=[
                ReviewIssue(
                    severity=issue.severity,
                    category=issue.category,
                    message=issue.message,
                    line=issue.line,
                    suggestion=issue.suggestion,
                )
                for issue in ai_response.issues
            ],
            positive_points=ai_response.positive_points,
            source="gemini",
        )

    def _build_prompt(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> str:

        return f"""
You are an AI coding reviewer for beginner Python programmers.

Review the following Python code using the supplied evidence.

CODE:
{code}

EVIDENCE:
Syntax valid: {evidence.syntax_valid}
Static issues: {evidence.static_issues}
Runtime error: {evidence.runtime_error}

Return ONLY valid JSON using this exact structure:

{{
  "summary": "short review summary",
  "issues": [
    {{
      "severity": "error or warning or info",
      "category": "syntax or static-analysis or runtime or logic",
      "message": "simple explanation",
      "line": 1,
      "suggestion": "beginner-friendly suggestion"
    }}
  ],
  "positive_points": [
    "positive observation"
  ]
}}

Rules:
- Do not invent errors.
- Use the supplied evidence.
- Explain problems in simple beginner-friendly language.
- Use null for line when no exact line is known.
- Return JSON only.
""".strip()

    def _parse_response(self, response: str) -> AIReviewResponse:

        data = json.loads(response)

        issues = [
            AIReviewIssue(
                severity=issue["severity"],
                category=issue["category"],
                message=issue["message"],
                line=issue.get("line"),
                suggestion=issue.get("suggestion"),
            )
            for issue in data.get("issues", [])
        ]

        return AIReviewResponse(
            summary=data["summary"],
            issues=issues,
            positive_points=data.get("positive_points", []),
        )