import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN

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
    print("Login response:", response.json())
    return response.json().get("access_token")


@pytest.fixture(scope="function")
def auth_header(test_db):
    token = get_authentication_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_anime(auth_header):
    response = client.post(
        "/animes",
        json={
            "title": "My Hero Academia",
            "description": "A superhero story",
            "rating": 8,
        },
        headers=auth_header,
    )
    assert response.status_code == HTTP_201_CREATED  # nosec
    assert response.json()["title"] == "My Hero Academia"  # nosec


def test_get_anime(auth_header):
    create_resp = client.post(
        "/animes",
        json={"title": "Naruto", "description": "Ninja world", "rating": 9},
        headers=auth_header,
    )
    anime_id = create_resp.json()["id"]
    response = client.get(f"/animes/{anime_id}", headers=auth_header)
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json()["title"] == "Naruto"  # nosec


def test_update_anime(auth_header):
    create_resp = client.post(
        "/animes",
        json={
            "title": "One Piece",
            "description": "Pirate adventure",
            "rating": 9,
        },
        headers=auth_header,
    )
    anime_id = create_resp.json()["id"]
    response = client.put(
        f"/animes/{anime_id}",
        json={
            "title": "One Piece",
            "description": "Pirate King story",
            "rating": 10,
        },
        headers=auth_header,
    )
    assert response.status_code == HTTP_200_OK  # nosec
    assert response.json()["description"] == "Pirate King story"  # nosec


def test_delete_anime(auth_header):
    create_resp = client.post(
        "/animes",
        json={
            "title": "Attack on Titan",
            "description": "Titans vs Humans",
            "rating": 10,
        },
        headers=auth_header,
    )
    anime_id = create_resp.json()["id"]
    response = client.delete(f"/animes/{anime_id}")
    assert response.status_code == HTTP_403_FORBIDDEN  # nosec
    get_response = client.get(f"/animes/{anime_id}")
    assert get_response.status_code == HTTP_403_FORBIDDEN  # nosec
