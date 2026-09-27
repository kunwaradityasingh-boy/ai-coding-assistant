import pytest

from src.review.reviewer import Reviewer


def test_reviewer_is_abstract():
    with pytest.raises(TypeError):
        Reviewer()