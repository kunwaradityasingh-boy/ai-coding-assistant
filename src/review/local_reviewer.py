from src.review.reviewer import Reviewer
from src.review.review_result import ReviewIssue, ReviewResult
from src.schemas.evidence import CodeEvidence


class LocalReviewer(Reviewer):

    def review(self, evidence: CodeEvidence) -> ReviewResult:
        issues = []
        positive_points = []

        if evidence.syntax_valid:
            positive_points.append(
                "The Python code has valid syntax."
            )
        else:
            error = evidence.syntax_error or {}

            issues.append(
                ReviewIssue(
                    severity="error",
                    category="syntax",
                    message=error.get(
                        "message",
                        "Syntax error.",
                    ),
                    line=error.get("line"),
                    suggestion=(
                        "Check the reported line and correct "
                        "the Python syntax."
                    ),
                )
            )

            return ReviewResult(
                summary="The code contains a syntax error.",
                issues=issues,
                positive_points=positive_points,
            )

        for issue in evidence.static_issues:
            issues.append(
                ReviewIssue(
                    severity="warning",
                    category="static-analysis",
                    message=issue["message"],
                    line=issue["line"],
                    suggestion=(
                        "Review this line and follow the "
                        "static-analysis recommendation."
                    ),
                )
            )

        runtime_result = evidence.runtime_result
        runtime_error = evidence.runtime_error

        if runtime_result and not runtime_result["success"]:
            if runtime_error:
                error_type = runtime_error.get("type")
                message = runtime_error.get("message")
                line = runtime_error.get("line")

                if error_type == "ExecutionTimeout":
                    issues.append(
                        ReviewIssue(
                            severity="error",
                            category="runtime",
                            message=(
                                "The program exceeded the allowed "
                                "execution time."
                            ),
                            line=None,
                            suggestion=(
                                "Check whether a loop has a stopping "
                                "condition and whether its state changes."
                            ),
                        )
                    )

                else:
                    formatted_message = (
                        f"{error_type}: {message}"
                    )

                    issues.append(
                        ReviewIssue(
                            severity="error",
                            category="runtime",
                            message=formatted_message,
                            line=line,
                            suggestion=(
                                "Check the reported line and understand "
                                "why the operation caused the runtime error."
                            ),
                        )
                    )

            else:
                issues.append(
                    ReviewIssue(
                        severity="error",
                        category="runtime",
                        message=(
                            "The program encountered a runtime error."
                        ),
                        suggestion=(
                            "Review the runtime error and correct "
                            "its cause."
                        ),
                    )
                )

        elif runtime_result and runtime_result["success"]:
            positive_points.append(
                "The code executed successfully."
            )

        if issues:
            summary = (
                f"The review found {len(issues)} issue(s)."
            )
        else:
            summary = (
                "No issues were detected by the current checks."
            )

        return ReviewResult(
            summary=summary,
            issues=issues,
            positive_points=positive_points,
            source="local",
        )