import re


def parse_runtime_error(stderr: str):
    line_match = re.search(r'File ".*?", line (\d+)', stderr)
    error_match = re.search(r"^(\w+Error): (.+)$", stderr, re.MULTILINE)

    line = int(line_match.group(1)) if line_match else None

    if error_match:
        error_type = error_match.group(1)
        message = error_match.group(2)
    else:
        error_type = None
        message = None

    return {
        "type": error_type,
        "message": message,
        "line": line,
    }