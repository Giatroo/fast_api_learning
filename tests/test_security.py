from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from fast_duno.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_current_user,
)


def test_jwt():
    data = {"sub": "test@test.com"}
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result["sub"] == data["sub"]
    # TODO: assert time is correct
    assert result["exp"]


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_getting_invalid_user(session):
    data = {"sub": "invalid@user.com"}
    token = create_access_token(data)

    with pytest.raises(HTTPException) as exp:
        get_current_user(session, token)
    assert exp.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exp.value.detail == "Could not validate credentials"
