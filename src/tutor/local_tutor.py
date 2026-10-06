from src.schemas.evidence import CodeEvidence
from src.tutor.tutor import Tutor
from src.tutor.tutor_result import TutorResult


class LocalTutor(Tutor):

    def teach(
        self,
        code: str,
        evidence: CodeEvidence,
    ) -> TutorResult:

        if evidence.runtime_error:
            error_type = evidence.runtime_error.get("type")
            message = evidence.runtime_error.get("message")
            line = evidence.runtime_error.get("line")

            if error_type == "ExecutionTimeout":
                return TutorResult(
                    explanation=(
                        "The program did not finish within the allowed "
                        "execution time. This can happen when a loop "
                        "does not have a stopping condition."
                    ),
                    hints=[
                        "Look at the loop condition.",
                        (
                            "Check whether something inside the loop "
                            "changes that condition."
                        ),
                        (
                            "Think about what condition would eventually "
                            "stop the loop."
                        ),
                    ],
                    concept="Loop termination",
                    next_step=(
                        "Add or correct the stopping condition so the "
                        "loop can eventually finish."
                    ),
                )

            if error_type == "ZeroDivisionError":
                return TutorResult(
                    explanation=(
                        f"Line {line} tries to divide a number by zero. "
                        "Python does not allow division by zero."
                    ),
                    hints=[
                        "Look at the value of the divisor.",
                        "What happens when the divisor is 0?",
                        ("Can you check the divisor before " "performing division?"),
                    ],
                    concept="Division by zero",
                    next_step=(
                        "Try adding a condition that prevents division "
                        "when the divisor is zero."
                    ),
                )

            return TutorResult(
                explanation=(f"The program produced {error_type}: {message}."),
                hints=[
                    "Look at the reported line.",
                    "Identify which operation caused the error.",
                    (
                        "Think about what input or value caused "
                        "that operation to fail."
                    ),
                ],
                concept=error_type,
                next_step=("Try correcting the cause of the runtime error."),
            )

        if not evidence.syntax_valid:
            return TutorResult(
                explanation=("Python could not understand the structure of the code."),
                hints=[
                    "Look at the reported line.",
                    "Check brackets, indentation, and punctuation.",
                    "Compare the line with normal Python syntax.",
                ],
                concept="Python syntax",
                next_step=("Correct the syntax and run the code again."),
            )

        return TutorResult(
            explanation=("No runtime or syntax problem was detected."),
            hints=[
                "Review the code logic step by step.",
                "Check whether the output matches your expectation.",
            ],
            concept="Code reasoning",
            next_step=("Test the program with different inputs."),
        )
