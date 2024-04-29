import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
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


def test_create_genre(auth_header):
    response = client.post(
        "/genres", json={"name": "Action"}, headers=auth_header
    )
    assert response.status_code == HTTP_201_CREATED  # nosec
    assert response.json()["name"] == "Action"  # nosec


def test_get_all_genres(auth_header):
    client.post("/genres", json={"name": "Action"}, headers=auth_header)
    client.post("/genres", json={"name": "Comedy"}, headers=auth_header)
    response = client.get("/genres", headers=auth_header)
    assert response.status_code == HTTP_200_OK  # nosec
    assert len(response.json()) == 2  # nosec


def test_get_genre_by_id(auth_header):
    create_response = client.post(
        "/genres", json={"name": "Romance"}, headers=auth_header
    )
    genre_id = create_response.json()["id"]
    response = client.get(f"/genres/{genre_id}", headers=auth_header)
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json()["name"] == "Romance"  # nosec


def test_update_genre(auth_header):
    create_response = client.post(
        "/genres", json={"name": "Thriller"}, headers=auth_header
    )
    genre_id = create_response.json()["id"]
    response = client.put(
        f"/genres/{genre_id}", json={"name": "Mystery"}, headers=auth_header
    )
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json()["name"] == "Mystery"  # nosec


def test_delete_genre(auth_header):
    create_response = client.post(
        "/genres", json={"name": "Drama"}, headers=auth_header
    )
    genre_id = create_response.json()["id"]
    response = client.delete(f"/genres/{genre_id}", headers=auth_header)
    assert response.status_code == HTTP_204_NO_CONTENT  # nosec
    response = client.get(f"/genres/{genre_id}", headers=auth_header)
    assert response.status_code == HTTP_404_NOT_FOUND  # nosec
