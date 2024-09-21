import sqlalchemy as sa
from sqlalchemy.orm import Session

from fast_duno.models import User


def test_create_user(session: Session):
    user = User(username="test", password="testpass", email="test@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(
        sa.select(User).where(User.email == "test@test.com")
    )

    assert result
    assert result.id == 1
    assert result.username == "test"
    assert result.password == "testpass"
    assert result.email == "test@test.com"
