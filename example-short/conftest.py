import flask_login
import pytest
from app import app, db
from app.models.users import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Обходит @login_required
    app.config["LOGIN_DISABLED"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def authenticated_request():
    # Решает проблему с flask_login.current_user.id:
    # AttributeError: 'AnonymousUser' object has no attribute 'id'
    # Создает авторизацию пользователя
    with app.test_request_context():
        test_user = db.session.query(User).filter_by(id=1).first()
        yield flask_login.login_user(test_user)
