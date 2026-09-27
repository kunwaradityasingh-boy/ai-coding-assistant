from src.analysis.flake8_analyzer import analyze_with_flake8
from src.parser.ast_parser import parse_python_code
from src.runtime.error_parser import parse_runtime_error
from src.schemas.evidence import CodeEvidence
from src.runtime.python_runner import run_python_code

def build_code_evidence(code: str) -> CodeEvidence:
    parse_result = parse_python_code(code)

    if parse_result["success"]:
        static_issues = analyze_with_flake8(code)
        runtime_result = run_python_code(code)

        runtime_error = None

        runtime_error = None
        if runtime_result["timed_out"]:
            runtime_error = {
                "type": "ExecutionTimeout",
                "message": "Execution timed out.",
                "line": None,
            }
        elif not runtime_result["success"]:
            runtime_error = parse_runtime_error(
                runtime_result["stderr"]
            )
        return CodeEvidence(
            syntax_valid=True,
            ast_tree=parse_result["tree"],
            syntax_error=None,
            static_issues=static_issues,
            runtime_result=runtime_result,
            runtime_error=runtime_error,
        )

    return CodeEvidence(
        syntax_valid=False,
        ast_tree=None,
        syntax_error=parse_result["error"],
        static_issues=[],
        runtime_result=None,
        runtime_error=None,
    )
