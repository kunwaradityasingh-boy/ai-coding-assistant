import json

from src.review.gemini_client import GeminiClient


def test_gemini_structured_live_call():

    client = GeminiClient()

    schema = {
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

    prompt = """
Review this Python code:

x = 10
y = 0
print(x / y)

Return a beginner-friendly code review.
Identify the runtime problem and explain how to fix it.
"""

    response = client.generate_structured(
        prompt,
        schema,
    )

    data = json.loads(response)

    assert isinstance(data, dict)
    assert isinstance(data["summary"], str)
    assert isinstance(data["issues"], list)
    assert isinstance(data["positive_points"], list)

    assert len(data["issues"]) > 0