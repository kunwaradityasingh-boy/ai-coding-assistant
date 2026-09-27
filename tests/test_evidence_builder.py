from src.analysis.evidence_builder import build_code_evidence


def test_build_evidence_for_valid_code():
    code = "x = 10"

    evidence = build_code_evidence(code)

    assert evidence.syntax_valid is True
    assert evidence.ast_tree is not None
    assert evidence.syntax_error is None


def test_build_evidence_for_invalid_code():
    code = "x ="

    evidence = build_code_evidence(code)

    assert evidence.syntax_valid is False
    assert evidence.ast_tree is None
    assert evidence.syntax_error["type"] == "SyntaxError"


def test_build_evidence_includes_runtime_result():
    code = 'print("Hello")'

    evidence = build_code_evidence(code)

    assert evidence.syntax_valid is True
    assert evidence.runtime_result is not None
    assert evidence.runtime_result["success"] is True

def test_build_evidence_parses_runtime_error():
    code = """x = 10
y = 0
print(x / y)
"""

    evidence = build_code_evidence(code)

    assert evidence.runtime_error is not None
    assert evidence.runtime_error["type"] == "ZeroDivisionError"
    assert evidence.runtime_error["message"] == "division by zero"
    assert evidence.runtime_error["line"] == 3
