#test_deliverable_routes.py

import pytest
from flask import jsonify
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import Deliverable, Project, Region, Ministry
from app.schemas import DeliverableSchema
from datetime import datetime

@pytest.fixture
def app():
    # Create the app with the 'testing' configuration
    app = create_app('testing')
    with app.app_context():
        # Create all database tables
        db.create_all()

        # Create a test region
        region = Region(name='Test Region', name_ar='منطقة الاختبار', governorate='Test Governorate', governorate_code='99', delegation_code='9999')
        db.session.add(region)
        db.session.commit()

        # Create a test ministry
        ministry = Ministry(name='Test Ministry', name_ar='وزارة الاختبار')
        db.session.add(ministry)
        db.session.commit()

        # Create a test project
        project_data = {
            'title': 'Test Project',
            'description': 'A test project',
            'budget': 100000.00,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
            'status': 'In Progress',
            'region_id': region.id,
            'ministry_id': ministry.id
        }
        project = Project(**project_data)
        db.session.add(project)
        db.session.commit()

        yield app
        # Drop all database tables after the test
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token(app):
    with app.app_context():
        # Create a test JWT token
        access_token = create_access_token(identity='test_user')
        return access_token

@pytest.fixture
def create_project(client, token, app):
    """Fixture to create a project for testing."""
    with app.app_context():
        # Retrieve the test region and ministry
        region = Region.query.filter_by(name='Test Region').first()
        ministry = Ministry.query.filter_by(name='Test Ministry').first()

        headers = {
            'Authorization': f'Bearer {token}'
        }
        project_data = {
            'title': 'Test Project for Deliverable',
            'description': 'This is a test project for deliverables',
            'budget': 100000.00,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
            'status': 'In Progress',
            'region_id': region.id,
            'ministry_id': ministry.id
        }
        response = client.post('/api/v1/projects/', json=project_data, headers=headers)
        assert response.status_code == 201
        return response.json  # Return the created project data

def test_create_deliverable(client, token, create_project):
    project = create_project
    headers = {
        'Authorization': f'Bearer {token}'
    }
    # Payload matches the DeliverableSchema
    data = {
        'title': 'Test Deliverable',
        'project_id': project['id']
    }
    response = client.post('/api/v1/deliverables/', json=data, headers=headers)
    print(response.json)  # Debugging: Print the response JSON
    assert response.status_code == 201
    assert 'id' in response.json  # Ensure the response includes the ID

def test_get_deliverables(client, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.get('/api/v1/deliverables/', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_deliverable(client, token, create_project):
    project = create_project
    headers = {
        'Authorization': f'Bearer {token}'
    }
    # First, create a deliverable to update
    data = {
        'title': 'Test Deliverable',
        'project_id': project['id']
    }
    create_response = client.post('/api/v1/deliverables/', json=data, headers=headers)
    print(create_response.json)  # Debugging: Print the response JSON
    deliverable_id = create_response.json['id']

    # Now, update the deliverable
    update_data = {
        'title': 'Updated Deliverable',  # Update the title
    }
    update_response = client.put(f'/api/v1/deliverables/{deliverable_id}', json=update_data, headers=headers)
    assert update_response.status_code == 200
    assert update_response.json['title'] == 'Updated Deliverable'

def test_delete_deliverable(client, token, create_project):
    project = create_project
    headers = {
        'Authorization': f'Bearer {token}'
    }
    # First, create a deliverable to delete
    data = {
        'title': 'Test Deliverable',
        'project_id': project['id']
    }
    create_response = client.post('/api/v1/deliverables/', json=data, headers=headers)
    print(create_response.json)  # Debugging: Print the response JSON
    deliverable_id = create_response.json['id']

    # Now, delete the deliverable
    delete_response = client.delete(f'/api/v1/deliverables/{deliverable_id}', headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Deliverable deleted successfully'

    # Verify that the deliverable is deleted
    get_response = client.get(f'/api/v1/deliverables/{deliverable_id}', headers=headers)
    assert get_response.status_code == 404