import pytest
from database import db
from app import app


@pytest.fixture
def client():
    # Prepare before your test
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Give control to your test
        yield client
    # Cleanup after the test run.
    # ... nothing here, for this simple example
