from http import HTTPStatus

from fastapi.testclient import TestClient


def test_read_root_returns_ok_and_hello_world(client: TestClient):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello world!"}


def test_read_page_returns_ok_and_html(client: TestClient):
    response = client.get("/page")

    assert response.status_code == HTTPStatus.OK
    assert response.text == "This is a page."


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "username": "user",
            "email": "test@test.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "user",
        "email": "test@test.com",
    }


def test_read_users(client: TestClient):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "username": "user",
                "email": "test@test.com",
            }
        ]
    }


def test_read_user(client: TestClient):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "user",
        "email": "test@test.com",
    }


def test_read_user_not_found(client: TestClient):
    response = client.get("/users/1234")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client: TestClient):
    response = client.put(
        "/users/1",
        json={
            "username": "testuser2",
            "email": "test@test.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testuser2",
        "email": "test@test.com",
    }


def test_update_user_raises_not_found(client: TestClient):
    response = client.put(
        "/users/1234",
        json={
            "username": "testuser2",
            "email": "test@test.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client: TestClient):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_raises_not_found(client: TestClient):
    response = client.delete("/users/1234")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
