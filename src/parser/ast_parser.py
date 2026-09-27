import ast


def parse_python_code(code: str):
    try:
        return {
            "success": True,
            "tree": ast.parse(code),
            "error": None,
        }

    except SyntaxError as error:
        return {
            "success": False,
            "tree": None,
            "error": {
                "type": "SyntaxError",
                "message": error.msg,
                "line": error.lineno,
                "column": error.offset,
            },
        }