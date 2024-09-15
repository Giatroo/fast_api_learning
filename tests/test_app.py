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


def test_read_page_returns_ok_and_html():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/page")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.text == "This is a page."
