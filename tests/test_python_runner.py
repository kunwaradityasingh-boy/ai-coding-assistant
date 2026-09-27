from src.runtime.python_runner import run_python_code


def test_successful_execution():
    result = run_python_code('print("Hello")')

    assert result["success"] is True
    assert result["stdout"].strip() == "Hello"
    assert result["timed_out"] is False


def test_runtime_error():
    code = "x = 10\ny = 0\nprint(x / y)"

    result = run_python_code(code)

    assert result["success"] is False
    assert "ZeroDivisionError" in result["stderr"]
    assert result["timed_out"] is False