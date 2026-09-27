from dataclasses import dataclass, field


@dataclass
class ReviewIssue:
    severity: str
    category: str
    message: str
    line: int | None = None
    suggestion: str | None = None


@dataclass
class ReviewResult:
    summary: str
    issues: list[ReviewIssue] = field(default_factory=list)
    positive_points: list[str] = field(default_factory=list)
    source: str = "local"