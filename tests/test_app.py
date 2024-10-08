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
