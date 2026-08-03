import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture(autouse=True)
def reset_store():
    main.tasks.clear()
    main.next_task_id = 1
    yield
    main.tasks.clear()


@pytest.fixture
def client():
    return TestClient(main.app)
