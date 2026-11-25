import os

# Đặt khóa trước khi import app (CI không có file .env)
os.environ.setdefault("SECRET_KEY", "khoa-chi-dung-de-test-" + "x" * 32)

import copy

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repository import repo

_SNAPSHOT = (copy.deepcopy(repo._items), repo._next_id)


@pytest.fixture(autouse=True)
def reset_data():
    """Trước mỗi test, đưa thực đơn về đúng 4 món mẫu."""
    repo._items = copy.deepcopy(_SNAPSHOT[0])
    repo._next_id = _SNAPSHOT[1]
    yield


@pytest.fixture
def client():
    return TestClient(app)


def _login(client, username, password):
    r = client.post("/auth/login",
                    data={"username": username, "password": password})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
def staff(client):
    return _login(client, "admin", "admin123")


@pytest.fixture
def student(client):
    return _login(client, "sinhvien", "sv123456")
