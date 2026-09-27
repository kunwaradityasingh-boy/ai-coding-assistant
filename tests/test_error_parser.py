from src.runtime.error_parser import parse_runtime_error


def test_parse_zero_division_error():
    stderr = """Traceback (most recent call last):
  File "C:\\temp\\code.py", line 3, in <module>
    print(x / y)
ZeroDivisionError: division by zero
"""

    error = parse_runtime_error(stderr)

    assert error["type"] == "ZeroDivisionError"
    assert error["message"] == "division by zero"
    assert error["line"] == 3