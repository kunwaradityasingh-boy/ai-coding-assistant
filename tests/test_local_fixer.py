from src.fixer.local_fixer import LocalFixer
from src.schemas.evidence import CodeEvidence


def test_local_fixer_handles_zero_division():

    fixer = LocalFixer()

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

    result = fixer.fix(
        code="""x = 10
y = 0
print(x / y)
""",
        evidence=evidence,
    )

    assert result.success is True
    assert result.fixed_code is not None
    assert "if y != 0:" in result.fixed_code
    assert "Cannot divide by zero." in result.fixed_code
    assert len(result.changes) == 2


def test_local_fixer_returns_failure_when_no_fix_exists():

    fixer = LocalFixer()

    evidence = CodeEvidence(
        syntax_valid=True,
        static_issues=[],
        runtime_result=None,
        runtime_error={
            "type": "ValueError",
            "message": "invalid value",
            "line": 2,
        },
    )

    result = fixer.fix(
        code="x = int('abc')",
        evidence=evidence,
    )

    assert result.success is False
    assert result.fixed_code is None
    assert result.changes == []


def test_local_fixer_preserves_original_code():

    fixer = LocalFixer()

    original_code = """a = 100
b = 0
print(a / b)
"""

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

    result = fixer.fix(
        code=original_code,
        evidence=evidence,
    )

    assert result.success is True
    assert result.fixed_code is not None

    assert "a = 100" in result.fixed_code
    assert "b = 0" in result.fixed_code
    assert "if b != 0:" in result.fixed_code
    assert "print(a / b)" in result.fixed_code

    assert "x = 10" not in result.fixed_code
    assert "y = 0" not in result.fixed_code