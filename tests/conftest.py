import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import Base
from app import app
from config import TESTING_DATABASE_URI


@pytest.fixture
def client():
    # Prepare before your test
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Give control to your test
        yield client
    # Cleanup after the test run.
    # ... nothing here, for this simple example


@pytest.fixture(scope="session")
def engine():
    return create_engine(TESTING_DATABASE_URI)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
