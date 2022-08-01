import json
from app import db, app
from app.models.categories import Category
from app.models.users import User
from app.repositories.category import get_category_by_id

headers = {
    "Content-Type": "application/json",
}


def test_category_rename(client):
    # Create test data
    user_id = 1
    cat = Category(user_id=user_id, name='Test Category')
    db.session.add(cat)
    db.session.commit()

    # Mock
    mock_name = 'Test Category New'
    mock_request_data = {
        'cat_id': cat.id,
        'name': mock_name,
    }

    with app.test_client() as client:
        # Solves the problem with flask_login.current_user.id:
        # AttributeError: 'AnonymousUser' object has no attribute 'id'
        # Creates a user authorization
        test_user = db.session.query(User).filter_by(id=user_id).first()

        @app.login_manager.request_loader
        def load_user_from_request(request):
            return test_user

        # Tests starts here
        url = 'http://127.0.0.1:5000/categories/update/'
        client.patch(url, headers=headers, data=json.dumps(mock_request_data))

    # Check new name
    category = get_category_by_id(user_id, cat.id)
    assert category.name == mock_name

    # Clear test data
    db.session.delete(category)
    db.session.commit()
