from google import genai
from google.genai import errors

from src.review.ai_config import GEMINI_API_KEY


GEMINI_MODEL = "gemini-3.6-flash"


class GeminiClient:

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return response.text

    def generate_structured(self, prompt: str, response_schema) -> str:
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": response_schema,
                },
            )

            return response.text

        except errors.ServerError as error:
            raise RuntimeError(
                "Gemini service is temporarily unavailable. "
                "Please try again later."
            ) from error