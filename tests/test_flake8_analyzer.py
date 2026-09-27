from src.analysis.flake8_analyzer import analyze_with_flake8


def test_flake8_detects_unused_import():
    code = """import os

x = 10
"""

    issues = analyze_with_flake8(code)

    assert len(issues) > 0
    assert any(issue["code"].startswith("F401") for issue in issues)