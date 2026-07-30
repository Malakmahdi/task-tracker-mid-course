from datetime import date, timedelta


def create_task(client, **overrides):
    payload = {
        "title": "Write tests",
        "description": "Cover the task API",
        "status": "todo",
        "priority": "high",
        "assignee": "Malak",
        "tags": ["course"],
    }
    payload.update(overrides)
    return client.post("/tasks", json=payload)


def test_create_and_list_task(client):
    response = create_task(client)
    assert response.status_code == 201
    assert response.json()["title"] == "Write tests"
    assert client.get("/tasks").json() == [response.json()]


def test_update_task_status(client):
    task = create_task(client).json()
    response = client.patch(f"/tasks/{task['id']}", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_delete_missing_task_returns_404(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404


def test_create_with_valid_due_date(client):
    response = create_task(client, due_date="2030-05-20")
    assert response.status_code == 201
    assert response.json()["due_date"] == "2030-05-20"


def test_invalid_due_date_format_is_rejected(client):
    response = create_task(client, due_date="20/05/2030")
    assert response.status_code == 422


def test_overdue_filter_excludes_done_and_future_tasks(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    overdue = create_task(client, title="Late", due_date=yesterday).json()
    create_task(client, title="Future", due_date=tomorrow)
    create_task(client, title="Completed late", due_date=yesterday, status="done")

    response = client.get("/tasks?overdue=true")
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [overdue["id"]]


def test_update_can_clear_due_date(client):
    task = create_task(client, due_date="2030-05-20").json()
    response = client.patch(f"/tasks/{task['id']}", json={"due_date": None})
    assert response.status_code == 200
    assert response.json()["due_date"] is None


def test_tags_are_trimmed_deduplicated_and_preserved(client):
    task = create_task(client, tags=[" frontend ", "Course", "course"]).json()
    assert task["tags"] == ["frontend", "Course"]

    updated = client.patch(f"/tasks/{task['id']}", json={"priority": "low"}).json()
    assert updated["tags"] == ["frontend", "Course"]


def test_blank_tag_is_rejected(client):
    response = create_task(client, tags=["valid", "  "])
    assert response.status_code == 422


def test_filter_by_tag_is_case_insensitive(client):
    tagged = create_task(client, title="UI task", tags=["Frontend"]).json()
    create_task(client, title="API task", tags=["backend"])

    response = client.get("/tasks?tag=frontend")
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [tagged["id"]]
