import pytest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import json

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-key'  # Add test JWT key
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(
            username='testuser',
            password=generate_password_hash('testpassword'),
            role='citizen',
            jurisdiction='Test Jurisdiction'
        )
        db.session.add(user)
        db.session.commit()
        return user

class TestAuthentication:
    def test_register_new_user(self, client):
        """Test registering a new user with valid data"""
        response = client.post('/api/v1/auth/register', 
            json={
                'username': 'newuser',
                'password': 'newpassword',
                'role': 'citizen',
                'jurisdiction': 'Test Jurisdiction'
            })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User registered successfully'

    def test_register_duplicate_user(self, client, test_user):
        """Test registering a user with existing username"""
        response = client.post('/api/v1/auth/register',
            json={
                'username': 'testuser',  # Same as test_user fixture
                'password': 'anotherpassword',
                'role': 'citizen',
                'jurisdiction': 'Another Jurisdiction'
            })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['message'] == 'User already exists'

    def test_login_valid_credentials(self, client, test_user):
        """Test login with valid credentials"""
        response = client.post('/api/v1/auth/login',
            json={
                'username': 'testuser',
                'password': 'testpassword'
            })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data

    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        response = client.post('/api/v1/auth/login',
            json={
                'username': 'testuser',
                'password': 'wrongpassword'
            })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['message'] == 'Invalid credentials'

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/api/v1/auth/login',
            json={
                'username': 'nonexistent',
                'password': 'testpassword'
            })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['message'] == 'Invalid credentials'

    def test_protected_route_access(self, client, test_user):
        """Test accessing protected route with valid token"""
        # First login to get token
        login_response = client.post('/api/v1/auth/login',
            json={
                'username': 'testuser',
                'password': 'testpassword'
            })
        
        token = json.loads(login_response.data)['access_token']
        
        # Then access protected route
        response = client.get('/api/v1/auth/protected',
            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['username'] == 'testuser'
        assert data['role'] == 'citizen'
        assert data['jurisdiction'] == 'Test Jurisdiction'