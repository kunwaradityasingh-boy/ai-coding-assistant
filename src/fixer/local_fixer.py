import ast

from src.fixer.fixer import Fixer
from src.fixer.fix_result import FixResult
from src.schemas.evidence import CodeEvidence


class LocalFixer(Fixer):

    def fix(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> FixResult:

        runtime_error = evidence.runtime_error

        if not runtime_error:
            return FixResult(
                success=False,
                fixed_code=None,
                explanation="No automatic local fix is available.",
                changes=[],
            )

        if runtime_error.get("type") != "ZeroDivisionError":
            return FixResult(
                success=False,
                fixed_code=None,
                explanation="No automatic local fix is available.",
                changes=[],
            )

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return FixResult(
                success=False,
                fixed_code=None,
                explanation=(
                    "The original code could not be parsed safely."
                ),
                changes=[],
            )

        division_node = None

        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(
                node.op,
                ast.Div,
            ):
                division_node = node
                break

        if division_node is None:
            return FixResult(
                success=False,
                fixed_code=None,
                explanation=(
                    "A safe division operation could not be identified."
                ),
                changes=[],
            )

        if not isinstance(
            division_node.right,
            ast.Name,
        ):
            return FixResult(
                success=False,
                fixed_code=None,
                explanation=(
                    "The divisor is not a simple variable, "
                    "so an automatic fix is not applied."
                ),
                changes=[],
            )

        divisor_name = division_node.right.id

        source_lines = code.splitlines()
        division_line = division_node.lineno - 1

        if division_line < 0 or division_line >= len(source_lines):
            return FixResult(
                success=False,
                fixed_code=None,
                explanation=(
                    "The division line could not be located safely."
                ),
                changes=[],
            )

        original_line = source_lines[division_line]

        indentation = original_line[
            :len(original_line) - len(original_line.lstrip())
        ]

        fixed_lines = list(source_lines)

        fixed_lines[division_line] = (
            f"{indentation}if {divisor_name} != 0:"
        )

        fixed_lines.insert(
            division_line + 1,
            f"{indentation}    {original_line.lstrip()}",
        )

        fixed_lines.insert(
            division_line + 2,
            f"{indentation}else:",
        )

        fixed_lines.insert(
            division_line + 3,
            (
                f'{indentation}    '
                f'print("Cannot divide by zero.")'
            ),
        )

        fixed_code = "\n".join(fixed_lines) + "\n"

        return FixResult(
            success=True,
            fixed_code=fixed_code,
            explanation=(
                "The divisor is checked before division while "
                "preserving the original code and variable names."
            ),
            changes=[
                f"Added a zero check for '{divisor_name}'.",
                "Preserved the original division statement.",
            ],
        )