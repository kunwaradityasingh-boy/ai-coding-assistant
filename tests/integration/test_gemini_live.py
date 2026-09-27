from src.review.gemini_client import GeminiClient


def test_gemini_live_call():
    client = GeminiClient()

    response = client.generate(
        "Reply with exactly: Gemini connection successful."
    )

    assert response
    assert isinstance(response, str)