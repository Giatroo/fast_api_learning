from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_duno.app import app


def test_read_root_returns_ok_and_hello_world():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello world!"}
