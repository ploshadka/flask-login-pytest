import json
import pytest

from app import db
from app.models.categories import Category
from app.repositories.category import get_category_by_id

headers = {"Content-Type": "application/json"}


@pytest.mark.usefixtures("authenticated_request")
def test_category_rename(client):
    # Create test data
    user_id = 1
    cat = Category(user_id=user_id, name='Test Category')
    db.session.add(cat)
    db.session.commit()

    # Mock
    mock_name = 'Category Test New'
    mock_request_data = {
        'cat_id': cat.id,
        'name': mock_name,
    }

    # Rename category
    url = 'http://127.0.0.1:5000/categories/update/'
    client.patch(url, headers=headers, data=json.dumps(mock_request_data))

    # Check new name
    category = get_category_by_id(user_id, cat.id)
    assert category.name == mock_name

    # Clear test data
    db.session.delete(category)
    db.session.commit()
