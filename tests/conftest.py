import factory
import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient

from fast_duno.app import app
from fast_duno.database import get_session
from fast_duno.models import User, table_registry
from fast_duno.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}+senha")


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
def user(session) -> User:
    pwd = "testtest"
    user_: User = UserFactory(password=get_password_hash(pwd))

    session.add(user_)
    session.commit()
    session.refresh(user_)

    user_.clean_password = pwd

    return user_


@pytest.fixture
def other_user(session) -> User:
    user_: User = UserFactory()

    session.add(user_)
    session.commit()
    session.refresh(user_)

    return user_


@pytest.fixture
def token(client, user):
    response = client.post(
        "/auth/token",
        data={
            "username": user.email,
            "password": user.clean_password,
        },
    )
    return response.json()["access_token"]
    return response.json()["access_token"]
