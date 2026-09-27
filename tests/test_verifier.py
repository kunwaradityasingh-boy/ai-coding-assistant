from src.verification.verifier import Verifier


def test_verifier_accepts_working_code():
    verifier = Verifier()

    code = """x = 10
print(x)
"""

    result = verifier.verify(
        original_code=code,
        fixed_code=code,
    )

    assert result.success is True
    assert result.syntax_valid is True
    assert result.runtime_success is True
    assert result.errors == []


def test_verifier_rejects_syntax_error():
    verifier = Verifier()

    code = """x = 10
if x
"""

    result = verifier.verify(
        original_code=code,
        fixed_code=code,
    )

    assert result.success is False
    assert result.syntax_valid is False
    assert result.runtime_success is None
    assert len(result.errors) > 0


def test_verifier_rejects_runtime_error():
    verifier = Verifier()

    code = """x = 10
y = 0
print(x / y)
"""

    result = verifier.verify(
        original_code=code,
        fixed_code=code,
    )

    assert result.success is False
    assert result.syntax_valid is True
    assert result.runtime_success is False
    assert len(result.errors) > 0


def test_verifier_rejects_semantically_wrong_zero_division_fix():
    verifier = Verifier()

    original_code = """a = 100
b = 0
print(a / b)
"""

    wrong_fixed_code = """a = 100
b = 0
print("Cannot divide by zero.")
"""

    result = verifier.verify(
        original_code=original_code,
        fixed_code=wrong_fixed_code,
    )

    assert result.success is False
    assert result.syntax_valid is True
    assert result.runtime_success is True
    assert len(result.errors) > 0


def test_verifier_accepts_verified_zero_division_fix():
    verifier = Verifier()

    original_code = """a = 100
b = 0
print(a / b)
"""

    fixed_code = """a = 100
b = 0

if b != 0:
    print(a / b)
else:
    print("Cannot divide by zero.")
"""

    result = verifier.verify(
        original_code=original_code,
        fixed_code=fixed_code,
    )

    assert result.success is True
    assert result.syntax_valid is True
    assert result.runtime_success is True
    assert result.errors == []
    assert (
        "zero-division protection"
        in " ".join(result.details).lower()
    )