from apps.api.main import app


def test_analyze_runtime_error():
    client = app.test_client()

    response = client.post(
        "/analyze",
        json={
            "code": """x = 10
y = 0
print(x / y)
"""
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert isinstance(data["review"]["summary"], str)
    assert data["review"]["summary"].strip()

    runtime_issues = [
        issue
        for issue in data["review"]["issues"]
        if issue["category"] == "runtime"
    ]

    assert len(runtime_issues) == 1
    assert runtime_issues[0]["line"] == 3

    runtime_message = runtime_issues[0]["message"].lower()

    assert "zero" in runtime_message
    assert "division" in runtime_message

def test_run_successful_execution():
    client = app.test_client()

    response = client.post(
        "/run",
        json={"code": "print(123)"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["stdout"] == "123\n"
    assert data["stderr"] == ""
    assert data["return_code"] == 0
    assert data["timed_out"] is False


def test_run_runtime_error():
    client = app.test_client()

    response = client.post(
        "/run",
        json={"code": "print(1 / 0)"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is False
    assert "ZeroDivisionError" in data["stderr"]
    assert "division by zero" in data["stderr"]
    assert data["timed_out"] is False


def test_run_rejects_empty_code():
    client = app.test_client()

    response = client.post(
        "/run",
        json={"code": ""},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["error"] == "Code cannot be empty."


def test_run_timeout():
    client = app.test_client()

    response = client.post(
        "/run",
        json={"code": "while True: pass"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is False
    assert data["timed_out"] is True
    assert data["stderr"] == "Execution timed out."