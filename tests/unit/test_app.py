# tests/unit/test_app.py

import pytest
from microblog import app
from app import db
from app.models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_homepage(client):
    """Test that the homepage loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Microblog' in response.data  # Adjust based on your homepage content

def test_user_registration(client):
    """Test user registration functionality."""
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password',
        'password2': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Congratulations, you are now a registered user!' in response.data

def test_login(client):
    """Test user login functionality."""
    # First, register a new user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password',
        'password2': 'password'
    }, follow_redirects=True)
    
    # Then, log in with the new user
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged in!' in response.data
