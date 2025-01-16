import pytest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import Project, Region, Ministry, User
from app.schemas import ProjectSchema
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Fixture for the application
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

        # Create a test user
        hashed_password = generate_password_hash('password')
        user = User(username='testuser', password=hashed_password, role='citizen', jurisdiction='Test Jurisdiction')
        db.session.add(user)
        db.session.commit()

        # Create a test region
        region = Region(name='Test Region', name_ar='منطقة الاختبار', governorate='Test Governorate', governorate_code='99', delegation_code='9999')
        db.session.add(region)
        db.session.commit()

        # Create a test ministry
        ministry = Ministry(name='Test Ministry', name_ar='وزارة الاختبار')
        db.session.add(ministry)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

# Fixture for the test client
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture for creating an access token
@pytest.fixture
def access_token(app):
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        token = create_access_token(identity=user.id)
    return token

# Test project creation
def test_create_project(client, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    project_data = {
        'title': 'Test Project',
        'description': 'A test project',
        'budget': 100000.00,
        'start_date': '2023-01-01',
        'end_date': '2024-01-01',
        'status': 'In Progress',
        'region_id': 1,
        'ministry_id': 1
    }
    response = client.post('/api/v1/projects/', json=project_data, headers=headers)
    assert response.status_code == 201
    assert 'Test Project' in str(response.data)

# Test getting a list of projects
def test_get_projects(client, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/api/v1/projects/', headers=headers)
    assert response.status_code == 200

# Test getting a project by ID
def test_get_project_by_id(client, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    # First, create a project to ensure there's something to retrieve
    project_data = {
        'title': 'Test Project for Retrieval',
        'description': 'A project to be retrieved by ID',
        'budget': 100000.00,
        'start_date': '2023-01-01',
        'end_date': '2024-01-01',
        'status': 'In Progress',
        'region_id': 1,
        'ministry_id': 1
    }
    create_response = client.post('/api/v1/projects/', json=project_data, headers=headers)
    assert create_response.status_code == 201
    project_id = create_response.json['id']  # Assuming the response includes the new project's ID

    # Now, attempt to retrieve the project by its ID
    response = client.get(f'/api/v1/projects/{project_id}', headers=headers)
    assert response.status_code == 200
    assert project_data['title'] in str(response.data)

# Test updating a project
def test_update_project(client, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    # First, create a project to update
    project_data = {
        'title': 'Project to Update',
        'description': 'This project will be updated',
        'budget': 50000.00,
        'start_date': '2023-02-01',
        'end_date': '2024-02-01',
        'status': 'In Progress',
        'region_id': 1,
        'ministry_id': 1
    }
    create_response = client.post('/api/v1/projects/', json=project_data, headers=headers)
    assert create_response.status_code == 201
    project_id = create_response.json['id']

    # Update data
    updated_data = {
        'title': 'Updated Project Title',
        'status': 'Completed'
    }
    response = client.put(f'/api/v1/projects/{project_id}', json=updated_data, headers=headers)
    assert response.status_code == 200
    assert 'Updated Project Title' in str(response.data)
    assert 'Completed' in str(response.data)

# Test deleting a project
def test_delete_project(client, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    # First, create a project to delete
    project_data = {
        'title': 'Project to Delete',
        'description': 'This project will be deleted',
        'budget': 75000.00,
        'start_date': '2023-03-01',
        'end_date': '2024-03-01',
        'status': 'In Progress',
        'region_id': 1,
        'ministry_id': 1
    }
    create_response = client.post('/api/v1/projects/', json=project_data, headers=headers)
    assert create_response.status_code == 201
    project_id = create_response.json['id']

    # Now, delete the project
    response = client.delete(f'/api/v1/projects/{project_id}', headers=headers)
    assert response.status_code == 200
    assert 'Project deleted successfully' in str(response.data)

    # Verify that the project is no longer accessible
    response = client.get(f'/api/v1/projects/{project_id}', headers=headers)
    assert response.status_code == 404