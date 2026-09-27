from src.schemas.evidence import CodeEvidence
from src.tutor.local_tutor import LocalTutor


def test_local_tutor_explains_zero_division():

    tutor = LocalTutor()

    evidence = CodeEvidence(
        syntax_valid=True,
        static_issues=[],
        runtime_result=None,
        runtime_error={
            "type": "ZeroDivisionError",
            "message": "division by zero",
            "line": 3,
        },
    )

    result = tutor.teach(
        code="""x = 10
y = 0
print(x / y)
""",
        evidence=evidence,
    )

    assert result.concept == "Division by zero"
    assert len(result.hints) == 3
    assert "zero" in result.explanation.lower()
    assert result.next_step


def test_local_tutor_handles_syntax_error():

    tutor = LocalTutor()

    evidence = CodeEvidence(
        syntax_valid=False,
        syntax_error={
            "type": "SyntaxError",
            "message": "invalid syntax",
            "line": 2,
            "column": 5,
        },
    )

    result = tutor.teach(
        code="x = 10\nif x\n",
        evidence=evidence,
    )

    assert result.concept == "Python syntax"
    assert len(result.hints) == 3
    assert result.next_step