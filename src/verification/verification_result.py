from dataclasses import dataclass, field


@dataclass
class VerificationResult:
    success: bool
    syntax_valid: bool
    runtime_success: bool | None = None
    errors: list[str] = field(default_factory=list)
    details: list[str] = field(default_factory=list)