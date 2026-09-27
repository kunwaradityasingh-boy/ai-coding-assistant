import subprocess
import tempfile
from pathlib import Path


DOCKER_IMAGE = (
    "python@sha256:"
    "cd04730b8511def3fbf14204d66a0c1536f290b8e896ed5a94cd64cb15ac1356"
)


def _is_docker_infrastructure_error(stderr: str) -> bool:
    infrastructure_markers = [
        "failed to connect to the docker API",
        "is the docker daemon running",
        "Cannot connect to the Docker daemon",
        "error during connect",
    ]

    return any(
        marker.lower() in stderr.lower()
        for marker in infrastructure_markers
    )


def run_python_code(code: str, timeout: int = 3):
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "code.py"
        file_path.write_text(code, encoding="utf-8")

        container_path = "/tmp/code.py"

        try:
            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--user",
                    "1000:1000",
                    "--cap-drop",
                    "ALL",
                    "--security-opt",
                    "no-new-privileges:true",
                    "--network",
                    "none",
                    "--read-only",
                    "--tmpfs",
                    "/tmp",
                    "--cpus",
                    "1",
                    "--memory",
                    "128m",
                    "--pids-limit",
                    "64",
                    "-v",
                    f"{file_path}:{container_path}:ro",
                    DOCKER_IMAGE,
                    "python",
                    container_path,
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            if _is_docker_infrastructure_error(result.stderr):
                return {
                    "success": False,
                    "return_code": None,
                    "stdout": "",
                    "stderr": "Code execution sandbox is currently unavailable.",
                    "timed_out": False,
                }

            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timed_out": False,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "return_code": None,
                "stdout": "",
                "stderr": "Execution timed out.",
                "timed_out": True,
            }

        except FileNotFoundError:
            return {
                "success": False,
                "return_code": None,
                "stdout": "",
                "stderr": "Docker is not available.",
                "timed_out": False,
            }