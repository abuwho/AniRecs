import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from anirecs.main import app
from anirecs.database import (
    Base,
    get_db,
    DATABASE_URL,
)

client = TestClient(app)

engine = create_engine(DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def get_authentication_token():
    client.post(
        "/register", json={"username": "testuser", "password": "testpassword"}
    )
    response = client.post(
        "/login", params={"username": "testuser", "password": "testpassword"}
    )
    return response.json().get("access_token")


@pytest.fixture(scope="function")
def auth_header(test_db):
    token = get_authentication_token()
    return {"Authorization": f"Bearer {token}"}


def test_get_current_user(auth_header):
    response = client.get("/users/me", headers=auth_header)
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json()["username"] == "testuser"  # nosec


def test_get_users(auth_header):
    response = client.get("/users", headers=auth_header)
    assert response.status_code == HTTP_200_OK  # nosec
    assert len(response.json()) >= 1  # nosec


def test_get_users_with_username(auth_header):
    response = client.get(
        "/users", params={"username": "test"}, headers=auth_header
    )
    assert response.status_code == HTTP_200_OK  # nosec
    assert all("test" in user["username"] for user in response.json())  # nosec


def test_get_user_by_id(auth_header):
    user_id = client.get("/users/me", headers=auth_header).json()["id"]
    response = client.get(f"/users/{user_id}", headers=auth_header)
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json()["id"] == user_id  # nosec


def test_update_user(auth_header):
    user_id = client.get("/users/me", headers=auth_header).json()["id"]
    response = client.put(
        f"/users/{user_id}",
        json={"username": "newtestuser"},
        headers=auth_header,
    )
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json()["username"] == "newtestuser"  # nosec


def test_delete_user(auth_header):
    response = client.delete("/users/me", headers=auth_header)
    assert response.status_code == HTTP_204_NO_CONTENT  # nosec
