import subprocess
import sys
import tempfile
from pathlib import Path


def analyze_with_flake8(code: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "code.py"
        file_path.write_text(code, encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "flake8",
                str(file_path),
                "--format=%(row)s:%(col)s:%(code)s:%(text)s",
            ],
            capture_output=True,
            text=True,
        )

        issues = []

        for line in result.stdout.splitlines():
            if not line.strip():
                continue

            parts = line.split(":", 3)

            if len(parts) != 4:
                continue

            issues.append(
                {
                    "line": int(parts[0]),
                    "column": int(parts[1]),
                    "code": parts[2],
                    "message": parts[3],
                }
            )

        return issues