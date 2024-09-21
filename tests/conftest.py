import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient

from fast_duno.app import app
from fast_duno.models import table_registry


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def session():
    engine = sa.create_engine("sqlite:///:memory:")
    table_registry.metadata.create_all(engine)

    with sa.orm.Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
