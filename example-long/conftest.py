import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Bypasses @login_required
    app.config["LOGIN_DISABLED"] = True
    with app.test_client() as client:
        yield client
