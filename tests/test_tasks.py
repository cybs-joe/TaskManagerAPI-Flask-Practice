import pytest
from app import create_app , db


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://"
    })

    with app.app_context():
        db.create_all()
        
    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == {"tasks": []}