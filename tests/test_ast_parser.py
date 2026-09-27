from src.parser.ast_parser import parse_python_code


def test_parse_valid_python():
    code = "x = 10"

    result = parse_python_code(code)

    assert result["success"] is True
    assert result["tree"] is not None
    assert result["error"] is None

def test_parse_invalid_python():
    code = "x ="

    result = parse_python_code(code)

    assert result["success"] is False
    assert result["tree"] is None
    assert result["error"]["type"] == "SyntaxError"