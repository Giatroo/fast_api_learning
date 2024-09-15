from http import HTTPStatus

from fastapi.testclient import TestClient


def test_read_root_returns_ok_and_hello_world(client: TestClient):
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello world!"}


def test_read_page_returns_ok_and_html(client: TestClient):
    # Act
    response = client.get("/page")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.text == "This is a page."


def test_create_user(client: TestClient):
    # Act
    response = client.post(
        "/users/",
        json={
            "username": "user",
            "email": "test@test.com",
            "password": "password",
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "user",
        "email": "test@test.com",
    }


def test_read_users(client: TestClient):
    # Act
    response = client.get("/users/")

    # Assert
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


def test_update_user(client: TestClient):
    # Arrange
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


def test_delete_user(client: TestClient):
    # Act
    response = client.delete("/users/1")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}
