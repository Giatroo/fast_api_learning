import sqlalchemy as sa

from fast_duno.settings import Settings

engine = sa.create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with sa.orm.Session(engine) as session:
        yield session
