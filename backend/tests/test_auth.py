import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
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


def test_register_new_user(test_db):
    response = client.post(
        "/register", json={"username": "newuser", "password": "newpass123"}
    )
    assert (
        response.status_code == HTTP_201_CREATED
    ), "Expected HTTP 201 Created response"  # nosec
    assert response.json() == {
        "message": "User registered successfully"
    }, "Expected success message not returned"  # nosec


def test_register_user_existing_username(test_db):
    client.post(
        "/register", json={"username": "testuser", "password": "testpass123"}
    )
    response = client.post(
        "/register", json={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == HTTP_400_BAD_REQUEST  # nosec
    assert "Username already exists" in response.json()["detail"]  # nosec


def test_login_valid(test_db):
    client.post(
        "/register", json={"username": "testuser", "password": "testpass123"}
    )
    response = client.post("/login?username=testuser&password=testpass123")
    assert response.status_code == HTTP_200_OK  # nosec
    assert "access_token" in response.json()  # nosec


def test_login_invalid(test_db):
    response = client.post("/login?username=nonexistent&password=wrongpass")
    assert response.status_code == HTTP_403_FORBIDDEN  # nosec
    assert "Invalid Credentials" in response.json()["detail"]  # nosec


def test_refresh_token_valid(test_db):
    client.post(
        "/register", json={"username": "testuser", "password": "testpass123"}
    )
    login_response = client.post(
        "/login?username=testuser&password=testpass123"
    )
    refresh_token = login_response.json()["refresh_token"]
    response = client.post("/refresh?refresh_token=" + refresh_token)
    assert response.status_code == HTTP_200_OK  # nosec
    assert "access_token" in response.json()  # nosec


def test_refresh_token_invalid(test_db):
    response = client.post("/refresh?refresh_token=invalidtoken")
    assert response.status_code == HTTP_401_UNAUTHORIZED  # nosec
    assert (
        "Invalid token or expired token" in response.json()["detail"]
    )  # nosec


def test_logout(test_db):
    client.post(
        "/register", json={"username": "testuser", "password": "testpass123"}
    )
    login_response = client.post(
        "/login?username=testuser&password=testpass123"
    )
    access_token = login_response.json()["access_token"]
    response = client.post(
        "/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json() == {"message": "Successfully logged out"}  # nosec
