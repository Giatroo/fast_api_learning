from http import HTTPStatus

from fastapi.testclient import TestClient


def test_get_token(client: TestClient, user):
    response = client.post(
        "/auth/token",
        data={
            "username": user.email,
            "password": user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert token["token_type"] == "Bearer"
