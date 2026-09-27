from dataclasses import dataclass, field
from typing import Any


@dataclass
class CodeEvidence:
    syntax_valid: bool
    ast_tree: Any | None = None
    syntax_error: dict | None = None
    static_issues: list[dict] = field(default_factory=list)
    runtime_result: dict | None = None
    runtime_error: dict | None = None