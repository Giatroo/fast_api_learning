import pytest
from fastapi.testclient import TestClient

from fast_duno.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
