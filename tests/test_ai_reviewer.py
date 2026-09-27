import pytest

from src.review.ai_reviewer import AIReviewer


def test_ai_reviewer_is_abstract():
    with pytest.raises(TypeError):
        AIReviewer()