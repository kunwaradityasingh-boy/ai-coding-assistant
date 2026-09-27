import ast

from src.parser.ast_parser import parse_python_code
from src.runtime.python_runner import run_python_code
from src.verification.verification_result import VerificationResult


class Verifier:

    def verify(
        self,
        original_code: str,
        fixed_code: str,
    ) -> VerificationResult:

        errors = []
        details = []

        # -------------------------------------------------
        # 1. Parse and verify fixed code syntax
        # -------------------------------------------------
        fixed_parse_result = parse_python_code(fixed_code)

        if not fixed_parse_result["success"]:
            syntax_error = fixed_parse_result["error"]

            errors.append(
                f"SyntaxError: {syntax_error['message']}"
            )

            return VerificationResult(
                success=False,
                syntax_valid=False,
                runtime_success=None,
                errors=errors,
                details=[
                    "The fixed code could not be parsed by Python."
                ],
            )

        details.append("Python syntax is valid.")

        # -------------------------------------------------
        # 2. Runtime verification
        # -------------------------------------------------
        runtime_result = run_python_code(fixed_code)

        if not runtime_result["success"]:

            if runtime_result["timed_out"]:
                errors.append("Execution timed out.")
                details.append(
                    "The fixed code did not finish within "
                    "the allowed time."
                )

            else:
                errors.append(
                    runtime_result["stderr"].strip()
                )
                details.append(
                    "The fixed code is syntactically valid "
                    "but failed during execution."
                )

            return VerificationResult(
                success=False,
                syntax_valid=True,
                runtime_success=False,
                errors=errors,
                details=details,
            )

        details.append(
            "The fixed code executed successfully."
        )

        # -------------------------------------------------
        # 3. Parse original code for fix validation
        # -------------------------------------------------
        original_parse_result = parse_python_code(
            original_code
        )

        if not original_parse_result["success"]:
            errors.append(
                "The original code could not be parsed "
                "for fix validation."
            )

            return VerificationResult(
                success=False,
                syntax_valid=True,
                runtime_success=True,
                errors=errors,
                details=details,
            )

        original_tree = original_parse_result["tree"]
        fixed_tree = fixed_parse_result["tree"]

        # -------------------------------------------------
        # 4. Detect original division operations
        # -------------------------------------------------
        original_divisions = [
            node
            for node in ast.walk(original_tree)
            if isinstance(node, ast.BinOp)
            and isinstance(node.op, ast.Div)
        ]

        # If the original code did not contain division,
        # there is no division-specific fix to validate.
        if not original_divisions:
            details.append(
                "No division-specific fix validation was required."
            )

            return VerificationResult(
                success=True,
                syntax_valid=True,
                runtime_success=True,
                errors=[],
                details=details,
            )

        # -------------------------------------------------
        # 5. Validate that original division is preserved
        # -------------------------------------------------
        fixed_divisions = [
            node
            for node in ast.walk(fixed_tree)
            if isinstance(node, ast.BinOp)
            and isinstance(node.op, ast.Div)
        ]

        if not fixed_divisions:
            errors.append(
                "The fixed code removed the original "
                "division operation."
            )

            details.append(
                "Fix validation failed: the original "
                "division operation was not preserved."
            )

            return VerificationResult(
                success=False,
                syntax_valid=True,
                runtime_success=True,
                errors=errors,
                details=details,
            )

        # -------------------------------------------------
        # 6. Validate zero-division protection
        # -------------------------------------------------
        for division in original_divisions:

            if not isinstance(
                division.right,
                ast.Name,
            ):
                continue

            divisor_name = division.right.id

            matching_guard = False

            for node in ast.walk(fixed_tree):

                if not isinstance(node, ast.If):
                    continue

                test = node.test

                if not isinstance(
                    test,
                    ast.Compare,
                ):
                    continue

                if len(test.ops) != 1:
                    continue

                if not isinstance(
                    test.ops[0],
                    ast.NotEq,
                ):
                    continue

                if not isinstance(
                    test.left,
                    ast.Name,
                ):
                    continue

                if test.left.id != divisor_name:
                    continue

                if len(test.comparators) != 1:
                    continue

                comparator = test.comparators[0]

                if not isinstance(
                    comparator,
                    ast.Constant,
                ):
                    continue

                if comparator.value != 0:
                    continue

                body_divisions = [
                    child
                    for child in ast.walk(node)
                    if isinstance(child, ast.BinOp)
                    and isinstance(child.op, ast.Div)
                ]

                if body_divisions:
                    matching_guard = True
                    break

            if not matching_guard:
                errors.append(
                    f"The fixed code does not provide a "
                    f"verified zero check for divisor "
                    f"'{divisor_name}'."
                )

                details.append(
                    "Fix validation failed: the original "
                    "division does not have a verified "
                    "zero-division guard."
                )

                return VerificationResult(
                    success=False,
                    syntax_valid=True,
                    runtime_success=True,
                    errors=errors,
                    details=details,
                )

        details.append(
            "The original division operation is preserved "
            "with verified zero-division protection."
        )

        # -------------------------------------------------
        # 7. Final verification success
        # -------------------------------------------------
        return VerificationResult(
            success=True,
            syntax_valid=True,
            runtime_success=True,
            errors=[],
            details=details,
        )