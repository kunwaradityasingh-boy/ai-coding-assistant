from dataclasses import dataclass, field


@dataclass
class AIReviewIssue:
    severity: str
    category: str
    message: str
    line: int | None = None
    suggestion: str | None = None


@dataclass
class AIReviewResponse:
    summary: str
    issues: list[AIReviewIssue] = field(default_factory=list)
    positive_points: list[str] = field(default_factory=list)