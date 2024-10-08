from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_duno.schemas import UserPublic


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


def test_create_user_with_existing_username(client: TestClient, user):
    response = client.post(
        "/users/",
        json={
            "username": "Teste",
            "email": "something@else.com",
            "password": "adifferentpassword",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_with_existing_email(client: TestClient, user):
    response = client.post(
        "/users/",
        json={
            "username": "somethingelse",
            "email": "teste@test.com",
            "password": "adifferentpassword",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_read_users(client: TestClient):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client: TestClient, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_user(client: TestClient, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_not_found(client: TestClient):
    response = client.get("/users/1234")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client: TestClient, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "testuser2",
            "email": "test@test.com",
            "password": "password",
            "id": 1,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "testuser2",
        "email": "test@test.com",
    }


def test_update_user_raises_not_found(client: TestClient, token):
    response = client.put(
        "/users/1234",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "testuser2",
            "email": "test@test.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_delete_user(client: TestClient, user, token):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_raises_not_found(client: TestClient, token):
    response = client.delete(
        "/users/1234", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}
