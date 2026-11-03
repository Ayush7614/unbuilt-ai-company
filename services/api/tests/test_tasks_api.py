def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_retrieve_task(client):
    created = client.post("/tasks", json={"task_type": "research", "input": {"topic": "MCP"}})
    assert created.status_code == 201
    payload = created.json()
    assert payload["task_type"] == "research"
    assert payload["status"] == "pending"
    assert payload["input"] == {"topic": "MCP"}

    fetched = client.get(f"/tasks/{payload['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == payload["id"]


def test_list_tasks(client):
    client.post("/tasks", json={"task_type": "research", "input": {"topic": "one"}})
    client.post("/tasks", json={"task_type": "content", "input": {"topic": "two"}})
    response = client.get("/tasks?limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_reject_invalid_task_type(client):
    response = client.post("/tasks", json={"task_type": "Research Task", "input": {}})
    assert response.status_code == 422


def test_task_state_transitions(client):
    created = client.post("/tasks", json={"task_type": "research", "input": {}}).json()
    started = client.patch(f"/tasks/{created['id']}/status", json={"status": "running"})
    assert started.status_code == 200
    completed = client.patch(
        f"/tasks/{created['id']}/status",
        json={"status": "completed", "result": {"report": "example"}},
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"


def test_reject_invalid_state_transition(client):
    created = client.post("/tasks", json={"task_type": "research", "input": {}}).json()
    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "completed"})
    assert response.status_code == 409


def test_failed_task_requires_error(client):
    created = client.post("/tasks", json={"task_type": "research", "input": {}}).json()
    client.patch(f"/tasks/{created['id']}/status", json={"status": "running"})
    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "failed"})
    assert response.status_code == 409
