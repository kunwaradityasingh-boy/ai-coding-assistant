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
