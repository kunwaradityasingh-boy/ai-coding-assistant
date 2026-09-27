from dataclasses import dataclass, field


@dataclass
class FixResult:
    success: bool
    fixed_code: str | None = None
    explanation: str | None = None
    changes: list[str] = field(default_factory=list)