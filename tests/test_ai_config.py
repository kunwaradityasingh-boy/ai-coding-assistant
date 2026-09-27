from src.review.ai_config import GEMINI_API_KEY


def test_gemini_api_key_configuration_exists():
    assert GEMINI_API_KEY is not None