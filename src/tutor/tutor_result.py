from dataclasses import dataclass, field


@dataclass
class TutorResult:
    explanation: str
    hints: list[str] = field(default_factory=list)
    concept: str | None = None
    next_step: str | None = None