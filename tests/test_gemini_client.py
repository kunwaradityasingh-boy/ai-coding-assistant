import pytest

from src.review.gemini_client import GeminiClient


def test_gemini_client_requires_api_key(monkeypatch):
    monkeypatch.setattr(
        "src.review.gemini_client.GEMINI_API_KEY",
        None,
    )

    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        GeminiClient()

def test_gemini_model_name():
    from src.review.gemini_client import GEMINI_MODEL

    assert GEMINI_MODEL == "gemini-3.6-flash"

def test_gemini_client_has_structured_generation_method():
    from src.review.gemini_client import GeminiClient

    assert hasattr(GeminiClient, "generate_structured")

def test_structured_generation_handles_server_error(monkeypatch):
    from src.review.gemini_client import GeminiClient

    class FakeModels:

        def generate_content(self, **kwargs):
            from google.genai.errors import ServerError

            raise ServerError(
                503,
                {
                    "error": {
                        "code": 503,
                        "message": "Service unavailable",
                        "status": "UNAVAILABLE",
                    }
                },
            )

    client = GeminiClient.__new__(GeminiClient)

    class FakeClient:
        models = FakeModels()

    client.client = FakeClient()

    with pytest.raises(
        RuntimeError,
        match="Gemini service is temporarily unavailable",
    ):
        client.generate_structured(
            "test prompt",
            {"type": "object"},
        )
