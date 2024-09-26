import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient

from fast_duno.app import app
from fast_duno.database import get_session
from fast_duno.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = sa.create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=sa.StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with sa.orm.Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username="Teste", email="teste@test.com", password="testtest")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
